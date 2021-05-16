#!/bin/sh
echo "Installing libxml2-dev g++ gcc libxslt-dev python3-dev packages"
RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
apk add libxml2-dev libxslt-dev python3-dev libffi-dev
echo "Done installing libxml2"
pip3 install lxml
pip3 install --upgrade pip setuptools wheel
pip3 install -r ${SRC_PKG}/requirements.txt -t ${SRC_PKG} && cp -r ${SRC_PKG} ${DEPLOY_PKG}
pip3 uninstall pandas
pip3 install numpy
pip3 install pandas
