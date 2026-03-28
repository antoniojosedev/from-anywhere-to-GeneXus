import os
from dotenv import load_dotenv
import click
import yaml
from pathlib import Path

from ai_providers_core.factory import ProviderFactory


@click.command()
@click.option('--programs_directory', help='a directory with the programs to specify')
@click.option('--spec_path', help='a path to output yaml with specifications of procedures.')
@click.option('--provider', default=None, help='AI provider to use (gxeai, openai, copilot)')
def anything_to_spec(programs_directory, spec_path, provider):
    """Convert source code to GeneXus procedure specifications.
    
    Uses AI_PROVIDER env var or --provider flag to select provider.
    Defaults to 'gxeai' if not specified.
    """
    load_dotenv()
    
    try:
        provider_instance = ProviderFactory.create(provider)
        print(f"Using provider: {provider_instance}")
    except ValueError as e:
        print(f"Error: {e}")
        available = ProviderFactory.get_available_providers()
        print(f"Available providers: {', '.join(available)}")
        return
    
    specs = []
    folder = Path(programs_directory)
    
    if not folder.is_dir():
        print(f"Error: {programs_directory} is not a valid directory")
        return
    
    for file_path in folder.iterdir():
        if file_path.is_file():
            name = file_path.name
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                print(f"Processing {name}")
                spec = provider_instance.generate_spec(name, content)
                if spec:
                    specs.append(spec)
            except Exception as e:
                print(f"Error processing {name}: {e}")
        elif file_path.is_dir():
            print(f"Skipping directory: {file_path.name}")
    
    # Save the YAML objects to a file
    with open(spec_path, 'w', encoding='utf-8') as file:
        yaml.dump(specs, file, default_flow_style=False, allow_unicode=True)
    
    print(f"Saved {len(specs)} specifications to {spec_path}")


if __name__ == "__main__":
    anything_to_spec()
