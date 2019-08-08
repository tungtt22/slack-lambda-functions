"""
Define all command when call from Slack
"""

import ec2
import rds
import constants


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


class Command(object):
    """
    All command list here
    """

    def call(self, command, instance):
        """
        Call functions
        """
        method_name = command
        method = getattr(self, method_name, lambda: 'Invalid command!')
        return method(instance)

    def aws_turnon(self, _instance):
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

    def aws_turnoff(self, _instance):
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
        elif number_instance == 1:
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

    def aws_status(self, _instance):
        """
        aws status command using for get status of instances
        """
        text = ""
        ec2_instances = ec2.get_list_instances()
        rds_instances = rds.get_list_instances()
        list_instance = ec2_instances + rds_instances
        instances = get_instance_id(_instance, list_instance, False)
        if instances:
            for _instance in instances:
                if _instance["ServiceType"] == "ec2":
                    text = (
                        "The instance `{0}` has current status as below:\n" +
                        "  - *Service Type:* `{1}`\n" +
                        "  - *Status:* `{2}`\n" + "  - *Public IP:* `{3}`\n" +
                        "  - *Local IP:* `{4}`\n" +
                        "  - *Instance Type:* `{5}`\n").format(
                            _instance["TagName"],
                            _instance["ServiceType"].upper(),
                            _instance["State"], _instance["PublicIpAddress"],
                            _instance["PrivateIpAddresses"],
                            _instance["InstanceType"])
                elif _instance["ServiceType"] == "rds":
                    text = (
                        "The instance `{0}` has current status as below:\n" +
                        "  - *Service Type:* `{1}`\n" +
                        "  - *Status:* `{2}`\n" + "  - *Endpoint:* `{3}`\n" +
                        "  - *Instance Type:* `{4}`\n" +
                        "  - *Engine:* `{5}`\n" +
                        "  - *Engine Version:* `{6}`\n").format(
                            _instance["TagName"],
                            _instance["ServiceType"].upper(),
                            _instance["State"], _instance["Endpoint"],
                            _instance["InstanceType"], _instance["Engine"],
                            _instance["EngineVersion"])
        else:
            return "Instance not found!"
        return text

    def aws_tags(self, _instance):
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
                    text = "{0}  - InstanceID `{1}`, Tags `{2}`, Service `ec2`\n".format(
                        text,
                        _instance["InstanceId"],
                        _instance["TagName"])
                elif _instance["ServiceType"] == "rds":
                    text = "{0}  - InstanceID `{1}`, Tags `{2}`, Service `rds`\n".format(
                        text,
                        _instance["InstanceId"],
                        _instance["TagName"])
        else:
            return "Instance not found!"
        return "The tags of instances as below:\n" + text
