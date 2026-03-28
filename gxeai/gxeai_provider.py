"""GXEAI Provider - Legacy provider for GXEAI assistant API."""

import os
import json
import yaml
import requests
from dotenv import load_dotenv

from ai_providers_core.base import BaseProvider


class GXEAIProvider(BaseProvider):
    """Provider for GXEAI assistant API."""

    def __init__(self):
        """Initialize GXEAI provider with environment variables."""
        load_dotenv()
        self.base_url = os.getenv('BASE_URL')
        self.api_token = os.getenv('SAIA_PROJECT_APITOKEN')
        self.spec_assistant = os.getenv('SPEC_ASSISTANT_NAME', 'ProcedureBaseSyntax')
        self.proc_assistant = os.getenv('PROC_ASSISTANT_NAME', 'ProcedureBaseSyntax')
        
        if not self.base_url or not self.api_token:
            raise ValueError(
                "GXEAI provider requires BASE_URL and SAIA_PROJECT_APITOKEN in .env"
            )

    def generate_spec(self, file_name: str, program: str) -> dict:
        """Generate spec from source code using GXEAI."""
        headers = {
            "Content-Type": "application/json",
            "Saia-Auth": self.api_token,
            "X-Saia-Cache-Enabled": "false"
        }
        
        payload = {
            "model": f"saia:assistant:{self.spec_assistant}",
            "messages": [{"role": "user", "content": program}],
            "stream": "false"
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload)
        json_data = json.loads(response.text)
        mk_answer = json_data['choices'][0]['message']['content']
        answer = self._remove_first_and_last_line(mk_answer)
        
        print(answer)
        try:
            content = yaml.safe_load(answer)
            content['file_name'] = file_name
            return content
        except yaml.YAMLError as e:
            print(f"Error loading YAML: {e}")
            return None

    def generate_procedure(self, name: str, spec: str) -> dict:
        """Generate GeneXus procedure from spec using GXEAI."""
        from gxeai.clean_proc import parse_procedure
        
        headers = {
            "Content-Type": "application/json",
            "Saia-Auth": self.api_token,
            "X-Saia-Cache-Enabled": "false"
        }
        
        payload = {
            "model": f"saia:assistant:{self.proc_assistant}",
            "messages": [{"role": "user", "content": spec}],
            "stream": "false"
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload)
        json_data = json.loads(response.text)
        answer = json_data['choices'][0]['message']['content']
        
        content = parse_procedure(answer, name)
        content['description'] = spec
        return content

    @staticmethod
    def _remove_first_and_last_line(text: str) -> str:
        """Remove first and last line from text."""
        lines = text.splitlines()
        if len(lines) <= 2:
            return ""
        return '\n'.join(lines[1:-1])
