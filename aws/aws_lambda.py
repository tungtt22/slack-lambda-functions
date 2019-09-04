"""
Define all function using for AWS Lambda Functions
"""

import boto3
from aws import constants

LAMBDA = boto3.client('lambda', region_name=constants.REGION)


def find_function(function_name):
    """
    Find an Lambda Function
    """
    response = LAMBDA.list_functions(FunctionVersion='ALL')
    for funct in response["Functions"]:
        if funct["FunctionName"] == function_name:
            return funct
    return "Lambda Function not found!"
