"""
Flask application for diagram generation service.

This module provides a REST API service for generating diagrams.
"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from src.routes.diagram_routes import register_routes

# Load environment variables before creating Flask app
load_dotenv()

app = Flask(__name__)
CORS(app)

# Register routes
register_routes(app)

if __name__ == '__main__':
    app.run(host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 5001)),
            debug=bool(os.getenv('FLASK_DEBUG', True)))
