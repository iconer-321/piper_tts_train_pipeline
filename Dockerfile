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

# Create a virtual environment
RUN python -m venv $VIRTUAL_ENV

WORKDIR /piper_tts_train_pipeline
COPY . .

ENTRYPOINT ["./setup_piper.sh"]

CMD ["bash", "-c", "source $VIRTUAL_ENV/bin/activate && python3 main.py"]
