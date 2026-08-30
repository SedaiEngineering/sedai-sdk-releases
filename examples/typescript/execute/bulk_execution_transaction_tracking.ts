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
 * ── Submitting cloud provider IDs ──────────────────────────────────────────────────────────
 * If you hold Azure/AWS/GCP native resource IDs rather than Sedai's internal IDs, pass them as
 * `cloudProviderIds` — there is no lookup step to do first. Set SEDAI_PROVIDER_RESOURCE_IDS
 * instead of SEDAI_RESOURCE_IDS below. Every result row carries both IDs back, so you can report
 * outcomes against the same identifiers you submitted.
 *
 * ── How long this takes ────────────────────────────────────────────────────────────────────
 * Real executions are slow, and how slow depends on the resource type (figures from the backend
 * team, 2026-08-29):
 *
 *   VMs and disks   ~20 minutes. An observed Azure disk took ~25 to go
 *                   IN_QUEUE → WAITING → IN_PROGRESS → VALIDATING → SUCCEEDED.
 *   Kubernetes      up to 8 hours to profile.
 *
 * A resource whose metrics are missing is a third case: it stays IN_QUEUE indefinitely and is
 * never picked up until metrics arrive. Polling it will never terminate, so treat a timeout as
 * "unknown", not "failed" — see POLL_TIMEOUT_MS below.
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   SEDAI_RESOURCE_IDS='sedai-resource-id-1,sedai-resource-id-2' \
 *   npx ts-node -P tsconfig.json execute/bulk_execution_transaction_tracking.ts
 *
 * Or with native cloud provider IDs:
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   SEDAI_PROVIDER_RESOURCE_IDS='/subscriptions/.../virtualMachines/vm-1,i-0abc1234567890def' \
 *   npx ts-node -P tsconfig.json execute/bulk_execution_transaction_tracking.ts
 */

import {
  configure,
  submitBulkExecutionRequest,
  getExecutionStatus,
  getExecutionItems,
  APIException,
} from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

const splitIds = (raw: string | undefined): string[] =>
  (raw ?? '').split(',').map(s => s.trim()).filter(Boolean);

// Sedai internal resource IDs (sedaiResourceId from getOpportunitiesForResources).
const SEDAI_RESOURCE_IDS = splitIds(process.env.SEDAI_RESOURCE_IDS);

// Native cloud provider IDs — Azure resource paths, AWS instance/volume IDs, GCP names.
// Submit these directly; no translation to Sedai IDs is needed.
const SEDAI_PROVIDER_RESOURCE_IDS = splitIds(process.env.SEDAI_PROVIDER_RESOURCE_IDS);

// Timings below are from Rajat (backend), 2026-08-29.
//
//   30s interval — 15s is too aggressive; the status query is expensive on a large tenant.
//   VMs and disks    finish in roughly 20 minutes.
//   Kubernetes       can take up to 8 HOURS to profile.
//   Missing metrics  a resource whose metrics are unavailable stays IN_QUEUE indefinitely — it is
//                    never picked up until metrics arrive, so polling it will never terminate.
//
// The default timeout covers VMs and disks with margin. For Kubernetes, raise it:
//   SEDAI_POLL_TIMEOUT_MIN=480
const POLL_INTERVAL_MS = 30_000;
const POLL_TIMEOUT_MS = Number(process.env.SEDAI_POLL_TIMEOUT_MIN ?? 45) * 60 * 1000;

