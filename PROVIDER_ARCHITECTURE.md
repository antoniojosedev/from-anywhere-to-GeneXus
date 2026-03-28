# Provider Architecture Documentation

## Overview

The project now supports multiple AI providers through a pluggable provider system. This allows users to choose their preferred LLM backend without changing core code.

## Supported Providers

1. **GXEAI** - Legacy provider (requires token)
2. **OpenAI** - GPT-4/4o (requires API key)
3. **GitHub Copilot** - Local CLI (requires Copilot CLI installation)

## Architecture

```
┌─────────────────────────────────────────┐
│         anything_to_spec.py             │
│          spec_to_xpz.py                 │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼─────────┐
        │ ProviderFactory  │
        └────────┬─────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌─────────┐ ┌────────┐ ┌──────────┐
│ GXEAI   │ │ OpenAI │ │ Copilot  │
│Provider │ │Provider│ │ Provider │
└─────────┘ └────────┘ └──────────┘
    │            │            │
    └────────────┼────────────┘
                 │
        ┌────────▼─────────┐
        │  BaseProvider    │
        │  (Abstract)      │
        └──────────────────┘
```

## Directory Structure

```
from-anywhere-to-GeneXus/
├── ai_providers_core/         # Core abstraction
│   ├── __init__.py
│   ├── base.py               # BaseProvider abstract class
│   └── factory.py            # ProviderFactory for creation
│
├── gxeai/                     # GXEAI provider implementation
│   ├── gxeai_provider.py     # Provider class
│   ├── call_spec_assistant.py  # Legacy (for compatibility)
│   ├── call_proc_assistant.py  # Legacy (for compatibility)
│   └── clean_proc.py          # Shared utility
│
├── openai_provider/           # OpenAI provider
│   ├── __init__.py
│   └── provider.py
│
├── copilot_provider/          # GitHub Copilot provider
│   ├── __init__.py
│   └── provider.py
│
├── anything_to_spec.py        # Main entry point (refactored)
├── spec_to_xpz.py            # Main entry point (refactored)
└── ...
```

## Creating a New Provider

### 1. Create a New Directory

```bash
mkdir -p my_provider
```

### 2. Implement BaseProvider

```python
# my_provider/provider.py

from ai_providers_core.base import BaseProvider

class MyProvider(BaseProvider):
    def __init__(self):
        """Initialize your provider."""
        pass

    def generate_spec(self, file_name: str, program: str) -> dict:
        """Generate specification from source code.
        
        Returns dict with:
        - name: Procedure name
        - spec: YAML-formatted specification
        - file_name: Original file name
        """
        # Your implementation
        return {
            'name': 'ProcName',
            'spec': 'specification...',
            'file_name': file_name
        }

    def generate_procedure(self, name: str, spec: str) -> dict:
        """Generate GeneXus procedure from spec.
        
        Returns dict with:
        - name: Procedure name
        - Parts: Dict with 'Source' code
        - description: Spec description
        """
        # Your implementation
        return {
            'name': name,
            'Parts': {'Source': 'Procedure code...'},
            'description': spec
        }
```

### 3. Create Package Init

```python
# my_provider/__init__.py

from my_provider.provider import MyProvider

__all__ = ['MyProvider']
```

### 4. Register Provider

The factory auto-registers providers via import detection:

```python
# In ai_providers_core/factory.py, _register_default_providers():
try:
    from my_provider.provider import MyProvider
    ProviderFactory.register('myprovider', MyProvider)
except ImportError:
    pass
```

## Using Providers

### Via Environment Variable

```bash
export AI_PROVIDER=openai
python anything_to_spec.py --programs_directory ./tests/cobol/test1/ --spec_path ./outputs/spec1.yml
```

### Via Command Line Flag

```bash
python anything_to_spec.py \
  --programs_directory ./tests/cobol/test1/ \
  --spec_path ./outputs/spec1.yml \
  --provider openai
```

### Programmatically

```python
from ai_providers_core.factory import ProviderFactory

# Create provider instance
provider = ProviderFactory.create('openai')

# Generate specification
spec = provider.generate_spec('myfile.py', source_code)

# Generate procedure
procedure = provider.generate_procedure('MyProcedure', spec_string)
```

## Testing

Run integration tests:

```bash
python tests/test_providers.py
python tests/test_mock.py
```

## Provider Configuration

### Environment Variables

Each provider reads from `.env`:

#### GXEAI
- `BASE_URL`: API endpoint
- `SAIA_PROJECT_APITOKEN`: Authentication token
- `SPEC_ASSISTANT_NAME`: Name of spec assistant
- `PROC_ASSISTANT_NAME`: Name of procedure assistant

#### OpenAI
- `OPENAI_API_KEY`: Your API key
- `OPENAI_SPEC_MODEL`: Model for spec generation (default: gpt-4)
- `OPENAI_PROC_MODEL`: Model for procedure generation (default: gpt-4)

#### Copilot
- No configuration needed (uses local CLI)

## Adding Optional Dependencies

If your provider requires external packages, add them to a conditional import:

```python
try:
    import mypackage
except ImportError:
    raise ImportError(
        "mypackage required for MyProvider. "
        "Install with: pip install mypackage"
    )
```

Then update `requirements.txt` with optional dependencies or create a separate requirements file.

## Error Handling

Providers should raise descriptive errors during initialization if required dependencies or configuration are missing:

```python
def __init__(self):
    if not os.getenv('REQUIRED_KEY'):
        raise ValueError(
            "MyProvider requires REQUIRED_KEY in .env"
        )
```

## Backward Compatibility

The original `gxeai.call_spec_assistant` and `gxeai.call_proc_assistant` modules are preserved but now route through the provider system internally. This ensures existing code continues to work.
