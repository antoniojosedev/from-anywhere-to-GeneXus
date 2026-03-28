"""Google Gemini Provider - Free tier with generous limits."""

import os
import yaml
from dotenv import load_dotenv

from ai_providers_core.base import BaseProvider


class GeminiProvider(BaseProvider):
    """Provider for Google Gemini API (free tier)."""

    def __init__(self):
        """Initialize Gemini provider with environment variables."""
        load_dotenv()
        
        try:
            import google.genai as genai
            self.client = genai
        except ImportError:
            raise ImportError(
                "google-genai package required for Gemini provider. "
                "Install with: pip install google-genai"
            )
        
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.spec_model = os.getenv('GEMINI_SPEC_MODEL', 'gemini-1.5-flash')
        self.proc_model = os.getenv('GEMINI_PROC_MODEL', 'gemini-1.5-flash')
        
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not set in .env. "
                "Get free API key from: https://aistudio.google.com/app/apikey"
            )
        
        # Configure Gemini
        self.client.configure(api_key=self.api_key)

    def generate_spec(self, file_name: str, program: str) -> dict:
        """Generate spec from source code using Google Gemini."""
        prompt = f"""Analyze this code and generate a YAML specification with:
- name: function/procedure name
- spec: detailed specification describing what it does

Code to analyze:
```
{program}
```

Return ONLY valid YAML without markdown formatting."""

        try:
            model = self.client.GenerativeModel(self.spec_model)
            response = model.generate_content(prompt)
            answer = response.text.strip()
            answer = self._remove_markdown_markers(answer)
            
            print(answer)
            try:
                content = yaml.safe_load(answer)
                content['file_name'] = file_name
                return content
            except yaml.YAMLError as e:
                print(f"Error loading YAML: {e}")
                return None
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}")

    def generate_procedure(self, name: str, spec: str) -> dict:
        """Generate GeneXus procedure from spec using Google Gemini."""
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

        try:
            model = self.client.GenerativeModel(self.proc_model)
            response = model.generate_content(prompt)
            answer = response.text.strip()
            
            content = parse_procedure(answer, name)
            content['description'] = spec
            return content
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}")

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
