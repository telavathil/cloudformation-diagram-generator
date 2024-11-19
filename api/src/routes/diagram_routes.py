from flask import jsonify, request, send_from_directory
from ..services.cloudformation_parser import parse_cloudformation
from ..services.diagram_generator import generate_diagram
import os
import diagrams

def register_routes(app):
    @app.route('/generate-diagram', methods=['POST'])
    def generate_diagram_route():
        try:
            yaml_content = request.json.get('yaml')
            if not yaml_content:
                return jsonify({'error': 'No YAML content provided'}), 400

            nodes, relationships = parse_cloudformation(yaml_content)
            svg_content = generate_diagram(nodes, relationships)
            return svg_content, 200, {'Content-Type': 'image/svg+xml'}

        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/icons/aws/<filename>')
    def serve_aws_icon(filename):
        resources_path = os.path.join(os.path.dirname(diagrams.__file__), "resources", "aws")
        try:
            for root, _, files in os.walk(resources_path):
                if filename in files:
                    return send_from_directory(root, filename)
            return "Icon not found", 404
        except Exception as e:
            app.logger.error(f"Error serving icon {filename}: {str(e)}")
            return f"Icon not found: {filename}", 404 