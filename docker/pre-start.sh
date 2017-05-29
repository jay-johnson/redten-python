#!/bin/bash

source /opt/tools/common-bash.sh

log="/tmp/pre-start.log"
echo "" > $log

lg "Running Pre-Start"

if [[ "${ENV_PRESTART_UPDATE_PIPS}" == "1" ]]; then
    if [[ -e /opt/python2/install_pips.sh ]]; then
        lg "Updating pips with: /opt/python2/install_pips.sh"
        /opt/python2/install_pips.sh
        xerr "Failed to update pips. Stopping container."
        lg "Done Updating pips with: /opt/python2/install_pips.sh"
    fi
fi

lg "Done Pre-Start"

exit 0
