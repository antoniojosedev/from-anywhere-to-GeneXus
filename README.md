# From Anywhere To GeneXus

## Description
Convert any code into a GeneXus procedure. Get the code of your choice, generate a spec, then use that spec to generate a GeneXus procedure inside an xpz file.

**Now with support for multiple AI providers:** GXEAI, OpenAI (GPT-4/4o), and GitHub Copilot!

## Prerequisites
Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/)

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/genexuslabs/from-anywhere-to-GeneXus
cd from-anywhere-to-GeneXus
```

### 2. Create a Virtual Environment
```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment (Linux/MacOS)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your AI Provider

Copy `.env.example` to `.env` and choose your provider:

```bash
cp .env.example .env
```

Edit `.env` and uncomment the section for your chosen provider:

#### Option 1: OpenAI (Recommended if you have paid plan)
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_SPEC_MODEL=gpt-4
OPENAI_PROC_MODEL=gpt-4
```

#### Option 2: GitHub Copilot (Free if you have Copilot subscription)
```env
AI_PROVIDER=copilot
# No additional config needed - uses local CLI
# Install: https://github.com/github/copilot-cli
```

#### Option 3: GXEAI (Legacy - requires token)
```env
AI_PROVIDER=gxeai
BASE_URL=https://api.qa.saia.ai/chat
SAIA_PROJECT_APITOKEN=<YOUR-GXEAI-TOKEN>
SPEC_ASSISTANT_NAME=ProcedureBaseSyntax
PROC_ASSISTANT_NAME=ProcedureBaseSyntax
```

### 5. Generate Specification from Source Code

```bash
python anything_to_spec.py --programs_directory ./tests/cobol/test1/ --spec_path ./outputs/spec1.yml

# Or specify provider via command line
python anything_to_spec.py \
  --programs_directory ./tests/cobol/test1/ \
  --spec_path ./outputs/spec1.yml \
  --provider openai
```

### 6. Generate GeneXus Procedure from Specification

```bash
python spec_to_xpz.py --spec_path ./outputs/spec1.yml --output ./outputs/test1

# Or specify provider via command line
python spec_to_xpz.py \
  --spec_path ./outputs/spec1.yml \
  --output ./outputs/test1 \
  --provider openai
```

You can import `outputs/import_file.xml` directly into GeneXus.

## AI Providers

### Available Providers

| Provider | Setup | Cost | Speed | Quality |
|----------|-------|------|-------|---------|
| **OpenAI (GPT-4/4o)** | API Key required | Paid | Fast | Excellent |
| **GitHub Copilot** | CLI required | Free/Paid* | Very Fast | Excellent |
| **GXEAI** | Token required | Contact GeneXus | Varies | Good |

*Free if you have Copilot subscription, otherwise paid

### Switching Providers

```bash
# Via environment variable
export AI_PROVIDER=openai
python anything_to_spec.py --programs_directory ./tests/cobol/test1/ --spec_path ./outputs/spec1.yml

# Or via command line flag
python anything_to_spec.py --programs_directory ./tests/cobol/test1/ --spec_path ./outputs/spec1.yml --provider copilot
```

## Project Structure

```
from-anywhere-to-GeneXus/
├── ai_providers_core/      # Core abstraction and factory
├── gxeai/                  # GXEAI provider
├── openai_provider/        # OpenAI provider
├── copilot_provider/       # GitHub Copilot provider
├── xpz/                    # XPZ file utilities
├── tests/                  # Test files and examples
├── anything_to_spec.py     # Code → Specification
├── spec_to_xpz.py         # Specification → GeneXus Procedure
└── requirements.txt        # Python dependencies
```

## Deactivating the Virtual Environment
When you're done, you can deactivate the virtual environment with:

```bash
deactivate
```

## License
```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
