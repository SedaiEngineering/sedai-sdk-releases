from sedai import optimizations, models


def show_recommended_state_kube(resource_id: str):
    recommended_state = optimizations.get_recommended_resource_state(resource_id)
    print(f"Recommended replicas: {recommended_state.replicas}")
    print("Recommended container configurations:\n")
    for container, config in recommended_state.kubeContainerConfigStateMap.__dict__.items():
        print(f"Container: {container}")
        print("Configuration:")
        print(models.to_json(config))


def show_recommended_state_lambda(resource_id: str):
    recommended_state = optimizations.get_recommended_resource_state(resource_id)
    print(f"Recommended memory: {recommended_state.memorySize}")
    print(f"Recommended timeout: {recommended_state.timeout}")
    print(f"Recommended reserved concurrency: {recommended_state.reservedConcurrency}")
    print(f"Recommended provisioned concurrency: {recommended_state.provisionedConcurrency}")


def show_recommended_state_s3(resource_id: str):
    recommended_state = optimizations.get_recommended_resource_state(resource_id)
    print("Recommended life cycle rules:")
    print(models.to_json(recommended_state.lifecycleRules))


def show_recommended_state_ebs(resource_id: str):
    recommended_state = optimizations.get_recommended_resource_state(resource_id)
    print(f"Recommended volume type: {recommended_state.volumeType}")
    print(f"Recommended volume size (GB): {recommended_state.sizeInGB}")
    print(f"Recommended IOPS: {recommended_state.iops}")
    print(f"Recommended throughput: {recommended_state.throughput}")


kube_resource_id = 'kube_resource_id'
print("Kube recommended state: ")
show_recommended_state_kube(kube_resource_id)

lambda_resource_id = 'lambda_resource_id'
print("\nLambda recommended state: ")
show_recommended_state_lambda(lambda_resource_id)

s3_resource_id = 's3_resource_id'
print("\nS3 recommended state: ")
show_recommended_state_s3(s3_resource_id)

ebs_resource_id = 'ebs_resource_id'
print("\nEBS recommended state: ")
show_recommended_state_ebs(ebs_resource_id)
