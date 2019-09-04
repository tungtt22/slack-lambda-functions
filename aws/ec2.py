"""
Define all function using for AWS EC2
"""

import json
import boto3
from aws import constants

INSTANCES = boto3.resource('ec2', region_name=constants.REGION)
CLIENT = boto3.client('ec2', region_name=constants.REGION)


def get_list_instances():
    """
    Get all instances
    """
    instances = []
    response = CLIENT.describe_instances()
    reservations = response.get('Reservations')
    if reservations:
        for reservation in reservations:
            instance = json.loads('{"InstanceId": " ", ' + '"TagName":" ", ' +
                                  '"PrivateIpAddresses":" ", ' +
                                  '"PublicIpAddress":" ", ' +
                                  '"InstanceType":" ", ' + '"State":" ", ' +
                                  '"ServiceType":" "}')
            instance_value = reservation.get("Instances")[0]
            instance["ServiceType"] = "ec2"
            instance["InstanceId"] = instance_value.get("InstanceId")
            instance["PrivateIpAddresses"] = instance_value.get(
                "PrivateIpAddress")
            instance["InstanceType"] = instance_value.get("InstanceType")
            instance["PublicIpAddress"] = instance_value.get("PublicIpAddress")

            state = instance_value.get("State")
            instance["State"] = state.get("Name")

            for tag in instance_value.get("Tags"):
                if tag.get("Key") == "Name":
                    instance["TagName"] = tag.get("Value")

            instances.append(instance)
        return instances
    return None


def start_all_instance(instances):
    """
    Start all instances
    """
    if instances:
        instance_ids = []
        text = ""

        for instance in instances:
            if instance["State"] == "stopped":
                instance_ids.append(instance["InstanceId"])
                text = text + 'The instance `' + str(
                    instance["TagName"]) + '` starting!\n'
            else:
                text = text + 'The instance `' + str(
                    instance["TagName"]) + '` already started!\n'

        if instance_ids:
            CLIENT.start_instances(InstanceIds=instance_ids)

        return text
    return "Instance not found!"


def stop_all_instance(instances):
    """
    Stop all instances
    """
    if instances:
        instance_ids = []
        text = ""
        for instance in instances:
            if instance["State"] == "running":
                instance_ids.append(instance["InstanceId"])
                text = text + 'The instance `' + str(
                    instance["TagName"]) + '` stopping!\n'
            else:
                text = text + 'The instance `' + str(
                    instance["TagName"]) + '` already stopped!\n'

        if instance_ids:
            CLIENT.stop_instances(InstanceIds=instance_ids)

        return text
    return "Instance not found!"


def start_instance(instance):
    """
    Start an instance
    """
    instance_ids = []
    text = ""
    if instance["State"] == "stopped":
        instance_ids.append(instance["InstanceId"])
        CLIENT.start_instances(InstanceIds=instance_ids)
        text = text + 'The instance `' + str(
            instance["TagName"]) + '` starting!\n'
    else:
        text = text + 'The instance `' + str(
            instance["TagName"]) + '` already started!\n'

    return text


def stop_instance(instance):
    """
    Stop an instance
    """
    instance_ids = []
    text = ""
    if instance["State"] == "running":
        instance_ids.append(instance["InstanceId"])
        CLIENT.stop_instances(InstanceIds=instance_ids)
        text = text + 'The instance `' + str(
            instance["TagName"]) + '` stopping!\n'
    else:
        text = text + 'The instance `' + str(
            instance["TagName"]) + '` already stopped!\n'

    return text
