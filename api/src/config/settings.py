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
        'width': '1.0',
        'height': '1.0',
        'shape': 'none',
        'margin': '0.6',
        'labelloc': 'b',  # Position label at bottom of node
        'labelsplines': 'ortho',  # Use orthogonal label placement
        'labeldistance': '3.0',
    },
    'edge_attr': {
        'fontsize': '12',
        'fontname': 'Liberation Sans',
        'penwidth': '1.0',
        'minlen': '3'
    }
}
