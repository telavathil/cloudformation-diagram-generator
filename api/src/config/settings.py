# Resource mappings and configurations
from diagrams.aws.compute import EC2, Lambda, ECS
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import VPC, ELB, Route53
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM, SecurityHub
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch

RESOURCE_MAP = {
    'AWS::EC2::Instance': EC2,
    'AWS::Lambda::Function': Lambda,
    # ... rest of your resource mappings
}

RESOURCE_GROUPS = {
    'network': ['AWS::EC2::VPC', 'AWS::EC2::SecurityGroup', 'AWS::ElasticLoadBalancingV2::LoadBalancer', 
                'AWS::Route53::RecordSet'],
    # ... rest of your resource groups
}

DIAGRAM_SETTINGS = {
    'graph_attr': {
        'splines': 'ortho',
        'fontname': 'Liberation Sans',
        'bgcolor': 'transparent',
        'pad': '3.0',
        'nodesep': '2.0',
        'ranksep': '2.0',
        'overlap': 'false',
        'sep': '+35',
    },
    'node_attr': {
        'fontname': 'Liberation Sans',
        'fontsize': '14',
        'imagescale': 'false',
        'fixedsize': 'true',
        'width': '0.8',
        'height': '0.8',
        'shape': 'none',
        'margin': '0.6',
        'labelloc': 'b',
        'labeljust': 'c',
    },
    'edge_attr': {
        'fontsize': '12',
        'fontname': 'Liberation Sans',
        'penwidth': '1.0',
        'minlen': '3'
    }
} 