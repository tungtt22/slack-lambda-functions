"""
Define all command when call from Slack
"""

from datetime import datetime
from aws import ec2
from aws import rds
from aws import cw_events
from aws import constants


def find_channel(channel_id, channel_ids):
    """
    Find channel is exist
    """
    for _id in channel_ids:
        if channel_id == _id:
            return True
    return False


def find_user(user_id, user_ids):
    """
    Find user is exist
    """
    for _id in user_ids:
        if user_id == _id:
            return True
    return False


def find_command(command, commands):
    """
    Find command is exist
    """
    for item in commands:
        if command == item:
            return True
    return False


def check_authorization(data):
    """
    Check user authorization with change
    """
    if data["token"] == constants.TOKEN and data[
            "team_id"] == constants.TEAM_ID:
        return True
    return False


def get_instance_id(instance, instance_list, regex):
    """
    Get all install match with tag name
    """
    instances = []
    if regex:
        for item in instance_list:
            if instance in item["TagName"].lower():
                instances.append(item)
    else:
        for item in instance_list:
            if instance == item["TagName"].lower():
                instances.append(item)
    return instances


def print_ec2_instance_info(_instance):
    """
    Format attachment for EC2 instance
    """
    attachment = {"text": "", "fields": [], "color": "#F35A00"}
    attachment["text"] = "The instance `" + _instance[
        "TagName"] + "` has current status as below:"
    field_service_type = {
        "title": "Service Type:",
        "value": _instance["ServiceType"].upper(),
        "short": "true"
    }
    field_status = {
        "title": "Status:",
        "value": _instance["State"],
        "short": "true"
    }
    field_instance_type = {
        "title": "Instance Type:",
        "value": _instance["InstanceType"],
        "short": "true"
    }
    field_local_ip = {
        "title": "Local IP:",
        "value": _instance["PrivateIpAddresses"],
        "short": "true"
    }
    attachment["fields"].append(field_service_type)
    attachment["fields"].append(field_instance_type)
    attachment["fields"].append(field_status)
    attachment["fields"].append(field_local_ip)
    if _instance["PublicIpAddress"] is not None:
        field_public_ip = {
            "title": "Public IP:",
            "value": _instance["PublicIpAddress"],
            "short": "true"
        }
        attachment["fields"].append(field_public_ip)

    return attachment


def print_rds_instance_info(_instance):
    """
    Format attachment for RDS instance
    """
    attachment = {"text": "", "fields": [], "color": "#F35A00"}
    attachment["text"] = "The instance `" + _instance[
        "TagName"] + "` has current status as below:"
    field_service_type = {
        "title": "Service Type:",
        "value": _instance["ServiceType"].upper(),
        "short": "true"
    }
    field_status = {
        "title": "Status:",
        "value": _instance["State"],
        "short": "true"
    }
    field_instance_type = {
        "title": "Instance Type:",
        "value": _instance["InstanceType"],
        "short": "true"
    }
    field_endpoint = {
        "title": "Endpoint:",
        "value": _instance["Endpoint"],
        "short": "true"
    }
    field_engine = {
        "title": "Engine:",
        "value": _instance["Engine"],
        "short": "true"
    }
    field_engine_version = {
        "title": "Engine Version:",
        "value": _instance["EngineVersion"],
        "short": "true"
    }
    attachment["fields"].append(field_service_type)
    attachment["fields"].append(field_instance_type)
    attachment["fields"].append(field_status)
    attachment["fields"].append(field_endpoint)
    attachment["fields"].append(field_engine)
    attachment["fields"].append(field_engine_version)

    return attachment


def convert_datetime_to_cron(date_time):
    """
    Convert date time to cron expression
    """
    date_time = datetime.strptime(date_time, '%d/%m/%Y %H:%M')

    cron_express = "cron({0} {1} {2} {3} ? {4})".format(
        date_time.minute, date_time.hour, date_time.day, date_time.month,
        date_time.year)
    return cron_express


