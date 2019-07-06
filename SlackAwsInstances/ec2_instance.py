import boto3
import Constants

class EC2():
  ec2 = boto3.client('ec2', region_name = Constants.REGION)
  ec2_instance = boto3.resource('ec2', region_name = Constants.REGION)
  def start_all_instance(instances):
    ec2.start_instances(InstanceIds=instances)
    print ('started your instances: ' + str(instances))

  def check_instance_running(instance):
    instance = ec2_instance.Instance(str(instanceID))
    print ("EC2 Instance: " + str(instanceID) + " Status=" + str(instance.state['Code']))
    if (instance.state['Code'] == 64 or instance.state['Code'] == 80):
      remove_instances.append(instanceID)
