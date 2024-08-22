from sedai import settings_history, settings
from datetime import datetime, timedelta
from typing import List

resource_id = "resourceid"
group_id = "groupid"
account_id = "accountid"


def swap_mode(mode):
    if mode == 'MANUAL':
        return 'AUTO'
    return 'MANUAL'


def print_events(events: List[settings_history.SettingsChangeEvent]):
    print(f"{len(events)} event(s) received...")
    for event in events:
        print(f"{event.event_type} event at {event.updated_time} by user {event.updated_user}")
        print("Modified settings:")
        for setting in event.updated_settings:
            print(f"\nSetting key: {setting.setting_key}")
            print(f"Initial value: {setting.initial_value}")
            print(f"New value: {setting.new_value}")


# Modify resource settings
resource_settings = settings.get_resource_settings(resource_id)
resource_settings.availabilityMode = swap_mode(resource_settings.availabilityMode)
resource_settings = settings.update_resource_settings(resource_id, resource_settings)

starttime = datetime.now() - timedelta(seconds=1)
endtime = datetime.now()
events = settings_history.get_resource_settings_history(resource_id, starttime, endtime)
print("Resource settings events:")
print_events(events)

# Modify group settings
group_settings = settings.get_group_settings(group_id)
group_settings.app_settings.availabilityMode = swap_mode(
    group_settings.app_settings.availabilityMode
)
group_settings = settings.update_group_settings(group_id, group_settings)

starttime = datetime.now() - timedelta(seconds=1)
endtime = datetime.now()
events = settings_history.get_group_settings_history(group_id, starttime, endtime)
print("\nGroup settings events:")
print_events(events)

# Modify account settings
account_settings = settings.get_account_settings(account_id)
account_settings.app_settings.availabilityMode = swap_mode(
    account_settings.app_settings.availabilityMode
)
account_settings = settings.update_account_settings(account_id, account_settings)

starttime = datetime.now() - timedelta(seconds=1)
endtime = datetime.now()
events = settings_history.get_account_settings_history(account_id, starttime, endtime)
print("\nAccount settings events:")
print_events(events)
