FROM centos:7
MAINTAINER Jay Johnson <jay.p.h.johnson@gmail.com>

# Install baseline os
RUN yum -y update && yum -y install epel-release && yum clean all
RUN yum -y install python-pip \
    && yum clean all \
    && pip install --upgrade pip \
    && yum -y install git \
        python-pip \
        python-setuptools \
        net-tools \
        wget \
        curl \
        mlocate \
        boost \
        boost-devel \
        make \
        autoconf \
        gcc \
        libffi-devel \
        libxml2-devel \
        perl \
        perl-devel \
        curl-devel \
        python-devel \
        libxslt \
        libxslt-devel \
        pcre-devel \
        gcc-c++ \
        sqlite-devel \
        procps \
        which \
        hostname \
        telnet \
        vim-enhanced \
        unzip \
        tkinter \
        net-tools \
        gcc-c++

# Allow running starters from outside the container

# Environment Deployment Type
ENV ENV_DEPLOYMENT_TYPE DEV
ENV ENV_PROJ_DIR /opt/work
ENV ENV_PROJ_SRC_DIR /opt/work/src
ENV ENV_DATA_DIR /opt/work/data
ENV ENV_DATA_SRC_DIR /opt/work/data/src
ENV ENV_DATA_DST_DIR /opt/work/data/dst
ENV ENV_SRC_DIR /opt/dev/src

# Allow running starters from outside the container
ENV ENV_BIN_DIR /opt/work/bins
ENV ENV_PRESTART_SCRIPT /opt/tools/pre-start.sh
ENV ENV_START_SCRIPT /opt/tools/start-services.sh
ENV ENV_POSTSTART_SCRIPT /opt/tools/post-start.sh
ENV ENV_CUSTOM_SCRIPT /opt/tools/custom-pre-start.sh

RUN mkdir -p -m 777 /opt \
    && mkdir -p -m 777 /opt/deps \
    && mkdir -p -m 777 /opt/work \
    && mkdir -p -m 777 /opt/work/src \
    && mkdir -p -m 777 /opt/shared \
    && mkdir -p -m 777 /opt/tools \
    && touch /tmp/firsttimerunning

WORKDIR /opt/work

# Add the starters and installers:
ADD ./docker/ /opt/tools/

# Add files to start default-locations
RUN chmod 777 /opt/tools/*.sh \
    && mv /opt/tools/python2 /opt/ \
    && chmod 777 /opt/python2 \
    && cp /opt/tools/pre-start.sh /usr/local/bin/ \
    && cp /opt/tools/start-container.sh /usr/local/bin/ \
    && cp /opt/tools/post-start.sh /usr/local/bin/ \
    && cp /opt/tools/custom-pre-start.sh /usr/local/bin/ \
    && cp /opt/tools/start-container.sh /opt/start-container.sh \
    && cp /opt/start-container.sh /usr/local/bin/start-container.sh 

RUN ls /opt
RUN ls /opt/tools

RUN pip install virtualenv && virtualenv /venv && /opt/python2/install_pips.sh

RUN /venv/bin/pip freeze > /opt/shared/python2-requirements.txt 

CMD [ "/opt/start-container.sh" ]
