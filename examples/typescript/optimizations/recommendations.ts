/**
 * Recommendations — getRecommendations() / getRecommendationsV3()
 *
 * Run:
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P examples/tsconfig.json examples/optimizations/recommendations.ts
 */

import { configure, getRecommendations, getRecommendationsV3 } from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

const ACCOUNT_ID = 'your-account-id';

async function main() {

  // --- Get recommendations by account ID ---
  console.log('\n--- Recommendations by account ---');
  for await (const rec of getRecommendations({ accountIds: [ACCOUNT_ID] })) {
    console.log(`Resource:  ${rec.resourceId} (${rec.resourceName})`);
    console.log(`  Action:  ${rec.actionName}`);
    console.log(`  Type:    ${rec.recommendationType}`);
    console.log(`  Status:  ${rec.status}`);
    console.log(`  Created: ${rec.createdTime.toISOString()}`);
    console.log(`  Expires: ${rec.expiryTime.toISOString()}`);
    console.log('');
  }

  // --- Get recommendations by resource ID ---
  console.log('\n--- Recommendations by resource ID ---');
  for await (const rec of getRecommendations({ resourceId: 'sedai-resource-id' })) {
    console.log(`${rec.resourceId} | ${rec.actionName} | ${rec.status}`);
  }

  // --- Filter by type and status ---
  console.log('\n--- EFFICIENCY recommendations in PROPOSED status ---');
  for await (const rec of getRecommendationsV3({
    accountIds: [ACCOUNT_ID],
    recommendationTypes: ['EFFICIENCY'],          // 'AVAILABILITY' | 'EFFICIENCY'
    recommendationStatus: ['PROPOSED'],            // 'PROPOSED' | 'EXECUTING' | 'SUCCESSFUL' | 'FAILED' | 'EXPIRED' | 'USER_REJECTED' | 'PAUSED' | 'UNSAFE_TO_ACT'
    pagination: { pageSize: 100 },
  })) {
    console.log(`${rec.resourceId} | ${rec.actionName}`);
  }

  // --- Include operation details ---
  console.log('\n--- Recommendations with operation details ---');
  for await (const rec of getRecommendationsV3({
    accountIds: [ACCOUNT_ID],
    includeOperationDetails: true,
    pagination: { pageSize: 20 },
  })) {
    console.log(`${rec.resourceId} | ${rec.actionName}`);
    if (rec.operation) {
      console.log(`  Operation type:   ${rec.operation.type}`);
      console.log(`  Operation action: ${rec.operation.action}`);
    }
  }

  // --- Date range filter ---
  console.log('\n--- Recommendations in a date range ---');
  const endTime = new Date();
  const startTime = new Date(endTime.getTime() - 14 * 24 * 60 * 60 * 1000); // last 14 days
  for await (const rec of getRecommendationsV3({
    accountIds: [ACCOUNT_ID],
    startTime,
    endTime,
  })) {
    console.log(`${rec.resourceId} | ${rec.actionName} | created: ${rec.createdTime.toISOString()}`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
