#!/bin/bash

source /opt/tools/common-bash.sh

log="/tmp/start-services.log"
echo "" > $log

source /venv/bin/activate

if [[ "${ENV_DEBUG}" == "1" ]]; then
    echo "---------------------------"
    lgenv
    echo "---------------------------"
fi

lg "Starting"
last_status=0
if [[ "${ENV_REDTEN_FORECAST}" != "" ]]; then
    lg "Running Forecast: ${ENV_REDTEN_FORECAST}"
    ${ENV_REDTEN_FORECAST}
    last_status=$?
    lg "Forecast exited with status: $last_status"
    exit $last_status
elif [[ "${ENV_REDTEN_PREDICTION}" != "" ]]; then
    lg "Running Prediction ${ENV_REDTEN_PREDICTION}"
    $ENV_REDTEN_PREDICTION
    last_status=$?
    lg "Prediction exited with status: $last_status"
    exit $last_status
fi

lg "Done Starting"

echo "Preventing the container from exiting"
tail -f /tmp/start.log
echo "Done preventing the container from exiting"

lg "Exiting"

exit 0
