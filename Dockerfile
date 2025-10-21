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

WORKDIR /bn_training
COPY . .

ENTRYPOINT ["./setup_piper.sh"]

CMD ["bash"]
