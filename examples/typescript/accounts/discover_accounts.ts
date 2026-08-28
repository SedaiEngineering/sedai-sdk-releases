/**
 * Account discovery — getAllAccounts() / searchAccountsByName()
 *
 * Run this first to find your Sedai account ID. You'll need it for most
 * other SDK calls (getOpportunitiesForResources, getRecommendationsV3, etc.)
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P tsconfig.json accounts/discover_accounts.ts
 */

import { configure, getAllAccounts, searchAccountsByName } from 'sedai-sdk';

configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
});

async function main() {

  // --- List all accounts ---
  console.log('\n--- All accounts ---');
  const accounts = await getAllAccounts();
  console.log(`Total: ${accounts.length}\n`);
  for (const acc of accounts) {
    console.log(`  Name:     ${acc.name}`);
    console.log(`  ID:       ${acc.id}   ← use this as accountId in other calls`);
    console.log(`  Provider: ${acc.accountDetails.cloudProvider}`);
    console.log(`  Type:     ${acc.accountDetails.integrationType}`);
    console.log('');
  }

  // --- Search by name (e.g. find all Azure accounts) ---
  console.log('\n--- Search by name ---');
  const matches = await searchAccountsByName('azure');
  console.log(`Matches for "azure": ${matches.length}`);
  for (const acc of matches) {
    console.log(`  ${acc.name} — ${acc.id}`);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
