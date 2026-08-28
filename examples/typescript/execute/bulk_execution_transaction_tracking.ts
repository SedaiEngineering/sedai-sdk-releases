/**
 * Submit a bulk optimization request and track it to completion by transaction ID.
 *
 * Live-verified against test.sedai.cloud, released in v1.2.0. Not yet confirmed deployed to any
 * production tenant — check before running this against a real customer environment.
 *
 * The workflow this replaces: instead of tracking your submitted resource-ID list yourself and
 * polling getRecommendations() for each one (Approach B, see bulk_execute_workflow.ts),
 * submitBulkExecutionRequest() returns a single transaction ID — poll that one ID instead.
 *
 * Run:
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   SEDAI_RESOURCE_IDS='sedai-resource-id-1,sedai-resource-id-2' \
 *   npx ts-node -P examples/tsconfig.json examples/execute/bulk_execution_transaction_tracking.ts
 */

import {
  configure,
  submitBulkExecutionRequest,
  getExecutionStatus,
  getExecutionItems,
} from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

const SEDAI_RESOURCE_IDS = (process.env.SEDAI_RESOURCE_IDS ?? '')
  .split(',')
  .map(s => s.trim())
  .filter(Boolean);

const POLL_INTERVAL_MS = 5000;
const MAX_POLLS = 24; // 2 minutes

async function main() {
  if (SEDAI_RESOURCE_IDS.length === 0) {
    console.error('Set SEDAI_RESOURCE_IDS to a comma-separated list of Sedai resource IDs.');
    process.exit(1);
  }

  // --- Step 1: Submit the whole batch, get back one transaction ID ---
  console.log(`\nSubmitting ${SEDAI_RESOURCE_IDS.length} resource(s) via submitBulkExecutionRequest()...`);
  const submission = await submitBulkExecutionRequest({ resourceIds: SEDAI_RESOURCE_IDS });
  console.log(`  transactionId: ${submission.transactionId}`);
  console.log(`  submitted: ${submission.submitted}`);

  if (submission.transactionId === null) {
    console.log('\nNone of the submitted resources were recognized — nothing to poll.');
    return;
  }

  // --- Step 2: Poll the single transaction ID to completion ---
  // includeItemsWhenComplete asks for per-resource results back on the final poll, saving a
  // separate getExecutionItems() call for small batches (one page only — see step 3 for the rest).
  console.log('\nPolling for status (checking every 5s, timeout 2min)...');
  let finalStatus;
  for (let i = 0; i < MAX_POLLS; i++) {
    await new Promise(res => setTimeout(res, POLL_INTERVAL_MS));

    const status = await getExecutionStatus(submission.transactionId, { includeItemsWhenComplete: true });
    console.log(`  [poll ${i + 1}] complete: ${status.complete}, counts:`, status.counts);
    if (status.complete) {
      finalStatus = status;
      break;
    }
  }

  if (finalStatus?.items) {
    console.log('\nResults (inline from getExecutionStatus):');
    for (const item of finalStatus.items) {
      console.log(`  ${item.resourceId} (${item.cloudProviderId}): ${item.status}${item.reason ? ` (${item.reason})` : ''}`);
    }
    return;
  }

  // --- Step 3: List per-resource results, including rejected/duplicate ones ---
  console.log('\nResults:');
  for await (const item of getExecutionItems(submission.transactionId)) {
    console.log(`  ${item.resourceId}: ${item.status}${item.reason ? ` (${item.reason})` : ''}`);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
