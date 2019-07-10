import json
import slackbot
import constants

def process_event(event):
  text = ""
  att_text = ""
  response = {
    "response_type": "in_channel",
    "text": None,
    "attachments": []
  }
  body = event.get('body').replace("&", "\",\"").replace("=", "\":\"")
  data = json.loads("{\"" + body + "\"}")

  command = data["command"].strip("%2F")
  instances = data["text"].split("+")

  if (slackbot.check_authorization(data)):
    text = "User <@" + data[
      "user_name"] + "> has run `" + command + " " + data["text"].replace("+", " ") + "` command"
  else:
    text = "User <@" + data[
      "user_name"] + "> are not have authorization access to this function!"

  cmd = slackbot.Command()
  if "devops" == instances[0]:
    if "all" in instances:
      att_text = cmd.call(command, "all")
    else:
      att_text = cmd.call(command, instances[0] + "-" + instances[1])
  else:
    att_text = "Command `{0} {1}` wrong".format(command, data["text"].replace("+", " "))

  att_text = {"text": att_text}
  response["text"] = text
  response["attachments"].append(att_text)
  return response

def lambda_handler(event, context):
  response = process_event(event)
  return {"isBase64Encoded": True, 'statusCode': 200, 'body': json.dumps(response)}

print (lambda_handler(json.loads(str(constants.BODY)), "aaaa"))
