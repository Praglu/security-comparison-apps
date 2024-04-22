FROM python:3.12-alpine

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get install -y \
  netcat \
  gettext \
  supervisor \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements /code/requirements
RUN pip install -r requirements/development.txt

COPY server /code
COPY bin/entrypoint.dev.sh /bin/
RUN chmod +x /bin/entrypoint.dev.sh

EXPOSE 8000
CMD ["sh", "/bin/entrypoint.dev.sh"]
