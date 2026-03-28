# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
```

## Setup (Choose One)

### Option 1: OpenAI (Recommended if you have paid plan)

```bash
cp .env.example .env
# Edit .env and set:
# AI_PROVIDER=openai
# OPENAI_API_KEY=sk-your-key
# OPENAI_SPEC_MODEL=gpt-4
# OPENAI_PROC_MODEL=gpt-4
```

### Option 2: GitHub Copilot

```bash
cp .env.example .env
# Edit .env and set:
# AI_PROVIDER=copilot

# Install Copilot CLI: https://github.com/github/copilot-cli
```

### Option 3: GXEAI (Legacy)

```bash
cp .env.example .env
# Edit .env and set:
# AI_PROVIDER=gxeai
# BASE_URL=https://api.qa.saia.ai/chat
# SAIA_PROJECT_APITOKEN=your-token
```

## Usage

### Step 1: Generate Specification

```bash
python anything_to_spec.py \
  --programs_directory ./tests/cobol/test1/ \
  --spec_path ./outputs/spec1.yml
```

### Step 2: Generate GeneXus Procedure

```bash
python spec_to_xpz.py \
  --spec_path ./outputs/spec1.yml \
  --output ./outputs/test1
```

Import `outputs/test1/import_file.xml` into GeneXus.

## Switch Providers

### Via Environment Variable

```bash
export AI_PROVIDER=openai
python anything_to_spec.py ...
```

### Via Command Line

```bash
python anything_to_spec.py \
  --programs_directory ./tests/cobol/test1/ \
  --spec_path ./outputs/spec1.yml \
  --provider openai
```

## Testing

```bash
# Integration tests
python tests/test_providers.py

# Mock tests
python tests/test_mock.py
```

## Documentation

- **README.md** - Full project documentation
- **PROVIDER_ARCHITECTURE.md** - Developer guide for adding providers
- **.env.example** - Configuration template
