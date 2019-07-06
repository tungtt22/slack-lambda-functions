import boto3
import Constants

def class rds:
  rds = boto3.client('rds', region_name = Constants.REGION)

  def get_instances():
    
  def start_instance(instance):
    rds.start_db_instance(DBInstanceIdentifier = str(instance))
    print ('Started RDS instance: ' + instance)
    rds_status = response.get('DBInstances')[0].get('DBInstanceStatus')
    print ("RDS Instance: " + str(instance) + " Status=" + str(rds_status))
    if rds_status == 'available' or rds_status == 'startting':
      remove_instances.append(instance)

  def stop_instance(instance):
    response = rds.describe_db_instances(DBInstanceIdentifier = str(instance))
    rds_status = response.get('DBInstances')[0].get('DBInstanceStatus')
    print ("RDS Instance: " + str(instance) + " Status=" + str(rds_status))
    if rds_status == 'stopped' or rds_status == 'stopping':
      remove_instances.append(instance)

  def start_all_instance(instances):
      # Start all DB Instance describe in instances variable
    for instance in instances.items():
      rds.start_db_instance(DBInstanceIdentifier = instance)
      print ('Started db instances: ' + instance)

    while True:
      time.sleep(300 - time.time() % 300)
      for instance in instances:
        response = rds.describe_db_instances(DBInstanceIdentifier= instance)
        rds_status = response.get('DBInstances')[0].get('DBInstanceStatus')
        rds_instance_id = response.get('DBInstances')[0].get('DBInstanceIdentifier')
        if rds_instance_id == instance:
              if rds_instance_id in instances:
                if rds_status == 'available':
                  ec2_instances.append(instances[rds_instance_id])
                  del instances[rds_instance_id]
              break

        print ('Request Response: ' + str(rds_status))
      ec2.start_instances(InstanceIds=ec2_instances)
  def start_instance(instance):
