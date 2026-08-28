/**
 * GSK Quickstart — end-to-end workflow
 *
 * Covers the core integration flow in order:
 *   1. Find your Sedai account ID
 *   2. Pull CO_PILOT opportunities for your Azure VMs
 *   3. Execute an optimization on a chosen resource
 *   4. Poll until SUCCESSFUL or FAILED
 *
 * Run (dry run — no execution):
 *   SEDAI_BASE_URL=https://gsk.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P examples/tsconfig.json examples/gsk_quickstart.ts
 *
 * Run (live execute on a specific resource):
 *   SEDAI_BASE_URL=https://gsk.sedai.app SEDAI_API_TOKEN=your-token \
 *   EXECUTE_RESOURCE_ID=<sedaiResourceId> \
 *   npx ts-node -P examples/tsconfig.json examples/gsk_quickstart.ts
 *
 * ⚠️  WARNING: Setting EXECUTE_RESOURCE_ID triggers a real optimization.
 * Only use a resource you have confirmed is safe to change.
 */

import {
  configure,
  getAllAccounts,
  getOpportunitiesForResources,
  executeWithCopilot,
  getRecommendationsV3,
  VMOpportunityDetails,
} from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://gsk.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

// Set this to a sedaiResourceId (from Step 2 output) to trigger execution in Step 3.
// Leave unset to run Steps 1 and 2 only (safe, read-only).
const EXECUTE_RESOURCE_ID = process.env.EXECUTE_RESOURCE_ID ?? '';

const POLL_INTERVAL_MS = 5000;
const MAX_POLLS = 24; // 2 minutes
const TERMINAL = new Set(['SUCCESSFUL', 'FAILED', 'USER_REJECTED', 'UNSAFE_TO_ACT', 'EXPIRED']);

async function main() {

  // ---------------------------------------------------------------------------
  // Step 1 — Find your account ID
  // ---------------------------------------------------------------------------
  // Sedai groups your cloud resources into accounts. You need an account ID
  // to query opportunities across all VMs in that account.
  console.log('\n=== Step 1: Accounts ===');
  const accounts = await getAllAccounts();
  console.log(`Found ${accounts.length} account(s):\n`);
  for (const acc of accounts) {
    console.log(`  ${acc.name.padEnd(40)} id: ${acc.id}  provider: ${acc.accountDetails.cloudProvider}`);
  }

  // Pick the account you want to work with and paste its id below, or
  // filter by name: accounts.find(a => a.name === 'my-azure-account')
  const account = accounts[0];
  if (!account) { console.error('No accounts found.'); return; }
  console.log(`\nUsing: ${account.name} (${account.id})`);

  // ---------------------------------------------------------------------------
  // Step 2 — Find CO_PILOT opportunities for Azure VMs in this account
  // ---------------------------------------------------------------------------
  // CO_PILOT mode means Sedai has a recommendation ready but is waiting for
  // human approval before executing. These are the resources you can act on.
  //
  // Azure VM provider resource ID format:
  //   /subscriptions/{subId}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name}
  //
  // You can pass specific Azure resource IDs instead of accountIds:
  //   getOpportunitiesForResources(['/subscriptions/...'], { configModes: ['CO_PILOT'] })
  console.log('\n=== Step 2: CO_PILOT opportunities ===');
  const opportunities: VMOpportunityDetails[] = [];

  for await (const opp of getOpportunitiesForResources([], {
    accountIds: [account.id],
    configModes: ['CO_PILOT'],
    pagination: { pageSize: 50 },
  })) {
    if (opp.resourceType !== 'vm') continue; // focus on VMs
    opportunities.push(opp as VMOpportunityDetails);

    const vm = opp as VMOpportunityDetails;
    console.log(`\n  ${vm.resourceName}`);
    console.log(`    sedaiResourceId:    ${vm.sedaiResourceId}   ← use this as EXECUTE_RESOURCE_ID`);
    console.log(`    Status:             ${vm.opportunityStatus}`);
    console.log(`    Current type:       ${vm.currentInstanceType}`);
    console.log(`    Recommended type:   ${vm.recommendedInstanceType}`);
    console.log(`    Monthly savings:    $${vm.monthlyCostImpact}`);
  }

  if (!opportunities.length) {
    console.log('  No CO_PILOT VM opportunities found for this account.');
    console.log('  Try configModes: [\'AUTO\', \'DATA_PILOT\', \'CO_PILOT\'] to see all modes.');
    return;
  }

  // ---------------------------------------------------------------------------
  // Step 3 — Execute (only runs if EXECUTE_RESOURCE_ID is set)
  // ---------------------------------------------------------------------------
  if (!EXECUTE_RESOURCE_ID) {
    console.log('\n=== Step 3: Execute ===');
    console.log('  Skipped — set EXECUTE_RESOURCE_ID to a sedaiResourceId above to trigger execution.');
    return;
  }

  const target = opportunities.find(o => o.sedaiResourceId === EXECUTE_RESOURCE_ID);
  if (!target) {
    console.error(`\nERROR: ${EXECUTE_RESOURCE_ID} not found in CO_PILOT opportunities for this account.`);
    console.error('Make sure the resource is in CO_PILOT mode and belongs to the selected account.');
    return;
  }

  console.log(`\n=== Step 3: Execute — ${target.resourceName} ===`);
  console.log(`  ${target.currentInstanceType} → ${target.recommendedInstanceType}`);
  console.log(`  Estimated monthly savings: $${target.monthlyCostImpact}`);

  // Verify status is PROPOSED before executing
  let currentStatus: string | null = null;
  for await (const rec of getRecommendationsV3({ resourceId: EXECUTE_RESOURCE_ID })) {
    currentStatus = rec.status;
    break;
  }

  if (currentStatus !== 'PROPOSED') {
    console.log(`\n  Status is "${currentStatus}" — only PROPOSED resources can be executed.`);
    return;
  }

  console.log('\n  Submitting execution...');
  const submitted = await executeWithCopilot(EXECUTE_RESOURCE_ID);
  console.log(`  Submitted: ${submitted}`);

  // ---------------------------------------------------------------------------
  // Step 4 — Poll for completion
  // ---------------------------------------------------------------------------
  console.log('\n=== Step 4: Tracking status ===');
  for (let i = 0; i < MAX_POLLS; i++) {
    await new Promise(res => setTimeout(res, POLL_INTERVAL_MS));

    for await (const rec of getRecommendationsV3({ resourceId: EXECUTE_RESOURCE_ID })) {
      const status = rec.status;
      console.log(`  [${new Date().toISOString()}] Status: ${status}`);

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

  console.log('\n⚠ Timed out — check the Sedai UI for current status.');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
