/**
 * Single resource opportunity — getOpportunityForResource()
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P tsconfig.json optimizations/individual_resource_opportunity.ts
 */

import {
  configure,
  getOpportunityForResource,
  VMOpportunityDetails,
  VolumeOpportunityDetails,
} from 'sedai-sdk';

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

// A native cloud provider ID — e.g. 'i-0abc1234567890def' (AWS EC2) or an Azure resource path.
const PROVIDER_RESOURCE_ID = requireEnv(
  'SEDAI_PROVIDER_RESOURCE_ID',
  'Use a providerResourceId from: npx ts-node -P tsconfig.json optimizations/bulk_opportunities.ts',
);

async function main() {
  const opp = await getOpportunityForResource(PROVIDER_RESOURCE_ID);

  if (!opp) {
    console.log('No opportunity found for this resource.');
    return;
  }

  console.log(`Sedai resource ID:  ${opp.sedaiResourceId}`);
  console.log(`Resource name:      ${opp.resourceName}`);
  console.log(`Opportunity status: ${opp.opportunityStatus}`);
  console.log(`Pilot mode:         ${opp.configMode ?? '(not returned)'}`);
  console.log(`Monthly cost:       $${opp.preOpsMonthlyCost} → $${opp.postOpsMonthlyCost}`);
  console.log(`Monthly savings:    $${opp.monthlyCostImpact} (${opp.monthlyCostImpactPct}%)`);

  if (opp.resourceType === 'vm') {
    const vm = opp as VMOpportunityDetails;
    console.log('\nVM details:');
    console.log(`  Current type:     ${vm.currentInstanceType}`);
    console.log(`  Recommended type: ${vm.recommendedInstanceType}`);
    console.log(`  On-demand price:  $${vm.preOnDemandPricing} → $${vm.postOnDemandPricing}`);
    console.log(`  Price impact:     $${vm.estimatedOnDemandPricingImpact}`);
    for (const cfg of vm.instanceConfigs) {
      console.log(`  Config: ${cfg.currentType} → ${cfg.recommendedType} (${cfg.region}, qty: ${cfg.quantity})`);
    }

  } else if (opp.resourceType === 'volume') {
    const disk = opp as VolumeOpportunityDetails;
    console.log('\nVolume details:');
    console.log(`  Current config:     ${JSON.stringify(disk.currentConfig)}`);
    console.log(`  Recommended config: ${JSON.stringify(disk.recommendedConfig)}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
