/**
 * Execute an optimization and track its status
 *
 * This is the core GSK workflow:
 *   1. Find a resource in CO_PILOT mode with an available opportunity
 *   2. Execute the optimization via executeWithCopilot()
 *   3. Poll getRecommendationsV3() to track status until SUCCESSFUL or FAILED
 *
 * ⚠️  WARNING: This example triggers a real optimization. Only run it against
 * a safe test resource. Never point SEDAI_BASE_URL at a production environment
 * unless you intend to execute the change.
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   SEDAI_RESOURCE_ID=<sedai-resource-id> \
 *   npx ts-node -P tsconfig.json execute/execute_opportunity.ts
 *
 * To get a sedaiResourceId, run bulk_opportunities.ts first and copy a value
 * where resourceType is 'vm' or 'volume' and configMode is 'CO_PILOT'.
 *
 * VM-specific note:
 *   For VMs in CO_PILOT mode you can also use approveExecution() / rejectExecution()
 *   instead of executeWithCopilot() if you need explicit approve/reject control.
 */

import {
  configure,
  executeWithCopilot,
  approveExecution,
  rejectExecution,
  getRecommendationsV3,
} from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

const SEDAI_RESOURCE_ID = process.env.SEDAI_RESOURCE_ID ?? '';
// Timings from the backend team, 2026-08-29: VMs and disks finish in ~20 minutes, Kubernetes
// resources can take up to 8 hours, and a resource with missing metrics stays IN_QUEUE
// indefinitely. 30s rather than 15s because the status query is expensive on a large tenant.
// Default covers VMs and disks; raise SEDAI_POLL_TIMEOUT_MIN for Kubernetes.
const POLL_INTERVAL_MS = 30_000;
const MAX_POLLS = Math.ceil((Number(process.env.SEDAI_POLL_TIMEOUT_MIN ?? 45) * 60_000) / POLL_INTERVAL_MS);
const TERMINAL = new Set(['SUCCESSFUL', 'FAILED', 'USER_REJECTED', 'UNSAFE_TO_ACT', 'EXPIRED']);

async function main() {
  if (!SEDAI_RESOURCE_ID) {
    console.error('Set SEDAI_RESOURCE_ID to a Sedai internal resource ID (sedaiResourceId from bulk_opportunities.ts)');
    process.exit(1);
  }

  // --- Step 1: Check current recommendation status before executing ---
  console.log(`\nChecking current recommendation for: ${SEDAI_RESOURCE_ID}`);
  let currentStatus: string | null = null;
  for await (const rec of getRecommendationsV3({ resourceId: SEDAI_RESOURCE_ID })) {
    currentStatus = rec.status;
    console.log(`  Status: ${rec.status}, operation: ${rec.operation?.type ?? 'none'}`);
    break;
  }

  if (!currentStatus) {
    console.log('  No recommendation found for this resource — nothing to execute.');
    return;
  }

  if (currentStatus !== 'PROPOSED') {
    console.log(`  Status is ${currentStatus} — resource is not in a PROPOSED state, cannot execute.`);
    return;
  }

  // --- Step 2: Execute ---
  console.log('\nExecuting optimization via executeWithCopilot()...');
  const submitted = await executeWithCopilot(SEDAI_RESOURCE_ID);
  console.log(`  Submitted: ${submitted}`);

  // --- Step 3: Poll for status ---
  console.log('\nPolling for status (checking every 5s, timeout 2min)...');
  for (let i = 0; i < MAX_POLLS; i++) {
    await new Promise(res => setTimeout(res, POLL_INTERVAL_MS));

    for await (const rec of getRecommendationsV3({ resourceId: SEDAI_RESOURCE_ID })) {
      const status = rec.status;
      console.log(`  [poll ${i + 1}] Status: ${status}`);

      if (status === 'SUCCESSFUL') {
        console.log('\n✓ Optimization completed successfully.');
        return;
      }
      if (status !== null && TERMINAL.has(status)) {
        console.log(`\n✗ Optimization ended with status: ${status}`);
        return;
      }
      break;
    }
  }

  console.log('\n⚠ Timed out waiting for completion — check the Sedai UI for current status.');
}

// --- VM-specific: approve / reject a pending CO_PILOT execution ---
async function vmApproveExample(sedaiResourceId: string) {
  // Use approveExecution() to explicitly approve a VM optimization.
  // Use rejectExecution() to decline it.
  const approved = await approveExecution(sedaiResourceId);
  console.log(`Approved: ${approved}`);

  // const rejected = await rejectExecution(sedaiResourceId);
}
void vmApproveExample; // shown for reference — not called by default

main().catch(err => {
  console.error(err);
  process.exit(1);
});
