#!/bin/bash

curpip=pip2

log="/tmp/install-xgb.log"

install_dir="/opt"

if [[ -e /venv/bin/pip ]]; then
    curpip=/venv/bin/pip
else
    if [[ -e /opt/redten/venv/bin/pip ]]; then
        curpip=/opt/redten/venv/bin/pip
    elif [[ -e /opt/conda/envs/python2/bin/pip ]]; then
        curpip=/opt/conda/envs/python2/bin/pip
    fi
fi

pushd ${install_dir} >> /dev/null

echo "" > $log
date >> $log
echo "Uninstalling XGBoost" &>> $log
${curpip} uninstall -y xgboost &>> $log

if [[ -e "${install_dir}/xgboost" ]]; then
    pushd ${install_dir}/xgboost
    echo "Updating repo: ${install_dir}/xgboost" &>> $log
    git pull &>> $log
    popd
else
    echo "Cloning repo: ${install_dir}/xgboost" &>> $log
    git clone --recursive https://github.com/dmlc/xgboost.git &>> $log
fi

echo "Installing XGBoost" &>> $log
cd xgboost  
./build.sh &>> $log
${curpip} install -e python-package &>> $log
last_status=$?
if [[ "${last_status}" != "0" ]]; then
    echo "Failed to Install xgboost" &>> $log
    exit 1
fi

test_installed=$(${curpip} list | grep "xgboost" | wc -l)
if [[ "${test_installed}" == "0" ]]; then
    echo "Did not find ${curpip} for xgboost" &>> $log
    exit 1
fi

echo "Done installing xgboost" &>> $log

exit 0
