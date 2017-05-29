#!/bin/bash

curpip=pip2

echo "Installing newest pip"
${curpip} install --upgrade pip && ${curpip} install --upgrade setuptools
echo ""

echo "Listing current pips"
${curpip} list --format=columns
echo ""

numpips=$(cat ./primary-requirements.txt | wc -l)
if [[ "${numpips}" != "0" ]]; then
    echo "Installing Primary set of pips(${numpips})"
    ${curpip} install --upgrade -r ./primary-requirements.txt
    last_status="$?"
    if [[ "${last_status}" != "0" ]]; then
        echo "Failed to install Primary Python 2 requirements"
        exit 1
    fi
fi

numpips=$(cat ./secondary-requirements.txt | wc -l)
if [[ "${numpips}" != "0" ]]; then
    echo "Installing Secondary set of pips(${numpips})"
    ${curpip} install --upgrade -r ./secondary-requirements.txt
    last_status="$?"
    if [[ "${last_status}" != "0" ]]; then
        echo "Failed to install Secondary Python 2 requirements"
        exit 1
    fi
fi

numpips=$(cat ./tertiary-requirements.txt | wc -l)
if [[ "${numpips}" != "0" ]]; then
    echo "Installing Tertiary set of pips(${numpips})"
    ${curpip} install --upgrade -r ./tertiary-requirements.txt
    last_status="$?"
    if [[ "${last_status}" != "0" ]]; then
        echo "Failed to install Tertiary Python 2 requirements"
        exit 1 
    fi
fi

# left them if you want to play around...not all of the alpine deps build perfectly

#./install_xgboost.sh
#last_status="$?"
#if [[ "${last_status}" != "0" ]]; then
#    echo "Failed to install xgboost for Python 2 requirements"
#    exit 1 
#fi

#./install_tensorflow.sh
#last_status="$?"
#if [[ "${last_status}" != "0" ]]; then
#    echo "Failed to install Tensorflow Python 2 requirements"
#    exit 1 
#fi

echo "Listing updated version of installed pips:"
${curpip} list --format=columns
echo ""

exit 0
