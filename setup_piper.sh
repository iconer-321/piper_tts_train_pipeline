#!/bin/bash
set -e  # Exit immediately on error
ROOT_DIR=$(pwd)
echo "🔧 [Setup] Updating package lists and installing system dependencies..."

# Install system dependencies
apt update
apt install -y \
    ffmpeg \
    espeak-ng \

echo "✅ [Setup] System packages installed."

# Create and activate virtual environment



echo "🐍 [Setup] Creating Python virtual environment..."

if [ ! -d "$VIRTUAL_ENV" ]; then
    echo "🐍 [Setup] Creating Python virtual environment..."
    python3 -m venv "$VIRTUAL_ENV"
fi

source "$VIRTUAL_ENV/bin/activate"

# Downgrade pip to a version compatible with legacy metadata
python3.10 -m pip install pip==23.3.1

# Install required Python packages inside the virtual environment
pip install numpy==1.24.4
pip install torchmetrics==0.11.4
pip install python-dotenv==1.1.1
pip install boto3==1.39.4

# Go to Piper directory
git clone -q https://github.com/masumr/viva_piper_fork.git
cd viva_piper_fork/src/python


# Install the local package in editable mode
python3.10 -m pip install --upgrade wheel setuptools
pip install -e .

# Make the script executable
chmod +x build_monotonic_align.sh

# Run the monotonic alignment build script
./build_monotonic_align.sh
cd "$ROOT_DIR"
echo "🎉 [Setup Complete] Piper environment is ready."
