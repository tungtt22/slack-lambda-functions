"""
This file receive incoming event and first process event from Application
"""

import json
import slackstash


def process_event(event):
    """
    Process incoming event
    """
    text = ""
    att_text = ""
    response = {"response_type": "in_channel", "text": None, "attachments": []}
    body = event.get('body').replace("&", "\",\"").replace("=", "\":\"")
    data = json.loads("{\"" + body + "\"}")

    command = data["command"].strip("%2F")

    data["text"] = " ".join(data["text"].replace("+", " ").split())
    instances = data["text"].split(" ")

    if slackstash.check_authorization(data):
        text = "User <@{0}> has run `{1} {2}` command".format(
            data["user_name"], command, data["text"])
    else:
        text = "User <@{0}> are not have authorization access to this function!".format(
            data["user_name"])

    cmd = slackstash.Command()
    if instances[0] == "turnon":
        att_text = cmd.call(command + "_turnon", instances[1])
    elif instances[0] == "turnoff":
        att_text = cmd.call(command + "_turnoff", instances[1])
    elif instances[0] == "status":
        att_text = cmd.call(command + "_status", instances[1])
    elif instances[0] == "tags":
        att_text = cmd.call(command + "_tags", instances[1])
    else:
        att_text = "Command `{0} {1}` wrong".format(
            command, data["text"].replace("+", " "))

    att_text = {"text": att_text, "color": "#3AA3E3"}

    response["text"] = text
    response["attachments"].append(att_text)
    return response


def lambda_handler(event, context):
    """
    Handler incoming request
    """
    print(context)
    response = process_event(event)
    return {
        "isBase64Encoded": True,
        'statusCode': 200,
        'body': json.dumps(response)
    }
