# Spark Extension Deployment on Azure Databricks

# Description
These instructions will guide you install spark monitoring and host monitoring extensions on azure databricks

## Short Description
Azure Databricks provides a way to install additional software and gives the option to customize the configuration of the Spark cluster. While creating/editing the Azure Databricks cluster, it provides the option to add an init-script. An init script is a shell script that runs during the startup of each cluster node before the Apache Spark driver and worker JVM starts. We will be enabling Spark Monitoring Extension on the Driver node and Host Monitoring Extension on each cluster node to get the insights of the Spark cluster and its compute machines.

## APM version
APM 22.3

## Installation
To configure Spark Monitoring and Host Monitoring extensions, follow these steps:

### Download Agent
- Log in to DX APM.
- Open the **DX Application Performance Management** tile.
- In the left navigation panel, click on **Agents**.
- In the Agents page, click on **Download Agent**. 
- On **Select Agent to Download** Page, Select UNIX as the operating system, then click on the **Infrastructure Agent** option.
- The **Configure Infrastructure Agent** dialog opens with Agent Controller, Attribute Decorator and Http Collector selected.
- In this dialog, select Spark and Host Monitoring, Configure the properties as described there.
- Click **Download**. The Infrastructure Agent is downloaded with Spark and Host Monitoring enabled.
- The **downloaded tar** file will later be uploaded to the Azure Databricks Workspace.

### Download init-script
- Download **apmia-installation.sh** script from the github repository. Here is the github link path
  ```
  https://github.com/CA-Application-Performance-Management/dxapm-cloud-monitoring/blob/master/azure/databricks/apmia-installation.sh
  ```  
  **Note**: downloaded sh file should be unix compatible
- The downloaded **apmia-installation.sh** file will later be uploaded to the Azure Databricks Workspace.

### Download and Configure Databricks CLI
Azure Databricks CLI setup is required to upload the installation script and the Spark Monitoring extension tar to the Azure Databricks Workspace. Follow the below steps to install the Databricks-CLI.

- Launch your Databricks Workspace.
- A personnel access token needs to be generated, this token will later be configured in Databricks-CLI
- To generate the token, click on the **Settings** in the lower left corner of your Azure Databricks workspace.
- Click **User Settings**.
- Go to the **Access Tokens tab**.
- Click the **Generate New Token** button.
- Optionally enter a description (comment) and expiration period.
- Click the **Generat**e button.
- Copy the generated token and store in a secure location.
- Install Databrick-cli following microsoft page. https://docs.microsoft.com/en-us/azure/databricks/dev-tools/cli/
- Configure credentials in databricks-cli. 
- Run `databricks configure --token` commands on console.
- It will prompt for hostname. Enter your per-workspace URL, with the format https://adb-<workspace-id>.<random-number>.azuredatabricks.net. Get it from your workspace address bar.
- Now it will prompt to enter the access token, enter the token that was generated in the above steps.

### Upload init-script and tar file on Azure workspace
- Create a spark-monitoring directory on your workspace, running below command
    ```
    dbfs mkdirs dbfs:/databricks/spark-monitoring
    ```
- Upload apmia-installation.sh script to workspace. 
    ```
    dbfs cp --overwrite apmia-installation.sh dbfs:/databricks/spark-monitoring/
    ```
- Upload tar file to workspace. 
    ```
    dbfs cp --overwrite <downloaded_tar_file> dbfs:/databricks/spark-monitoring/
    ```
### Configure init-script path on Azure Databricks. 
- Go to your Spark cluster and expand Advanced Options.
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

### Verify that the Spark Agent is connected
- On **DX Application Performance Management**, In the left navigation panel, click on **Agents**.
- Check if databricks cluster's master hostname (**ClusterID-MasterIP**) is listed there. You may find the `Cluster ID` on the cluster's environment tab.

## Troubleshooting
- Make sure while creating the cluster the Network Related setting for master, task or core nodes should have communication channels enabled to communicate with Enterprise Manager, So that Spark Monitor and HostMonitor can report the Metrics to Enterprise Manager without any issue.
- In case Init-sciprt fails, check logs in configured directory Ex: `dbfs:/cluster-logs`
- In case Agent doesnt report metrics, check apmia logs available on `/etc/broadcom_apm/apmia/logs` path

# Change log
Changes for each version.

Version | Author | Comment
--------|--------|--------
1.0 | Deepak Tiwari | First version