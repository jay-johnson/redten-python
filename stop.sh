#!/bin/bash

source ./properties.sh 

filetouse="./docker-compose.yml"

echo "Stopping Docker image($registry/$maintainer/$imagename)"
docker-compose -f $filetouse down
docker stop $imagename &>> /dev/null
docker stop rtpy &>> /dev/null
docker rm rtpy &>> /dev/null

exit 0
