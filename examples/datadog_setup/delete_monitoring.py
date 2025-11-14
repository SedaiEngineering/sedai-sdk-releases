from sedai import monitoring_provider

import sys

# Collect the following command line arges:
# Monitoring Provider Id

# Read the args from the command line
args = sys.argv[1:]

if len(args) != 3:
    print("Usage: python delete_monitoring.py <monitoring_provider_id>")
    sys.exit(1)

monitoring_provider_id = args[0]
api_key = args[1]
application_key = args[2]

dd_mp = monitoring_provider.delete_monitoring_provider(
    monitoring_provider_id = monitoring_provider_id
)

print(f"Datadog monitoring provider {monitoring_provider_id} deleted successfully")
