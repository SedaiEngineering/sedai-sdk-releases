from sedai import operation_compatibility

account_ids = ['account_id']
optimization_modes = ['DATA_PILOT']
availability_modes = ['CO_PILOT']
is_compatible = False

# Get the eligilibity details for all resources meeting the specified criteria ineligible for Sedai action
eligibility_details = operation_compatibility.get_operation_compatibility(
    account_ids=account_ids,
    optimization_modes=optimization_modes,
    availability_modes=availability_modes,
    is_compatible=is_compatible,
    include_factors=True,
)

for ed in eligibility_details:
    print()
    print("Resource: ", ed.resource_name)
    print("Is compatible: ", ed.is_compatible)
    print("Availability mode: ", ed.availability_mode)
    print("Optimization mode: ", ed.optimization_mode)
    print("Positive factors: ", ed.positive_factors)
    print("Blockers:")
    for blocker in ed.blockers:
        print("Reason: ", blocker.factor)
        print("Suggested actions: ", blocker.suggested_actions)
        print("Active: ", blocker.active)
        print()
