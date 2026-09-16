from sedai.measurement import K8sCpuValue, MemoryValue, MetricUnit
from sedai.settings import (
    Settings,
    SettingsConfigMode,
    get_account_settings,
    update_account_settings,
)

account_id = 'vqxi7rgo'
account_settings: Settings = get_account_settings(account_id)


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


print("\nInitial Kube Settings Values\n")
print("------------------")
print("Availabilty Mode", account_settings.kube_app_settings.availabilityMode)
print("Optimization Mode", account_settings.kube_app_settings.optimizationMode)

print("Horizontal Scaling Enabled", account_settings.kube_app_settings.horizontalScaling_enabled)
print(
    "Horizontal Scaling Min Replicas",
    account_settings.kube_app_settings.horizontalScaling_minReplicas,
)
print(
    "Horizontal Scaling Max Replicas",
    account_settings.kube_app_settings.horizontalScaling_maxReplicas,
)
print(
    "Horizontal Scaling Replica Multiplier",
    account_settings.kube_app_settings.horizontalScaling_replicaMultiplier,
)

print("Vertical Scaling Enabled", account_settings.kube_app_settings.verticalScaling_enabled)
print(
    "Vertical Scaling Min Per Container CPU",
    account_settings.kube_app_settings.verticalScaling_minPerContainerCpu,
)
print(
    "Vertical Scaling Min Per Container Memory",
    account_settings.kube_app_settings.verticalScaling_minPerContainerMemory,
)
print(
    "Vertical Scaling Max Per Container CPU",
    account_settings.kube_app_settings.verticalScaling_maxPerContainerCpu,
)
print(
    "Vertical Scaling Max Per Container Memory",
    account_settings.kube_app_settings.verticalScaling_maxPerContainerMemory,
)
print("Optimize PVC Deployments", account_settings.kube_app_settings.optimizePvcDeployments)


# Swap the modes, status and increment the values
account_settings.kube_app_settings.availabilityMode = SettingsConfigMode.DATA_PILOT
account_settings.kube_app_settings.optimizationMode = SettingsConfigMode.CO_PILOT

account_settings.kube_app_settings.horizontalScaling_enabled = (
    not account_settings.kube_app_settings.horizontalScaling_enabled
)
account_settings.kube_app_settings.horizontalScaling_minReplicas = increment_value(
    account_settings.kube_app_settings.horizontalScaling_minReplicas
)
account_settings.kube_app_settings.horizontalScaling_maxReplicas = increment_value(
    account_settings.kube_app_settings.horizontalScaling_maxReplicas
)
account_settings.kube_app_settings.horizontalScaling_replicaMultiplier = increment_value(
    account_settings.kube_app_settings.horizontalScaling_replicaMultiplier
)

account_settings.kube_app_settings.verticalScaling_enabled = (
    not account_settings.kube_app_settings.verticalScaling_enabled
)
account_settings.kube_app_settings.verticalScaling_minPerContainerCpu = increment_guardrail(
    account_settings.kube_app_settings.verticalScaling_minPerContainerCpu,
    K8sCpuValue,
    MetricUnit.CORES,
)
account_settings.kube_app_settings.verticalScaling_minPerContainerMemory = increment_guardrail(
    account_settings.kube_app_settings.verticalScaling_minPerContainerMemory,
    MemoryValue,
    MetricUnit.GIBI_BYTES,
)
account_settings.kube_app_settings.verticalScaling_maxPerContainerCpu = increment_guardrail(
    account_settings.kube_app_settings.verticalScaling_maxPerContainerCpu,
    K8sCpuValue,
    MetricUnit.CORES,
)
account_settings.kube_app_settings.verticalScaling_maxPerContainerMemory = increment_guardrail(
    account_settings.kube_app_settings.verticalScaling_maxPerContainerMemory,
    MemoryValue,
    MetricUnit.GIBI_BYTES,
)
account_settings.kube_app_settings.optimizePvcDeployments = (
    not account_settings.kube_app_settings.optimizePvcDeployments
)

update_account_settings(account_id, account_settings)
print("Updated Resource Settings")

account_settings = get_account_settings(account_id)

print("\nUpdated Kube Settings Values\n")
print("------------------")

print("Availabilty Mode", account_settings.kube_app_settings.availabilityMode)
print("Optimization Mode", account_settings.kube_app_settings.optimizationMode)

print("Horizontal Scaling Enabled", account_settings.kube_app_settings.horizontalScaling_enabled)
print(
    "Horizontal Scaling Min Replicas",
    account_settings.kube_app_settings.horizontalScaling_minReplicas,
)
print(
    "Horizontal Scaling Max Replicas",
    account_settings.kube_app_settings.horizontalScaling_maxReplicas,
)
print(
    "Horizontal Scaling Replica Multiplier",
    account_settings.kube_app_settings.horizontalScaling_replicaMultiplier,
)

print("Vertical Scaling Enabled", account_settings.kube_app_settings.verticalScaling_enabled)
print(
    "Vertical Scaling Min Per Container CPU",
    account_settings.kube_app_settings.verticalScaling_minPerContainerCpu,
)
print(
    "Vertical Scaling Min Per Container Memory",
    account_settings.kube_app_settings.verticalScaling_minPerContainerMemory,
)
print(
    "Vertical Scaling Max Per Container CPU",
    account_settings.kube_app_settings.verticalScaling_maxPerContainerCpu,
)
print(
    "Vertical Scaling Max Per Container Memory",
    account_settings.kube_app_settings.verticalScaling_maxPerContainerMemory,
)
print("Optimize PVC Deployments", account_settings.kube_app_settings.optimizePvcDeployments)
