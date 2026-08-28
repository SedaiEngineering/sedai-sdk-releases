/**
 * Resource optimizations — getResourceOptimizations() / getRecommendedResourceState()
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   SEDAI_ACCOUNT_ID=<account-id> SEDAI_RESOURCE_ID=<sedai-resource-id> \
 *   npx ts-node -P tsconfig.json optimizations/resource_optimizations.ts
 */

import { configure, getResourceOptimizations, getRecommendedResourceState } from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

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

const FIND_IDS = 'Find one with: npx ts-node -P tsconfig.json accounts/discover_accounts.ts';

const ACCOUNT_ID  = requireEnv('SEDAI_ACCOUNT_ID', FIND_IDS);
const RESOURCE_ID = requireEnv('SEDAI_RESOURCE_ID', 'Use a sedaiResourceId from the account listing above.');

async function main() {

  // --- Get all optimizations for an account ---
  console.log('\n--- Resource optimizations by account ---');
  for await (const opt of getResourceOptimizations({ accountId: ACCOUNT_ID })) {
    console.log(`Resource: ${opt.resourceId} (${opt.resourceName})`);
    console.log(`  Account:          ${opt.accountId}`);
    console.log(`  Pre hourly cost:  $${opt.preHourlyCost}`);
    console.log(`  Post hourly cost: $${opt.postHourlyCost}`);
    console.log(`  Cost change/hr:   $${opt.costChangePerHour}`);
    if (opt.optimizationTime) {
      console.log(`  Optimized at:     ${opt.optimizationTime.toISOString()}`);
    }
    console.log('');
  }

  // --- Filter to a specific resource over a date range ---
  console.log('\n--- Optimizations for a specific resource (last 14 days) ---');
  const endTime   = new Date();
  const startTime = new Date(endTime.getTime() - 14 * 24 * 60 * 60 * 1000);
  for await (const opt of getResourceOptimizations({
    resourceId: RESOURCE_ID,
    startTime,
    endTime,
    sortBy: 'optimization_time',   // 'optimization_time' | 'cpu_change_core' | 'cpu_change_vcpu' | 'memory_change_mib' | 'storage_change_gib'
    sortDir: 'desc',
    pagination: { pageSize: 50 },
  })) {
    console.log(`${opt.resourceId} | cost change: $${opt.costChangePerHour}/hr | optimized: ${opt.optimizationTime?.toISOString()}`);
  }

  // --- Get the proposed config Sedai would apply to a resource ---
  console.log('\n--- Recommended resource state ---');
  const state = await getRecommendedResourceState(RESOURCE_ID);
  if (state) {
    console.log('Proposed configuration:');
    console.log(JSON.stringify(state, null, 2));
  } else {
    console.log('No proposed state available for this resource.');
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
