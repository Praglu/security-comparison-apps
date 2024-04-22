#!/bin/bash
set -e
cp -n safe_app/env-example safe_app/.docker.env

cp -n unsafe_app/env-example unsafe_app/.docker.env

docker compose build
docker compose up --no-start
