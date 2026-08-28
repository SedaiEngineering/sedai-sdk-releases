# Sedai SDK Examples

Runnable examples for both SDKs. Install instructions for each are in the
[top-level README](../README.md).

- **Python** — the directories below, one per setup or workflow area.
- **TypeScript / JavaScript** — [`typescript/`](./typescript)

Every example documents its own required environment variables and its run command in a comment
block at the top of the file. Read that header before running anything.

---

## TypeScript / JavaScript

New to the SDK? Start with [`typescript/gsk_quickstart.ts`](./typescript/gsk_quickstart.ts) — it
covers the core integration flow end to end. Then run
[`typescript/accounts/discover_accounts.ts`](./typescript/accounts/discover_accounts.ts) to find the
account ID that most other examples need.

### Setup

The examples directory is a self-contained npm project — it declares the SDK and the TypeScript
toolchain itself, so one `npm install` is all you need:

```bash
git clone https://github.com/SedaiEngineering/sedai-sdk-releases.git
cd sedai-sdk-releases/examples/typescript
npm install

SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
  npx ts-node -P tsconfig.json gsk_quickstart.ts
```

**Run every example from this directory** — the paths in each file's header are relative to it.
A ready-to-use [`typescript/tsconfig.json`](./typescript/tsconfig.json) and
[`typescript/package.json`](./typescript/package.json) are included; `package.json` pins
`typescript@5`, because `ts-node` does not work with TypeScript 7.

### Start here

| Example | What it shows |
|---|---|
| [`gsk_quickstart.ts`](./typescript/gsk_quickstart.ts) | The core integration flow end to end |
| [`error_handling.ts`](./typescript/error_handling.ts) | What the SDK throws and what it retries for you — read before building anything that runs unattended |

### Accounts

| Example | What it shows |
|---|---|
| [`accounts/discover_accounts.ts`](./typescript/accounts/discover_accounts.ts) | `getAllAccounts()` / `searchAccountsByName()` — run this first to find your account ID |

### Optimizations

| Example | What it shows |
|---|---|
| [`optimizations/recommendations.ts`](./typescript/optimizations/recommendations.ts) | `getRecommendations()` / `getRecommendationsV3()` |
| [`optimizations/resource_optimizations.ts`](./typescript/optimizations/resource_optimizations.ts) | `getResourceOptimizations()` / `getRecommendedResourceState()` |
| [`optimizations/individual_resource_opportunity.ts`](./typescript/optimizations/individual_resource_opportunity.ts) | `getOpportunityForResource()` — a single resource |
| [`optimizations/bulk_opportunities.ts`](./typescript/optimizations/bulk_opportunities.ts) | `getOpportunitiesForResources()` — many resources in one call |

### Executing optimizations

> These examples trigger real actions against real resources. Read each file's header and
> understand what it will do before running it against anything but a test environment. The one
> exception is `in_progress_and_cloud_ids.ts`, which is read-only.

| Example | What it shows |
|---|---|
| [`execute/execute_opportunity.ts`](./typescript/execute/execute_opportunity.ts) | Execute one optimization and track its status — the core workflow |
| [`execute/bulk_execute_workflow.ts`](./typescript/execute/bulk_execute_workflow.ts) | Execute a batch and track it by polling each resource |
| [`execute/bulk_execution_transaction_tracking.ts`](./typescript/execute/bulk_execution_transaction_tracking.ts) | Execute a batch and track the whole thing by a single transaction ID — poll one ID instead of many. Accepts native Azure/AWS/GCP resource IDs directly, with no lookup step |
| [`execute/in_progress_and_cloud_ids.ts`](./typescript/execute/in_progress_and_cloud_ids.ts) | Read-only: list in-progress executions, map Sedai resource IDs to cloud provider IDs |

### Settings

| Example | What it shows |
|---|---|
| [`settings/group_settings.ts`](./typescript/settings/group_settings.ts) | `getGroupSettings()` / `updateGroupSettings()` |
| [`settings/resource_settings.ts`](./typescript/settings/resource_settings.ts) | `getResourceSettings()` / `updateResourceSettings()` |

**Full API reference:** https://sedaiengineering.github.io/sedai-sdk-typescript/

---

## Python

| Directory | What it covers |
|---|---|
| [`aws_account/`](./aws_account) | AWS account setup, CloudWatch, bulk account creation, connection tests |
| [`azure_setup/`](./azure_setup) | Azure accounts with a shared service principal |
| [`gcp_setup/`](./gcp_setup) | GCP accounts with a shared service-account JSON key |
| [`gke_setup/`](./gke_setup), [`gke_setup_multiple/`](./gke_setup_multiple) | GKE cluster and monitoring setup, single and CSV-driven bulk |
| [`self_managed_setup/`](./self_managed_setup) | Self-managed Kubernetes cluster setup |
| [`datadog_setup/`](./datadog_setup), [`newrelic_setup/`](./newrelic_setup), [`prometheus_setup/`](./prometheus_setup) | Monitoring provider setup, update, and removal |
| [`optimizations/`](./optimizations) | Recommendations, opportunities, operation compatibility, prohibited namespaces, resource tags, sync |
| [`settings/`](./settings) | Account, group, and resource settings, plus settings history |
| [`groups/`](./groups) | Group management and priorities |
| [`health/`](./health) | Smart Agent health |
| [`workloads/`](./workloads) | Kubernetes workloads |
| [`pagination/`](./pagination) | Iterating paginated results |

**Full API reference:** https://sedaiengineering.github.io/sedai-sdk-python/