async function main() {
  if (SEDAI_RESOURCE_IDS.length === 0 && SEDAI_PROVIDER_RESOURCE_IDS.length === 0) {
    console.error(
      'Set SEDAI_RESOURCE_IDS (Sedai internal IDs) or SEDAI_PROVIDER_RESOURCE_IDS ' +
      '(Azure/AWS/GCP native IDs) to a comma-separated list.',
    );
    process.exit(1);
  }

  // --- Step 1: Submit the whole batch, get back one transaction ID ---
  // Both fields may be supplied together; the two lists are combined into one transaction.
  const total = SEDAI_RESOURCE_IDS.length + SEDAI_PROVIDER_RESOURCE_IDS.length;
  console.log(`\nSubmitting ${total} resource(s) via submitBulkExecutionRequest()...`);

  const submission = await submitBulkExecutionRequest({
    ...(SEDAI_RESOURCE_IDS.length > 0 && { resourceIds: SEDAI_RESOURCE_IDS }),
    ...(SEDAI_PROVIDER_RESOURCE_IDS.length > 0 && { cloudProviderIds: SEDAI_PROVIDER_RESOURCE_IDS }),
  });

  console.log(`  transactionId: ${submission.transactionId}`);
  console.log(`  submitted: ${submission.submitted}`);

  if (submission.transactionId === null) {
    console.log('\nNone of the submitted resources were recognized — nothing to poll.');
    return;
  }

  // --- Step 2: Poll the single transaction ID to completion ---
  // includeItemsWhenComplete asks for per-resource results back on the final poll, saving a
  // separate getExecutionItems() call for small batches (one page only — see step 3 for the rest).
  const deadline = Date.now() + POLL_TIMEOUT_MS;
  console.log(
    `\nPolling for status (every ${POLL_INTERVAL_MS / 1000}s, ` +
    `giving up after ${POLL_TIMEOUT_MS / 60000} minutes)...`,
  );

  let finalStatus;
  let poll = 0;
  while (Date.now() < deadline) {
    await new Promise(res => setTimeout(res, POLL_INTERVAL_MS));
    poll++;

    const status = await getExecutionStatus(submission.transactionId, { includeItemsWhenComplete: true });
    console.log(`  [poll ${poll}] complete: ${status.complete}, counts:`, status.counts);
    if (status.complete) {
      finalStatus = status;
      break;
    }
  }

  // Distinguish "finished" from "gave up waiting" — they are not the same outcome, and a caller
  // driving a workflow needs to tell them apart before deciding to notify or keep waiting.
  if (!finalStatus) {
    console.warn(
      `\nGave up after ${POLL_TIMEOUT_MS / 60000} minutes — the transaction is STILL RUNNING, ` +
      'not failed.',
    );
    console.warn(
      '  Expected if the batch contains Kubernetes resources (up to 8 hours) — raise\n' +
      '  SEDAI_POLL_TIMEOUT_MIN and re-run. A resource with missing metrics never leaves\n' +
      '  IN_QUEUE at all, so polling it would not terminate however long you wait.',
    );
    console.warn(`Resume polling later with transactionId: ${submission.transactionId}`);
    console.log('\nPartial results so far:');
    for await (const item of getExecutionItems(submission.transactionId)) {
      console.log(`  ${item.resourceId} (${item.cloudProviderId}): ${item.status}`);
    }
    process.exitCode = 1;
    return;
  }

  if (finalStatus.items) {
    console.log('\nResults (inline from getExecutionStatus):');
    for (const item of finalStatus.items) {
      console.log(`  ${item.resourceId} (${item.cloudProviderId}): ${item.status}${item.reason ? ` (${item.reason})` : ''}`);
    }
    return;
  }

  // --- Step 3: List per-resource results, including rejected/duplicate ones ---
  // Use this when the batch is larger than one page — items is capped at a single page.
  console.log('\nResults:');
  for await (const item of getExecutionItems(submission.transactionId)) {
    console.log(`  ${item.resourceId} (${item.cloudProviderId}): ${item.status}${item.reason ? ` (${item.reason})` : ''}`);
  }
}

main().catch(err => {
  // APIException means the API itself rejected the call or stayed unreachable after the SDK's
  // built-in retries. Anything else is a local problem — a bad argument, or a bug in this script.
  // See error_handling.ts for the full treatment.
  if (err instanceof APIException) {
    console.error(`\nSedai API error: ${err.message}`);
  } else {
    console.error('\nUnexpected error:', err);
  }
  process.exit(1);
});
