import yaml
from yaml.constructor import Constructor

def construct_cfn_tag(loader, tag_suffix, node):
    """Generic constructor for CloudFormation tags"""
    if isinstance(node, yaml.ScalarNode):
        return {tag_suffix: loader.construct_scalar(node)}
    elif isinstance(node, yaml.SequenceNode):
        return {tag_suffix: loader.construct_sequence(node)}
    elif isinstance(node, yaml.MappingNode):
        return {tag_suffix: loader.construct_mapping(node)}

class CloudFormationLoader(yaml.SafeLoader):
    pass

# Register CloudFormation intrinsic functions
cfn_tags = ['Ref', 'Sub', 'Join', 'Select', 'Split', 'GetAtt', 'GetAZs', 'ImportValue', 'FindInMap']
for tag in cfn_tags:
    CloudFormationLoader.add_constructor(f'!{tag}', 
        lambda loader, node, tag=tag: construct_cfn_tag(loader, tag, node)) 