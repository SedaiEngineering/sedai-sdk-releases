/**
 * Read-only: check in-progress optimization executions and resolve Sedai resource IDs back to
 * their cloud provider IDs. Neither function triggers any action — safe to run against any
 * environment at any time. Unlike bulk_execute_workflow.ts, this does not call
 * bulkExecuteWithCopilot() and carries no real-execution risk.
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P tsconfig.json execute/in_progress_and_cloud_ids.ts
 */

import { configure, getInProgressExecutions, getCloudProviderIds } from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

// Replace with resource IDs you already know, if you want to try the cloud-provider-ID lookup.
/** Fail immediately on a missing ID rather than sending a placeholder to the API, which
 *  returns an empty result set and looks indistinguishable from "no data". */
function requireEnv(name: string, hint: string): string {
  const value = process.env[name];
  if (!value) {
    console.error(`Missing ${name}.\n  ${hint}`);
    process.exit(1);
  }
  return value;
}

const KNOWN_SEDAI_RESOURCE_IDS = requireEnv(
  'SEDAI_RESOURCE_IDS',
  'Comma-separated sedaiResourceIds from: npx ts-node -P tsconfig.json optimizations/bulk_opportunities.ts',
).split(',').map(s => s.trim()).filter(Boolean);

async function main() {
  // --- Everything in progress right now, tenant-wide (no filter) ---
  // An empty resourceIds array is not "no results" — it means "no filter." This is the easiest
  // way to try the function: no need to already know a resource ID.
  console.log('\n--- Everything in progress right now (no filter) ---');
  let count = 0;
  for await (const exec of getInProgressExecutions([])) {
    // operationExecutionStatus (and operationUuid) are null for pre-execution rows — the
    // resource is queued, waiting for a maintenance window, or being validated, but hasn't
    // reached In Progress yet.
    console.log(`${exec.resourceId} | ${exec.operationExecutionStatus ?? '(pre-execution)'} | uuid: ${exec.operationUuid ?? '(none yet)'}`);
    count++;
    if (count >= 20) break; // sample only — this list can be large across a whole tenant
  }
  if (count === 0) console.log('(nothing in progress right now)');

  // --- Narrow with the optional filters ---
  console.log('\n--- Narrowed: KUBE resources, pre-execution states only ---');
  count = 0;
  for await (const exec of getInProgressExecutions([], {
    settingsTypes: ['KUBE'],
    states: ['IN_QUEUE', 'VALIDATING', 'WAITING'],
    pagination: { pageSize: 10 },
  })) {
    console.log(`${exec.resourceId} | ${exec.operationExecutionStatus ?? '(pre-execution)'}`);
    count++;
  }
  if (count === 0) console.log('(none matching that filter right now)');

  // --- Resolve known Sedai resource IDs back to their cloud provider IDs ---
  console.log('\n--- Resolving Sedai IDs to cloud provider IDs ---');
  const providerIds = await getCloudProviderIds(KNOWN_SEDAI_RESOURCE_IDS);

  // Unresolved IDs are echoed back mapped to themselves, not omitted — every input key is always
  // present, so `providerIds[id] ?? '(not found)'` can never fire. Compare value against key.
  for (const id of KNOWN_SEDAI_RESOURCE_IDS) {
    const resolved = providerIds[id];
    const unresolved = resolved === id;
    console.log(`${id} → ${unresolved ? '(not resolved — echoed back)' : resolved}`);
  }

  // Note: Kubernetes resources have no separate provider ID, so theirs legitimately equals the
  // Sedai resource ID. This test reports those as unresolved — exclude them if you have any.
  const unresolvedIds = KNOWN_SEDAI_RESOURCE_IDS.filter(id => providerIds[id] === id);
  if (unresolvedIds.length > 0) {
    console.log(`\n  ${unresolvedIds.length} of ${KNOWN_SEDAI_RESOURCE_IDS.length} did not resolve.`);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
