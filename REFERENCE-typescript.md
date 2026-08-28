<!-- Generated file — do not edit here.
     Extracted verbatim from README.md inside sedai-sdk-typescript-latest.tgz at release time.
     Edit the SDK's own README in the source repo instead; this copy is regenerated on each release.
     Regenerate: tar -xzOf sedai-sdk-typescript-latest.tgz package/README.md > REFERENCE-typescript.md -->

# Sedai SDK for JavaScript / TypeScript

Official JavaScript/TypeScript client for the Sedai platform API. Mirrors the [Python SDK](https://github.com/SedaiEngineering/sedai-sdk-python) method for method.

---

## Requirements

- Node.js ≥ 16

---

## Installation

```bash
npm install https://github.com/SedaiEngineering/sedai-sdk-releases/raw/main/sedai-sdk-typescript-latest.tgz
```

### Reinstalling after a new release

The install URL always serves the latest build, so npm may report "up to date" and silently keep
your existing copy. Force a real refetch:

```bash
rm -rf node_modules/sedai-sdk
npm cache clean --force
npm install https://github.com/SedaiEngineering/sedai-sdk-releases/raw/main/sedai-sdk-typescript-latest.tgz
```

Confirm you got what you expected with `cat node_modules/sedai-sdk/package.json | grep version`.

### Examples

Runnable examples live in the releases repo, under
[`examples/typescript`](https://github.com/SedaiEngineering/sedai-sdk-releases/tree/main/examples/typescript) —
accounts, optimizations, settings, and bulk execution. Each file documents its own environment
variables and run command at the top.

```bash
git clone https://github.com/SedaiEngineering/sedai-sdk-releases.git
cd sedai-sdk-releases/examples/typescript

SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
  npx ts-node gsk_quickstart.ts
```

---

## TypeScript Project Setup

The SDK ships with full type declarations. To use it in a TypeScript project, add the following to your `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "types": ["node"],
    "strict": true,
    "esModuleInterop": true,
    "outDir": "dist"
  }
}
```

You will also need `@types/node`:

```bash
npm install --save-dev @types/node typescript@5 ts-node
```

> **Pin `typescript@5`.** `ts-node` is not compatible with TypeScript 7 — installing `typescript`
> unpinned resolves to 7.x and every `ts-node` run fails with
> `TypeError: Cannot read properties of undefined (reading 'fileExists')` before your code executes.
> If you prefer to stay on current TypeScript, use [`tsx`](https://www.npmjs.com/package/tsx)
> (`npx tsx your-file.ts`) instead of `ts-node` — it works with 7.x.

To run a TypeScript file directly without compiling first:

```bash
npx ts-node your-file.ts
```

---

## Authentication

1. Log in to your Sedai instance (e.g. `https://your-org.sedai.app`)
2. Go to **Settings → API Keys → Create New Key**
3. Copy the generated token — you won't be able to see it again

**API key roles:** A **user-role** key is sufficient for all read operations (listing accounts, resources, recommendations, opportunities, etc.). An **admin-role** key is required for any write/update operations (e.g. `updateResourceSettings`, `updateGroupSettings`, `updateAccountSettings`). If a write call returns a `403`, the API key role is the most likely cause.

Use the token and your instance URL in `configure()`:

```typescript
import { configure } from 'sedai-sdk';

configure({
  baseUrl: 'https://your-org.sedai.app',
  apiToken: 'your-api-token',
});
```

---

## Getting Started

Call `configure()` once at startup before using any other SDK function:

```typescript
import { configure } from 'sedai-sdk';

configure({
  baseUrl: 'https://your-instance.sedai.io',
  apiToken: 'your-api-token',
});
```

**Options**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `baseUrl` | `string` | — | Base URL of your Sedai instance |
| `apiToken` | `string` | — | API token for authentication |
| `retries` | `number` | `3` | Max retries on 429 / 503 / 504 (exponential backoff) |

---

## Key Concepts

**`resourceId`** — Sedai's internal UUID for a cloud resource (e.g. `"res_abc123"`). It is different from your cloud provider's resource identifier (`providerResourceId`, e.g. an EC2 instance ID like `"i-0abc123"`). Use `getAllAccounts()` or `searchAccountsByName()` to discover account IDs, then use functions like `getRecommendations({ accountIds: [accountId] })` or `getResourceOptimizations({ accountId })` to iterate resources and find their `resourceId` values.

**`configure()` is a global singleton** — call it once at startup. All SDK functions share the same connection. If you need to connect to multiple Sedai environments in the same process, create separate Node.js processes.

---

## Typical Workflow

```
1. configure()                        — set baseUrl and apiToken
2. createAccount()                    — connect a cloud account
3. initializeGroupSettings(groupId)   — once per group, before reading settings
4. getGroupSettings() / updateGroupSettings() — configure autopilot, co-pilot, etc.
5. getRecommendations() / getOpportunitiesForResources() — read optimization results
```

## Exploring an Existing Environment

If you are connecting to an environment that already has accounts and resources set up, start here instead:

```typescript
import { configure, getAllAccounts, getRecommendations } from 'sedai-sdk';

configure({ baseUrl: 'https://your-org.sedai.app', apiToken: 'your-token' });

// 1. List accounts to find an account ID
const accounts = await getAllAccounts();
if (accounts.length === 0) {
  throw new Error('No cloud accounts are set up in this Sedai tenant yet.');
}
const accountId = accounts[0].id;
console.log('Using account:', accounts[0].name, accountId);

// 2. Pull recommendations for that account
for await (const rec of getRecommendations({ accountIds: [accountId] })) {
  console.log(rec.resourceId, rec.actionName);
}
```

---

## Pagination

List endpoints return a `PageIterator<T>`. Iterate with `for await`:

```typescript
import { getRecommendations } from 'sedai-sdk';

for await (const rec of getRecommendations({ accountIds: ['account-id'] })) {
  console.log(rec.resourceId, rec.actionName);
}
```

You can also pass `pageSize` and `start` to control pagination. **`start` is a 1-based page number, not a record offset** — to start at page 2, pass `start: 2` regardless of `pageSize`. The record it lands on is `(start - 1) * pageSize`.

```typescript
import { getRecommendations } from 'sedai-sdk';

for await (const rec of getRecommendations({ accountIds: ['account-id'], pagination: { pageSize: 50, start: 2 } })) {
  // starts at page 2 — record 50
}
```

> Passing a record offset here silently returns the wrong slice rather than erroring. With
> `pageSize: 50`, `start: 50` means *page 50* — record 2,450 — not record 50. `numPages` is
> likewise a count of pages, not records.

---

## Error Handling

All API errors throw `APIException`. Pre-condition violations (missing required fields, invalid enum values) throw `Error`.

```typescript
import { getAllAccounts, APIException } from 'sedai-sdk';

try {
  const accounts = await getAllAccounts();
} catch (e) {
  if (e instanceof APIException) {
    // HTTP-level failure (4xx / 5xx after retries exhausted)
  } else {
    // Invalid argument or SDK misconfiguration
    throw e;
  }
}
```

**Common HTTP errors:**

| Status | Meaning | Fix |
|---|---|---|
| `401` | Invalid or expired API token | Re-generate the token in Settings → API Keys |
| `403` | Valid token but insufficient role or missing feature flag | Write/update operations require an admin-role key. Some endpoints also require a feature flag per tenant (e.g. `getOpportunitiesForResources` requires `BULK_OPPORTUNITIES_API_ENABLED`). Contact Sedai support if neither applies. |
| `429` | Rate limited | The SDK retries automatically up to 3 times with exponential backoff |
| `503` / `504` | Transient server error | Also retried automatically |

---

## API Reference

### Accounts

```typescript
import {
  getAllAccounts,        // → Account[]
  getAllAccountsLite,    // → AccountLite[]
  searchAccountsByName, // (name: string) → AccountLite[]  — exact match, case-sensitive
  searchAccountsById,   // (id: string) → Account[]
  searchAccountsByProviderAccountId, // (providerId: string) → Account[]
  createAccount,        // (name, cloudProvider, credentials, integrationType, opts?) → string (accountId)
  updateAccount,        // (id, opts?) → string (accountId)
  deleteAccount,        // (name: string) → boolean
  deleteAccountById,    // (id: string) → boolean
  testConnection,       // (accountId: string) → boolean
  getAgentInstallationCommand, // (name: string) → AgentInstallationCommand | null
} from 'sedai-sdk';
```

**`Account` shape**

Cloud provider and integration details are nested under `accountDetails`, not at the top level:

```typescript
import { getAllAccounts } from 'sedai-sdk';

const accounts = await getAllAccounts();
for (const acc of accounts) {
  console.log(acc.id, acc.name, acc.accountDetails.cloudProvider, acc.accountDetails.integrationType);
  // acc.accountDetails also has: projectId (GCP), subscriptionId (Azure), tenantId (Azure)
}
```

> Note: `getAllAccountsLite()` returns `AccountLite[]`, which does have `cloudProvider` at the top level — but it is a lighter type with fewer fields.

**Integration types**

| Value | Meaning |
|---|---|
| `AGENT_BASED` | Sedai deploys a lightweight agent into your environment to collect metrics. Required for Kubernetes. |
| `AGENTLESS` | Sedai connects via cloud provider APIs only — no agent deployed. Works for AWS, Azure, GCP. |

**Create an account (AWS, role-based):**

```typescript
import { createAccount } from 'sedai-sdk';
import type { AwsRoleCredentials } from 'sedai-sdk';

const credentials: AwsRoleCredentials = {
  credentialsProvider: 'AWS_ENV_SUPPLIED',
  role: 'arn:aws:iam::123456789012:role/SedaiRole',
  externalId: 'optional-external-id', // recommended for cross-account roles
};

const accountId = await createAccount('my-aws-account', 'AWS', credentials, 'AGENTLESS');
```

**Create an account (AWS, static access key):**

```typescript
import { createAccount } from 'sedai-sdk';
import type { AwsKeyCredentials } from 'sedai-sdk';

const credentials: AwsKeyCredentials = {
  credentialsProvider: 'AWS_STATIC',
  accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
  secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
};

const accountId = await createAccount('my-aws-account', 'AWS', credentials, 'AGENTLESS');
```

**Create an account (Azure):**

```typescript
import { createAccount, updateAccount } from 'sedai-sdk';
import type { AzureClientCredentials } from 'sedai-sdk';

const credentials: AzureClientCredentials = {
  credentialsProvider: 'AZURE_CLIENT_CREDENTIALS',
  clientId: 'your-azure-client-id',
  clientSecret: 'your-azure-client-secret',
};

const accountId = await createAccount('my-azure-account', 'AZURE', credentials, 'AGENTLESS');

// subscriptionId and tenantId must be set in a follow-up updateAccount call:
await updateAccount(accountId, {
  subscriptionId: 'your-subscription-id',
  tenantId: 'your-tenant-id',
});
```

**Create an account (GCP):**

```typescript
import { createAccount } from 'sedai-sdk';
import type { GCPServiceAccountJsonCredentials } from 'sedai-sdk';
import { readFileSync } from 'fs';

const credentials: GCPServiceAccountJsonCredentials = {
  credentialsProvider: 'GCP_SERVICE_ACCOUNT_JSON',
  serviceAccountJson: readFileSync('service-account.json', 'utf8'),
};

const accountId = await createAccount(
  'my-gcp-project',
  'GCP',
  credentials,
  'AGENTLESS',
  { projectId: 'your-gcp-project-id' },
);
```

**Create a Kubernetes account (agent-based):**

```typescript
import { createAccount } from 'sedai-sdk';

const accountId = await createAccount(
  'my-k8s-cluster',
  'KUBERNETES',
  null,           // credentials injected automatically for AGENTLESS
  'AGENTLESS',
  { clusterProvider: 'AWS' },  // 'AWS' | 'AZURE' | 'GCP' | 'SELF_MANAGED'
);
```

---

### Groups

```typescript
import {
  getAllGroups,          // → GroupDefinition[]
  searchGroupsByName,   // (name: string) → GroupSummary[]
  searchGroupsById,     // (id: string) → GroupSummary[]
  getGroup,             // (name: string) → GroupDefinition | null
  getGroupById,         // (id: string) → GroupDefinition | null
  createGroup,          // (name, cloudProvider, accountId, opts?) → string (groupId)
  updateGroup,          // (id, opts?) → string (groupId)
  updateGroupPriorities, // (groupId, priorities) → GroupPriorityUpdateStatus
  deleteGroup,          // (name: string) → boolean
  enableOrDisableGroup, // (id, enabled: boolean) → boolean
  initializeGroupSettings, // (groupId) → boolean  — call once before getGroupSettings
} from 'sedai-sdk';
```

> **Note:** `getGroupSettings` throws if settings have never been initialized for that group. Call `initializeGroupSettings(groupId)` once after creating a group before reading or updating its settings.

---

### Monitoring Providers

```typescript
import {
  getMonitoringProvidersForAccount, // (accountId) → MonitoringProvider[]
  getMonitoringProvider,            // (id) → MonitoringProvider | null
  addCloudwatchMonitoring,          // (accountId, opts?) → boolean
  addNewRelicMonitoring,            // (accountId, newRelicAccountId, apiServer, credentials, opts?) → boolean
  addOrUpdateGkeMonitoring,         // (accountId, projectId, credentials, opts?) → boolean
  addGkeMonitoring,                 // (accountId, projectId, credentials, opts?) → boolean
  addDatadogMonitoring,             // (accountId, credentials, opts?) → boolean
  addOrUpdateDatadogMonitoring,     // (accountId, credentials, opts?) → boolean
  addFederatedPrometheusMonitoring, // (accountId, credentials, endpoint, opts?) → boolean
  deleteMonitoringProvider,         // (id) → boolean
} from 'sedai-sdk';
```

**Add Cloudwatch monitoring (AWS):**

```typescript
import { addCloudwatchMonitoring } from 'sedai-sdk';

await addCloudwatchMonitoring('account-id');
```

**Add Datadog monitoring:**

```typescript
import { addDatadogMonitoring } from 'sedai-sdk';
import type { DatadogCredentials } from 'sedai-sdk';

const credentials: DatadogCredentials = {
  credentialsProvider: 'DATADOG',
  apiKey: 'your-datadog-api-key',
  applicationKey: 'your-datadog-app-key',
};

await addDatadogMonitoring('account-id', credentials);
```

---

### Workloads

```typescript
import { getAllKubeWorkloads } from 'sedai-sdk';

for await (const workload of getAllKubeWorkloads('account-id')) {
  console.log(workload.name, workload.namespace);
}
```

---

### Optimizations

#### Recommendations

```typescript
import { getRecommendations, getRecommendationsV3 } from 'sedai-sdk';

// All recommendations for an account
for await (const rec of getRecommendations({ accountIds: ['account-id'] })) {
  console.log(rec.resourceId, rec.actionName);
}

// V3 with pagination
for await (const rec of getRecommendationsV3({ accountIds: ['account-id'], pagination: { pageSize: 100 } })) {
  console.log(rec.resourceId, rec.actionName);
}
```

**Filters** — both `getRecommendations` and `getRecommendationsV3` accept the same options:

```typescript
import { getRecommendationsV3 } from 'sedai-sdk';

for await (const rec of getRecommendationsV3({
  accountIds: ['account-id'],
  resourceId: 'sedai-resource-id',               // filter to a specific resource
  startTime: new Date('2024-01-01'),              // date range
  endTime: new Date('2024-12-31'),
  recommendationTypes: ['EFFICIENCY'],             // 'AVAILABILITY' | 'EFFICIENCY'
  recommendationStatus: ['PROPOSED', 'EXECUTING'], // see status table below
  includeOperationDetails: true,                   // populate rec.operation
  actionName: 'RIGHT_SIZE_INSTANCE',               // filter by action name
  pagination: { pageSize: 100 },
})) {
  console.log(rec.actionName, rec.status);
  if (rec.operation) {
    console.log(rec.operation.type, rec.operation.action);
  }
}
```

**`recommendationStatus` values:**

| Value | Meaning |
|---|---|
| `PROPOSED` | Sedai has a pending recommendation |
| `EXECUTING` | An action is currently being applied |
| `SUCCESSFUL` | Action completed successfully |
| `FAILED` | Action failed |
| `EXPIRED` | Recommendation was not acted on and has expired |
| `USER_REJECTED` | A human dismissed the recommendation |
| `PAUSED` | Execution is paused |
| `UNSAFE_TO_ACT` | Sedai determined it was not safe to act |

#### Individual Resource Opportunities

Bulk-fetch optimization opportunities for a specific list of resources:

> **Feature flag required:** This endpoint is off by default for all tenants. If you receive a 403 `APIException`, contact Sedai support to enable the `BULK_OPPORTUNITIES_API_ENABLED` flag for your account.

```typescript
import { getOpportunitiesForResources } from 'sedai-sdk';

// Pass cloud provider IDs in your cloud's native path format — no SDK lookup needed.
// Azure: '/subscriptions/{subId}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name}'
// AWS:   'i-0abc1234567890def'  (EC2) or 'vol-0abc1234567890def'  (EBS)
const resourceIds = [
  '/subscriptions/abb3c293-f595-4468-843d-82f49d0cd956/resourceGroups/MY-RG/providers/Microsoft.Compute/virtualMachines/my-vm',
];

for await (const opp of getOpportunitiesForResources(resourceIds)) {
  console.log(opp.sedaiResourceId, opp.opportunityStatus, opp.monthlyCostImpact);
}
```

**Options** — filter by account, group, pilot mode, or request cloud provider tags:

```typescript
import { getOpportunitiesForResources } from 'sedai-sdk';

for await (const opp of getOpportunitiesForResources([], {
  accountIds: ['account-id'],           // filter to specific accounts
  groupIds: ['group-id'],               // filter to specific groups
  configModes: ['AUTO', 'DATA_PILOT'],  // only return resources in these pilot modes
  includeTags: true,                    // include cloud provider tags per row
  pagination: { pageSize: 50 },
})) {
  console.log(opp.sedaiResourceId, opp.configMode, opp.monthlyCostImpact);
}
```

Each row includes a `configMode` field (`'AUTO' | 'DATA_PILOT' | 'CO_PILOT'`) indicating the resource's current pilot mode. When `includeTags: true`, each row also includes a `tags` array of `{ key, value }` pairs from your cloud provider:

```typescript
import { getOpportunitiesForResources, OpportunityTag } from 'sedai-sdk';

for await (const opp of getOpportunitiesForResources(['i-0abc123'], { includeTags: true })) {
  console.log('mode:', opp.configMode);
  const tags: OpportunityTag[] = opp.tags ?? [];
  for (const tag of tags) {
    console.log(tag.key, '=', tag.value);  // e.g. 'env' = 'prod'
  }
}
```

**Resource types** — each row has a `resourceType` field. VM rows include instance type and pricing; volume rows include disk config; base rows carry cost/savings fields only:

```typescript
import { getOpportunitiesForResources, VMOpportunityDetails, VolumeOpportunityDetails } from 'sedai-sdk';

for await (const opp of getOpportunitiesForResources(['i-0abc123', 'vol-0abc123'])) {
  if (opp.resourceType === 'vm') {
    const vm = opp as VMOpportunityDetails;
    console.log(vm.currentInstanceType, '→', vm.recommendedInstanceType);
  } else if (opp.resourceType === 'volume') {
    const disk = opp as VolumeOpportunityDetails;
    console.log(disk.currentConfig, '→', disk.recommendedConfig);
  } else {
    // resourceType === 'base' — cost/savings fields only
    console.log('savings:', opp.monthlyCostImpact);
  }
}
```

#### Single Resource Opportunity

Fetch the opportunity for a single resource without going through the bulk endpoint:

```typescript
import { getOpportunityForResource } from 'sedai-sdk';

// Returns null if the resource has no opportunity or is not found.
const opp = await getOpportunityForResource('i-0abc123');
if (opp) {
  console.log(opp.resourceType, opp.opportunityStatus, opp.monthlyCostImpact);
}
```

#### Cluster Opportunities (Kubernetes)

```typescript
import { getClusterOpportunities } from 'sedai-sdk';

// Returns a single ClusterOpportunity or null — not a list.
const opportunity = await getClusterOpportunities('cluster-id', {
  includeWorkloadOptimization: true,
});

if (opportunity) {
  const savings = opportunity.nodeCostProjectionSummary?.predictedAverageMonthlySavings;
  console.log(opportunity.resourceName, savings);
  for (const workload of opportunity.workloadOptimizations) {
    console.log(workload.resourceId);
  }
}
```

#### Co-pilot Execution

When a resource is in `CO_PILOT` mode and has a pending recommendation, you can execute it programmatically.

**All resource types (disk, storage, VM, etc.)** — use `executeWithCopilot()`:

```typescript
import { executeWithCopilot } from 'sedai-sdk';

const success = await executeWithCopilot('sedai-resource-id');
```

**VM only — approve or reject** — use `approveExecution()` / `rejectExecution()`:

```typescript
import { approveExecution, rejectExecution } from 'sedai-sdk';

// Approve — triggers the recommended change (e.g. resize)
const approved = await approveExecution('sedai-resource-id');

// Reject — dismisses the pending recommendation
const rejected = await rejectExecution('sedai-resource-id');
```

> The `resourceId` is the Sedai internal ID — use the `resourceId` field from `getResourceOptimizations()` or `getOpportunitiesForResources()`.
>
> `executeWithCopilot()` wraps `POST /api/execute-with-copilot/resource` and works for all resource types. `approveExecution()`/`rejectExecution()` are VM-only and additionally support rejection via `/api/virtualMachines/optimization/manualexecution/approve`.

#### Bulk Execution & Status Tracking

Submit a list of resources for optimization in a single call, then track them to completion.

**Submit a batch** — `bulkExecuteWithCopilot()`:

```typescript
import { bulkExecuteWithCopilot } from 'sedai-sdk';

// Pass the Sedai resource IDs from getOpportunitiesForResources().
const accepted = await bulkExecuteWithCopilot([
  'sedai-resource-id-1',
  'sedai-resource-id-2',
]);
```

**Track a batch to completion.** Because submission is asynchronous, there is no batch-level tracking ID — you track by the same resource IDs you submitted. Record the submission time, then poll `getRecommendations()` filtered to those resource IDs and that start time. Each recommendation carries a `status` reaching a terminal value (`SUCCESSFUL`, `FAILED`, `USER_REJECTED`, `UNSAFE_TO_ACT`, or `EXPIRED`):

```typescript
import { bulkExecuteWithCopilot, getRecommendations } from 'sedai-sdk';

const resourceIds = ['sedai-resource-id-1', 'sedai-resource-id-2'];
const submittedAt = new Date();

await bulkExecuteWithCopilot(resourceIds);

// Poll for status — one paginated call covers the whole batch.
const TERMINAL = new Set(['SUCCESSFUL', 'FAILED', 'USER_REJECTED', 'UNSAFE_TO_ACT', 'EXPIRED']);
const status = new Map<string, string | null>();
for await (const rec of getRecommendations({ resourceIds, startTime: submittedAt })) {
  status.set(rec.resourceId, rec.status);
}
```

**In-progress executions** — `getInProgressExecutions()` surfaces resources whose optimization is currently underway, along with each one's `operationUuid`. Rows still in a pre-execution state (queued, waiting for a maintenance window, validating) have `operationUuid: null` and `operationExecutionStatus: null` — it's only populated once the resource reaches In Progress:

```typescript
import { getInProgressExecutions } from 'sedai-sdk';

for await (const exec of getInProgressExecutions(['sedai-resource-id-1', 'sedai-resource-id-2'])) {
  console.log(exec.resourceId, exec.operationUuid, exec.operationExecutionStatus);
}
```

Pass an empty array to see everything currently in progress across your whole tenant — an empty `resourceIds` list means "no filter," not "no results":

```typescript
import { getInProgressExecutions } from 'sedai-sdk';

for await (const exec of getInProgressExecutions([])) {
  console.log(exec.resourceId, exec.operationExecutionStatus);
}
```

Narrow the search with additional optional filters:

```typescript
import { getInProgressExecutions } from 'sedai-sdk';

for await (const exec of getInProgressExecutions([], {
  accountIds: ['account-id'],
  groupIds: ['group-id'],
  settingsTypes: ['KUBE', 'VOLUME'],     // resource kind
  stateTypes: ['OPTIMIZATION'],          // optimization state category
  states: ['IN_QUEUE', 'VALIDATING'],    // pre-execution state
  search: 'my-resource-name',
})) {
  console.log(exec.resourceId, exec.operationExecutionStatus);
}
```

**Resolve Sedai IDs back to cloud provider IDs** — `getCloudProviderIds()` returns a map keyed by Sedai resource ID:

```typescript
import { getCloudProviderIds } from 'sedai-sdk';

const map = await getCloudProviderIds(['sedai-resource-id-1', 'sedai-resource-id-2']);
console.log(map['sedai-resource-id-1']); // e.g. "/subscriptions/.../virtualMachines/vm-web-01"
```

#### Transaction-Level Bulk Execution Tracking

> ⚠️ **Available in the test environment only, not yet in production.** This SDK has live-verified
> `submitBulkExecutionRequest()`, `getExecutionStatus()`, and `getExecutionItems()` end-to-end
> against the test environment, but the branch has not merged/shipped yet. Use
> `bulkExecuteWithCopilot()` + `getRecommendations()` above in the meantime, which is fully live
> today in production.

`submitBulkExecutionRequest()` submits a batch by Sedai resource ID, cloud provider ID, or both,
and returns a single transaction ID — poll that one ID instead of tracking your original
resource-ID list yourself:

```typescript
import { submitBulkExecutionRequest } from 'sedai-sdk';

const submission = await submitBulkExecutionRequest({
  resourceIds: ['sedai-resource-id-1', 'sedai-resource-id-2'],
});
console.log(submission.transactionId, submission.submitted);
```

If none of the submitted resources are recognized, `submitted` is `0` and `transactionId` is
`null` — there's nothing to poll. Check for `null` before passing it to `getExecutionStatus()` or
`getExecutionItems()`.

**Poll status** — `getExecutionStatus()` returns per-status counts for the whole transaction, and
a `complete` flag that's `true` once every resource has reached a terminal status:

```typescript
import { getExecutionStatus } from 'sedai-sdk';

const transactionId = 'transaction-id-from-submitBulkExecutionRequest';
const status = await getExecutionStatus(transactionId);
console.log(status.complete, status.counts);
```

Pass `includeItemsWhenComplete: true` to get one page of per-resource results back inline once the
transaction finishes, instead of a separate `getExecutionItems()` call:

```typescript
import { getExecutionStatus } from 'sedai-sdk';

const transactionId = 'transaction-id-from-submitBulkExecutionRequest';
const status = await getExecutionStatus(transactionId, { includeItemsWhenComplete: true });
if (status.complete) {
  console.log(status.items); // present only when includeItemsWhenComplete was requested and complete is true
}
```

**List per-resource results** — `getExecutionItems()` returns every submitted resource, including
rejected/duplicate ones, with standard `PageIterator` pagination:

```typescript
import { getExecutionItems } from 'sedai-sdk';

const transactionId = 'transaction-id-from-submitBulkExecutionRequest';
for await (const item of getExecutionItems(transactionId)) {
  console.log(item.resourceId, item.cloudProviderId, item.status, item.reason);
}
```

Every item also carries `cloudProviderId` — the native cloud identifier (an Azure resource path,
an AWS ARN, etc.) alongside the Sedai `resourceId`. For Kubernetes resources it's identical to
`resourceId`, since there's no separate provider-ID concept there.

#### Operations

```typescript
import { getOperation, getOperationCompatibility } from 'sedai-sdk';

// Get a specific operation by its ID
const op = await getOperation('operation-id');

// Check operation compatibility — default returns non-compatible rows (isCompatible: false)
for await (const row of getOperationCompatibility()) {
  console.log(row.resourceId, row.isCompatible);
}

// Include blocker details — blockers is only populated when includeFactors: true
for await (const row of getOperationCompatibility({ includeFactors: true })) {
  console.log(row.resourceId, row.isCompatible, row.blockers);
}

// Filter to only compatible rows, limit page size
for await (const row of getOperationCompatibility({ isCompatible: true, pagination: { pageSize: 50 } })) {
  console.log(row.resourceId);
}
```

#### Resource Optimizations

```typescript
import { getResourceOptimizations } from 'sedai-sdk';

for await (const opt of getResourceOptimizations({ accountId: 'account-id' })) {
  console.log(opt.resourceId, opt.preHourlyCost, opt.postHourlyCost, opt.costChangePerHour);
}
```

All options:

```typescript
import { getResourceOptimizations } from 'sedai-sdk';

for await (const opt of getResourceOptimizations({
  accountId: 'account-id',
  resourceId: 'sedai-resource-id',    // filter to a specific resource
  startTime: new Date('2024-01-01'),  // date range
  endTime: new Date('2024-12-31'),
  sortBy: 'optimization_time',        // 'optimization_time' | 'cpu_change_core' | 'cpu_change_vcpu' | 'memory_change_mib' | 'storage_change_gib'
  sortDir: 'desc',
  pagination: { pageSize: 50 },
})) {
  console.log(opt.resourceId, opt.costChangePerHour);
}
```

**Recommended resource state** — get the configuration Sedai would propose to apply to a resource:

```typescript
import { getRecommendedResourceState } from 'sedai-sdk';

// Returns null if no proposed state is available for this resource.
const state = await getRecommendedResourceState('sedai-resource-id');
if (state) {
  console.log(state);
}
```

#### Prohibited Namespaces

```typescript
import {
  getProhibitedNamespaces,
  addProhibitedNamespaces,
  deleteProhibitedNamespaces,
} from 'sedai-sdk';

const namespaces = await getProhibitedNamespaces();
await addProhibitedNamespaces(['kube-system', 'monitoring']);
await deleteProhibitedNamespaces(['monitoring']);
```

---

### Settings

```typescript
import {
  getResourceSettings,
  updateResourceSettings,
  getGroupSettings,
  updateGroupSettings,
  initializeGroupSettings,
  enableGroupForSettings,
  disableGroupForSettings,
  getAccountSettings,
  updateAccountSettings,
  disableAccountMonitoring,
  disableGroupMonitoring,
  disableResourceMonitoring,
} from 'sedai-sdk';

// Always get-then-modify to avoid clobbering existing settings.
const settings = await getResourceSettings('resource-id');
settings.optimization = {
  ...settings.optimization,
  setting: { configMode: 'AUTO' },
};
await updateResourceSettings('resource-id', settings);
```

**`configMode` values:**

| Value | Meaning |
|---|---|
| `AUTO` | Sedai applies optimizations automatically (autopilot) |
| `CO_PILOT` | Sedai proposes changes; a human approves each one |
| `DATA_PILOT` | Sedai monitors and reports only — no changes applied |
| `MANUAL` | **Deprecated** — use `CO_PILOT` instead |
| `OFF` | **Deprecated** — use `DATA_PILOT` instead |

---

### Settings History

```typescript
import {
  getResourceSettingsHistory,
  getGroupSettingsHistory,
  getAccountSettingsHistory,
} from 'sedai-sdk';

// These return a plain array, not a PageIterator — use await, not for await
const events = await getResourceSettingsHistory('resource-id');
for (const event of events) {
  console.log(event.updatedTime, event.eventType, event.updatedUser);
}
```

---

### User Profile

```typescript
import { getProfile } from 'sedai-sdk';

const profile = await getProfile();
console.log(profile.displayName, profile.email);
```

---

### Health

> **Note:** `getHealthInfo()` is **global** — it returns health data for all agents across all accounts, not filtered to a single account. There is no per-account variant.

```typescript
import { getHealthInfo, getAgentMessageStats } from 'sedai-sdk';

// Returns SmartAgentHealth[] — one entry per agent/account
const agents = await getHealthInfo();
for (const agent of agents) {
  console.log(agent.accountName, agent.isHealthy, agent.version);
}

// Per-account message stats — duration is required (ISO 8601, e.g. 'PT8H' = last 8 hours)
const stats = await getAgentMessageStats('account-id', 'PT8H');
```

---

### Resource Tags

```typescript
import { getResourceTags } from 'sedai-sdk';

const tags = await getResourceTags('resource-id');
if (tags) {
  for (const tag of tags) {
    console.log(tag.key, tag.value);
  }
}
```

---

## TypeScript

The SDK is written in TypeScript and ships with full type declarations. No `@types/` package needed.

```typescript
import type {
  Account,
  AccountLite,
  Recommendation,
  RecommendationType,
  GetRecommendationsOptions,
  ClusterOpportunity,
  SedaiCredentials,
  AwsRoleCredentials,
  VMOpportunityDetails,
  VolumeOpportunityDetails,
  OpportunityDetails,
  OpportunityTag,
  ResourceConfigMode,
  GetOpportunitiesOptions,
  ResourceOptimization,
  KubeResourceOptimization,
  AnyOperation,
  PageIterator,
} from 'sedai-sdk';
```

---

## License

UNLICENSED — proprietary. All rights reserved by Sedai.
