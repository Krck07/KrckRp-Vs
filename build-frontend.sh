#!/bin/bash

# Build script for KrckRP frontend

cd frontend

echo "Building frontend..."
npm run build

if [ $? -eq 0 ]; then
    echo "Frontend built successfully!"
else
    echo "Failed to build frontend"
    exit 1
fi