from sedai.settings import get_group_settings, update_group_settings
from sedai.settings import Settings


group_id = '9f9300f6-7192-41ea-87e2-7dac93344aea'


# Get the default settings for the group
group_settings: Settings = get_group_settings(group_id)


# If mode is MANUAL, set it to AUTO, else set it to MANUAL
def swap_mode(mode):
    if mode == 'MANUAL':
        return 'AUTO'
    return 'MANUAL'

def increment_value(value):
    if value is None:
        return 1
    return value + 1

print("\nInitial Group Settings Values for Kube\n")
print("------------------")
print("Availabilty Mode", group_settings.kube_app_settings.availabilityMode)
print("Optimization Mode", group_settings.kube_app_settings.optimizationMode)

print("Horizontal Scaling Enabled", group_settings.kube_app_settings.horizontalScaling_enabled)
print("Horizontal Scaling Min Replicas", group_settings.kube_app_settings.horizontalScaling_minReplicas)
print("Horizontal Scaling Max Replicas", group_settings.kube_app_settings.horizontalScaling_maxReplicas)
print("Horizontal Scaling Replica Multiplier", group_settings.kube_app_settings.horizontalScaling_replicaMultiplier)

print("Vertical Scaling Enabled", group_settings.kube_app_settings.verticalScaling_enabled)
print("Vertical Scaling Min Per Container CPU", group_settings.kube_app_settings.verticalScaling_minPerContainerCpuInCores)
print("Vertical Scaling Min Per Container Memory", group_settings.kube_app_settings.verticalScaling_minPerContainerMemoryInBytes)


# Swap the modes, status and increment the values
group_settings.kube_app_settings.availabilityMode = swap_mode(group_settings.kube_app_settings.availabilityMode)
group_settings.kube_app_settings.optimizationMode = swap_mode(group_settings.kube_app_settings.optimizationMode)

group_settings.kube_app_settings.horizontalScaling_enabled = not group_settings.kube_app_settings.horizontalScaling_enabled
group_settings.kube_app_settings.horizontalScaling_minReplicas = increment_value(group_settings.kube_app_settings.horizontalScaling_minReplicas)
group_settings.kube_app_settings.horizontalScaling_maxReplicas = increment_value(group_settings.kube_app_settings.horizontalScaling_maxReplicas)
group_settings.kube_app_settings.horizontalScaling_replicaMultiplier = increment_value(group_settings.kube_app_settings.horizontalScaling_replicaMultiplier)

group_settings.kube_app_settings.verticalScaling_enabled = not group_settings.kube_app_settings.verticalScaling_enabled
group_settings.kube_app_settings.verticalScaling_minPerContainerCpuInCores = increment_value(group_settings.kube_app_settings.verticalScaling_minPerContainerCpuInCores)
group_settings.kube_app_settings.verticalScaling_minPerContainerMemoryInBytes = increment_value(group_settings.kube_app_settings.verticalScaling_minPerContainerMemoryInBytes)

update_group_settings(group_id, group_settings)
print("Updated Group Settings")

group_settings = get_group_settings(group_id)

print("\nUpdated Group Settings Values for Kube\n")
print("------------------")

print("Availabilty Mode", group_settings.kube_app_settings.availabilityMode)
print("Optimization Mode", group_settings.kube_app_settings.optimizationMode)

print("Horizontal Scaling Enabled", group_settings.kube_app_settings.horizontalScaling_enabled)
print("Horizontal Scaling Min Replicas", group_settings.kube_app_settings.horizontalScaling_minReplicas)
print("Horizontal Scaling Max Replicas", group_settings.kube_app_settings.horizontalScaling_maxReplicas)
print("Horizontal Scaling Replica Multiplier", group_settings.kube_app_settings.horizontalScaling_replicaMultiplier)

print("Vertical Scaling Enabled", group_settings.kube_app_settings.verticalScaling_enabled)
print("Vertical Scaling Min Per Container CPU", group_settings.kube_app_settings.verticalScaling_minPerContainerCpuInCores)
print("Vertical Scaling Min Per Container Memory", group_settings.kube_app_settings.verticalScaling_minPerContainerMemoryInBytes)

