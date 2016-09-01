#!/bin/bash

set -e
set -x

yum -y update
yum -y upgrade
yum -y install python27-devel python27-pip gcc libjpeg-devel zlib-devel gcc-c++ libxml2-devel libxslt-devel
