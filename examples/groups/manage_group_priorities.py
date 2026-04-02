from sedai import groups

# Bulk create, enable, and prioritize a list of groups
# To update priorities for multiple groups at once, provide a list of GroupPriority objects.
# Each GroupPriority object should include:
# - group_id: The unique identifier for the group
# - priority: An integer representing the priority level (1-based, where 1 is the highest priority)
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