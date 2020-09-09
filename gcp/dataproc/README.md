# Enable Host Monitoring with GCP Dataproc Cluster nodes

# Description
This project is intended to enable Host Monitor for GCP Compute VM machine which are running under GCP Dataproc cluster.

## Short Description
GCP Dataproc Initialization action to install additional software or customize the configuration of cluster instances. If you add nodes to a running cluster, Initialization actions also run on those nodes in the same way. We are enabling Host Monitor to get the insight of compute machine under Dataproc cluster.

## APM version
APM 11.1.

## Installation
To configure HostMonitor, follow these steps:
- Navigate to the DX Application Performance Management Console, and click Agents.
- Select an Agent and download the Hostmonitor on your Linux system. Upload the Hostmonitor to the Storage bucket, which is associated with the Dataproc cluster.
- Download install_host.sh script from github and replace the actual URI path of the Hostmonitor Agent in script(Line 4), upload it to the Storage bucket, which is associated with the Dataproc cluster.
- Configure and add Initialization Action while creating the cluster as follows:

	- GCP CLI Argument
	    ```
           --initialization-actions=gs://mystoragebucket/install_host.sh
        ```
	- GCP Console
        ```
		    while creating the cluster click on Advanced options:
		    Under the heading - Initialization actions (Optional)
			Click Button - Add initialization action
			Then a new textbox with Browse button Option will be provided, where either we can browse the storage bucket location of install_host.sh, or if we have the path handy it can be pasted in the textbox.
        ```
	Note: 1. mystoragebucket is sample Storage Bucket Name Used, we need to use the URI path of the script location of install_host.sh
	      2. replace the Actual APMIA HostMonitor File URI Path in the install_host.sh (Line number 4), before uploading the install_host.sh to Storage Bucket	      
## Uninstall HostMonitor
To uninstall the HostMonitor, follow these steps:
- Login to the GCP Compute VM instance.
- Navigate to the apmia directory and run the following command:
    ```
	cd /home/hadoop/apm/apmia
    ```
- Run the following command to uninstall the HostMonitor.
    ```
	./APMIACtrl.sh uninstall
    ```

## Troubleshooting
- Make sure while creating the cluster the Network Related setting for master, task or core nodes should have communication channels enabled to communicate with Enterprise Manager, So that HostMonitor can report the Metrics to Enterprise Manager with out any issue.

# Change log
Changes for each version.

Version | Author | Comment
--------|--------|--------
1.0 | Siva Teja Varun Bysani | First version