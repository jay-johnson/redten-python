#!/bin/bash

container="rtpy"

echo "SSH-ing into Docker Container($container)"
docker exec -ti $container env TERM=xterm /bin/bash

exit 0
