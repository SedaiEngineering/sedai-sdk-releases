from sedai import pagination, optimizations

# Custom pagination configuration
pagination_config = pagination.PaginationConfig(page_size=10, num_pages=5)

# Or use the default configuration
pagination_config = pagination.DEFAULT_PAGINATION_CONFIG

recommendations_iterator = optimizations.get_recommendations(
    pagination_config=pagination_config,
)

print(f"Total pages: {recommendations_iterator.total_pages}")

# Custom pagination configuration
# Paginate first n pages of size 10
num_pages = 5
pagination_config = pagination.PaginationConfig(page_size=10, num_pages=num_pages)

recommendations_iterator = optimizations.get_recommendations(
    pagination_config=pagination_config,
)
for recommendation in recommendations_iterator:
    print(f"Recommendation Type: {recommendation.recommendation_type}")
    print(f"Recommended action: {recommendation.action_name}")
    print(f"Recommendation Status: {recommendation.status}")

# Get n-th page
page_num = 3
pagination_config = pagination.PaginationConfig(page_size=10, start=page_num, num_pages=1)

recommendations_iterator = optimizations.get_recommendations(
    pagination_config=pagination_config,
)
while recommendations_iterator.has_next():
    recommendation = next(recommendations_iterator)
    print(f"Recommendation Type: {recommendation.recommendation_type}")
    print(f"Recommended action: {recommendation.action_name}")
    print(f"Recommendation Status: {recommendation.status}")

# Get all elements in the collection
resource_id = "resource_id"
recommendations_iterator = optimizations.get_recommendations(resource_id=resource_id, pagination_config=pagination.DEFAULT_PAGINATION_CONFIG)
recommendations = list(recommendations_iterator)
print(f"Total recommendations for resource {resource_id}: {len(recommendations)}")
