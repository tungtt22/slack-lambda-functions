"""
This file receive incoming event and first process event from Application
"""

import json
import urllib.parse
from aws import slackstash
from aws import constants


def process_schedule_option(options):
    """
    Process schedule options
    """
    schedule = {
        "turnon": None,
        "turnoff": None,
        "instance_tag": None,
        "requester": None
    }
    if options[1] == "schedule":
        options_size = len(options)
        if 3 < options_size < 8:
            i = 2
            while i < options_size:
                if options[i] == "turnon":
                    i = i + 1
                    schedule["turnon"] = urllib.parse.unquote(
                        options[i]).replace("-", " ")
                elif options[i] == "turnoff":
                    i = i + 1
                    schedule["turnoff"] = urllib.parse.unquote(
                        options[i]).replace("-", " ")
                else:
                    return constants.MESSAGE_WRONG_COMMAND
                i = i + 2
            schedule["instance_tag"] = options[options_size - 1]
        else:
            return constants.MESSAGE_WRONG_COMMAND
    else:
        return constants.MESSAGE_WRONG_COMMAND
    return schedule


def process_event(event):
    """
    Process incoming event
    """
    text = ""
    att_text = ""
    response = {
        "response_type": "in_channel",
        "mrkdwn": "true",
        "text": None,
        "attachments": []
    }
    body = event.get('body').replace("&", "\",\"").replace("=", "\":\"")
    data = json.loads("{\"" + body + "\"}")

    command = data["command"].strip("%2F")

    data["text"] = " ".join(data["text"].replace("+", " ").split())
    options = data["text"].split(" ")

    if slackstash.check_authorization(data):
        text = "User <@{0}> has run `{1} {2}` command".format(
            data["user_name"], command, urllib.parse.unquote(data["text"]))
    else:
        text = "User <@{0}> are not have authorization access to this function!".format(
            data["user_name"])
    attach = ""
    cmd = slackstash.Command()
    if options[0] == "turnon":
        att_text = cmd.call(command + "_turnon", options[1])
    elif options[0] == "turnoff":
        att_text = cmd.call(command + "_turnoff", options[1])
    elif options[0] == "status":
        attach = cmd.call(command + "_status", options[1])
    elif options[0] == "tags":
        att_text = cmd.call(command + "_tags", options[1])
    elif options[0] == "set":
        schedule = process_schedule_option(options)
        if schedule == constants.MESSAGE_WRONG_COMMAND:
            response["text"] = schedule
            return response

        schedule["requester"] = data["user_name"]
        att_text = cmd.call(command + "_schedule", schedule)
    else:
        att_text = "Command `{0} {1}` wrong".format(
            command, data["text"].replace("+", " "))

    att_text = {"text": att_text, "color": "#3AA3E3"}

    response["text"] = text
    response["attachments"].append(att_text)
    response["attachments"].append(attach)
    return response


def lambda_handler(event, context):
    """
    Handler incoming request
    """
    response = process_event(event)
    return {
        "isBase64Encoded": True,
        'statusCode': 200,
        'body': json.dumps(response)
    }
