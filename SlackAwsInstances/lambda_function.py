import json
import SlackBotData
import Constants

def lambda_handler(event, context):
    response = json.loads('{"message":"message"}')
    body = event.get('body').replace("&","\",\"").replace("=","\":\"")
    data = json.loads("{\"" + body + "\"}")
    
    command = data["command"].strip("%2F")
    instances = data["text"].split("+")

    if (SlackBotData.check_authorization(data)):
      response["message"] = "You are have authorization access to Lambda function!"
    else:
      response["message"] = "You are not have authorization access to Lambda function!"  

    sw = SlackBotData.Switcher()
    sw.action(command,"bastion")

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

print (lambda_handler(json.loads(str(Constants.BODY)), "aaaa"))
