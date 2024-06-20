import csv
from sedai import groups
from sedai import settings as manage_settings

group_name = "Test Group 001"

group = groups.get_group(group_name)
if group:
    print(f"Group {group_name} already exists with Id {group.groupId}")

# Define a new group
group_definition = groups.GroupDefinition(group_name)
group_definition.add_tag('app', 'db-backend')
group_definition.add_cluster("arn:aws:ecs:us-east-1:000000000000:cluster/sedai-labs-ecs-02")

# Create the group in Sedai
try:
    create_status = groups.create_group(group_definition)

    print(f"Group {group_name} created with status {create_status}")
    group = groups.get_group(group_name)
    print(f"Id of the group is Id {group.groupId}")
except Exception as e:

    # Creating failed because group already exists
    # For this example, we will delete the group and recreate it

    # Find the existing group
    group = groups.get_group(group_name)
    print(f"Group {group.name} already exists with Id {group.groupId}")

    # Delete the group
    groups.delete_group(group.groupId)
    print(f"Group with name {group_name} and Id {group.groupId} deleted")

    # Recreate the group with the same name but with our definition
    new_create_status = groups.create_group(group_definition)
    print(f"Group {group_name} re created with status {new_create_status}")

    # Find the recreated group
    group = groups.get_group(group_name)
    print(f"Id of recreated group is {group.groupId}")



# Details of an existing group
group = groups.get_group(group_name)


print(f"Id of the group is {group.groupId}")
print("Number of matching aws load balancers in the group: ", group.awsLbCount)
print("Number of matching aws tags in the group: ", group.awsTagsCount)
print("Number of matching azure load balancers in the group: ", group.azureLbCount)
print("Number of matching azure tags in the group: ", group.azureTagsCount)
print("Number of matching azure virtual machines in the group: ", group.azureVmCount)
print("Number of matching aws elastic block storage in the group: ", group.ebsCount)
print("Number of matching aws ec2 instances in the group: ", group.ec2Count)
print("Number of matching aws ecs instances in the group: ", group.ecsCount)
print("Number of matching kubernetes resources in the group: ", group.kubeCount)
print("Number of matching aws lambda functions in the group: ", group.lambdaCount)
print("Number of matching aws s3 buckets in the group: ", group.s3Count)
print("Number of matching streaming resources in the group: ", group.streamingCount)


# Update the group
group_definition = group.definition
group_definition.add_tag('env', 'prod')
group_definition.add_cluster('cluster')
group_definition.add_region('region')
group_definition.add_namespace('namespace')
group_definition.set_auto_refresh(True)
groups.update_group(group)


# Getting the updated group details
group = groups.get_group(group_name)


print(f"Id of the group is {group.groupId}")
print("Number of matching aws load balancers in the group: ", group.awsLbCount)
print("Number of matching aws tags in the group: ", group.awsTagsCount)
print("Number of matching azure load balancers in the group: ", group.azureLbCount)
print("Number of matching azure tags in the group: ", group.azureTagsCount)
print("Number of matching azure virtual machines in the group: ", group.azureVmCount)
print("Number of matching aws elastic block storage in the group: ", group.ebsCount)
print("Number of matching aws ec2 instances in the group: ", group.ec2Count)
print("Number of matching aws ecs instances in the group: ", group.ecsCount)
print("Number of matching kubernetes resources in the group: ", group.kubeCount)
print("Number of matching aws lambda functions in the group: ", group.lambdaCount)
print("Number of matching aws s3 buckets in the group: ", group.s3Count)
print("Number of matching streaming resources in the group: ", group.streamingCount)


# Getting the settings of a newly created will fail

try:
    manage_settings.get_group_settings(group.groupId)
except Exception as e:
    print(f"Failed to get settings of group {group_name} with Id {group.groupId}")
    print(e)
# This will fail because we just created a group. We have to explicitly initialize the settings for the group

manage_settings.initialize_group_settings(group.groupId)
print(f"Settings initialized for group {group_name} with Id {group.groupId}")

# Now we can get the settings of the group
group_settings = manage_settings.get_group_settings(group.groupId)
print(f"Settings of group {group_name} with Id {group.groupId}")
print(group_settings)
