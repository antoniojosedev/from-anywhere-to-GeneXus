"""OpenAI Provider for code specification and procedure generation."""

import os
import json
import yaml
from dotenv import load_dotenv

from ai_providers_core.base import BaseProvider


class OpenAIProvider(BaseProvider):
    """Provider for OpenAI API (GPT-4, GPT-4o, etc)."""

    def __init__(self):
        """Initialize OpenAI provider with environment variables."""
        load_dotenv()
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        except ImportError:
            raise ImportError(
                "openai package required for OpenAI provider. "
                "Install with: pip install openai"
            )
        
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.spec_model = os.getenv('OPENAI_SPEC_MODEL', 'gpt-4')
        self.proc_model = os.getenv('OPENAI_PROC_MODEL', 'gpt-4')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set in .env")

    def generate_spec(self, file_name: str, program: str) -> dict:
        """Generate spec from source code using OpenAI."""
        prompt = f"""Analyze this code and generate a YAML specification with:
- name: function/procedure name
- spec: detailed specification describing what it does

Code to analyze:
```
{program}
```

Return ONLY valid YAML without markdown formatting."""

        response = self.client.chat.completions.create(
            model=self.spec_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        
        answer = response.choices[0].message.content.strip()
        answer = self._remove_markdown_markers(answer)
        
        print(answer)
        try:
            content = yaml.safe_load(answer)
            content['file_name'] = file_name
            return content
        except yaml.YAMLError as e:
            print(f"Error loading YAML: {e}")
            return None

    def generate_procedure(self, name: str, spec: str) -> dict:
        """Generate GeneXus procedure from spec using OpenAI."""
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

        response = self.client.chat.completions.create(
            model=self.proc_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        
        answer = response.choices[0].message.content.strip()
        content = parse_procedure(answer, name)
        content['description'] = spec
        return content

    @staticmethod
    def _remove_markdown_markers(text: str) -> str:
        """Remove markdown code block markers."""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split('\n')
            # Remove first line if it's ```yaml or similar
            if lines[0].startswith("```"):
                lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = '\n'.join(lines)
        return text.strip()
