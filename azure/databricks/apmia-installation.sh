#!/bin/bash
mkdir -p /etc/broadcom_apm
# For spark monitoring, we are using spark-driver-ip and spark-ui-port. This spark-ui-port is created after init script file execution finishes. so we created below file with in init-script and run it as seprate process.
cat <<EOF >> /etc/broadcom_apm/agentinstallation.sh 
#!/bin/bash
# Give 1 minute of sleep so that file is genrated sussessfully from where spark-ui-port is extracted.
sleep 1m 
# below commands gives uploaded latest tar file available in spark-monitoring folder
APMIA_TAR_FILE=\$(find /dbfs/databricks/spark-monitoring/ -type f -iname 'Infrastructure*' | sort -n | head -1)
# Extract tar file and install apmia
tar -xvf \$APMIA_TAR_FILE -C /etc/broadcom_apm/
/etc/broadcom_apm/apmia/APMIACtrl.sh install
# Give 1 minute sleep just to insall apmia successfully.
sleep 1m
if [ $DB_IS_DRIVER = TRUE ]
then
# this sections update spark driver ip and port in bundle.properties
    SPARK_EXT_DIR=\$(find /etc/broadcom_apm/apmia/extensions -type d -iname "*spark-*")
    SPARK_UI_PORT=\$(grep -i 'CONF_UI_PORT' /tmp/driver-env.sh | cut -d'=' -f2)
    \$(sed -i '/introscope.agent.spark.profiles.default.url/d' \$SPARK_EXT_DIR/bundle.properties)
    \$(sed -i '/introscope.agent.spark.profiles.default.port/d' \$SPARK_EXT_DIR/bundle.properties)
    echo introscope.agent.spark.profiles.default.url=http://$DB_DRIVER_IP:\$SPARK_UI_PORT >> \$SPARK_EXT_DIR/bundle.properties
else
# this section removes spark extension entry from Extesion profile. Hence worker nodes will have only Hostmonitor running
    sed -i '/introscope.agent.extensions.bundles.boot.load/d' /etc/broadcom_apm/apmia/extensions/Extensions.profile
fi
#Once updatation are done, we restarts apmia
/etc/broadcom_apm/apmia/APMIACtrl.sh restart
EOF
#Here starting agentinstallation as separate process.
chmod u+x /etc/broadcom_apm/agentinstallation.sh
source /etc/broadcom_apm/agentinstallation.sh &
