from sedai.measurement import K8sCpuValue, MemoryValue, MetricUnit
from sedai.settings import (
    KubeAppSettings,
    SettingsConfigMode,
    get_resource_settings,
    update_resource_settings,
)

kube_resource_id = 'resource_id'

kuber_resource_settings: KubeAppSettings = get_resource_settings(kube_resource_id)


def increment_value(value):
    if value is None:
        return 1
    return value + 1


def increment_guardrail(guardrail, value_type, unit):
    """
    Bump a cpu or memory guardrail by one, keeping whatever unit it is already expressed in. A
    guardrail that is not set yet is created in `unit`.
    """
    if guardrail is None:
        return value_type(1, unit)
    guardrail.value += 1
    return guardrail


print("\nInitial Values\n")
print("------------------")
print("Availabilty Mode", kuber_resource_settings.availabilityMode)
print("Optimization Mode", kuber_resource_settings.optimizationMode)

print("Horizontal Scaling Enabled", kuber_resource_settings.horizontalScaling_enabled)
print("Horizontal Scaling Min Replicas", kuber_resource_settings.horizontalScaling_minReplicas)
print("Horizontal Scaling Max Replicas", kuber_resource_settings.horizontalScaling_maxReplicas)
print(
    "Horizontal Scaling Replica Multiplier",
    kuber_resource_settings.horizontalScaling_replicaMultiplier,
)

print("Vertical Scaling Enabled", kuber_resource_settings.verticalScaling_enabled)
print(
    "Vertical Scaling Min Per Container CPU",
    kuber_resource_settings.verticalScaling_minPerContainerCpu,
)
print(
    "Vertical Scaling Min Per Container Memory",
    kuber_resource_settings.verticalScaling_minPerContainerMemory,
)
print(
    "Vertical Scaling Max Per Container CPU",
    kuber_resource_settings.verticalScaling_maxPerContainerCpu,
)
print(
    "Vertical Scaling Max Per Container Memory",
    kuber_resource_settings.verticalScaling_maxPerContainerMemory,
)
print("Optimize PVC Deployments", kuber_resource_settings.optimizePvcDeployments)


# Changing the availability and Optimization modes.
kuber_resource_settings.availabilityMode = SettingsConfigMode.DATA_PILOT
kuber_resource_settings.optimizationMode = SettingsConfigMode.CO_PILOT

kuber_resource_settings.horizontalScaling_enabled = (
    not kuber_resource_settings.horizontalScaling_enabled
)
kuber_resource_settings.horizontalScaling_minReplicas = increment_value(
    kuber_resource_settings.horizontalScaling_minReplicas
)
kuber_resource_settings.horizontalScaling_maxReplicas = increment_value(
    kuber_resource_settings.horizontalScaling_maxReplicas
)
kuber_resource_settings.horizontalScaling_replicaMultiplier = increment_value(
    kuber_resource_settings.horizontalScaling_replicaMultiplier
)

kuber_resource_settings.verticalScaling_enabled = (
    not kuber_resource_settings.verticalScaling_enabled
)
kuber_resource_settings.verticalScaling_minPerContainerCpu = increment_guardrail(
    kuber_resource_settings.verticalScaling_minPerContainerCpu, K8sCpuValue, MetricUnit.CORES
)
kuber_resource_settings.verticalScaling_minPerContainerMemory = increment_guardrail(
    kuber_resource_settings.verticalScaling_minPerContainerMemory,
    MemoryValue,
    MetricUnit.GIBI_BYTES,
)
kuber_resource_settings.verticalScaling_maxPerContainerCpu = increment_guardrail(
    kuber_resource_settings.verticalScaling_maxPerContainerCpu, K8sCpuValue, MetricUnit.CORES
)
kuber_resource_settings.verticalScaling_maxPerContainerMemory = increment_guardrail(
    kuber_resource_settings.verticalScaling_maxPerContainerMemory,
    MemoryValue,
    MetricUnit.GIBI_BYTES,
)
kuber_resource_settings.optimizePvcDeployments = not kuber_resource_settings.optimizePvcDeployments

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
print(
    "Horizontal Scaling Replica Multiplier",
    kuber_resource_settings.horizontalScaling_replicaMultiplier,
)

print("Vertical Scaling Enabled", kuber_resource_settings.verticalScaling_enabled)
print(
    "Vertical Scaling Min Per Container CPU",
    kuber_resource_settings.verticalScaling_minPerContainerCpu,
)
print(
    "Vertical Scaling Min Per Container Memory",
    kuber_resource_settings.verticalScaling_minPerContainerMemory,
)
print(
    "Vertical Scaling Max Per Container CPU",
    kuber_resource_settings.verticalScaling_maxPerContainerCpu,
)
print(
    "Vertical Scaling Max Per Container Memory",
    kuber_resource_settings.verticalScaling_maxPerContainerMemory,
)
print("Optimize PVC Deployments", kuber_resource_settings.optimizePvcDeployments)
