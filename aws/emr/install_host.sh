#!/bin/bash
set -ex
url=${1?Error: no url given}
aws s3 cp $url host.tar.gz
mkdir -p /home/hadoop/apm
export APM_HOME=/home/hadoop/apm
chmod 777 host.tar.gz
tar -xvf ./host.tar.gz -C $APM_HOME
rm -rf host.tar.gz
sudo $APM_HOME/apmia/APMIACtrl.sh install
