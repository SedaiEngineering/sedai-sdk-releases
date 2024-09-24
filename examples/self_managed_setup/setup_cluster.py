from sedai import account, credentials, monitoring_provider

cluster_name = "cluster-name"
cluster_url = "https://cluster-url"
cluster_ca = "cluster-ca"
cluster_token = "cluster-token"

monitoring_providers = [
    {
        "endpoint": "endpoint",
        "token_url": "token_url",
        "client_id": "client_id",
        "client_secret": "client_secret",
        "mp_name": "name",
    },
]

account_created = account.create_account(
    name=cluster_name,
    cloud_provider='KUBERNETES',
    integration_type='AGENTLESS',
    credentials=credentials.TokenCredentials(cluster_token),
    cluster_provider='SELF_MANAGED',
    cluster_url=cluster_url,
    ca_certificate=cluster_ca,
)

if not account_created:
    print(f"Failed to create account {cluster_name}")
    exit(1)

print(f"Account {cluster_name} created successfully")

created_account = account.search_accounts_by_name(cluster_name)[0]
for mp in monitoring_providers:
    mp_credentials = credentials.FederatedPrometheusClientCredentials(
        token_endpoint=mp['token_url'], client_id=mp['client_id'], client_secret=mp['client_secret']
    )
    mp_created = monitoring_provider.add_federated_prometheus_monitoring(
        account_id=created_account.id,
        credentials=mp_credentials,
        endpoint=mp['endpoint'],
        name=mp['mp_name'],
    )

    if not mp_created:
        print(f"Failed to create monitoring provider for {cluster_name}")
        exit(1)

    print(f"Monitoring provider {mp['mp_name']} created successfully")
