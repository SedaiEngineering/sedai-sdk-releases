from sedai import optimizations, models
from typing import List
from datetime import datetime


def get_opportunities_for_account(account_id: str):
    level = "account"
    return optimizations.get_opportunities(level, account_id)


def show_cluster_opportunities(
    cluster_id: str,
    targets: List[str] = None,
):
    cluster_opts = optimizations.get_cluster_opportunities(cluster_id, targets)
    if cluster_opts is None:
        print(f"No optimizations for cluster: {cluster_id}")
        return

    costProjection = cluster_opts.cost_projection_summary
    print(f"Opportunities available for cluster: {cluster_opts.resource_name}")
    if costProjection is not None:
        print(f"Current monthly cost: {costProjection.currentMonthlyCost}")
        print(f"Total predicted monthly cost: {costProjection.predictedMonthlyCost.total}")
        print(f"Predicted monthly savings: {costProjection.predictedMonthlySavings}")
        print("\n")

    workload_optimizations = cluster_opts.workload_optimizations
    for optimization in workload_optimizations:
        print(f"Resource Name: {optimization.resource_name}")
        print(f"Resource ID: {optimization.resource_id}")
        print(f"Account ID: {optimization.account_id}")
        print(f"Optimization Time: {optimization.optimization_time}")
        if type(optimization) is optimizations.KubeResourceOptimization:
            orig_cont_config = optimization.original_container_config
            recommended_cont_config = optimization.recommended_container_config
            for name, pre_config in orig_cont_config.items():
                post_config = recommended_cont_config[name]
                print(f"Container: {name}, Original configuration:\n")
                print(f"Memory request: {models.to_json(pre_config.memory_request)}")
                print(f"Memory limit: {models.to_json(pre_config.memory_limit)}")
                print(f"CPU request: {models.to_json(pre_config.cpu_request)}")
                print(f"CPU limit: {models.to_json(pre_config.cpu_limit)}\n")

                print(f"Container: {name}, Recommended configuration:\n")
                print(f"Memory request: {models.to_json(post_config.memory_request)}")
                print(f"Memory limit: {models.to_json(post_config.memory_limit)}")
                print(f"CPU request: {models.to_json(post_config.cpu_request)}")
                print(f"CPU limit: {models.to_json(post_config.cpu_limit)}\n")

            print(
                f"Original workload configuration: {optimization.original_workload_config.replicas} replicas"
            )
            print(
                f"Recommended workload configuration: {optimization.recommended_workload_config.replicas} replicas\n"
            )
        else:
            print("Original resource configuration:")
            print(models.to_json(optimization.original_resource_config))

            print("Recommended resource configuration:")
            print(models.to_json(optimization.recommended_resource_config))

    orig_node_config = cluster_opts.nodegroup_optimization.original_nodegroup_config
    recommended_curr_node_config = (
        cluster_opts.nodegroup_optimization.recommended_nodegroup_config_original
    )
    recommended_optimal_node_config = (
        cluster_opts.nodegroup_optimization.recommended_nodegroup_config_optimal
    )
    print("\nOriginal node configuration:")
    print(
        [
            f"Name: {ng.name}, Instance type: {ng.instance_type}, Memory (bytes): {ng.memory_bytes}, VCPUS: {ng.vcpus}"
            for ng in orig_node_config.nodegroups
            if ng is not None
        ]
    )
    print("\nRecommendations for original node configuration:")
    print(
        [
            f"Name: {ng.name}, Instance type: {ng.instance_type}, Memory (bytes): {ng.memory_bytes}, VCPUS: {ng.vcpus}"
            for ng in recommended_curr_node_config.nodegroups
            if ng is not None
        ]
    )
    print("\nOptimal node configuration:")
    print(
        [
            f"Name: {ng.name}, Instance type: {ng.instance_type}, Memory (bytes): {ng.memory_bytes}, VCPUS: {ng.vcpus}"
            for ng in recommended_optimal_node_config.nodegroups
            if ng is not None
        ]
    )


def show_optimizations(starttime: datetime, endtime: datetime, resource_id: str):
    opts = optimizations.get_resource_optimizations(
        starttime=starttime, endtime=endtime, resource_id=resource_id
    )
    if len(opts) == 0:
        print(f"No optimizations for resource: {resource_id} from {starttime} to {endtime}")
        return
    for opt in opts:
        print(f"Resource ID: {opt.resource_id}")
        print(f"Account ID: {opt.account_id}")
        print(f"Optimization Time: {opt.optimization_time}")
        if type(opt) is optimizations.KubeResourceOptimization:
            orig_cont_config = opt.original_container_config
            recommended_cont_config = opt.recommended_container_config
            for name, pre_config in orig_cont_config.items():
                post_config = recommended_cont_config[name]
                print(f"Container: {name}, Original configuration:\n")
                print(f"Memory request: {models.to_json(pre_config.memory_request)}")
                print(f"Memory limit: {models.to_json(pre_config.memory_limit)}")
                print(f"CPU request: {models.to_json(pre_config.cpu_request)}")
                print(f"CPU limit: {models.to_json(pre_config.cpu_limit)}\n")

                print(f"Container: {name}, Recommended configuration:\n")
                print(f"Memory request: {models.to_json(post_config.memory_request)}")
                print(f"Memory limit: {models.to_json(post_config.memory_limit)}")
                print(f"CPU request: {models.to_json(post_config.cpu_request)}")
                print(f"CPU limit: {models.to_json(post_config.cpu_limit)}\n")

            print(
                f"Original workload configuration: {opt.original_workload_config.replicas} replicas"
            )
            print(
                f"Recommended workload configuration: {opt.recommended_workload_config.replicas} replicas\n"
            )
        else:
            print("Original resource configuration:")
            print(models.to_json(opt.original_resource_config))

            print("Recommended resource configuration:")
            print(models.to_json(opt.recommended_resource_config))


account_id = "account_id"
opts = get_opportunities_for_account(account_id)
print("Available opportunities:")
for opt_details in opts['content']:
    cluster_id = opt_details['clusterId']
    targets = ["NODE", "WORK_LOAD", "PURCHASE_OPTION"]
    show_cluster_opportunities(
        cluster_id=cluster_id,
        targets=targets,
    )

starttime_str = "09/01/23 00:00:00"
starttime = datetime.strptime(starttime_str, "%m/%d/%y %H:%M:%S")
endtime = datetime.now()
resource_id = "resource_id"

print("\n\nCompleted Optimizations:")
show_optimizations(starttime=starttime, endtime=endtime, resource_id=resource_id)
