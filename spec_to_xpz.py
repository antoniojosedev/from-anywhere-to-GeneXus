import os
from dotenv import load_dotenv
import click
import yaml

from ai_providers_core.factory import ProviderFactory
import xpz.from_json_to_xpz


@click.command()
@click.option('--spec_path', help='a path to a yaml with specifications of procedures.')
@click.option('--output', help='a path to output the xml path ready to import.')
@click.option('--provider', default=None, help='AI provider to use (gxeai, openai, copilot)')
def spec_to_xpz(spec_path, output, provider):
    """Generate GeneXus procedures from specifications.
    
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
    
    procs = []
    if not os.path.exists(output):
        os.makedirs(output)
    
    xml_path = os.path.join(output, "import_file.xml")

    with open(spec_path, 'r', encoding='utf-8') as yf:
        data = yaml.safe_load(yf)
        if not data:
            print("No specifications found in file")
            return
        
        for row in data:
            try:
                name = row.get('name')
                spec = row.get('spec')
                print(f"Processing {name}")
                
                content = provider_instance.generate_procedure(name, spec)
                
                # Save program file
                program_path = os.path.join(output, name)
                with open(program_path, 'w', encoding='utf-8') as f:
                    f.write(content["Parts"]["Source"])

                procs.append(content)
            except Exception as e:
                print(f"Error processing {name}: {e}")

    # Save xpz
    xml_string = xpz.from_json_to_xpz.json_to_xml({'Procedures': procs})
    with open(xml_path, "w", encoding='utf-8') as file:
        file.write(xml_string)
    
    print(f"Generated {len(procs)} procedures")
    print(f"XPZ file saved to: {xml_path}")


if __name__ == "__main__":
    spec_to_xpz()
