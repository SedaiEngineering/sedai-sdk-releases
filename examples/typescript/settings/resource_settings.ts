/**
 * Resource settings — getResourceSettings() / updateResourceSettings()
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P tsconfig.json settings/resource_settings.ts
 *
 * Note: updateResourceSettings() requires an admin-role API key.
 */

import { configure, getResourceSettings, updateResourceSettings } from 'sedai-sdk';

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

const RESOURCE_ID = requireEnv(
  'SEDAI_RESOURCE_ID',
  'Use a sedaiResourceId from: npx ts-node -P tsconfig.json optimizations/bulk_opportunities.ts',
);

async function main() {

  // --- Read current settings ---
  const settings = await getResourceSettings(RESOURCE_ID);

  console.log('Current settings:');
  console.log(JSON.stringify(settings, null, 2));

  // --- Update: always get-then-modify to avoid clobbering other fields ---
  // Set the pilot mode for this resource.
  // configMode values: 'AUTO' (autopilot) | 'CO_PILOT' (human approves) | 'DATA_PILOT' (monitor only)
  settings.optimization = {
    ...settings.optimization,
    setting: {
      ...settings.optimization?.setting,
      configMode: 'CO_PILOT',
    },
  };

  await updateResourceSettings(RESOURCE_ID, settings);
  console.log('\nSettings updated.');

  // --- Read back to confirm ---
  const updated = await getResourceSettings(RESOURCE_ID);
  console.log('\nUpdated settings:');
  console.log(JSON.stringify(updated, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
