/**
 * Bulk execute a set of optimizations and track the batch to completion
 *
 * The full GSK workflow:
 *   1. Pull opportunities in bulk by Azure resource ID (getOpportunitiesForResources)
 *   2. Submit the whole selected batch for optimization (bulkExecuteWithCopilot)
 *   3. Track the batch to completion by polling getRecommendations() filtered to
 *      the submitted resource IDs and the submission time (Approach B — no batch
 *      tracking ID; you track by resource ID + start time)
 *   4. Report against the original Azure resource IDs — already captured in Step 1
 *      via providerResourceId, no separate lookup needed for resources discovered
 *      this way (see getCloudProviderIds() below for resolving IDs from elsewhere)
 *
 * ⚠️  WARNING: This example triggers real optimizations. Only run it against a
 * safe test environment. Never point SEDAI_BASE_URL at production unless you
 * intend to execute the changes.
 *
 * Run:
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   PROVIDER_RESOURCE_IDS='/subscriptions/.../virtualMachines/vm-1,/subscriptions/.../virtualMachines/vm-2' \
 *   npx ts-node -P examples/tsconfig.json examples/execute/bulk_execute_workflow.ts
 */

import {
  configure,
  getOpportunitiesForResources,
  bulkExecuteWithCopilot,
  getInProgressExecutions,
  getRecommendations,
  getCloudProviderIds,
} from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

const PROVIDER_RESOURCE_IDS = (process.env.PROVIDER_RESOURCE_IDS ?? '')
  .split(',')
  .map(s => s.trim())
  .filter(Boolean);

const TERMINAL = new Set(['SUCCESSFUL', 'FAILED', 'USER_REJECTED', 'UNSAFE_TO_ACT', 'EXPIRED']);
const POLL_INTERVAL_MS = 5000;
const MAX_POLLS = 24; // 2 minutes

async function main() {
  if (PROVIDER_RESOURCE_IDS.length === 0) {
    console.error('Set PROVIDER_RESOURCE_IDS to a comma-separated list of Azure resource IDs.');
    process.exit(1);
  }

  // --- Step 1: Pull opportunities in bulk, by Azure resource ID ---
  console.log(`\nFetching opportunities for ${PROVIDER_RESOURCE_IDS.length} resource(s)...`);
  const resourceIds: string[] = [];
  const providerIdByResourceId = new Map<string, string>();
  for await (const opp of getOpportunitiesForResources(PROVIDER_RESOURCE_IDS)) {
    if (opp.opportunityStatus === 'OPPORTUNITY_AVAILABLE') {
      resourceIds.push(opp.sedaiResourceId);
      // providerResourceId comes back directly alongside sedaiResourceId — capture it now so
      // Step 4 doesn't need a separate getCloudProviderIds() round-trip for these resources.
      if (opp.providerResourceId) providerIdByResourceId.set(opp.sedaiResourceId, opp.providerResourceId);
    }
  }
  console.log(`  ${resourceIds.length} resource(s) have an available opportunity.`);
  if (resourceIds.length === 0) return;

  // --- Step 2: Submit the whole batch ---
  console.log('\nSubmitting batch via bulkExecuteWithCopilot()...');
  const submittedAt = new Date();
  const accepted = await bulkExecuteWithCopilot(resourceIds);
  console.log(`  Accepted: ${accepted}`);

  // --- Step 3: Track to completion (Approach B) ---
  console.log('\nPolling for status (checking every 5s, timeout 2min)...');
  const status = new Map<string, string | null>();
  for (let i = 0; i < MAX_POLLS; i++) {
    await new Promise(res => setTimeout(res, POLL_INTERVAL_MS));

    // Optional: see what is actively in progress right now. Narrow a large batch with the
    // newer filters if needed — e.g. { states: ['IN_PROGRESS'] } to skip queued/validating rows,
    // or { accountIds: [...] } / { search: '...' } to scope by account or name.
    for await (const exec of getInProgressExecutions(resourceIds)) {
      console.log(`  [in-progress] ${exec.resourceId} — ${exec.operationExecutionStatus ?? '(pre-execution)'}`);
    }

    // Status of operations performed after we submitted, in one paginated call.
    for await (const rec of getRecommendations({ resourceIds, startTime: submittedAt })) {
      status.set(rec.resourceId, rec.status);
    }

    const done = [...status.values()].filter(s => s !== null && TERMINAL.has(s)).length;
    console.log(`  [poll ${i + 1}] ${done}/${resourceIds.length} reached a terminal status.`);
    if (done === resourceIds.length) break;
  }

  // --- Step 4: Report against the original Azure resource IDs ---
  // Most IDs are already known from Step 1. getCloudProviderIds() is still useful standalone —
  // e.g. for resource IDs discovered some other way (getResourceOptimizations(), a list saved
  // from a previous run) rather than via getOpportunitiesForResources() — kept here as a
  // fallback for anything Step 1 didn't already resolve.
  const missingIds = resourceIds.filter(id => !providerIdByResourceId.has(id));
  if (missingIds.length > 0) {
    const resolved = await getCloudProviderIds(missingIds);
    for (const [id, providerId] of Object.entries(resolved)) providerIdByResourceId.set(id, providerId);
  }

  console.log('\nResults:');
  for (const id of resourceIds) {
    console.log(`  ${providerIdByResourceId.get(id) ?? id}: ${status.get(id) ?? 'unknown'}`);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
