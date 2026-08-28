/**
 * Bulk resource opportunities — getOpportunitiesForResources()
 *
 * Run:
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P examples/tsconfig.json examples/optimizations/bulk_opportunities.ts
 *
 * Requires: npm run build (so examples/tsconfig.json can resolve sedai-sdk → dist/)
 */

import {
  configure,
  getOpportunitiesForResources,
  VMOpportunityDetails,
  VolumeOpportunityDetails,
  OpportunityTag,
} from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

// Cloud provider resource IDs in their native format:
//   AWS EC2:   'i-0abc1234567890def'
//   AWS EBS:   'vol-0abc1234567890def'
//   Azure VM:  '/subscriptions/{subId}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name}'
const RESOURCE_IDS = [
  'i-0abc1234567890def',
  'vol-0abc1234567890def',
];

const ACCOUNT_ID = 'your-account-id';

async function main() {

  // --- Basic: fetch opportunities for a list of resource IDs ---
  console.log('\n--- Opportunities for specific resources ---');
  for await (const opp of getOpportunitiesForResources(RESOURCE_IDS)) {
    console.log(`Resource:        ${opp.sedaiResourceId}`);
    console.log(`  Provider ID:   ${opp.providerResourceId ?? '(not returned)'}`);
    console.log(`  Name:          ${opp.resourceName}`);
    console.log(`  Status:        ${opp.opportunityStatus}`);
    console.log(`  Pilot mode:    ${opp.configMode ?? '(not returned)'}`);
    console.log(`  Monthly cost:  $${opp.preOpsMonthlyCost} → $${opp.postOpsMonthlyCost}`);
    console.log(`  Savings:       $${opp.monthlyCostImpact} (${opp.monthlyCostImpactPct}%)`);
    console.log('');
  }

  // --- Filter by account and pilot mode ---
  console.log('\n--- Opportunities filtered by account and pilot mode ---');
  for await (const opp of getOpportunitiesForResources([], {
    accountIds: [ACCOUNT_ID],
    configModes: ['AUTO', 'DATA_PILOT'],   // 'AUTO' | 'DATA_PILOT' | 'CO_PILOT'
    pagination: { pageSize: 50 },
  })) {
    console.log(`${opp.sedaiResourceId} | mode: ${opp.configMode} | savings: $${opp.monthlyCostImpact}`);
  }

  // --- Include cloud provider tags ---
  console.log('\n--- Opportunities with cloud provider tags ---');
  for await (const opp of getOpportunitiesForResources([], {
    accountIds: [ACCOUNT_ID],
    includeTags: true,
  })) {
    const tags: OpportunityTag[] = opp.tags ?? [];
    console.log(`${opp.sedaiResourceId}`);
    for (const tag of tags) {
      console.log(`  tag: ${tag.key} = ${tag.value}`);
    }
  }

  // --- Narrow by resource type to access type-specific fields ---
  console.log('\n--- VM and volume details ---');
  for await (const opp of getOpportunitiesForResources(RESOURCE_IDS)) {
    if (opp.resourceType === 'vm') {
      const vm = opp as VMOpportunityDetails;
      console.log(`VM: ${vm.sedaiResourceId}`);
      console.log(`  Current type:     ${vm.currentInstanceType}`);
      console.log(`  Recommended type: ${vm.recommendedInstanceType}`);
      console.log(`  On-demand price:  $${vm.preOnDemandPricing} → $${vm.postOnDemandPricing}`);
      console.log(`  Monthly savings:  $${vm.monthlyCostImpact}`);
      for (const cfg of vm.instanceConfigs) {
        console.log(`  Config: ${cfg.currentType} → ${cfg.recommendedType}`);
        console.log(`    Region:   ${cfg.region}`);
        console.log(`    Quantity: ${cfg.quantity}`);
        if (cfg.preCpu)    console.log(`    CPU:      ${cfg.preCpu.value} ${cfg.preCpu.unit} → ${cfg.postCpu?.value} ${cfg.postCpu?.unit}`);
        if (cfg.preMemory) console.log(`    Memory:   ${cfg.preMemory.value} ${cfg.preMemory.unit} → ${cfg.postMemory?.value} ${cfg.postMemory?.unit}`);
      }

    } else if (opp.resourceType === 'volume') {
      const disk = opp as VolumeOpportunityDetails;
      console.log(`Volume: ${disk.sedaiResourceId}`);
      console.log(`  Monthly savings:    $${disk.monthlyCostImpact}`);
      if (disk.currentConfig)     console.log(`  Current config:     ${JSON.stringify(disk.currentConfig)}`);
      if (disk.recommendedConfig) console.log(`  Recommended config: ${JSON.stringify(disk.recommendedConfig)}`);

    } else {
      // resourceType === 'base' — cost/savings fields only, no type-specific config
      console.log(`Other: ${opp.sedaiResourceId} | savings: $${opp.monthlyCostImpact}`);
    }
    console.log('');
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
