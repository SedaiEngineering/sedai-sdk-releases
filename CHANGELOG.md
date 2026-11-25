# Changelog — Python SDK

Changes to the `sedai_sdk` Python package, newest first.
For the TypeScript / JavaScript SDK, see [CHANGELOG-typescript.md](./CHANGELOG-typescript.md).

# 1.4.0 - 2026-11-24

### Added

- [`sedai.aggression_mode.AggressionMode`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/aggression_mode.html):
  three-valued optimization-aggression setting for Kube and ECS resources — `PROD` /
  `EXPEDITE` / `TURBO` — mirroring the server-side Java enum `OptimizationMode`
  (`org.sedai.models.common.optimization.OptimizationMode`). Renamed to `AggressionMode` in the
  SDK because the Python name `optimizationMode` was already taken on `BaseSettings` for the
  autonomy level (`SettingsConfigMode`). Available as `KubeAppSettings.aggressionMode` and
  `ECSAppSettings.aggressionMode`; accepts either an `AggressionMode` enum value or the matching
  wire string on assignment.
- [`optimizations.get_opportunities_for_resources`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#get_opportunities_for_resources):
  optimization opportunities for many resources at once, filtered by cloud provider resource ID,
  account, group or mode, fetched page by page. VMs and disks come back with their current and
  recommended configuration; all other resource types with cost and savings. An empty ID list means
  "don't filter by ID", as in the TypeScript SDK. Pass it with `account_ids` to get a whole account,
  which on large tenants is much faster than filtering by ID. Pages are numbered from 1. The
  `PaginationConfig` you pass is not changed, so it can be reused. A single string or None in place
  of the ID list raises `TypeError`. The API must be enabled for the tenant; contact Sedai support
  if the call fails with HTTP 403.
- [`GCPDiskConfig`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#GCPDiskConfig):
  GCP persistent disk details (disk type, replication, size, IOPS, throughput) on
  `VolumeOpportunityDetails`. GCP disks previously had no configuration.
- [`OpportunityDetails`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#OpportunityDetails)
  now has `provider_resource_id`, `config_mode` and `tags` (a list of
  [`OpportunityTag`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#OpportunityTag)).
  `tags` is a list when tags are requested, empty for an untagged resource, and None otherwise.
- Before and after values for three more kinds of completed operation. They appear in
  `Recommendation.operation` when you call
  [`get_recommendations`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#get_recommendations) or
  [`get_recommendations_v3`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#get_recommendations_v3) with `include_operation_details=True`.
  Until now these came back as a plain `Operation` with only `action`.
  - [`VMRightSizingOperation`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#VMRightSizingOperation):
    operations that change a virtual machine's instance type, such as rightsizing and rolling it
    back. `current_state` and `proposed_state` are
    [`VMInstanceSpec`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#VMInstanceSpec)
    objects: instance type, vCPUs, memory in MiB, instance family, CPU architecture and clock speed,
    network bandwidth and EBS throughput. Some of these are None for Google Cloud machine types.
    `instance_ids` lists the instances changed.
  - [`AzureDiskTypeTuningOperation`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#AzureDiskTypeTuningOperation):
    Azure disk type tuning. `current_state` and `proposed_state` are
    [`AzureDiskConfig`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#AzureDiskConfig)
    objects: disk type, performance tier, size, IOPS and throughput.
  - [`GCPBucketAutoclassOperation`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#GCPBucketAutoclassOperation):
    turning on Autoclass for a Google Cloud Storage bucket. `current_state` and `proposed_state` are
    [`GCPBucketConfig`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#GCPBucketConfig)
    objects: whether Autoclass is on, the coldest storage class it may use, and the lifecycle rules.
- [`KubeAppOperation`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#KubeAppOperation)
  now has `original_hpa` and `proposed_hpa`: the HorizontalPodAutoscaler settings before and after
  the operation, as
  [`KubeHpaSpec`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#KubeHpaSpec)
  objects (minimum and maximum replicas, and the metrics it scales on as
  [`KubeHpaMetric`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#KubeHpaMetric)).
  When `proposed_hpa` is None, `action` says what that means: after `KUBERNETES_DELETE_HPA`,
  `KUBERNETES_DELETE_HPA_AND_PERFORM_RIGHTSIZING`,
  `USER_DRIVEN_ROLLBACK_KUBERNETES_DELETE_HPA_AND_PERFORM_RIGHTSIZING` or
  `USER_DRIVEN_ROLLBACK_TO_PREVIOUS_RELEASE` the app has no autoscaler (the one in `original_hpa`
  was removed); after any other action the autoscaler was left as it was.
- [`Operation.raw`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#Operation.raw):
  for an operation type this version of the SDK does not recognise, everything Sedai sent for it,
  so its before and after values are still available. None for the recognised types.
- [Example: before and after values of completed operations](./examples/optimizations/completed_operations.py)
- `sedai.mode`: a dedicated surface for changing the optimization-aggression mode of a resource,
  group or account without reading-then-writing the full settings DTO.
  - `change_resource_mode(resource_id, mode, *, ignore_guardrail_reset=False)` switches one
    resource to `PROD`, `EXPEDITE` or `TURBO`. On `TURBO` it fetches the resource's settings and
    rejects non-Kube resources with `TurboNotSupportedForResourceTypeError` at the SDK boundary —
    the server stores but does not act on TURBO for ECS, so the SDK fails fast on the client.
    Cold resources (no settings row on the server) short-circuit to `False` via a typed
    `ResourceSettingsNotFoundError` catch instead of posting.
  - `change_group_mode(group_id, resource_type, mode, *, ignore_guardrail_reset=False)` and
    `change_account_mode(account_id, resource_type, mode, *, ignore_guardrail_reset=False)` change
    the group-tier or account-tier settings row for the given `resource_type`. The settings
    cascade handles the rest: groups and resources that carry their own overrides are unaffected.
    `resource_type` is mandatory (a `ResourceType` enum — `KUBE` or `ECS`); `TURBO` on `ECS` is
    rejected O(1) at the tier boundary.
  - `change_resource_mode_bulk(items, resource_type, *, ignore_guardrail_reset=False)` applies a
    per-resource mode change to many resources in one batch. `resource_type` is mandatory; the
    homogeneous-batch assumption eliminates per-resource TURBO type-check fetches. Returns a
    `BulkModeChangeResult` carrying `.results`, `.errors`, `.succeeded` and `.failed`.
  - `preview_mode_change(resource_id, target_mode)` returns the `ModeChangeDiff` the server would
    apply — a per-field classification into `.keeps`, `.overwrites` and `.clears`, with
    `has_destructive_changes` summing the last two. Mirrors the server's
    `ModeGuardrailDefaults.java` apply semantics: a stored value of `None`, `-1` sentinel or
    wire-wrapped null MetricValue is `unset` and preserved on any transition, and null target
    fields in the mode defaults clear CPU/memory guardrails. No mode sets a replica default
    today, so a switch leaves replicas as they are, and they are not surfaced in the diff.
  - `get_mode_defaults()` returns the mode defaults as a mapping `AggressionMode →
    KubeModeGuardrailDefaults | None` (four fields: min/max per-container CPU and min/max
    per-container memory). Of these, only `maxPerContainerCpu` and `maxPerContainerMemory` are
    populated in current product configuration; the min bounds ship as `null` on the wire. The
    server DTO also carries three replica fields (`minReplicas`, `maxReplicas`,
    `replicaMultiplier`), which the SDK drops: no mode sets a replica default today, so a switch
    leaves replicas as they are, and the UI shows only the vertical-sizing fields. Global per
    installation — the same values for every account, so the call takes no tier or account
    parameter. An unknown mode shipped by a future server emits a `RuntimeWarning` and is
    skipped, rather than breaking the SDK.
  - `ignore_guardrail_reset=False` (the default) is a safety contract: at the resource tier, if
    the preview shows destructive changes, the call raises
    `GuardrailResetRequiresAcknowledgementError` with the full diff and never posts. At the group
    and account tiers, preview isn't wired yet, so the call raises `NotImplementedError` to make
    the gap visible — the previous warn-and-proceed behavior was invisible under default Python
    warning filters. Pass `ignore_guardrail_reset=True` to opt out (bulk returns partial results
    under this mode; the aggregate case raises `BulkGuardrailResetRequiresAcknowledgementError`
    with a per-id diff map before any POST fires). Most `PROD` ↔ `TURBO` switches need
    `ignore_guardrail_reset=True`, because the max-CPU and max-memory defaults differ between
    modes (`TURBO` lifts max CPU from `10` to `12` cores, for example): the switch overwrites the
    stored guardrail, which the preview reports as destructive.
- `settings.ResourceSettingsNotFoundError` (a `RuntimeError` subclass carrying `.resource_id`):
  raised by `get_resource_settings` when the server returns `200 OK` with `result: null` for a
  resource it does not know about. Existing `except RuntimeError:` catches continue to work; the
  subclass lets new code distinguish "cold resource" from other server errors (what
  `change_resource_mode` now uses to short-circuit a cold resource to `False`).

### Deprecated

- `KubeAppSettings.isProd` / `ECSAppSettings.isProd` as a write-time surface. Reads continue to
  work as a derived view of `aggressionMode` (`PROD → True`; `EXPEDITE`/`TURBO → False`, matching
  the server's `getIsProd()` facade). Writes emit a `DeprecationWarning` and mirror the
  server-side `OptimizationMode.fromIsProd(isProd, current)` rule: `isProd=True` always maps to
  `PROD`; `isProd=False` maps to `EXPEDITE` unless the resource is already in `TURBO`, in which
  case `TURBO` is preserved — preventing the silent downgrade a round-trip would otherwise
  cause.

### Changed

- **Breaking.** [`PaginationConfig`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/pagination.html#PaginationConfig)
  `num_pages` is now the number of pages fetched, counted from `start`, in every paged function.
  When `start` was above 1, `num_pages` used to work as the number of the last page to fetch (with
  at least one page fetched). For example, `start=3, num_pages=5` fetched pages 3 to 5, and now
  fetches pages 3 to 7. To fetch pages 3 to 5 now, pass `start=3, num_pages=3`. With no `start`, or
  `start=1`, nothing changes.
- **Breaking.** A [`PaginationConfig`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/pagination.html#PaginationConfig)
  `start` or `num_pages` below 1 now raises `ValueError` when you call a paged function. Pages are
  counted from 1 in every paged function, as before, and this is now documented on
  `PaginationConfig.start`. Previously, `start=0` failed with a server error in
  `workloads.get_all_kube_workloads` and `get_operation_compatibility`, but quietly returned the
  first page in `optimizations.get_recommendations` and `get_recommendations_v3`. For the first page,
  pass `start=1` or leave `start` out. `num_pages=0` used to fetch one page.
- **Breaking.** In a [`KubeAppOperation`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#KubeAppOperation)
  (from `get_operation`, or `Recommendation.operation` with `include_operation_details=True`), the
  container values in `original_config` and `proposed_config` (`memory_request`, `memory_limit`,
  `cpu_request` and `cpu_limit`) are now objects with `value` and `metricUnit`, as
  [`KubeContainerConfig`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#KubeContainerConfig)
  documents and as `get_resource_optimizations` returns them. They used to be dictionaries, so
  change `memory_request["value"]` to `memory_request.value`. The other dictionary keys, such as
  `humanReadableRepresentation`, are no longer included. A value is None when the container
  doesn't set it. It is also None when Sedai's data for a container lacks that value, which used
  to raise `KeyError`.
- `KubeAppSettings` / `ECSAppSettings` now parse the server's `optimizationMode.mode` field on
  the resource-setting DTO (shipped in server release 1.147 via
  [`V1_147_36__register_optimization_mode_settings_key.sql`](https://github.com/SedaiEngineering/sedai-core/blob/dev/core/src/main/resources/db/migration/V1_147_36__register_optimization_mode_settings_key.sql)).
  Falls back to `isProd.enabled` for older server builds that don't yet populate the field, and
  tolerates `"isProd": null` or `"optimizationMode": null` on the new server, where either key
  may be present-but-null when the resource has no mode set yet. Serialize writes both
  `optimizationMode.mode` (authoritative) and `isProd.enabled` (derived facade) only when the
  server actually sent the key OR the caller changed the value, so round-trips preserve TURBO
  without data loss and don't pin a mode onto resources whose server state has none set.
- `ECSAppSettings` rejects `AggressionMode.TURBO` on serialize with a `ValueError` only when the
  caller actively moves the mode to TURBO. TURBO is a Kube-only mode today — the server stores
  but does not act on TURBO for ECS, so the SDK fails fast on the client to make the gap
  visible, while leaving ECS resources whose server state is already TURBO updatable for every
  other field.
- Operations of the three types above (VM rightsizing, Azure disk type tuning and Google Cloud
  Storage Autoclass) are now returned as their new classes instead of a plain `Operation`. They are
  subclasses of `Operation`, so `isinstance(op, Operation)` still works, but code that checks the
  exact class (for example `type(op) is Operation`) will see the new classes.

### Fixed

- Reusing a [`PaginationConfig`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/pagination.html#PaginationConfig)
  no longer skips results. Paged functions used to move the `start` of the configuration you passed
  forward as they fetched pages. So a second call with the same configuration, or a call after
  breaking out of a loop early, started part-way through. This also affected calls with no
  configuration to `workloads.get_all_kube_workloads` and `get_operation_compatibility`, which share
  one default configuration. The configuration you pass is now never changed.
- `PageIterator` no longer crashes with an `AttributeError` when a page comes back empty, or when
  a page loader returns None for one. For example, `workloads.get_all_kube_workloads` on a cluster
  with no workloads now returns no results instead of raising. An empty page is skipped while more
  pages remain, and `has_next()` now fetches ahead when needed, so it is only True when `next()`
  has an element to return.
- [`get_opportunity_for_resource`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/optimizations.html#get_opportunity_for_resource)
  no longer crashes on resource types other than VMs and disks. It now returns an
  `OpportunityDetails` with cost and savings, and returns None for a type it does not recognise.
  Missing fields in opportunity results, such as CPU or memory values, are now None instead of
  raising.

# 1.3.21 - 2026-09-16

### Changed

- **Breaking.** The Kubernetes and ECS vertical scaling guardrails are now
  [value + unit objects](https://sedaiengineering.github.io/sedai-sdk-python/sedai/measurement.html)
  rather than bare numbers, matching the API. A guardrail now carries the unit it is expressed in, so
  it can be set in cores or millicores, CPU units or vCPUs, bytes or GiB.
  - `KubeAppSettings`: `verticalScaling_minPerContainerCpu`, `verticalScaling_maxPerContainerCpu`
    (`K8sCpuValue`), `verticalScaling_minPerContainerMemory`, `verticalScaling_maxPerContainerMemory`
    (`MemoryValue`) replace the `...InCores` / `...InBytes` fields. The old names stay as deprecated
    accessors that read and write in cores and bytes, so existing code keeps working.
  - `ECSAppSettings`: `verticalScaling_minCpu` is now an `ECSCpuValue` and `verticalScaling_minMemory`
    a `MemoryValue`, where both were previously bare numbers of CPU units and mebibytes. Code that
    *reads* either field has to be updated; the pre-existing units are available as
    `verticalScaling_minCpuInCpuUnits` and `verticalScaling_minMemoryInMiB`. Assigning a bare number
    still works and keeps its old meaning.
- **Breaking.** Account names are not unique in Sedai.
  [`account.delete_account`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/account.html#delete_account) and
  [`account.get_agent_installation_command`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/account.html#get_agent_installation_command)
  now raise if the name matches no account or more than one, listing the matching ids, where they
  previously returned `False`. Use the `_by_id` variants when a name may be ambiguous.

### Added

- [`sedai.measurement`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/measurement.html):
  `MetricUnit`, `K8sCpuValue`, `ECSCpuValue` and `MemoryValue`, with conversion between units.
- [`account.get_agent_installation_command_by_id`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/account.html#get_agent_installation_command_by_id):
  the agent installation command for a specific account id, such as the one returned by
  [`create_account`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/account.html#create_account).
- [`RDSSettings`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/settings.html#RDSSettings) for RDS instances and clusters, with instance-recommendation guardrails.
- [`KubeNodePoolSettings`](https://sedaiengineering.github.io/sedai-sdk-python/sedai/settings.html#KubeNodePoolSettings) for Kubernetes node pools, with node-count, disk, and instance-category/family recommendation guardrails.
- Kubernetes vertical-scaling guardrails: CPU/memory limit-modification and request/limit-ratio controls, plus VPA integration.
- Account instance-type allow/deny lists via `get`/`add`/`remove_whitelisted_instance_type(s)` and their `blacklisted` equivalents.

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
