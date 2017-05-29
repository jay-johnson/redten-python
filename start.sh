#!/bin/bash

if [[ -e ./docker/common-bash.sh ]]; then
    source ./docker/common-bash.sh
    log=/dev/null
fi

filetouse="./docker-compose.yml"

echo ""
amnt "Stopping Docker Composition($filetouse)"
docker-compose -f $filetouse stop

echo ""
amnt "Starting Docker Composition($filetouse)"
docker-compose -f $filetouse up -d

echo ""

exit 0
