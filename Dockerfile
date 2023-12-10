FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update

RUN apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential \
    git \
    python3.10 \
    python3-pip


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY setup.cfg /app/
COPY pyproject.toml /app/
COPY setup.py /app/
COPY src /app/src

RUN pip install .

EXPOSE 5000

ENTRYPOINT ["dlim_api"]