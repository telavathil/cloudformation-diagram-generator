# CloudFormation Diagram Generator

Automatically generate architecture diagrams from AWS CloudFormation templates. This tool simplifies the visualization of cloud infrastructure by converting YAML-based CloudFormation templates into clear, professional architecture diagrams.

## Overview

The CloudFormation Diagram Generator is a web-based tool that helps developers and architects visualize their AWS infrastructure. By parsing CloudFormation templates, it creates interactive diagrams that make it easier to understand, document, and share your cloud architecture.

### Key Features

- 🔄 Diagram generation from CloudFormation YAML
- 📝 Interactive YAML editor with syntax highlighting
- 🎨 Clean, professional diagram output in SVG format
- 🏗️ Support for common AWS resources and their relationships
- 📱 Responsive design for desktop and mobile viewing

### Why Use This Tool?

- **Simplify Documentation**: Automatically create visual documentation from your existing CloudFormation templates
- **Improve Communication**: Share clear visualizations with team members and stakeholders
- **Catch Issues Early**: Visualize your infrastructure before deployment to identify potential problems
- **Save Time**: Eliminate the need for manual diagram creation and updates

## Features

- YAML editor with syntax highlighting
- Real-time diagram generation
- Support for common AWS resources
- Interactive SVG output

## Prerequisites

- Python 3.12.2
- Node.js 22.6.0
- [asdf](https://asdf-vm.com/) version manager
- [Poetry](https://python-poetry.org/) for Python dependency management
- [Docker](https://www.docker.com/) (optional, for containerized deployment)

## Installation & Setup

### Using Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd cloudformation-diagram-generator
   ```

2. Build and run the application:

   ```bash
   make build  # Build Docker images
   make run    # Start the application
   ```

3. Access the application at <http://localhost:5173>

To stop the application:

  ```bash
  make stop
  ```

## Development Commands

- `make test` - Run all tests
- `make lint` - Run linters
- `make clean` - Clean temporary files
- `make help` - Show all available commands
