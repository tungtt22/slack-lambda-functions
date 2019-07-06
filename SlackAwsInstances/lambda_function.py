import json
import SlackBotData

body = "token=EtICe4Z3iBoPDrZJcnDUPLPn&team_id=TL239EXAR&team_domain=akaworkfpt&channel_id=CL1JHGQQ4&channel_name=akaworkio&user_id=UL239KT37&user_name=tungtt22&command=%2Fturnon&text=devops+sonar+bastion&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FTL239EXAR%2F685159751284%2FEqJN9lE9jYVyjvhJzha4u6g4&trigger_id=687775014278.682111507365.7b35887deae71483412bc7a28172bb46"

def lambda_handler(event, context):
    response = json.loads('{"message":"message"}')
    # body = event.get('body')
    data = json.loads("{\"" + body.replace("&","\",\"").replace("=","\":\"") + "\"}")
    
    command = data["command"].strip("%2F")
    instances = data["text"].split("+")
    print(instances)
    sw = SlackBotData.Switcher()
    sw.indirect(instances,command)

    if (SlackBotData.check_authorization(data)):
      response["message"] = "You are have authorization access to Lambda function!"
    else:
      response["message"] = "You are not have authorization access to Lambda function!"  

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

print (lambda_handler("addd", "aaaa"))