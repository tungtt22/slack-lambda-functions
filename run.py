"""
This file using for test
"""

import json
import lambda_function
from AwsInstances import constants

print(lambda_function.lambda_handler(json.loads(str(constants.BODY)), "aaaa"))
