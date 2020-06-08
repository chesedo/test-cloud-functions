# Update the VARIANT arg in devcontainer.json to pick a Python version: 3, 3.8, 3.7, 3.6
ARG VARIANT="3.7"
FROM python:${VARIANT}-slim as base

# Update the FUNCTION arg in devcontainer.json to customise this image per cloud function
ARG FUNCTION="function-name"

COPY $FUNCTION/requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

from base as debug

# For access needed by aliases
ARG FUNCTION="function-name"
ENV FUNCTION $FUNCTION

COPY _container/aliases.sh /tmp/
RUN cat /tmp/aliases.sh >> ~/.bashrc \
   && rm -f /tmp/aliases.sh

COPY _container/commands/* /usr/bin/

COPY _container/flake8.ini /root/.config/flake8
COPY _container/mypy.ini /root/.config/mypy/config

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
   && apt-get -y install --no-install-recommends git \
   && apt-get autoremove -y \
   && apt-get clean -y \
   && rm -rf /var/lib/apt/lists/*
ENV DEBIAN_FRONTEND=dialog

COPY _container/requirements.devel.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.devel.txt \
   && rm -rf /tmp/pip-tmp