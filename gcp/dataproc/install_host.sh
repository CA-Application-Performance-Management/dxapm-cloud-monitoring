#!/bin/bash
set -ex
#replace the URI path of the Host Monitor Agent in below command before uploading this script to Storage Bucket
gsutil cp gs://storagebucket/Host-apmia-xxxxxxxx_v1.tar host.tar.gz
mkdir -p /home/hadoop/apm
export APM_HOME=/home/hadoop/apm
chmod 777 host.tar.gz
tar -xvf ./host.tar.gz -C $APM_HOME
rm -rf host.tar.gz
sudo $APM_HOME/apmia/APMIACtrl.sh install
