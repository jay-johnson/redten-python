#!/bin/bash

curpip=pip2

virtualenv /venv

if [[ -e /venv/bin/pip ]]; then
    curpip=/venv/bin/pip
    source /venv/bin/activate
else
    err "Missing virtual env: /venv"
    exit 1
fi

echo "Installing newest pip"
${curpip} install --upgrade pip && ${curpip} install --upgrade setuptools
echo ""

echo "Listing current pips"
${curpip} list --format=columns
echo ""

numpips=$(cat /opt/python2/primary-requirements.txt | wc -l)
if [[ "${numpips}" != "0" ]]; then
    echo "Installing Primary set of pips(${numpips})"
    ${curpip} install --upgrade -r /opt/python2/primary-requirements.txt
    last_status="$?"
    if [[ "${last_status}" != "0" ]]; then
        echo "Failed to install Primary Python 2 requirements"
        exit 1
    fi
fi

numpips=$(cat /opt/python2/secondary-requirements.txt | wc -l)
if [[ "${numpips}" != "0" ]]; then
    echo "Installing Secondary set of pips(${numpips})"
    ${curpip} install --upgrade -r /opt/python2/secondary-requirements.txt
    last_status="$?"
    if [[ "${last_status}" != "0" ]]; then
        echo "Failed to install Secondary Python 2 requirements"
        exit 1
    fi
fi

numpips=$(cat /opt/python2/tertiary-requirements.txt | wc -l)
if [[ "${numpips}" != "0" ]]; then
    echo "Installing Tertiary set of pips(${numpips})"
    ${curpip} install --upgrade -r /opt/python2/tertiary-requirements.txt
    last_status="$?"
    if [[ "${last_status}" != "0" ]]; then
        echo "Failed to install Tertiary Python 2 requirements"
        exit 1 
    fi
fi

# This is getting updated for the latest pandas on pypi...for now here's the best we got:
${curpip} install git+https://github.com/pydata/pandas-datareader.git

echo "Listing updated version of installed pips:"
${curpip} list --format=columns
echo ""

exit 0