class Command(object):
    """
    All command list here
    """

    def call(self, command, option):
        """
        Call functions
        """
        method_name = command
        method = getattr(self, method_name, lambda: 'Invalid command!')
        return method(option)

    @classmethod
    def aws_turnon(cls, _instance):
        """
        Turn on command
        """
        ec2_instances = ec2.get_list_instances()
        rds_instances = rds.get_list_instances()
        list_instance = ec2_instances + rds_instances
        instances = get_instance_id(_instance, list_instance, False)
        number_instance = len(instances)
        if number_instance == 0:
            return "Instance not found!"
        elif number_instance == 1:
            _instance = instances[0]
            if _instance["ServiceType"] == "ec2":
                value = ec2.start_instance(_instance)
            elif _instance["ServiceType"] == "rds":
                value = rds.start_instance(_instance)
        else:
            for _instance in instances:
                if _instance["ServiceType"] == "ec2":
                    value = ec2.start_all_instance(instances)
                elif _instance["ServiceType"] == "rds":
                    value = rds.start_all_instances(instances)
        return value

    @classmethod
    def aws_turnoff(cls, _instance):
        """
        Turnoff command
        """
        ec2_instances = ec2.get_list_instances()
        rds_instances = rds.get_list_instances()
        list_instance = ec2_instances + rds_instances
        instances = get_instance_id(_instance, list_instance, False)
        number_instance = len(instances)
        if number_instance == 0:
            return "Instance not found!"
        if number_instance == 1:
            _instance = instances[0]
            if _instance["ServiceType"] == "ec2":
                value = ec2.stop_instance(_instance)
            elif _instance["ServiceType"] == "rds":
                value = rds.stop_instance(_instance)
        else:
            for _instance in instances:
                if _instance["ServiceType"] == "ec2":
                    value = ec2.stop_all_instance(_instance)
                elif _instance["ServiceType"] == "rds":
                    value = rds.stop_all_instances(_instance)

        return value

    @classmethod
    def aws_status(cls, _instance):
        """
        aws status command using for get status of instances
        """
        attachment = {}
        ec2_instances = ec2.get_list_instances()
        rds_instances = rds.get_list_instances()
        list_instance = ec2_instances + rds_instances
        instances = get_instance_id(_instance, list_instance, False)
        if instances:
            for _instance in instances:
                if _instance["ServiceType"] == "ec2":
                    attachment = print_ec2_instance_info(_instance)
                elif _instance["ServiceType"] == "rds":
                    attachment = print_rds_instance_info(_instance)
        else:
            attachment["text"] = "Instance not found!"
            return attachment
        return attachment

    @classmethod
    def aws_tags(cls, _instance):
        """
        aws tag command using for get all instance tags
        """
        text = "The tags of instances as below:\n"
        ec2_instances = ec2.get_list_instances()
        rds_instances = rds.get_list_instances()
        list_instance = ec2_instances + rds_instances
        if _instance == "all":
            instances = list_instance
        else:
            instances = get_instance_id(_instance, list_instance, True)

        if instances:
            for _instance in instances:
                if _instance["ServiceType"] == "ec2":
                    text = "{0}  - *Tags:* `{1}`     *Service:* `ec2`\n".format(
                        text, _instance["TagName"])
                elif _instance["ServiceType"] == "rds":
                    text = "{0}  - *Tags:* `{1}`     *Service:* `rds`\n".format(
                        text, _instance["TagName"])
        else:
            return "Instance not found!"
        return text

    @classmethod
    def aws_schedule(cls, schedule):
        """
        aws schedule command using for set schedule turn-on and turn-off instance
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        if schedule["turnon"] is not None:
            cron_express = convert_datetime_to_cron(schedule["turnon"])
            cw_events.create_event(schedule["requester"] + "_turnon_" + timestamp,
                                   cron_express, constants.LAMBDA_TURNON)
        if schedule["turnoff"] is not None:
            cron_express = convert_datetime_to_cron(schedule["turnoff"])
            cw_events.create_event(schedule["requester"] + "_turnoff_" + timestamp,
                                   cron_express, constants.LAMBDA_TURNOFF)
        return schedule
