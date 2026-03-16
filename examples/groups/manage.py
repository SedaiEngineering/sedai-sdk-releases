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


# Settings of the group is initialized when the group is created, so to get settings of the group call get group settings
group_settings = manage_settings.get_group_settings(group.groupId)
print(f"Settings of group {group_name} with Id {group.groupId}")
print(group_settings)


# Bulk create, enable, and prioritize a list of groups
# To update priorities for multiple groups at once, provide a list of GroupPriority objects.
# Each GroupPriority object should include:
# - group_id: The unique identifier for the group
# - priority: An integer representing the priority level (starts from 0)
# - parent_group_id: (Optional) The ID of the parent group, if the group is a sub-group
groups_to_setup = [
    {"name": "Parent-Group-Alpha", "priority": 1},
    {"name": "Sub-Group-Alpha-1", "priority": 2, "parent_name": "Parent-Group-Alpha"},
    {"name": "Parent-Group-Beta", "priority": 3},
    {"name": "Sub-Group-Beta-1", "priority": 1, "parent_name": "Parent-Group-Beta"},
]

# Collect priorities to update in a single batch after creation/verification
priorities_to_update = []

for group_cfg in groups_to_setup:
    name = group_cfg["name"]
    priority = group_cfg["priority"]
    parent_name = group_cfg.get("parent_name")
    
    # Handle Parent ID for subgroups
    parent_id = None
    if parent_name:
        parent_group = groups.get_group(parent_name)
        if parent_group:
            parent_id = parent_group.groupId
            print(f"Found parent '{parent_name}' with ID: {parent_id}")
        else:
            print(f"Warning: Parent group '{parent_name}' not found. Creating/using as top-level group.")

    # Check if group already exists
    existing = groups.get_group(name)
    gid = None
    
    if existing:
        gid = existing.groupId
        print(f"Group '{name}' already exists (ID: {gid}).")
    else:
        # Create Group if it doesn't exist
        print(f"  Group '{name}' not found. Creating new group...")
        new_group_def = groups.GroupDefinition(name)
        if parent_id:
            new_group_def.set_parent_group_id(parent_id)


        if groups.create_group(new_group_def):
            group_info = groups.get_group(name)
            gid = group_info.groupId
            print(f"Created group '{name}' (ID: {gid})")
        else:
            print(f"Failed to create group '{name}'")
            continue

    # Enable the group
    if gid:
        if groups.enable_or_disable_group(gid, True):
            print(f"Enabled group '{name}'")

            priorities_to_update.append(
                groups.GroupPriority(group_id=gid, priority=priority, parent_group_id=parent_id)
            )
        else:
            print(f"Failed to enable group '{name}'")

# Perform batch priority update
if priorities_to_update:
    print(f"\nApplying priorities for {len(priorities_to_update)} groups in batch...")
    status_list = groups.update_group_priorities(priorities_to_update)
    if status_list and all(s.success for s in status_list):
        print("All group priorities updated successfully")
    else:
        print("Some group priorities failed to update:")
        for s in status_list:
            if not s.success:
                print(f"  Group {s.groupId}: {s.message}")