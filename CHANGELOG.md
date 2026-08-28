# Changelog

> Entries are labeled by SDK. Unlabeled entries below this point are the Python SDK's history —
> the TypeScript SDK didn't bump version numbers before 1.1.0, so it has no earlier entries here.

# 1.2.0 - 2026-08-28 (TypeScript SDK)

### Added

- Transaction-level bulk execution tracking: `submitBulkExecutionRequest()`, `getExecutionStatus()`, `getExecutionItems()` — submit a batch of resources and poll a single transaction ID for completion, instead of tracking a resource-ID list yourself.
- `includeItemsWhenComplete` option on `getExecutionStatus()` — get per-resource results back inline once a transaction finishes, without a separate `getExecutionItems()` call.
- `cloudProviderId` field on every execution item — the native cloud identifier (e.g. an Azure resource path or AWS ARN) alongside the Sedai resource ID. Identical to `resourceId` for Kubernetes resources.

# 1.3.20 - 2026-07-07

### Added

- [PVC Optimization Setting](https://sedaiengineering.github.io/sedai-sdk-python/sedai/settings.html#KubeAppSettings.optimizePvcDeployments)

# 1.3.19 - 2026-05-28

### Added

- [Max resource limits for Kube recommendations](https://sedaiengineering.github.io/sedai-sdk-python/sedai/settings.html#KubeAppSettings.verticalScaling_maxPerContainerCpuInCores)

# 1.3.18 - 2026-05-08

### Added

- GCP Account Update

# 1.3.17 - 2026-04-14

### Added

- Azure Account Update

# 1.3.16 - 2026-04-13

### Added

- GCP Account Update

# 1.3.15 - 2026-04-02

### Fixed

- [Group priorities](https://sedaiengineering.github.io/sedai-sdk-python/sedai/groups.html#update_group_priorities) fixes

# 1.3.14 - 2026-03-16

### Added

- [Manage group priorities](https://sedaiengineering.github.io/sedai-sdk-python/sedai/groups.html#update_group_priorities)

# 1.3.13 - 2026-03-09

### Added

- Manage prohibited namespaces
- [Smart Agent Health API](https://sedaiengineering.github.io/sedai-sdk-python/sedai/health.html)

# 1.3.12 - 2026-02-19

### Added

- GCP Account Onboarding

# 1.3.11 - 2025-12-03

### Added

- [Group Details API](https://sedaiengineering.github.io/sedai-sdk-python/sedai/groups.html#get_group_by_id)

# 1.3.10 - 2025-11-14

### Added

- [Update Datadog Monitoring Provider](https://sedaiengineering.github.io/sedai-sdk-python/sedai/monitoring_provider.html#add_or_update_datadog_monitoring)
- [Hourly cost savings in resource optimizations](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#ResourceOptimization.cost_change_per_hour)

# 1.3.9 - 2025-11-12

### Added

- [Resource Tags API](https://sedaiengineering.github.io/sedai-sdk-python/sedai/resource.html)

# 1.3.8 - 2025-10-03

### Fixed

- Issue in datetime for `get_resource_optimizations`.
- Issue with setting `horizontalScaling_replicaMultiplier` for `KubeAppSettings`.

## 1.3.7 - 2025-09-12

### Added

- [Individual resource opportunity API](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#get_opportunity_for_resource)
  - New API endpoint to fetch individual optimization opportunities for Virtual Machines (VMs) and Storage Volumes.

  - The `get_opportunity_for_resource` API accepts `provider_resource_id` as a parameter,
      which corresponds to the instance ID for VMs and the volume ID for storage volumes.


## 1.3.6 - 2025-09-11

### Added

- [SettingsConfigMode Enum](https://sedaiengineering.github.io/sedai-sdk-python/sedai/settings.html#SettingsConfigMode)
    - Introduced a new `SettingsConfigMode` enum class for Sedai settings. This enum defines how Sedai manages resources by specifying configuration modes.

    **Possible values:**
    - `DATA_PILOT`: Provides recommendations for availability and optimization.
    - `CO_PILOT`: Provides recommendations but requires manual action.
    - `AUTO`: Manages the resource autonomously.

    **Deprecated values:**
    - `OFF`
    - `MANUAL`


## 1.3.5 - 2025-08-15

### Fixed

- Issue updating group settings

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
