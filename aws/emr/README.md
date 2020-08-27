# Enable Host Monitoring with AWS EMR Cluster nodes

# Description
This project is intended to enable Host Monitor for EC2 machine which are running under AWS EMR cluster.

## Short Description
EMR Bootstrap action to install additional software or customize the configuration of cluster instances. If you add nodes to a running cluster, bootstrap actions also run on those nodes in the same way. We are enabling Host Monitor to get the insight of coumpute machine under EMR cluster.

## APM version
APM 11.1.

## Installation
To configure HostMonitor, follow these steps:
- Navigate to the DX Application Performance Management Console, and click Agents.
- Select an Agent and download the Hostmonitor on your Linux system. Upload the Hostmonitor to the S3 bucket where the EMR cluster is located.
- Download install_host.sh script and upload it to the S3 bucket where the EMR cluster is located.
- Configure and add Bootstrap Action while creating the cluster as follows:

	- AWS CLI
	    ```
            --bootstrap-actions Path="s3://mybucket/install_host.sh",Args=["s3://mybucket/Host-apmia-xxx.tar"]
        ```
	- AWS Console
        ```
		    Navigate to the Bootstrap actions tab, select Configure and add the following details:
		    Name: Specify the name for the bootstrap action.
		    Location: Specify the script location (s3://mybucket/install_host.sh).
		    Optional arguments: Specify the argument (s3://mybucket/Host-apmia-xxx.tar).
		    Select Add. The Bootstrap action is added.
        ```
	
## Uninstall HostMonitor
To uninstall the HostMonitor, follow these steps:
- Login to the EC2 system.
- Navigate to the apmia directory and run the following command:
    ```
	cd/home/hadoop/apm/apmia
    ```
- Run the following command to uninstall the HostMonitor.
    ```
	./APMIACtrl.sh uninstall
    ```

## Troubleshooting
- Make sure while creating the cluster the security group for master, task or core nodes should have outbound traffic enable for Enterprise manager.
- For further investigation, bootstrap action logs can be check in here  `s3://mybucket/elasticmapreduce/<cluster id>/node/<instance id>/bootstrap-actions/`.

# Change log
Changes for each version.

Version | Author | Comment
--------|--------|--------
1.0 | Ankit Gupta | First version