from sedai.settings import get_account_settings, update_account_settings, SettingsConfigMode
from sedai.settings import Settings

account_id = 'account_id'
account_settings: Settings = get_account_settings(account_id)

def increment_value(value):
    if value is None:
        return 1
    return value + 1

print("\nInitial Kube Settings Values\n")
print("------------------")
print("Availabilty Mode", account_settings.kube_app_settings.availabilityMode)
print("Optimization Mode", account_settings.kube_app_settings.optimizationMode)

print("Horizontal Scaling Enabled", account_settings.kube_app_settings.horizontalScaling_enabled)
print("Horizontal Scaling Min Replicas", account_settings.kube_app_settings.horizontalScaling_minReplicas)
print("Horizontal Scaling Max Replicas", account_settings.kube_app_settings.horizontalScaling_maxReplicas)
print("Horizontal Scaling Replica Multiplier", account_settings.kube_app_settings.horizontalScaling_replicaMultiplier)

print("Vertical Scaling Enabled", account_settings.kube_app_settings.verticalScaling_enabled)
print("Vertical Scaling Min Per Container CPU", account_settings.kube_app_settings.verticalScaling_minPerContainerCpuInCores)
print("Vertical Scaling Min Per Container Memory", account_settings.kube_app_settings.verticalScaling_minPerContainerMemoryInBytes)


# Swap the modes, status and increment the values
account_settings.kube_app_settings.availabilityMode = SettingsConfigMode.DATA_PILOT
account_settings.kube_app_settings.optimizationMode = SettingsConfigMode.CO_PILOT

account_settings.kube_app_settings.horizontalScaling_enabled = not account_settings.kube_app_settings.horizontalScaling_enabled
account_settings.kube_app_settings.horizontalScaling_minReplicas = increment_value(account_settings.kube_app_settings.horizontalScaling_minReplicas)
account_settings.kube_app_settings.horizontalScaling_maxReplicas = increment_value(account_settings.kube_app_settings.horizontalScaling_maxReplicas)
account_settings.kube_app_settings.horizontalScaling_replicaMultiplier = increment_value(account_settings.kube_app_settings.horizontalScaling_replicaMultiplier)

account_settings.kube_app_settings.verticalScaling_enabled = not account_settings.kube_app_settings.verticalScaling_enabled
account_settings.kube_app_settings.verticalScaling_minPerContainerCpuInCores = increment_value(account_settings.kube_app_settings.verticalScaling_minPerContainerCpuInCores)
account_settings.kube_app_settings.verticalScaling_minPerContainerMemoryInBytes = increment_value(account_settings.kube_app_settings.verticalScaling_minPerContainerMemoryInBytes)

update_account_settings(account_id, account_settings)
print("Updated Resource Settings")

account_settings = get_account_settings(account_id)

print("\nUpdated Kube Settings Values\n")
print("------------------")

print("Availabilty Mode", account_settings.kube_app_settings.availabilityMode)
print("Optimization Mode", account_settings.kube_app_settings.optimizationMode)

print("Horizontal Scaling Enabled", account_settings.kube_app_settings.horizontalScaling_enabled)
print("Horizontal Scaling Min Replicas", account_settings.kube_app_settings.horizontalScaling_minReplicas)
print("Horizontal Scaling Max Replicas", account_settings.kube_app_settings.horizontalScaling_maxReplicas)
print("Horizontal Scaling Replica Multiplier", account_settings.kube_app_settings.horizontalScaling_replicaMultiplier)

print("Vertical Scaling Enabled", account_settings.kube_app_settings.verticalScaling_enabled)
print("Vertical Scaling Min Per Container CPU", account_settings.kube_app_settings.verticalScaling_minPerContainerCpuInCores)

print("Vertical Scaling Min Per Container Memory", account_settings.kube_app_settings.verticalScaling_minPerContainerMemoryInBytes)



