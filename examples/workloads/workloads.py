from sedai import workloads, pagination
from sedai.workloads import SedaiScalableKubeWorkload


def show_all_kube_workloads(account_id: str, pagination_config: pagination.PaginationConfig = None):

    if not account_id:
        print("Account ID is required.")
        return

    print("fetching workloads for account:", account_id)
    workloads_list = workloads.get_all_kube_workloads(account_id, pagination_config=pagination_config)
    if workloads_list is None:
        print("No workloads found or an error occurred.")
        return
    print(f"Total pages: {workloads_list.total_pages}\n\n")

    for workload in workloads_list:
        print(f"-----------------------------------------------")
        print(f"Workload Name: {workload.name}")
        print(f"Inference Type: {workload.inference_type}")
        print(f"Namespace: {workload.namespace}")
        print(f"Cluster Name: {workload.cluster_name}")
        print(f"Desired Replicas: {workload.desired_replicas}")

        if workload.instance_ids is not None and len(workload.instance_ids) > 0:
            print(f"Instance IDs: {', '.join(workload.instance_ids)}")

        if workload.load_balancer_ids is not None and len(workload.load_balancer_ids) > 0:
            print(f"Load Balancer IDs: {', '.join(workload.load_balancer_ids)}")

        if workload.node_id_vs_replica_count :
            print("\nNode ID vs Replica Count:")
            for node_id, count in workload.node_id_vs_replica_count.items():
                print(f"  {node_id}: {count}", end="\n")

        print("\nContainer Specs:")
        for index, container in enumerate(workload.container_specs):
            print(f"{index + 1}: Name: {container.name}, Image: {container.image}, \n"
                  f"\tCPU Limit: {container.cpu_limit}, CPU Request: {container.cpu_request} \n"
                  f"\tMemory Limit (bytes): {container.memory_limit_bytes}, "
                  f"\tMemory Request (bytes): {container.memory_request_bytes}\n")
        print("\n")

        if isinstance(workload, SedaiScalableKubeWorkload):
            print(f"Ready replicas: {workload.ready_replicas}")
            print(f"Available replicas: {workload.available_replicas}")
            print(f"Updated replicas: {workload.updated_replicas}")
            print(f"labels: {workload.labels}")
            print(f"annotations: {workload.annotations}")



account_id = 'account_id'
page_cofig = pagination.PaginationConfig(page_size=10, num_pages=2)
show_all_kube_workloads(account_id, pagination_config = page_cofig)




