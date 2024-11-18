# Development stage only
FROM node:20-alpine

WORKDIR /app

# First, copy only package files to leverage Docker cache
COPY package*.json ./
COPY tsconfig*.json ./

# Clean install dependencies
RUN rm -rf node_modules && \
  npm cache clean --force && \
  npm install

# Copy the rest of the application
COPY . .

# Add these environment variables
ENV NODE_ENV=development

EXPOSE 5173

# The command will be specified in docker-compose.yml
