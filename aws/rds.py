"""
Define all function using for AWS RDS
"""

import json
import boto3
from aws import constants

RDS = boto3.client('rds', region_name=constants.REGION)


def get_list_instances():
    """
    Get all instance
    """
    instances = []
    response = RDS.describe_db_instances()
    db_instances = response.get("DBInstances")

    if db_instances:
        for item in db_instances:
            instance = json.loads('{"InstanceId":" ", ' + '"TagName":" ", ' +
                                  '"Endpoint":" ", ' +
                                  '"EngineVersion":" ", ' +
                                  '"InstanceType":" ", ' + '"State":" ", ' +
                                  '"Engine":" ", ' + '"ServiceType":" "}')
            instance["ServiceType"] = "rds"
            instance["InstanceId"] = item.get("DBInstanceIdentifier")
            instance["InstanceType"] = item.get("DBInstanceClass")
            instance["Engine"] = item.get("Engine")
            instance["TagName"] = item.get("DBInstanceIdentifier")
            instance["State"] = item.get("DBInstanceStatus")
            instance["Endpoint"] = item.get("Endpoint")["Address"]
            instance["EngineVersion"] = item.get("EngineVersion")
            instances.append(instance)
        return instances
    return None


def start_all_instances(instances):
    """
    Start all instances
    """
    text = ""
    if instances:
        for instance in instances:
            instance = json.loads(instance)
            if instance["State"] == "stopped":
                RDS.start_db_instance(
                    DBInstanceIdentifier=str(instance["InstanceId"]))
                text = "{0}The instance `{1}` starting!\n".format(
                    text, instance["TagName"])
            else:
                text = "{0}The instance `{1}` already started!\n".format(
                    text, instance["TagName"])

        return text
    return "Instance not found!"


def stop_all_instances(instances):
    """
    Stop all instances
    """
    text = ""
    if instances:
        for instance in instances:
            instance = json.loads(instance)
            if instance["State"] == "available":
                RDS.stop_db_instance(
                    DBInstanceIdentifier=str(instance["InstanceId"]))
                text = "{0}The instance `{1}` stopping!\n".format(
                    text, str(instance["TagName"]))
            else:
                text = "{0}The instance `{1}` already stopped!\n".format(
                    text, str(instance["TagName"]))

        return text
    return "Instance not found!"


def start_instance(instance):
    """
    Start an instance
    """
    text = ""
    if instance["State"] == "stopped":
        RDS.start_db_instance(
            DBInstanceIdentifier=str(instance["InstanceId"]))
        text = "{0}The instance `{1}` starting!\n".format(
            text, str(instance["TagName"]))
    else:
        text = "{0}The instance `{1}` already started!\n".format(
            text, str(instance["TagName"]))

    return text


def stop_instance(instance):
    """
    Stop an instance
    """
    text = ""
    if instance["State"] == "available":
        RDS.stop_db_instance(
            DBInstanceIdentifier=str(instance["InstanceId"]))
        text = "{0}The instance `{1}` stopping!\n".format(
            text, str(instance["TagName"]))
    else:
        text = "{0}The instance `{1}` already stopped!\n".format(
            text, str(instance["TagName"]))

    return text
