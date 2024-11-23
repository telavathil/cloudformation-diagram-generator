import os
import tempfile
import re
from diagrams import Diagram, Edge
from ..config.settings import RESOURCE_MAP, DIAGRAM_SETTINGS

def generate_diagram(nodes, relationships):
    """Generate architecture diagram from parsed CloudFormation resources."""
    # TODO: Add logging
    print("Generating diagram...")
    print("Nodes:", nodes)
    print("Relationships:", relationships)

    with tempfile.TemporaryDirectory() as tmpdir:
        diagram_path = os.path.join(tmpdir, "architecture")

        with Diagram(
            'AWS Architecture',
            show=False,
            filename=diagram_path,
            direction='TB',
            curvestyle='ortho',
            **DIAGRAM_SETTINGS,
            outformat='svg'
        ) as diagram:
            created_nodes = create_nodes(nodes)
            create_edges(created_nodes, relationships)

        return process_svg_content(f"{diagram_path}.svg")

def create_nodes(nodes):
    created_nodes = {}
    for resource_id, resource_info in nodes.items():
        if resource_info['type'] in RESOURCE_MAP:
            node_class = RESOURCE_MAP[resource_info['type']]
            label = simplify_label(resource_id)
            created_nodes[resource_id] = node_class(label)
    return created_nodes

def create_edges(nodes, relationships):
    edge_style = {
        'color': '#707070',
        'style': 'dashed',
        'penwidth': '0.5',
        'constraint': 'true',
        'weight': '1'
    }
    for source, target in relationships:
        if source in nodes and target in nodes:
            nodes[source] >> Edge(**edge_style) >> nodes[target]

def simplify_label(label):
    for prefix in ['Service', 'AWS', 'Task', 'Security']:
        label = label.replace(prefix, '')
    return label[:20] + '...' if len(label) > 20 else label

def process_svg_content(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as svg_file:
        svg_content = svg_file.read()
        return re.sub(
            r'xlink:href="(/usr/local/lib/python3.12/site-packages/resources/aws/[^"]+)"',
            lambda m: f'xlink:href="http://localhost:5001/icons/aws/{os.path.basename(m.group(1))}"',
            svg_content
        )
