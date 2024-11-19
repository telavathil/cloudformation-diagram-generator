"""
Flask application for diagram generation service.

This module provides a REST API service for generating diagrams.
"""
import os
import tempfile
import re
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import yaml
from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2, Lambda, ECS
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import VPC, ELB, Route53
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM, SecurityHub
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from yaml.constructor import Constructor

# Load environment variables before creating Flask app
load_dotenv()

app = Flask(__name__)
CORS(app)

# Map CloudFormation resource types to Diagram nodes
RESOURCE_MAP = {
    'AWS::EC2::Instance': EC2,
    'AWS::Lambda::Function': Lambda,
    'AWS::RDS::DBInstance': RDS,
    'AWS::DynamoDB::Table': Dynamodb,
    'AWS::EC2::VPC': VPC,
    'AWS::ElasticLoadBalancing::LoadBalancer': ELB,
    'AWS::S3::Bucket': S3,
    'AWS::IAM::Role': IAM,
    'AWS::SQS::Queue': SQS,
    'AWS::SNS::Topic': SNS,
    'AWS::CloudWatch::Alarm': Cloudwatch,
    'AWS::ECS::Service': ECS,
    'AWS::ECS::TaskDefinition': ECS,
    'AWS::ElasticLoadBalancingV2::LoadBalancer': ELB,
    'AWS::ElasticLoadBalancingV2::TargetGroup': ELB,
    'AWS::ElasticLoadBalancingV2::Listener': ELB,
    'AWS::Route53::RecordSet': Route53,
    'AWS::EC2::SecurityGroup': SecurityHub,
}

# Resource type groupings for better layout
RESOURCE_GROUPS = {
    'network': ['AWS::EC2::VPC', 'AWS::EC2::SecurityGroup', 'AWS::ElasticLoadBalancingV2::LoadBalancer', 
                'AWS::Route53::RecordSet'],
    'compute': ['AWS::ECS::Service', 'AWS::ECS::TaskDefinition', 'AWS::EC2::Instance', 'AWS::Lambda::Function'],
    'security': ['AWS::IAM::Role'],
    'database': ['AWS::RDS::DBInstance', 'AWS::DynamoDB::Table'],
    'storage': ['AWS::S3::Bucket'],
    'integration': ['AWS::SQS::Queue', 'AWS::SNS::Topic'],
    'monitoring': ['AWS::CloudWatch::Alarm']
}

# Add custom YAML constructors for CloudFormation intrinsic functions
def construct_cfn_tag(loader, tag_suffix, node):
    """Generic constructor for CloudFormation tags"""
    if isinstance(node, yaml.ScalarNode):
        return {tag_suffix: loader.construct_scalar(node)}
    elif isinstance(node, yaml.SequenceNode):
        return {tag_suffix: loader.construct_sequence(node)}
    elif isinstance(node, yaml.MappingNode):
        return {tag_suffix: loader.construct_mapping(node)}

# Create custom YAML loader for CloudFormation
class CloudFormationLoader(yaml.SafeLoader):
    pass

# Register CloudFormation intrinsic functions
cfn_tags = ['Ref', 'Sub', 'Join', 'Select', 'Split', 'GetAtt', 'GetAZs', 'ImportValue', 'FindInMap']
for tag in cfn_tags:
    CloudFormationLoader.add_constructor(f'!{tag}', 
        lambda loader, node, tag=tag: construct_cfn_tag(loader, tag, node))

def parse_cloudformation(yaml_content):
    """Parse CloudFormation YAML and extract resources with their relationships."""
    try:
        # Use CloudFormationLoader instead of safe_load
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

                # Look for relationships in resource properties
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

@app.route('/generate-diagram', methods=['POST'])
def generate_diagram():
    """Generate an architecture diagram from CloudFormation YAML."""
    try:
        yaml_content = request.json.get('yaml')
        if not yaml_content:
            return jsonify({'error': 'No YAML content provided'}), 400

        nodes, relationships = parse_cloudformation(yaml_content)

        with tempfile.TemporaryDirectory() as tmpdir:
            diagram_path = os.path.join(tmpdir, "architecture")

            with Diagram(
                'AWS Architecture',
                show=False,
                filename=diagram_path,
                direction='TB',
                curvestyle='ortho',
                graph_attr={
                    'splines': 'ortho',
                    'fontname': 'Liberation Sans',
                    'bgcolor': 'transparent',
                    'pad': '3.0',
                    'nodesep': '2.0',
                    'ranksep': '2.0',
                    'overlap': 'false',
                    'sep': '+35',
                },
                node_attr={
                    'fontname': 'Liberation Sans',
                    'fontsize': '14',
                    'imagescale': 'false',
                    'fixedsize': 'true',
                    'width': '0.8',
                    'height': '0.8',
                    'shape': 'none',
                    'margin': '0.8',
                    'labelloc': 'b',
                    'labeljust': 'c',
                },
                edge_attr={
                    'fontsize': '12',
                    'fontname': 'Liberation Sans',
                    'penwidth': '1.0',
                    'minlen': '3'
                },
                outformat='svg'
            ) as diagram:
                created_nodes = {}
                
                # Create nodes with logical names
                for resource_id, resource_info in nodes.items():
                    if resource_info['type'] in RESOURCE_MAP:
                        node_class = RESOURCE_MAP[resource_info['type']]
                        # Simplified label processing with longer length
                        label = resource_id
                        for prefix in ['Service', 'AWS', 'Task', 'Security']:
                            label = label.replace(prefix, '')
                        label = label[:20] + '...' if len(label) > 20 else label
                        created_nodes[resource_id] = node_class(label)

                # Create relationships with custom styling
                for source, target in relationships:
                    if source in created_nodes and target in created_nodes:
                        edge_style = {
                            'color': '#707070',
                            'style': 'dashed',
                            'penwidth': '0.5',
                            'constraint': 'true',
                            'weight': '1'
                        }
                        created_nodes[source] >> Edge(**edge_style) >> created_nodes[target]

            # Read and process SVG content
            svg_path = f"{diagram_path}.svg"
            with open(svg_path, 'r', encoding='utf-8') as svg_file:
                svg_content = svg_file.read()

                # Replace icon paths with absolute URLs
                svg_content = re.sub(
                    r'xlink:href="(/usr/local/lib/python3.12/site-packages/resources/aws/[^"]+)"',
                    lambda m: f'xlink:href="http://localhost:5001/icons/aws/{os.path.basename(m.group(1))}"',
                    svg_content
                )

            return svg_content, 200, {'Content-Type': 'image/svg+xml'}

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/icons/aws/<filename>')
def serve_aws_icon(filename):
    """Serve AWS icon files from the diagrams package."""
    import diagrams
    resources_path = os.path.join(os.path.dirname(diagrams.__file__), "resources", "aws")

    try:
        for root, _, files in os.walk(resources_path):
            if filename in files:
                return send_from_directory(root, filename)
        return "Icon not found", 404

    except Exception as e:
        app.logger.error(f"Error serving icon {filename}: {str(e)}")
        return f"Icon not found: {filename}", 404

if __name__ == '__main__':
    app.run(host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 5001)), debug=bool(os.getenv('FLASK_DEBUG', True)))
