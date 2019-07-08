import boto3
import Constants

ec2 = boto3.client('ec2', region_name = Constants.REGION)
rds = boto3.client('rds', region_name = Constants.REGION)
ec2_instance = boto3.resource('ec2', region_name = Constants.REGION)

def start_all_ec2_instance(instances):
  ec2.start_instances(InstanceIds=instances)
  print ('started your instances: ' + str(instances))

def check_ec2_instance_status(instance_id):
  instance = ec2_instance.Instance(str(instance_id))
  print ("EC2 Instance: " + str(instance_id) + " Status=" + str(instance.state['Code']))
  if (instance.state['Code'] == 64 or instance.state['Code'] == 80):
    remove_instances.append(instance_id)
