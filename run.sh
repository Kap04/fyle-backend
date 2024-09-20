#!/bin/bash

# to stop on first error
set -e

# Activate the virtual environment
source env/Scripts/activate

# Run the server with waitress
waitress-serve --host=0.0.0.0 --port=8000 core.server:app
