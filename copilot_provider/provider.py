"""GitHub Copilot Provider - Local CLI integration."""

import subprocess
import json
import yaml
import tempfile
import os
from pathlib import Path

from ai_providers_core.base import BaseProvider


class CopilotProvider(BaseProvider):
    """Provider for GitHub Copilot CLI local integration."""

    def __init__(self):
        """Initialize Copilot provider."""
        self._check_copilot_available()

    @staticmethod
    def _check_copilot_available() -> bool:
        """Check if GitHub Copilot CLI is available."""
        try:
            import platform
            
            # On Windows, need to use shell=True or full path
            if platform.system() == "Windows":
                result = subprocess.run(
                    'copilot --version',
                    shell=True,
                    capture_output=True,
                    timeout=5,
                    text=True
                )
            else:
                result = subprocess.run(
                    ['copilot', '--version'],
                    capture_output=True,
                    timeout=5,
                    text=True
                )
            
            if result.returncode == 0:
                print(f"GitHub Copilot CLI: {result.stdout.strip()}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        raise RuntimeError(
            "GitHub Copilot CLI not found. "
            "Install from: https://github.com/github/copilot-cli"
        )

    def generate_spec(self, file_name: str, program: str) -> dict:
        """Generate spec from source code using Copilot CLI."""
        prompt = f"""Analyze this code and generate a YAML specification with:
- name: function/procedure name
- spec: detailed specification describing what it does

Code to analyze:
```
{program}
```

Return ONLY valid YAML without markdown formatting."""

        response = self._call_copilot(prompt)
        answer = self._remove_markdown_markers(response)
        
        print(answer)
        try:
            content = yaml.safe_load(answer)
            content['file_name'] = file_name
            return content
        except yaml.YAMLError as e:
            print(f"Error loading YAML: {e}")
            return None

    def generate_procedure(self, name: str, spec: str) -> dict:
        """Generate GeneXus procedure from spec using Copilot CLI."""
        from gxeai.clean_proc import parse_procedure
        
        prompt = f"""Generate a GeneXus procedure based on this specification:

{spec}

Generate ONLY the procedure code in GeneXus syntax with this format:
Procedure <name> {{
#Variables
[variable definitions]
#EndVariables

[procedure source code]
}}

Ensure the procedure is complete and functional."""

        response = self._call_copilot(prompt)
        content = parse_procedure(response, name)
        content['description'] = spec
        return content

    @staticmethod
    def _call_copilot(prompt: str) -> str:
        """
        Call GitHub Copilot CLI with a prompt.
        
        Args:
            prompt: Prompt to send to Copilot
            
        Returns:
            Response from Copilot
        """
        try:
            # Escape quotes in prompt for shell
            escaped_prompt = prompt.replace('"', '\\"')
            
            # On Windows, copilot is found via PATH but requires shell=True
            result = subprocess.run(
                f'copilot -p "{escaped_prompt}"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0 and result.stdout:
                return result.stdout
            elif result.returncode == 0:
                # Success but no output
                return prompt  # Return original prompt as fallback
            else:
                raise RuntimeError(
                    f"Copilot error: {result.stderr}"
                )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Copilot request timed out")
        except FileNotFoundError:
            raise RuntimeError(
                "GitHub Copilot CLI not found. "
                "Install from: https://github.com/github/copilot-cli"
            )

    @staticmethod
    def _remove_markdown_markers(text: str) -> str:
        """Remove markdown code block markers."""
        if not text:
            return ""
        
        text = text.strip()
        if text.startswith("```"):
            lines = text.split('\n')
            # Remove first line if it's ```
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = '\n'.join(lines)
        return text.strip()
