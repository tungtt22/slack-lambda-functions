"""
Define all function using for AWS CloudWatch Event
"""

import boto3
from aws import constants
from aws import aws_lambda

# Create CloudWatchEvents client
CW_EVENTS = boto3.client('events', region_name=constants.REGION)


def create_event(rule_name, cron_expression, function):
    """
    Create an event and push to AWS
    """
    # Put an event rule
    response = CW_EVENTS.put_rule(Name=rule_name,
                                  ScheduleExpression=cron_expression,
                                  State='ENABLED')
    print(response)
    funct = aws_lambda.find_function(function)
    response = CW_EVENTS.put_targets(Rule=rule_name,
                                     Targets=[{
                                         'Arn': funct["FunctionArn"],
                                         'Id': funct["FunctionName"]
                                     }])
    print(response)


def delete_event(rule_name):
    """
    Delete an event and push to AWS
    """
    # delete an event rule
    response = CW_EVENTS.delete_rule(Name=rule_name, Force=True)
    print(response)
