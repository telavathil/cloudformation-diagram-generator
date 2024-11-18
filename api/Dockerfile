FROM python:3.12-slim

# Install system dependencies including ALL graphviz packages
RUN apt-get update && \
  apt-get install -y \
  graphviz \
  graphviz-dev \
  pkg-config \
  curl \
  gcc \
  g++ \
  make \
  fonts-liberation \
  git \
  && rm -rf /var/lib/apt/lists/*

# Install poetry and configure it
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.7.1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Install Poetry using the recommended method
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# First install diagrams normally
RUN pip install diagrams

# Then clone the repo and copy resources
RUN git clone https://github.com/mingrammer/diagrams.git /tmp/diagrams && \
  mkdir -p /usr/local/lib/python3.12/site-packages/diagrams/resources && \
  cp -r /tmp/diagrams/resources/* /usr/local/lib/python3.12/site-packages/diagrams/resources/ && \
  rm -rf /tmp/diagrams

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies directly with pip from poetry export
RUN poetry export -f requirements.txt --output requirements.txt && \
  pip install -r requirements.txt


# Copy the rest of the application
COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
