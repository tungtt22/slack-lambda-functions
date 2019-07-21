import json
import constants
import ec2
import rds

def find_channel(channel_id, channel_ids):
  for id in channel_ids:
    if (channel_id == id):
      return True

    number_channel = number_channel + 1

  if (number_channel == channel_ids.count()):
    return False

def find_user(user_id, user_ids):
  for id in user_ids:
    if (user_id == id):
      return True

    number_user = number_user + 1

  if (number_user == user_ids.count()):
    return False

def find_command(command, commands):
  for item in commands:
    if (command == item):
      return True

    number_command = number_command + 1

  if (number_command == commands.count()):
    return False

def check_authorization(data):
  if (data["token"] == constants.TOKEN):
    if (data["team_id"] == constants.TEAM_ID):
      return True
    else:
      return False
  else:
    return False

def get_instance_id(instance, instance_list):
  i = 0
  instances = []
  for item in instance_list:
    i = i + 1
    if instance == item["TagName"].lower():
      instances.append(item)
  return instances

class Command(object):
  def call(self,command, instance):
    method_name = command
    method=getattr(self, method_name, lambda :'Invalid command!')
    return method(instance)

  def turnon(self, instance):
    ec2_instances = ec2.get_list_instances()
    rds_instances = rds.get_list_instances()
    list_instance = ec2_instances + rds_instances
    instances = get_instance_id(instance, list_instance)
    if (len(instances) == 0):
      return "Instance not found!" 
    elif (len(instances) == 1):
      instance = instances[0]
      if (instance["ServiceType"] == "ec2"):
        value = ec2.start_instance(instance)
      elif (instance["ServiceType"] == "rds"):
        value = rds.start_instance(instance)
    else:
      for instance in instances:
        if (instance["ServiceType"] == "ec2"):
          value = ec2.start_all_instance(instances)
        elif (instance["ServiceType"] == "rds"):
          value = rds.start_all_instance(instances)
    return value

  def turnoff(self, instance):
    ec2_instances = ec2.get_list_instances()
    rds_instances = rds.get_list_instances()
    list_instance = ec2_instances + rds_instances
    instances = get_instance_id(instance, list_instance)
    if (len(instances) == 0):
      return "Instance not found!" 
    elif (len(instances) == 1):
      instance = instances[0]
      if (instance["ServiceType"] == "ec2"):
        value = ec2.stop_instance(instance)
      elif (instance["ServiceType"] == "rds"):
        value = rds.stop_instance(instance)
    else:
      for instance in instances:
        if (instance["ServiceType"] == "ec2"):
          value = ec2.stop_all_instance(instance)
        elif (instance["ServiceType"] == "rds"):
          value = rds.stop_all_instance(instance)

    return value

  def aws_status(self, instance):
    text  = ""
    ec2_instances = ec2.get_list_instances()
    rds_instances = rds.get_list_instances()
    list_instance = ec2_instances + rds_instances
    instances = get_instance_id(instance, list_instance)
    if (len(instances) > 0):
      for instance in instances:
        if (instance["ServiceType"] == "ec2"):
          text = (
                    "The instance `{0}` has current status as below:\n" +
                    "  - *Service Type:* `{1}`\n" +
                    "  - *Status:* `{2}`\n" +
                    "  - *Public IP:* `{3}`\n" +
                    "  - *Local IP:* `{4}`\n" +
                    "  - *Instance Type:* `{5}`\n"
                ).format(
                  instance["TagName"],
                  instance["ServiceType"].upper(),
                  instance["State"],
                  instance["PublicIpAddress"],
                  instance["PrivateIpAddresses"],
                  instance["InstanceType"]
                )
        elif (instance["ServiceType"] == "rds"):
          text = (
                    "The instance `{0}` has current status as below:\n" +
                    "  - *Service Type:* `{1}`\n" +
                    "  - *Status:* `{2}`\n" +
                    "  - *Endpoint:* `{3}`\n" +
                    "  - *Instance Type:* `{4}`\n" +
                    "  - *Engine:* `{5}`\n" +
                    "  - *Engine Version:* `{6}`\n"
                ).format(
                  instance["TagName"],
                  instance["ServiceType"].upper(),
                  instance["State"],
                  instance["Endpoint"],
                  instance["InstanceType"],
                  instance["Engine"],
                  instance["EngineVersion"]
                )
    else:
      return "Instance not found!"
    return text
