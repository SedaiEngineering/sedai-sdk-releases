from sedai.optimizations import AzureDiskConfig, EBSVolumeConfig
from sedai.optimizations.individual_resource_opportunities import get_opportunity_for_resource, VMOpportunityDetails, \
    VolumeOpportunityDetails

def show_common_vm_details(opp):
    print(f"Resource Name : {opp.resource_name}")
    print(f"Opportunity status : {opp.opportunity_status}")
    print(f"Monthly cost impact percentage : {opp.monthly_cost_impact_pct} %")
    print(f"Monthly cost impact : {opp.monthly_cost_impact}")
    print(f"Monthly cost before the optimization : {opp.pre_ops_monthly_cost}")
    print(f"Monthly cost after the optimization : {opp.post_ops_monthly_cost}")

def show_vm_opportunity_details(opp):
    vm_opp : VMOpportunityDetails = opp

    show_common_vm_details(vm_opp)
    print(f"Current instance type : {vm_opp.current_instance_type}")
    print(f"Recommended instance type : {vm_opp.recommended_instance_type}")
    print(f"On-demand pricing before optimization : {vm_opp.pre_on_demand_pricing}")
    print(f"On-demand pricing after optimization : {vm_opp.post_on_demand_pricing}")
    print(f"Estimated on-demand pricing impact : {vm_opp.estimated_on_demand_pricing_impact}")

    print(f"Instance Configs..")
    for instance in vm_opp.instance_configs:
        print(f"Instance Names : {[name for name in instance.instance_names]}")
        print(f"Current Type : {instance.current_type}")
        print(f"Recommended Type : {instance.recommended_type}")
        print(f"Account : {instance.account}")
        print(f"Region : {instance.region}")
        print(f"Quantity : {instance.quantity}")
        print(f"CPU before optimization : {instance.pre_cpu}")
        print(f"CPU after optimization : {instance.post_cpu}")
        print(f"Memory before optimization : {instance.pre_memory}")
        print(f"Memory after optimization : {instance.post_memory}")

        print(f"Max Network Bandwidth before optimization : {instance.pre_max_network_bandwidth}")
        print(f"Max Network Bandwidth after optimization : {instance.post_max_network_bandwidth}")
        print(f"EBS Throughput before optimization : {instance.pre_ebs_throughput}")
        print(f"EBS Throughput after optimization : {instance.post_ebs_throughput}")
        print(f"Max EBS Bandwidth before optimization : {instance.pre_max_ebs_bandwidth}")
        print(f"Max EBS Bandwidth after optimization : {instance.post_max_ebs_bandwidth}")
        print(f"Instance Family before optimization : {instance.pre_instance_family}")
        print(f"Instance Family after optimization : {instance.post_instance_family}")
        print(f"CPU Clock Speed before optimization (GHz) : {instance.pre_cpu_clockspeed}")
        print(f"CPU Clock Speed after optimization (GHz) : {instance.post_cpu_clockspeed}")


def show_disk_config_details(config):
    disk_config: AzureDiskConfig = config

    print(f"Disk Type : {disk_config.disk_type}")
    print(f"Tier : {disk_config.tier}")
    print(f"Size (GB) : {disk_config.size_gb}")
    print(f"IOPS : {disk_config.iops}")
    print(f"Throughput : {disk_config.throughput}")

def show_ebs_volume_config_details(config):
    ebs_config: EBSVolumeConfig = config

    print(f"Volume type : {ebs_config.volume_type}")
    print(f"Size (GB) : {ebs_config.size_gb}")
    print(f"IOPS : {ebs_config.iops}")
    print(f"Throughput : {ebs_config.throughput}")


def show_volume_opportunity_details(opp):
    vol_opp : VolumeOpportunityDetails = opp

    show_common_vm_details(vol_opp)
    if isinstance(vol_opp.current_config, AzureDiskConfig):
        print("\nCurrent Configuration....")
        print("-----------------------------")
        show_disk_config_details(vol_opp.current_config)

        print("\n")
        print("Recommended Configuration....")
        print("-----------------------------")
        show_disk_config_details(vol_opp.recommended_config)

    elif isinstance(vol_opp.current_config, EBSVolumeConfig):
        print("\nCurrent Configuration....")
        print("-----------------------------")
        show_ebs_volume_config_details(vol_opp.current_config)

        print("\n")
        print("Recommended Configuration....")
        print("-----------------------------")
        show_ebs_volume_config_details(vol_opp.recommended_config)


def print_opportunity_details(opp):

    if isinstance(opp, VMOpportunityDetails):
        show_vm_opportunity_details(opp)
    elif isinstance(opp, VolumeOpportunityDetails):
        show_volume_opportunity_details(opp)
    else:
        print('Invalid opportunity details')


# Individual resource opportunity

provider_resource_id = 'provider_resource_id'
opportunity = get_opportunity_for_resource(provider_resource_id)
print("Opportunity Details ...")
print_opportunity_details(opportunity)
