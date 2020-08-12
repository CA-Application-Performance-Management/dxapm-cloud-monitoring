import logging
import boto3
import json
import gzip
import traceback
import six.moves.urllib as urllib  # for for Python 2.7 urllib.unquote_plus
from botocore.vendored import requests 
from io import BytesIO, BufferedReader
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)
############################################################
# defining the api-endpoint 
API_ENDPOINT = '<public data ingestion endpoint>/ingestion'
    
# your Tenant id key here 
TENANT_ID = '<TENANT_ID>'

############################################################
## To add new service
# 1. add servicename in list_supported_cw_services
# 2. add interested event name in include_json[<servicename>] array and exclude_json[<servicename>]
# 3. add hostname logic in getHostName() function

## To add new events in existing service
# 1. just update the interested event name in include_json[<servicename>] array
###########################################################
#list of supported events
list_supported_cw_services = {'ec2','ecs','rds','elasticache'}

#include event list
include_json = {}
#include ec2 event list
include_json['ec2'] = ['StartInstances','RunInstances','TerminateInstances','StopInstances']
include_json['ecs'] = ['CreateService','RunTask','DeleteCluster']
include_json['rds'] = ['CreateDBInstance','StartDBInstance','StopDBInstance','RebootDBInstance','DeleteDBInstance','ModifyDBInstance']
include_json['elasticache'] = ['CreateCacheCluster','ModifyCacheCluster']

#exclude event list
exclude_json = {}
#exclude ec2 event list
exclude_json['ec2'] = None
exclude_json['ecs'] = None
exclude_json['rds'] = None
exclude_json['elasticache'] = None


#main function
def lambda_handler(event, context):
    response = '';
    if event:
        s3 = boto3.client("s3")
        # Get the object from the event and show its content type
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])
        logger.info('CloudTrail event occurred:: '+ str(bucket) + '::' + str(key))
        # Extract the S3 object
        eventBody = s3.get_object(Bucket=bucket, Key=key)
        body = eventBody["Body"]
        data = body.read()
        # If the name has a .gz extension, then decompress the data
        if key[-3:] == ".gz":
            with gzip.GzipFile(fileobj=BytesIO(data)) as decompress_stream:
                # Reading line by line avoid a bug where gzip would take a very long time (>5min) for
                # file around 60MB gzipped
                data = b"".join(BufferedReader(decompress_stream))

        log_result = []
        event_result = []
        try:
            json_data = json.loads(data)

            if 'Records' in json_data:
                for record in json_data['Records']:
                    if filter_events(record):
                        logger.info('Filter event occurred:: ' + str(record))
                        logger.debug(record)
                        event_result.append(parse_change_event(record))
                        log_result.append(record)

            #send all collected events
            if not event_result:   
                logger.info('No matching event found..')
            else:
                rawJsonForEs = {
                    "documents": [
                        {
                            "header": {
                                "doc_type_id": "itoa_events_change_custom",
                                "doc_type_version": "1",
                                "product_id": "ao",
                                "tenant_id": TENANT_ID
                            },
                            "body": event_result
                        }
                        ]
                }
                logger.debug('matching events found..' + json.dumps(rawJsonForEs))
                response = post_data(rawJsonForEs)            
            
            #send all collected event logs
            if not log_result:   
                logger.debug('No matching log found..')
            else:
                rawJsonForEs = {
                    "documents": [
                        {
                            "header": {
                                "doc_type_id": "itoa_logs_aws_cloudtrail",
                                "doc_type_version": "1",
                                "product_id": "ao",
                                "tenant_id": TENANT_ID
                            },
                            "body": log_result
                        }
                        ]
                }
                logger.debug('matching logs found..' + json.dumps(rawJsonForEs))
                response ='Event message: ' + response + '\n Log Message:' + post_data(rawJsonForEs)

        except Exception as e:
            logger.error('Something went wrong: ' + str(e))
            traceback.print_exc()
            return False
        finally:
            if event_result:
                logger.info("Lambda execution completed with " + response)

def post_data(body):
    #send to endpoint
    headers = {'Content-type': 'application/json'} 
    
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data=json.dumps(body), headers=headers) 
    
    # extracting response text 
    if r.status_code == 202:
        logger.info('The request accepted successfuly') 
    response = 'statusCode: '+ str(r.status_code)
    return response

#parse the change event field
def parse_change_event(record):
    serviceName = getServiceName(record)
    host = getHostName(serviceName, record)
    #prepare event
    eventBody = {}
    eventBody['event_unique_id'] = str(serviceName) + '_' + str(host) + '_' + str(record['eventTime'])
    eventBody['host'] = host
    eventBody['product'] = 'Application Performance Monitoring'
    eventBody['message'] = 'Event is: ' + str(record['eventName']) + ' on host: '+ str(host)
    eventBody['timestamp'] = record['eventTime']
    return eventBody;
    

# should only be called when INCLUDE_EVENTS and/or EXCLUDE_EVENTS exist
def filter_events(record):
    serviceName = getServiceName(record)
    if serviceName is not None:
        if serviceName in list_supported_cw_services:
            #check for patterns    
            if include_json[serviceName] is None and exclude_json[serviceName] is None:
                return False
            try:
               if exclude_json[serviceName] is not None:
               # if an exclude match is found, do not add event to events_to_send
                    if searchPattern(exclude_json[serviceName], str(record)):
                       return False
               if include_json[serviceName] is not None:
                # if no include match is found, do not add event to events_to_send
                   if searchPattern(include_json[serviceName], str(record)):
                      return True
            except Exception:
               raise Exception("could not filter the event")
    return False          
    

# Use for include, exclude
def searchPattern(patterns, text):
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    #if nothing match
    return False
    
#get service name
def getServiceName(record):
    eventSource = str(record['eventSource'])
    service = eventSource.split(".")
    serviceName = None
    if len(service) > 1:
        serviceName = service[0]
        logger.debug('serviceName:: ' + str(serviceName))
    return serviceName;    
    
#get hostname
def getHostName(serviceName, record):
    hostName = None
    if 'ec2' == serviceName:
        matchObject = re.search('instanceId\':\s+\'(.*?)\'', str(record))
        if matchObject is not None:
            hostName = matchObject.group(1)
            logger.info('ec2 hostName:: ' + str(hostName))
    if 'ecs' == serviceName:
        matchObject = re.search('clusterName\':\s+\'(.*?)\'', str(record))
        if matchObject is not None:
            hostName = matchObject.group(1)
            logger.info('ecs hostName:: ' + str(hostName))
    if 'rds' == serviceName:
        matchObject = re.search('dBInstanceIdentifier\':\s+\'(.*?)\'', str(record))
        if matchObject is not None:
            hostName = matchObject.group(1)
            logger.info('rds hostName:: ' + str(hostName))
    if 'elasticache' == serviceName:
        matchObject = re.search('cacheClusterId\':\s+\'(.*?)\'', str(record))
        if matchObject is not None:
            hostName = matchObject.group(1)
            logger.info('elasticache hostName:: ' + str(hostName))
    return hostName
