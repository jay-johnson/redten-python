#!/bin/bash

source /opt/tools/common-bash.sh

log="/opt/work/logs/prediction.log"
echo "" > $log

source /venv/bin/activate

lg "Starting"
pip list
last_status=0

if [[ "${ENV_REDTEN_PREDICTION_NAME}" == "" ]]; then
    lg "Running Predict: /opt/work/bins/predict.py"
    /opt/work/bins/predict.py
    last_status=$?
else
    lg "Running Predict: /opt/work/bins/predict.py ${ENV_REDTEN_PREDICTION_NAME}"
    /opt/work/bins/predict.py ${ENV_REDTEN_PREDICTION_NAME}
    last_status=$?
fi

lg "Predict exited with status: $last_status"
exit $last_status

lg "Done Starting"

lg "Exiting"

exit 0
