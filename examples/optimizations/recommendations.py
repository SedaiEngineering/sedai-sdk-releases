from sedai import optimizations, pagination

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

# get recommendations via the POST-based v3 endpoint (filters sent in request body)
account_ids = ["account_id"]
recommendations_iterator = optimizations.get_recommendations_v3(
    account_ids=account_ids,
    pagination_config=pagination.DEFAULT_PAGINATION_CONFIG,
)
recommendation = next(recommendations_iterator)

# get recommendations via v3 by resource id
resource_id = "resource_id"
recommendations_iterator = optimizations.get_recommendations_v3(
    resource_id=resource_id,
    pagination_config=pagination.DEFAULT_PAGINATION_CONFIG,
)
recommendation = next(recommendations_iterator)

# get recommendations via v3 with associated operation details
recommendations_iterator = optimizations.get_recommendations_v3(
    pagination_config=pagination.DEFAULT_PAGINATION_CONFIG,
    include_operation_details=True,
)
recommendation = next(recommendations_iterator)
operation = recommendation.operation
