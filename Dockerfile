FROM python:3.10

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    ffmpeg \
    espeak-ng \
    sox \
    libsndfile1-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv $VIRTUAL_ENV

WORKDIR /piper_tts_train_pipeline

COPY setup_piper.sh .
RUN chmod +x setup_piper.sh && ./setup_piper.sh

# Copy all remaining files
COPY . .

# Default command: activate venv and run Python main.py
CMD ["bash", "-c", "source $VIRTUAL_ENV/bin/activate && python3 main.py"]
