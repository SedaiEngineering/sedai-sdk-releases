from sedai import optimizations, pagination
from sedai.optimizations import (
    AzureDiskTypeTuningOperation,
    GCPBucketAutoclassOperation,
    KubeAppOperation,
    KubeHpaSpec,
    VMRightSizingOperation,
)

# After these actions the app has no autoscaler, so a proposed_hpa of None means it was removed.
# After any other action, a proposed_hpa of None means the autoscaler was left as it was.
# This is Sedai's own list, which may grow in later Sedai versions.
ACTIONS_THAT_LEAVE_NO_HPA = {
    "KUBERNETES_DELETE_HPA",
    "KUBERNETES_DELETE_HPA_AND_PERFORM_RIGHTSIZING",
    "USER_DRIVEN_ROLLBACK_KUBERNETES_DELETE_HPA_AND_PERFORM_RIGHTSIZING",
    "USER_DRIVEN_ROLLBACK_TO_PREVIOUS_RELEASE",
}


def show_change(name, before, after):
    print(f"  {name}: {before} -> {after}")


def describe_hpa(hpa: KubeHpaSpec | None):
    if hpa is None:
        return "none"
    # hpa.metrics lists what the autoscaler scales on, for example CPU at 80% utilization.
    return f"{hpa.min_replicas} to {hpa.max_replicas} replicas"


def describe_value(value):
    # A container's CPU or memory value: the amount and its unit, for example 0.1 CORES.
    if value is None:
        return "not set"
    return f"{value.value} {value.metricUnit}"


# Show what Sedai changed in recently completed operations: each value before and after.
# include_operation_details=True makes one extra request per recommendation, so keep pages small.
recommendations_iterator = optimizations.get_recommendations(
    recommendation_status=["SUCCESSFUL"],
    include_operation_details=True,
    pagination_config=pagination.PaginationConfig(page_size=5, num_pages=1),
)

for recommendation in recommendations_iterator:
    operation = recommendation.operation
    print(f"{recommendation.resource_name}: {operation.action}")

    # Each operation type has its own class with before and after values. This example shows a
    # few. Others, such as node pools, ECS, EBS volumes, S3 buckets and Lambda functions, are in
    # sedai.optimizations too.
    if isinstance(operation, VMRightSizingOperation):
        before, after = operation.current_state, operation.proposed_state
        if before and after:
            show_change("Instance type", before.instance_type, after.instance_type)
            show_change("vCPUs", before.vcpus, after.vcpus)
            show_change("Memory (MiB)", before.memory_mib, after.memory_mib)

    elif isinstance(operation, AzureDiskTypeTuningOperation):
        before, after = operation.current_state, operation.proposed_state
        if before and after:
            show_change("Disk type", before.disk_type, after.disk_type)
            show_change("Performance tier", before.tier, after.tier)

    elif isinstance(operation, GCPBucketAutoclassOperation):
        before, after = operation.current_state, operation.proposed_state
        if before and after:
            show_change("Autoclass enabled", before.autoclass_enabled, after.autoclass_enabled)

    elif isinstance(operation, KubeAppOperation):
        before, after = operation.original_config, operation.proposed_config
        show_change("Replicas", before.replicas, after.replicas)
        for name, old in before.container_configs.items():
            new = after.container_configs.get(name)
            if new:
                print(f"  Container {name}:")
                show_change(
                    "  CPU request",
                    describe_value(old.cpu_request),
                    describe_value(new.cpu_request),
                )
                show_change(
                    "  Memory request",
                    describe_value(old.memory_request),
                    describe_value(new.memory_request),
                )

        if operation.proposed_hpa is not None:
            show_change(
                "Autoscaler",
                describe_hpa(operation.original_hpa),
                describe_hpa(operation.proposed_hpa),
            )
        elif operation.original_hpa is not None and operation.action in ACTIONS_THAT_LEAVE_NO_HPA:
            show_change("Autoscaler", describe_hpa(operation.original_hpa), "removed")

    elif operation.raw is not None:
        # A type this version of the SDK doesn't recognise. operation.raw holds the server's own
        # fields, and raw["type"] names the type.
        print(f"  Not recognised by this SDK version: {operation.raw.get('type')}")
