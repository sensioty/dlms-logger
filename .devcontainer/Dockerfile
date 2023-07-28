FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye


COPY requirements.txt /tmp/requirements.txt

## Pip dependencies
# Upgrade pip & install requirements
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt