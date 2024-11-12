from sedai import pagination, optimizations


# get recommendations by account id
account_ids = ["account_id"]
recommendations_iterator = optimizations.get_recommendations(
    account_ids=account_ids,
    pagination_config=pagination.DEFAULT_PAGINATION_CONFIG,
)
recommendation = next(recommendations_iterator)

# get recommendations by resource id
resource_id = "resource_id"
recommendations_iterator = optimizations.get_recommendations(
    resource_id=resource_id,
    pagination_config=pagination.DEFAULT_PAGINATION_CONFIG,
)
recommendation = next(recommendations_iterator)

# get recommendations with associated operation details
recommendations_iterator = optimizations.get_recommendations(
    pagination_config=pagination.DEFAULT_PAGINATION_CONFIG,
    include_operation_details=True,
)
recommendation = next(recommendations_iterator)
operation = recommendation.operation
