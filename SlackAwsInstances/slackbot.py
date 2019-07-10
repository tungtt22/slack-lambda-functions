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
    list_instance = ec2_instances
    instances = get_instance_id(instance, list_instance)
    value = ec2.start_all_instance(instances)
    return value

  def turnoff(self, instance):
    ec2_instances = ec2.get_list_instances()
    list_instance = ec2_instances
    instances = get_instance_id(instance, list_instance)
    value = ec2.stop_all_instance(instances)
    return value

  def aws_status(self, instance):
    print ("Get status command")
    ec2_instances = ec2.get_list_instances()
    list_instance = ec2_instances
    instances = get_instance_id(instance, list_instance)
    for instance in instances:
      status = ec2.check_instance_status(instance)
    return status
