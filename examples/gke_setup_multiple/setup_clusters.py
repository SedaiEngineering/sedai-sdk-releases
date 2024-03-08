import csv
from sedai import account, credentials
from sedai import monitoring_provider
from sedai import credentials
from sedai import account
import os
import json

import sys

# Read csv to list of dictionaries
def read_csv_to_list_of_dicts(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)


# Write list of dictionaries to csv
def write_list_of_dicts_to_csv(file_path, list_of_dicts):
    with open(file_path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=list_of_dicts[0].keys())
        writer.writeheader()
        writer.writerows(list_of_dicts)

def add_installation_command_to_cluster(cluster):
    install_command = account.get_agent_installation_command(cluster['cluster_name'])
    cluster['kube_ctl_command'] = install_command.kubeInstallCmd
    cluster['helm_command'] = install_command.helmInstallCmd
    return cluster

def setup_cluster(cluster):
    ret_cluster = {
        "cluster_name": cluster['cluster_name'],
        "project id": cluster['project id'],
        "service_account_file_path": cluster['service_account_file_path'],
        "status": cluster['status'],
        "kube_ctl_command": cluster['kube_ctl_command'],
        "helm_command": cluster['helm_command'],
        "notes": []
    }

    # Check if the account_name exists
    accounts = account.search_accounts_by_name(ret_cluster['cluster_name'])
    if len(accounts) > 0:
        ret_cluster["notes"].append(f"The account/cluster with name {ret_cluster['cluster_name']} already exists")
        ret_cluster['status'] = 'Cluster already exists'
        return ret_cluster

    # So ok to add the cluster
    kubernetes_account_status = account.create_account(
        name=ret_cluster['cluster_name'],
        cloud_provider='KUBERNETES',
        integration_type='AGENT_BASED',
        credentials=credentials.SedaiCredentials(),
        cluster_provider='GCP'
    )

    if not kubernetes_account_status:
        ret_cluster["notes"].append(f"Failed to create account: {kubernetes_account_status}")
        ret_cluster['status'] = 'Failed to create account'
        return ret_cluster
    else:
        kube_account = account.search_accounts_by_name(ret_cluster['cluster_name'])[0]
        account_id = kube_account.id

        # Read the service account json file
        with open(ret_cluster['service_account_file_path'], 'r') as f:
            service_account_json = json.load(f)
            # Convert the json to a json string
            service_account_json = json.dumps(service_account_json)

        # Create the monitoring provider
        tc = credentials.GKEMonitoringCredentials(
            service_account_json=service_account_json
        )

        # Add monitoring provikube_accountder
        gke_mp = monitoring_provider.add_GKE_monitoring(
            account_id=account_id,
            project_id=ret_cluster['project id'],
            credentials=tc,
            cluster_name=ret_cluster['cluster_name'],
            namespace_dimensions=['destination_service_namespace', 'namespace_name'],
            lb_dimensions=['service'],
            app_dimensions=['application_id'],
            pod_dimensions=['pod_name'],
            container_dimensions=['container_name'],

            region_dimensions=['region_val1', 'region_val_2'],
        )



        # First check if the service_account_json_file_path exists and is a valid json
        if not os.path.exists(ret_cluster['service_account_file_path']):
            ret_cluster["notes"].append(f"The service account file {ret_cluster['service_account_file_path']} does not exist")
            return ret_cluster

    add_installation_command_to_cluster(ret_cluster)
    return ret_cluster

# Iff main
if __name__ == "__main__":

    data = read_csv_to_list_of_dicts('clusters.csv')
    # "id","cluster_name","project id","service_account_file_path","status","kube_ctl_command","helm_command"

    for cluster in data:
        status = cluster['status']
        if status == 'DONE':
            continue





