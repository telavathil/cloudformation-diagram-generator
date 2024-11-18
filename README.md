# CloudFormation Diagram Generator

A web application that generates architecture diagrams from AWS CloudFormation templates. Built with React, Flask, and the Python Diagrams library.

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

3. Access the application at http://localhost:5173

To stop the application:
  ```bash
  make stop
  ```

## Development Commands

- `make test` - Run all tests
- `make lint` - Run linters
- `make clean` - Clean temporary files
- `make help` - Show all available commands

