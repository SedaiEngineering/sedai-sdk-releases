from sedai.measurement import K8sCpuValue, MemoryValue, MetricUnit
from sedai.settings import Settings, SettingsConfigMode, get_group_settings, update_group_settings

group_id = 'group_id'


# Get the default settings for the group
group_settings: Settings = get_group_settings(group_id)


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


print("\nInitial Group Settings Values for Kube\n")
print("------------------")
print("Availabilty Mode", group_settings.kube_app_settings.availabilityMode)
print("Optimization Mode", group_settings.kube_app_settings.optimizationMode)

print("Horizontal Scaling Enabled", group_settings.kube_app_settings.horizontalScaling_enabled)
print(
    "Horizontal Scaling Min Replicas",
    group_settings.kube_app_settings.horizontalScaling_minReplicas,
)
print(
    "Horizontal Scaling Max Replicas",
    group_settings.kube_app_settings.horizontalScaling_maxReplicas,
)
print(
    "Horizontal Scaling Replica Multiplier",
    group_settings.kube_app_settings.horizontalScaling_replicaMultiplier,
)

print("Vertical Scaling Enabled", group_settings.kube_app_settings.verticalScaling_enabled)
print(
    "Vertical Scaling Min Per Container CPU",
    group_settings.kube_app_settings.verticalScaling_minPerContainerCpu,
)
print(
    "Vertical Scaling Min Per Container Memory",
    group_settings.kube_app_settings.verticalScaling_minPerContainerMemory,
)
print(
    "Vertical Scaling Max Per Container CPU",
    group_settings.kube_app_settings.verticalScaling_maxPerContainerCpu,
)
print(
    "Vertical Scaling Max Per Container Memory",
    group_settings.kube_app_settings.verticalScaling_maxPerContainerMemory,
)
print("Optimize PVC Deployments", group_settings.kube_app_settings.optimizePvcDeployments)


# Swap the modes, status and increment the values
group_settings.kube_app_settings.availabilityMode = SettingsConfigMode.DATA_PILOT
group_settings.kube_app_settings.optimizationMode = SettingsConfigMode.CO_PILOT

group_settings.kube_app_settings.horizontalScaling_enabled = (
    not group_settings.kube_app_settings.horizontalScaling_enabled
)
group_settings.kube_app_settings.horizontalScaling_minReplicas = increment_value(
    group_settings.kube_app_settings.horizontalScaling_minReplicas
)
group_settings.kube_app_settings.horizontalScaling_maxReplicas = increment_value(
    group_settings.kube_app_settings.horizontalScaling_maxReplicas
)
group_settings.kube_app_settings.horizontalScaling_replicaMultiplier = increment_value(
    group_settings.kube_app_settings.horizontalScaling_replicaMultiplier
)

group_settings.kube_app_settings.verticalScaling_enabled = (
    not group_settings.kube_app_settings.verticalScaling_enabled
)
group_settings.kube_app_settings.verticalScaling_minPerContainerCpu = increment_guardrail(
    group_settings.kube_app_settings.verticalScaling_minPerContainerCpu,
    K8sCpuValue,
    MetricUnit.CORES,
)
group_settings.kube_app_settings.verticalScaling_minPerContainerMemory = increment_guardrail(
    group_settings.kube_app_settings.verticalScaling_minPerContainerMemory,
    MemoryValue,
    MetricUnit.GIBI_BYTES,
)
group_settings.kube_app_settings.verticalScaling_maxPerContainerCpu = increment_guardrail(
    group_settings.kube_app_settings.verticalScaling_maxPerContainerCpu,
    K8sCpuValue,
    MetricUnit.CORES,
)
group_settings.kube_app_settings.verticalScaling_maxPerContainerMemory = increment_guardrail(
    group_settings.kube_app_settings.verticalScaling_maxPerContainerMemory,
    MemoryValue,
    MetricUnit.GIBI_BYTES,
)
group_settings.kube_app_settings.optimizePvcDeployments = (
    not group_settings.kube_app_settings.optimizePvcDeployments
)

update_group_settings(group_id, group_settings)
print("Updated Group Settings")

group_settings = get_group_settings(group_id)

print("\nUpdated Group Settings Values for Kube\n")
print("------------------")

print("Availabilty Mode", group_settings.kube_app_settings.availabilityMode)
print("Optimization Mode", group_settings.kube_app_settings.optimizationMode)

print("Horizontal Scaling Enabled", group_settings.kube_app_settings.horizontalScaling_enabled)
print(
    "Horizontal Scaling Min Replicas",
    group_settings.kube_app_settings.horizontalScaling_minReplicas,
)
print(
    "Horizontal Scaling Max Replicas",
    group_settings.kube_app_settings.horizontalScaling_maxReplicas,
)
print(
    "Horizontal Scaling Replica Multiplier",
    group_settings.kube_app_settings.horizontalScaling_replicaMultiplier,
)

print("Vertical Scaling Enabled", group_settings.kube_app_settings.verticalScaling_enabled)
print(
    "Vertical Scaling Min Per Container CPU",
    group_settings.kube_app_settings.verticalScaling_minPerContainerCpu,
)
print(
    "Vertical Scaling Min Per Container Memory",
    group_settings.kube_app_settings.verticalScaling_minPerContainerMemory,
)
print(
    "Vertical Scaling Max Per Container CPU",
    group_settings.kube_app_settings.verticalScaling_maxPerContainerCpu,
)
print(
    "Vertical Scaling Max Per Container Memory",
    group_settings.kube_app_settings.verticalScaling_maxPerContainerMemory,
)
print("Optimize PVC Deployments", group_settings.kube_app_settings.optimizePvcDeployments)
