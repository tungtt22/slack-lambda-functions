import boto3
import json
import constants

ec2_instance = boto3.resource('ec2', region_name = constants.REGION)
ec2_client = boto3.client('ec2', region_name = constants.REGION)

def get_list_instances():
  instances = []
  response = ec2_client.describe_instances()
  reservations = response.get('Reservations')
  if len(reservations) > 0:
    for reservation in reservations:
      instance = json.loads('{"InstanceId": " ", "TagName":" ", "PrivateIpAddresses":" ", "PublicIpAddress":" ", "InstanceType":" ", "State":" ", "ServiceType":" "}')
      instance_value = reservation.get("Instances")[0]
      instance["ServiceType"] = "ec2"
      instance["InstanceId"] = instance_value.get("InstanceId")
      instance["PrivateIpAddresses"] = instance_value.get("PrivateIpAddress")
      instance["InstanceType"] = instance_value.get("InstanceType")
      instance["PublicIpAddress"] = instance_value.get("PublicIpAddress")

      state = instance_value.get("State")
      instance["State"] = state.get("Name")

      for tag in instance_value.get("Tags"):
        if tag.get("Key") == "Name":
          instance["TagName"] = tag.get("Value")

      instances.append(instance)
    return instances
  else:
    return None

def start_all_instance(instances):
  if len(instances) > 0:
    instance_ids = []
    text = ""

    for instance in instances:
      if instance["State"] == "stopped":
        instance_ids.append(instance["InstanceId"])
        text = text + 'The instance `' + str(instance["TagName"]) + '` starting!\n'
      else:
        text = text + 'The instance `' + str(instance["TagName"]) + '` already started!\n'

    if len(instance_ids) > 0:
      ec2_client.start_instances(InstanceIds = instance_ids)

    return text
  else:
    return "Instance not found!"

def stop_all_instance(instances):
  if len(instances) > 0:
    instance_ids = []
    text = ""
    for instance in instances:
      if instance["State"] == "running":
        instance_ids.append(instance["InstanceId"])
        text = text + 'The instance `' + str(instance["TagName"]) + '` stopping!\n'
      else:
        text = text + 'The instance `' + str(instance["TagName"]) + '` already stopped!\n'

    if len(instance_ids) > 0:
      ec2_client.stop_instances(InstanceIds = instance_ids)

    return text
  else:
    return "Instance not found!"

def start_instance(instance):
  instance_ids = []
  text = ""
  if instance["State"] == "stopped":
    instance_ids.append(instance["InstanceId"])
    ec2_client.start_instances(InstanceIds = instance_ids)
    text = text + 'The instance `' + str(instance["TagName"]) + '` starting!\n'
  else:
    text = text + 'The instance `' + str(instance["TagName"]) + '` already started!\n'

  return text

def stop_instance(instance):
  instance_ids = []
  text = ""
  if instance["State"] == "running":
    instance_ids.append(instance["InstanceId"])
    ec2_client.stop_instances(InstanceIds = instance_ids)
    text = text + 'The instance `' + str(instance["TagName"]) + '` stopping!\n'
  else:
    text = text + 'The instance `' + str(instance["TagName"]) + '` already stopped!\n'

  return text
