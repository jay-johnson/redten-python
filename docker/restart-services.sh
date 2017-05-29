#!/bin/bash

source /opt/tools/common-bash.sh

log="/tmp/start-services.log"
echo "" > $log

if [[ "${ENV_DEBUG}" == "1" ]]; then
    echo "---------------------------"
    lgenv
    echo "---------------------------"
fi

lg "Restarting Services"

lg "Done Restarting Services"

exit 0
