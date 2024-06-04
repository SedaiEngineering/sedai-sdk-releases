from sedai.settings import get_resource_settings, update_resource_settings
from sedai.settings import KubeAppSettings

kube_resource_id = '8ryzpatt/Deployment/GKE - agentless/cert-manager/cert-manager'

kuber_resource_settings: KubeAppSettings = get_resource_settings(kube_resource_id)

# If mode is MANUAL, set it to AUTO, else set it to MANUAL
def swap_mode(mode):
    if mode == 'MANUAL':
        return 'AUTO'
    return 'MANUAL'

def increment_value(value):
    if value is None:
        return 1
    return value + 1

print("\nInitial Values\n")
print("------------------")
print("Availabilty Mode", kuber_resource_settings.availabilityMode)
print("Optimization Mode", kuber_resource_settings.optimizationMode)

print("Horizontal Scaling Enabled", kuber_resource_settings.horizontalScaling_enabled)
print("Horizontal Scaling Min Replicas", kuber_resource_settings.horizontalScaling_minReplicas)
print("Horizontal Scaling Max Replicas", kuber_resource_settings.horizontalScaling_maxReplicas)
print("Horizontal Scaling Replica Multiplier", kuber_resource_settings.horizontalScaling_replicaMultiplier)

print("Vertical Scaling Enabled", kuber_resource_settings.verticalScaling_enabled)
print("Vertical Scaling Min Per Container CPU", kuber_resource_settings.verticalScaling_minPerContainerCpuInCores)
print("Vertical Scaling Min Per Container Memory", kuber_resource_settings.verticalScaling_minPerContainerMemoryInBytes)


# Swap the modes, status and increment the values
kuber_resource_settings.availabilityMode = swap_mode(kuber_resource_settings.availabilityMode)
kuber_resource_settings.optimizationMode = swap_mode(kuber_resource_settings.optimizationMode)

kuber_resource_settings.horizontalScaling_enabled = not kuber_resource_settings.horizontalScaling_enabled
kuber_resource_settings.horizontalScaling_minReplicas = increment_value(kuber_resource_settings.horizontalScaling_minReplicas)
kuber_resource_settings.horizontalScaling_maxReplicas = increment_value(kuber_resource_settings.horizontalScaling_maxReplicas)
kuber_resource_settings.horizontalScaling_replicaMultiplier = increment_value(kuber_resource_settings.horizontalScaling_replicaMultiplier)

kuber_resource_settings.verticalScaling_enabled = not kuber_resource_settings.verticalScaling_enabled
kuber_resource_settings.verticalScaling_minPerContainerCpuInCores = increment_value(kuber_resource_settings.verticalScaling_minPerContainerCpuInCores)
kuber_resource_settings.verticalScaling_minPerContainerMemoryInBytes = increment_value(kuber_resource_settings.verticalScaling_minPerContainerMemoryInBytes)

resp = update_resource_settings(kube_resource_id, kuber_resource_settings)
print(resp)
print("Updated Resource Settings")

kuber_resource_settings = get_resource_settings(kube_resource_id)

print("\nUpdated Values\n")
print("------------------")

print("Availabilty Mode", kuber_resource_settings.availabilityMode)
print("Optimization Mode", kuber_resource_settings.optimizationMode)

print("Horizontal Scaling Enabled", kuber_resource_settings.horizontalScaling_enabled)
print("Horizontal Scaling Min Replicas", kuber_resource_settings.horizontalScaling_minReplicas)
print("Horizontal Scaling Max Replicas", kuber_resource_settings.horizontalScaling_maxReplicas)
print("Horizontal Scaling Replica Multiplier", kuber_resource_settings.horizontalScaling_replicaMultiplier)

print("Vertical Scaling Enabled", kuber_resource_settings.verticalScaling_enabled)
print("Vertical Scaling Min Per Container CPU", kuber_resource_settings.verticalScaling_minPerContainerCpuInCores)
print("Vertical Scaling Min Per Container Memory", kuber_resource_settings.verticalScaling_minPerContainerMemoryInBytes)

