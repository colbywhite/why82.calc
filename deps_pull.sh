#!/bin/bash

set -e

OPTIONS=`vagrant ssh-config | tail -n +2 | head -n 9 | awk -v ORS=' ' '{print "-o " $1 "=" $2}'`
CUR_DIR=`pwd`

set -x

scp ${OPTIONS} blah:/vagrant/why82.tar.gz why82.tar.gz
