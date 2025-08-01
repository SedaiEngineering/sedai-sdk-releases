# Changelog

## 1.3.4 - 2025-07-29

### Fixed

- Issue parsing `account.update_account` response

## 1.3.3 - 2025-07-07

### Added

- [Workloads API](https://sedaiengineering.github.io/sedai-sdk-python/sedai/workloads.html)

## 1.3.2 - 2025-04-23

### Added

- [New version of cluster opportunities api](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#get_cluster_opportunities)
  - `optimizations.get_cluster_opportunities` api 's param `targets` is deprecated and
    marked for removal in future version
- [Introduction of new fields in ClusterOpportunity class](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#ClusterOpportunity)
  - `cost_projection_summary` field is deprecated as of 1.3.2 and will be removed in a future version.
  - Support for proxy connections

## 1.3.1 - 2025-01-23

### Added

- [New Relic monitoring provider support](https://sedaiengineering.github.io/sedai-sdk-python/sedai/monitoring_provider.html#add_new_relic_monitoring)

## 1.3.0 - 2024-11-12

### Added

- [Pagination Support](https://sedaiengineering.github.io/sedai-sdk-python/sedai/pagination.html)
- [Retrieve Sedai Recommendations](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#get_recommendations)
- [Operation Compatibility Details](https://sedaiengineering.github.io/sedai-sdk-python/sedai/operation_compatibility.html)

### Removed

- The deprecated `optimizations.get_workload_opportunities` function has been removed

## 1.2.5 - 2024-10-07

### Added

- [Retrieve recommended configuration by resource](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#get_recommended_resource_state)

## 1.2.4 - 2024-09-24

### Added

- [Add Federated Prometheus Monitoring Provider](https://sedaiengineering.github.io/sedai-sdk-python/sedai/monitoring_provider.html#add_federated_prometheus_monitoring)
- [Agentless Kubernetes setup examples](./examples/self_managed_setup/setup_cluster.py)

## 1.2.3 - 2024-08-20

### Added

- [Settings History: Retrieve history of settings changes](https://sedaiengineering.github.io/sedai-sdk-python/sedai/settings_history.html)
- [Enable/Disable group settings overrides](https://sedaiengineering.github.io/sedai-sdk-python/sedai/settings.html#enable_group_for_settings)
- Sort options for retrieving resource optimizations
