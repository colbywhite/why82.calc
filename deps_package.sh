#!/bin/bash

set -e
set -x

mkdir -p /opt/why82
cp -r /why82/lib/python2.7/site-packages/* /opt/why82
cp -r /why82/lib64/python2.7/site-packages/* /opt/why82
cd /opt/why82/
tar -cvzf /vagrant/why82.tar.gz .