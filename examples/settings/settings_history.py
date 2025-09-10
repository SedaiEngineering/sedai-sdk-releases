from sedai import settings_history, settings
from datetime import datetime, timedelta
from typing import List

from sedai.settings import SettingsConfigMode

resource_id = "resourceid"
group_id = "groupid"
account_id = "accountid"

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
resource_settings.availabilityMode = SettingsConfigMode.DATA_PILOT
resource_settings = settings.update_resource_settings(resource_id, resource_settings)

start_time = datetime.now() - timedelta(seconds=1)
endtime = datetime.now()
events = settings_history.get_resource_settings_history(resource_id, start_time, endtime)
print("Resource settings events:")
print_events(events)

# Modify group settings
group_settings = settings.get_group_settings(group_id)
group_settings.app_settings.availabilityMode = SettingsConfigMode.DATA_PILOT
group_settings = settings.update_group_settings(group_id, group_settings)

start_time = datetime.now() - timedelta(seconds=1)
endtime = datetime.now()
events = settings_history.get_group_settings_history(group_id, start_time, endtime)
print("\nGroup settings events:")
print_events(events)

# Modify account settings
account_settings = settings.get_account_settings(account_id)
account_settings.app_settings.availabilityMode = SettingsConfigMode.DATA_PILOT
account_settings = settings.update_account_settings(account_id, account_settings)

start_time = datetime.now() - timedelta(seconds=1)
endtime = datetime.now()
events = settings_history.get_account_settings_history(account_id, start_time, endtime)
print("\nAccount settings events:")
print_events(events)
