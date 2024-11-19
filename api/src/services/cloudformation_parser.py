from ..utils.yaml_loader import CloudFormationLoader
from ..config.settings import RESOURCE_MAP
import yaml

def parse_cloudformation(yaml_content):
    """Parse CloudFormation YAML and extract resources with their relationships."""
    try:
        cf_template = yaml.load(yaml_content, Loader=CloudFormationLoader)
        resources = cf_template.get('Resources', {})

        nodes = {}
        relationships = []

        for resource_id, resource_data in resources.items():
            resource_type = resource_data.get('Type')
            if resource_type in RESOURCE_MAP:
                nodes[resource_id] = {
                    'type': resource_type,
                    'node': None
                }

                properties = resource_data.get('Properties', {})
                for prop_key, prop_value in properties.items():
                    if isinstance(prop_value, dict) and 'Ref' in prop_value:
                        referenced_resource = prop_value['Ref']
                        if referenced_resource in resources:
                            relationships.append((resource_id, referenced_resource))

        return nodes, relationships
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing CloudFormation template: {str(e)}") 