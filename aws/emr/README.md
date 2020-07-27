# Enable Host Monitoring with AWS EMR Cluster nodes

# Description
This project is intended to enable Host Monitor for EC2 machine which are running under AWS EMR cluster.

## Short Description
EMR Bootstrap action to install additional software or customize the configuration of cluster instances. If you add nodes to a running cluster, bootstrap actions also run on those nodes in the same way. We are enabling Host Monitor to get the insight of coumpute machine under EMR cluster.

## APM version
APM 11.1.

## Prerequisites
- Download the latest `Host Monitor` extension from CA APM. And upload to s3 bucket.
- Download `install_host.sh` script. And upload to s3 bucket.

## Installation
While creating the cluster, configure and add Bootstrap Action. For example -
- AWS CLI
```
    --bootstrap-actions Path="s3://mybucket/install_host.sh",Args=["s3://mybucket/Host-apmia-xxx.tar"]
```
- AWS Console
    - Under Bootstrap Actions select Configure and add to specify the Name, Script location `s3://mybucket/install_host.sh`, and arguments as `s3://mybucket/Host-apmia-xxx.tar`. Choose Add.

## Troubleshooting
- Make sure while creating the cluster the security group for master, task or core nodes should have outbound traffic enable for Enterprise manager.
- For further investigation, bootstrap action logs can be check in here  `s3://mybucket/elasticmapreduce/<cluster id>/node/<instance id>/bootstrap-actions/`.

# Change log
Changes for each version.

Version | Author | Comment
--------|--------|--------
1.0 | Ankit Gupta | First version
