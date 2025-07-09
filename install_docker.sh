#!/bin/bash

# Install Docker Desktop for macOS
brew install --cask docker

# Start Docker Desktop
open /Applications/Docker.app

# Create docker group if it doesn't exist
sudo dseditgroup -o create docker

# Add user to docker group
sudo dseditgroup -o edit -a $(whoami) -t user docker

# Add Docker to PATH
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
docker --version
docker compose version