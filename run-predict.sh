#!/bin/bash

filetouse="./predict-compose.yml"

echo ""
echo "Stopping Docker Composition: $filetouse"
docker-compose -f $filetouse stop

echo ""
echo "Starting Docker Composition: $filetouse"
docker-compose -f $filetouse up 

exit 0
