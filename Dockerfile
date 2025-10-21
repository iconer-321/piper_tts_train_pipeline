FROM python:3.10

# Set virtual environment path
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install system dependencies required for Piper
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    ffmpeg \
    espeak-ng \
    sox \
    libsndfile1-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv $VIRTUAL_ENV

WORKDIR /piper_tts_train_pipeline

# Copy only setup script first so it can run before copying the rest
COPY setup_piper.sh .

# Run setup script
RUN chmod +x setup_piper.sh && ./setup_piper.sh

# Now copy all files (after setup is done)
COPY . .

CMD ["bash"]
