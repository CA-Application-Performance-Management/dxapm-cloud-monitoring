# Spark Extension Deployment on Azure Databricks

# Description
This project is intended to install spark monitoring and host monitoring extension on azure databricks

## Short Description
Azure Databricks provides a way to install additional software or customization the configuration of Spark cluster. While creating/editing azure databricks cluster, It provides option to add an init-script. An init script is a shell script that runs during startup of each cluster node before the Apache Spark driver or worker JVM starts. We are enabling Spark Monitoring Extension on driver node and Host Monitor to each custer node to get the insight of spark cluster and its compute machine.

## APM version
APM 22.3

## Installation
To configure Spark Extension and HostMonitoringa, follow these steps:

### Download Agent
- Log in to DX APM.
- Open the DX Application Performance Management tile.
- In the left navigation, under Settings, click Agents.
- In the Settings Agents page, click Download Agent. The Select Agent to Download dialog opens with the agents that each operating system supports.
- Select UNIX as the operating system. Click on Infrastructure Agent 
- In the Infrastructure tab, select Spark and Host Monitoring. The Configure Spark dialog opens with Agent Controller
- Keep the downloaded tar file to upload on Azure Databricks Workspace.

### Download and Configure Databricks CLI
Azure Databricks Cli setup is requited to upload installation script and spark extension tar over azure databricks workspace. Follow below steps to install Databricks-cli.

- Launch your databricks workspace.
- Generate a personnel access token to configure in databricks-cli.
- Click Settings in the lower left corner of your Azure Databricks workspace.
- Click User Settings.
- Go to the Access Tokens tab.
- Click the Generate New Token button.
- Optionally enter a description (comment) and expiration period.
- Click the Generate button.
- Copy the generated token and store in a secure location.
- Install Databrick-cli following microsoft page. https://docs.microsoft.com/en-us/azure/databricks/dev-tools/cli/
- Configure credentials in databricks-cli. 
- Run "databricks configure --token"commands on console.
- It will prompt for hostname. Enter your per-workspace URL, with the format https://adb-<workspace-id>.<random-number>.azuredatabricks.net. Get it from your workspace address bar.
- Now it will prompt for token. enter the token you created above.

### Download init-script
- Download apmia-installation.sh script from github
- Keep the downloaded sh file to upload on Azure Databricks Workspace

### Upload init-script and tar file on Azure workspace
- Create a spark-monitoring directory on your workspace, running below command
    ```
    dbfs mkdirs dbfs:/databricks/spark-monitoring
    ```
- Upload apmia-installation.sh script on workspace. 
    ```
    dbfs cp --overwrite apmia-installation.sh dbfs:/databricks/spark-monitoring/
    ```
- Upload tar file on workspace. 
    ```
    dbfs cp --overwrite <downloaded_tar_file> dbfs:/databricks/spark-monitoring/
    ```
### Configure init-script path on Azure Databricks. 
- Go to your Park cluster and expand Advanced Options.
- Under the Spark tab, in the Spark Config field, add the below properties.
    ```
    spark.metrics.appStatusSource.enabled true 
    spark.metrics.executorMetricsSource.enabled true 
    spark.sql.streaming.metricsEnabled true 
    spark.metrics.staticSources.enabled true
    ```
-  Under the Init Scripts tab, 
    ```
    1) from Destination, select DBFS.
    2) In Init Script Path, type the script file path. For example, 
    3) dbfs:/databricks/spark-monitoring/apmia-installation.sh.
    4) Click Add.
    ```
- Under the Logging tab,
    ```
    1) from Destination, select DBFS.
    2) In the Cluster log path, type the cluster log path. For example, 
    3) dbfs:/cluster-logs.
    4) Click Add.
    ```
- Click Create.
- Restart the cluster.

## Troubleshooting
- Make sure while creating the cluster the Network Related setting for master, task or core nodes should have communication channels enabled to communicate with Enterprise Manager, So that Spark Monitor and HostMonitor can report the Metrics to Enterprise Manager with out any issue.
- In case Init-sciprt fails, check logs in configured directory Ex: `dbfs:/cluster-logs`
- In case Agent doesnt report metrics, check apmia logs available on `/etc/broadcom_apm/apmia/logs` path

# Change log
Changes for each version.

Version | Author | Comment
--------|--------|--------
1.0 | Deepak Tiwari | First version