/**
 * GSK Quickstart — end-to-end workflow
 *
 * Covers the core integration flow in order:
 *   1. Find your Sedai account ID
 *   2. Pull CO_PILOT opportunities for your Azure VMs
 *   3. Execute an optimization on a chosen resource
 *   4. Poll until SUCCESSFUL or FAILED
 *
 * Run (from the examples directory, after `npm install`) — dry run, no execution:
 *   SEDAI_BASE_URL=https://gsk.sedai.app SEDAI_API_TOKEN=your-token \
 *   SEDAI_ACCOUNT_ID=<account-id> \
 *   npx ts-node -P tsconfig.json gsk_quickstart.ts
 *
 * Run (from the examples directory, after `npm install`) — live execute on a specific resource:
 *   SEDAI_BASE_URL=https://gsk.sedai.app SEDAI_API_TOKEN=your-token \
 *   SEDAI_ACCOUNT_ID=<account-id> \
 *   SEDAI_EXECUTE_RESOURCE_ID=<sedaiResourceId> \
 *   npx ts-node -P tsconfig.json gsk_quickstart.ts
 *
 * ⚠️  WARNING: Setting SEDAI_EXECUTE_RESOURCE_ID triggers a real optimization.
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
const SEDAI_EXECUTE_RESOURCE_ID = process.env.SEDAI_EXECUTE_RESOURCE_ID ?? '';

// Real optimizations are slow — an observed Azure disk took ~25 minutes end to end, and a
// resource waiting on a maintenance window can take considerably longer. Size the timeout for
// that, not for a quick demo.
const POLL_INTERVAL_MS = 15_000;
const MAX_POLLS = 160; // 40 minutes
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

  if (accounts.length === 0) {
    console.error('No accounts found in this tenant.');
    process.exit(1);
  }

  // Choose deliberately. Large tenants have thousands of accounts, most of which hold no VMs —
  // picking accounts[0] will usually land on one with nothing to optimize and make the SDK look
  // like it returned no data.
  const wanted = process.env.SEDAI_ACCOUNT_ID;
  if (!wanted) {
    console.error(
      `\nSet SEDAI_ACCOUNT_ID to one of the ${accounts.length} account IDs listed above, then re-run.\n` +
      '  Pick an account you know has VMs — most accounts in a large tenant have none.',
    );
    process.exit(1);
  }

  const account = accounts.find(a => a.id === wanted);
  if (!account) {
    console.error(`\nAccount ${wanted} not found in this tenant. Pick an id from the list above.`);
    process.exit(1);
  }
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
    console.log(`    sedaiResourceId:    ${vm.sedaiResourceId}   ← use this as SEDAI_EXECUTE_RESOURCE_ID`);
    console.log(`    Status:             ${vm.opportunityStatus}`);
    console.log(`    Current type:       ${vm.currentInstanceType}`);
    console.log(`    Recommended type:   ${vm.recommendedInstanceType}`);
    console.log(`    Monthly savings:    $${vm.monthlyCostImpact}`);
  }

  if (!opportunities.length) {
    console.log('  No CO_PILOT VM opportunities found for this account.');
    console.log('  This usually means the account holds no VMs — try a different SEDAI_ACCOUNT_ID.');
    console.log('  (Widening configModes will not help: this step also filters to resourceType');
    console.log('   \'vm\', and the extra modes mostly return \'base\' rows that get filtered out.)');
    return;
  }

  // ---------------------------------------------------------------------------
  // Step 3 — Execute (only runs if SEDAI_EXECUTE_RESOURCE_ID is set)
  // ---------------------------------------------------------------------------
  if (!SEDAI_EXECUTE_RESOURCE_ID) {
    console.log('\n=== Step 3: Execute ===');
    console.log('  Skipped — set SEDAI_EXECUTE_RESOURCE_ID to a sedaiResourceId above to trigger execution.');
    return;
  }

  const target = opportunities.find(o => o.sedaiResourceId === SEDAI_EXECUTE_RESOURCE_ID);
  if (!target) {
    console.error(`\nERROR: ${SEDAI_EXECUTE_RESOURCE_ID} not found in CO_PILOT opportunities for this account.`);
    console.error('Make sure the resource is in CO_PILOT mode and belongs to the selected account.');
    return;
  }

  console.log(`\n=== Step 3: Execute — ${target.resourceName} ===`);
  console.log(`  ${target.currentInstanceType} → ${target.recommendedInstanceType}`);
  console.log(`  Estimated monthly savings: $${target.monthlyCostImpact}`);

  // Verify status is PROPOSED before executing
  let currentStatus: string | null = null;
  for await (const rec of getRecommendationsV3({ resourceId: SEDAI_EXECUTE_RESOURCE_ID })) {
    currentStatus = rec.status;
    break;
  }

  if (currentStatus !== 'PROPOSED') {
    console.log(`\n  Status is "${currentStatus}" — only PROPOSED resources can be executed.`);
    return;
  }

  console.log('\n  Submitting execution...');
  const submitted = await executeWithCopilot(SEDAI_EXECUTE_RESOURCE_ID);
  console.log(`  Submitted: ${submitted}`);

  // ---------------------------------------------------------------------------
  // Step 4 — Poll for completion
  // ---------------------------------------------------------------------------
  console.log('\n=== Step 4: Tracking status ===');
  for (let i = 0; i < MAX_POLLS; i++) {
    await new Promise(res => setTimeout(res, POLL_INTERVAL_MS));

    for await (const rec of getRecommendationsV3({ resourceId: SEDAI_EXECUTE_RESOURCE_ID })) {
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

  console.log('\n⚠ Gave up waiting after 40 minutes — the optimization is STILL RUNNING, not failed.');
  console.log(`  Re-check later with getRecommendationsV3({ resourceId: '${SEDAI_EXECUTE_RESOURCE_ID}' }),`);
  console.log('  or look it up in the Sedai UI.');
  process.exitCode = 1;
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
