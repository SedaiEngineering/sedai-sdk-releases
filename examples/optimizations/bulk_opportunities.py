from sedai.optimizations import (
    AzureDiskConfig,
    EBSVolumeConfig,
    GCPDiskConfig,
    VMOpportunityDetails,
    VolumeOpportunityDetails,
    get_opportunities_for_resources,
)
from sedai.pagination import PaginationConfig
from sedai.settings import SettingsConfigMode


def describe_disk(config):
    if isinstance(config, EBSVolumeConfig):
        return f"EBS {config.volume_type}, {config.size_gb} GB, {config.iops} IOPS"
    if isinstance(config, AzureDiskConfig):
        return f"Azure {config.disk_type} {config.tier}, {config.size_gb} GB, {config.iops} IOPS"
    if isinstance(config, GCPDiskConfig):
        return (
            f"GCP {config.disk_type} {config.replication}, {config.size_gb} GB, {config.iops} IOPS"
        )
    return "no configuration"


def print_opportunity(opp):
    print(f"{opp.resource_name} ({opp.provider_resource_id})")
    print(f"  Mode : {opp.config_mode.value if opp.config_mode else 'unknown'}")
    print(f"  Monthly cost impact : {opp.monthly_cost_impact} ({opp.monthly_cost_impact_pct} %)")
    # VM and disk results are also OpportunityDetails, so check for them first.
    if isinstance(opp, VMOpportunityDetails):
        print(f"  Instance type : {opp.current_instance_type} -> {opp.recommended_instance_type}")
    elif isinstance(opp, VolumeOpportunityDetails):
        print(f"  Current disk : {describe_disk(opp.current_config)}")
        print(f"  Recommended disk : {describe_disk(opp.recommended_config)}")
    if opp.tags:
        # Some resources have many tags, so show only the first few
        shown = ', '.join(f'{tag.key}={tag.value}' for tag in opp.tags[:3])
        print(f"  Tags ({len(opp.tags)}) : {shown}")


def show_opportunities_for_resources(provider_resource_ids):
    # Only resources that currently have an opportunity are returned.
    for opp in get_opportunities_for_resources(provider_resource_ids, include_tags=True):
        print_opportunity(opp)


def show_opportunities_for_account(account_id):
    # An empty ID list means "don't filter by ID". With account_ids it returns every opportunity
    # in the account, which on large tenants is much faster than filtering by ID.
    opportunities = get_opportunities_for_resources(
        [],
        account_ids=[account_id],
        config_modes=[SettingsConfigMode.DATA_PILOT, SettingsConfigMode.CO_PILOT],  # optional
        pagination_config=PaginationConfig(page_size=50),
    )
    for opp in opportunities:
        print_opportunity(opp)


if __name__ == '__main__':
    # Cloud provider resource IDs, in the provider's own format
    provider_resource_ids = [
        'i-0abc1234567890def',  # AWS EC2 instance
        'vol-0abc1234567890def',  # AWS EBS volume
        '/subscriptions/{subscription}/resourceGroups/{group}/providers/Microsoft.Compute/virtualMachines/{name}',
        'https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/disks/{name}',
    ]
    print("Opportunities for specific resources ...")
    show_opportunities_for_resources(provider_resource_ids)

    account_id = 'account_id'
    print(f"\nOpportunities for account {account_id} ...")
    show_opportunities_for_account(account_id)
