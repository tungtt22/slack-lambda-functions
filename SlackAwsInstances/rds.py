import boto3
import json
import constants

rds_client = boto3.client('rds', region_name = constants.REGION)

def get_list_instances():
  instances = []
  response = rds_client.describe_db_instances()
  db_instances = response.get("DBInstances")

  if len(db_instances) > 0:
    for item in db_instances:
      instance = json.loads('{"InstanceId":" ", "TagName":" ", "Endpoint":" ", "EngineVersion":" ", "InstanceType":" ", "State":" ", "Engine":" ", "ServiceType":" "}')
      instance["ServiceType"] = "rds"
      instance["InstanceId"] = item.get("DBInstanceIdentifier")
      instance["InstanceType"] = item.get("DBInstanceClass")
      instance["Engine"] = item.get("Engine")
      instance["TagName"] = item.get("DBInstanceIdentifier")
      instance["State"] = item.get("DBInstanceStatus")
      instance["Endpoint"] = item.get("Endpoint")["Address"]
      instance["EngineVersion"] = item.get("EngineVersion")
      instances.append(instance)
    return instances
  else:
    return None

def start_all_instances(instances):
  text = ""
  if len(instances) > 0:
    for instance in instances:
      instance = json.loads(instance)
      if instance["State"] == "stopped":
        rds_client.start_db_instance(DBInstanceIdentifier = str(instance["InstanceId"]))
        text = text + 'The instance `' + str(instance["TagName"]) + '` starting!\n'
      else:
        text = text + 'The instance `' + str(instance["TagName"]) + '` already started!\n'

    return text
  else:
    return "Instance not found!"

def stop_all_instances(instances):
  text = ""
  if len(instances) > 0:
    for instance in instances:
      instance = json.loads(instance)
      if instance["State"] == "available":
        rds_client.stop_db_instance(DBInstanceIdentifier = str(instance["InstanceId"]))
        text = text + 'The instance `' + str(instance["TagName"]) + '` stopping!\n'
      else:
        text = text + 'The instance `' + str(instance["TagName"]) + '` already stopped!\n'
    
    return text
  else:
    return "Instance not found!"

def start_instance(instance):
  text = ""
  if instance["State"] == "stopped":
    rds_client.start_db_instance(DBInstanceIdentifier = str(instance["InstanceId"]))
    text = text + 'The instance `' + str(instance["TagName"]) + '` starting!\n'
  else:
    text = text + 'The instance `' + str(instance["TagName"]) + '` already started!\n'

  return text

def stop_instance(instance):
  text = ""
  if instance["State"] == "available":
    rds_client.stop_db_instance(DBInstanceIdentifier = str(instance["InstanceId"]))
    text = text + 'The instance `' + str(instance["TagName"]) + '` stopping!\n'
  else:
    text = text + 'The instance `' + str(instance["TagName"]) + '` already stopped!\n'
    
  return text
