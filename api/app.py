"""
Flask application for diagram generation service.

This module provides a REST API service for generating diagrams.
"""
import os
import tempfile
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import yaml
from diagrams import Diagram
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import VPC, ELB
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch

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
    'AWS::CloudWatch::Alarm': Cloudwatch
}

def parse_cloudformation(yaml_content):
    """Parse CloudFormation YAML and extract resources with their relationships."""
    try:
        cf_template = yaml.safe_load(yaml_content)
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
                direction='LR',
                curvestyle='ortho',
                graph_attr={
                    'splines': 'ortho',
                    'fontname': 'Liberation Sans',
                    'bgcolor': 'transparent',
                    'pad': '0.5',
                    'nodesep': '1',
                    'ranksep': '1'
                },
                node_attr={
                    'fontname': 'Liberation Sans',
                    'fontsize': '12',
                    'imagescale': 'true',
                    'fixedsize': 'true',
                    'width': '1.5',
                    'height': '1.5',
                    'shape': 'none'
                },
                outformat='svg'
            ) as diagram:
                created_nodes = {}
                for resource_id, resource_info in nodes.items():
                    node_class = RESOURCE_MAP[resource_info['type']]
                    created_nodes[resource_id] = node_class(resource_id)

                for source, target in relationships:
                    if source in created_nodes and target in created_nodes:
                        created_nodes[source] >> created_nodes[target]

            svg_path = f"{diagram_path}.svg"

            with open(svg_path, 'r', encoding='utf-8') as svg_file:
                svg_content = svg_file.read()

                # Replace icon paths with absolute URLs
                import re
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
