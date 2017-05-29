#!/bin/bash

echo "Loading common bash methods"
source /opt/tools/common-bash.sh

log="/tmp/container.log"
echo "" > $log

lg "Starting Container"
date >> $log
lg ""

lg "Activating Virtual Env"
source /venv/bin/activate

lg "Starting Container Services"

prestartscript="$ENV_PRESTART_SCRIPT"
startscript="$ENV_START_SCRIPT"
poststartscript="$ENV_POSTSTART_SCRIPT"
customprestartscript="$ENV_CUSTOM_SCRIPT"

if [ -e "$customprestartscript" ]; then
    lg "Starting Custom Script($customprestartscript)"
    $customprestartscript 
    lg "Done Custom Script($customprestartscript)"
else
    lg "Custom Script does not Exist($customprestartscript)"
fi

if [ -e "$prestartscript" ]; then
    lg "Running PreStart($prestartscript)"
    $prestartscript 
    lg "Done Running PreStart($prestartscript)"
else
    lg "PreStart does not Exist($prestartscript)"
fi

if [ -e "$startscript" ]; then
    lg "Running Start($startscript)"
    $startscript 
    lg "Done Running Start($startscript)"
else
    lg "Start does not Exist($startscript)"
fi

if [ -e "$poststartscript" ]; then
    lg "Running PostStart($poststartscript)"
    $poststartscript 
    lg "Done Running PostStart($poststartscript)"
else
    lg "PostStart does not Exist($poststartscript)"
fi

lg "Done Starting Container Services"

exit 0
