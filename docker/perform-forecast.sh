#!/bin/bash

source /opt/tools/common-bash.sh

log="/opt/work/logs/forecast.log"
echo "" > $log

source /venv/bin/activate

lg "Starting"
pip list
last_status=0

if [[ "${ENV_REDTEN_FORECAST_NAME}" == "" ]]; then
    lg "Running Forecast: /opt/work/bins/forecast.py"
    /opt/work/bins/forecast.py 
    last_status=$?
else
    lg "Running Forecast: /opt/work/bins/forecast.py ${ENV_REDTEN_FORECAST_NAME}"
    /opt/work/bins/forecast.py ${ENV_REDTEN_FORECAST_NAME} 
    last_status=$?
fi

lg "Forecast exited with status: $last_status"
exit $last_status

lg "Done Starting"

lg "Exiting"

exit 0
