import json
import Constants

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
  if (data["token"] == Constants.TOKEN):
    if (data["team_id"] == Constants.TEAM_ID):
      return True
    else:
      return False
  else:
    return False

class Switcher(object):
  def indirect(self,command,instances):
     method_name=command
     method=getattr(self,method_name,lambda :'Invalid command!')
     return method(instances)

def turn_on(self):
    print ("turn on" + self)
    switcher={
      "sonar":"hello",
      "nexus":"hello",
      "jenkins":"hello",
      "gitlab":"hello",
      "jira":"hello",
      "confluence":"hello"
    }
    return switcher.get(instance,"Instance not found!")

def turn_off(self):
    print ("turn off" + self)
    switcher={
      "sonar":"hello",
      "nexus":"hello",
      "jenkins":"hello",
      "gitlab":"hello",
      "jira":"hello",
      "confluence":"hello"
    }
    return switcher.get(instance,"Instance not found!")

def status(self):
  print ("status" + self)
  switcher={
    "sonar":"hello",
    "nexus":"hello",
    "jenkins":"hello",
    "gitlab":"hello",
    "jira":"hello",
    "confluence":"hello"
  }
  return switcher.get(instance,"Instance not found!")