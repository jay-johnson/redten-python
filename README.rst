================
Red10 Python API
================

The standalone python client and docker container for: https://redten.io

.. figure:: http://i.imgur.com/65dsKzX.png
    :alt: Red10 distributed machine learning on Redis

#.  To authenticate you will need valid login credentials

    - Username
    - Password
    - Email

#.  Please export these environment variables

    ::
    
        export ENV_REDTEN_USER=Username
        export ENV_REDTEN_PASS=Password
        export ENV_REDTEN_EMAIL=Email
        export ENV_REDTEN_URL=https://api.redten.io

#.  Optional exports

    Set the csv file path. Note this file must be accessible on all worker nodes.

    ::

        export ENV_REDTEN_CSV_FILE=<path to csv>

    Send forecast results to emails. Comma-separated without any spacing.

    ::

        export ENV_REDTEN_FORECAST_EMAILS=email1@email.com,email2@email.com

    Can also set it to an empty string which will skip sending emails:
    
    ::

        export ENV_REDTEN_FORECAST_EMAILS=

#.  Using the ``redten-python`` docker container

    Please note the docker image inflates to over 1 GB as it has the math libraries pandas and numpy installed.

    To run a forecast:

    ::

        ./run-forecast.sh
    
    Run predictions:

    ::

        ./run-predict.sh

#.  Install required pips

    If you do not want to use the docker container, here's how to setup the local environment.

    ::

        pip install -r requirements.txt

    Under the hood these are the current installed pips (pandas takes some time):

    ::
    
        pandas==0.20.0rc1
        requests>=2.13.0
        uuid>=1.30
        unittest2>=1.1.0
        simplejson>=3.10.0

#.  Install the pip from pypi repository

    ::

        pip install redten

#.  Run a forecast job

    ::

        ./bins/forecast.py <Dataset-Name>


#.  Run a prediction job

    ::

        ./bins/predict.py 

For more information:

#. `Intro`_
#. `Forecast`_
#. `Predictions with the IRIS dataset`_

.. _Intro: https://redten.io:8101/RedTen-Intro.slides.html#/
.. _Forecast: https://redten.io:8103/RT-Price-Forecast.slides.html#/
.. _Predictions with the IRIS dataset: https://redten.io:8102/RT-Run-IRIS.slides.html#/

=======
Version
=======

1.0.1


=========
Debugging
=========

I'm on fedora 24 and on a virtual env I started hitting:

::

    Failed to Run ML Job with exception='unknown error (_ssl.c:2831)'
    Predict job failed with error=Failed to Run ML Job with exception='unknown error (_ssl.c:2831)

After I reinstalled ``certifi`` it started working again.

::

    pip uninstall certifi
    pip install certifi

================
Release Commands
================

#. Upload to pypitest:

::

    python setup.py sdist upload -r pypitest

#. Upload to pypi:

::

    python setup.py sdist upload -r pypi
