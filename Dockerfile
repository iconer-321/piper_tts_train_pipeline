FROM python:3.10-slim

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    espeak-ng \
    sox \
    ffmpeg \
    wget \
    libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv $VIRTUAL_ENV
RUN pip install --no-cache-dir pip==23.3.1 setuptools wheel
RUN pip install --no-cache-dir numpy==1.24.4 torchmetrics==0.11.4
RUN pip install python-dotenv==1.1.1
RUN pip install boto3==1.39.4


RUN mkdir /bn_training
WORKDIR /bn_training

RUN git clone https://github.com/rhasspy/piper.git
WORKDIR /bn_training/piper/src/python
RUN pip install --no-cache-dir -e .
RUN chmod +x ./build_monotonic_align.sh && ./build_monotonic_align.sh
COPY . .

CMD ["bash"]