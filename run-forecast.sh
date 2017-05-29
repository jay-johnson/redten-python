#!/bin/bash

filetouse="./forecast-compose.yml"

echo ""
echo "Stopping Docker Composition: $filetouse"
docker-compose -f $filetouse stop

echo ""
echo "Starting Docker Composition: $filetouse"
docker-compose -f $filetouse up

echo ""

exit 0
