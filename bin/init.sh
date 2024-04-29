#!/bin/bash
set -e
cp -n safe_app/env-example safe_app/.docker.env

cp -n unsafe_app/env-example unsafe_app/.docker.env

touch unsafe_app/server/unsafe_sqlite.db

docker compose build
docker compose up --no-start
