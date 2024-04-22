#!/bin/sh
set -e
docker compose stop
docker compose rm -svf
docker images | egrep 'security-comparison-apps-.+' | awk '{ print $1 }' | xargs docker rmi -f

rm safe_app/.docker.env

rm unsafe_app/.docker.env

# docker volume list | egrep 'security-comparison-apps-.+data' | awk '{ print $2 }' | xargs docker volume rm
