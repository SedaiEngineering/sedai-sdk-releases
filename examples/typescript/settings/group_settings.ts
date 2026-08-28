/**
 * Group settings — getGroupSettings() / updateGroupSettings()
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P tsconfig.json settings/group_settings.ts
 *
 * Note: updateGroupSettings() requires an admin-role API key.
 * Note: Call initializeGroupSettings(groupId) once after creating a new group
 *       before reading or updating its settings.
 */

import {
  configure,
  getGroupSettings,
  updateGroupSettings,
  initializeGroupSettings,
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

const GROUP_ID = requireEnv('SEDAI_GROUP_ID', 'Find one with getAllGroups() against your tenant.');

async function main() {

  // Initialize settings once for a new group (safe to call again on existing groups).
  await initializeGroupSettings(GROUP_ID);

  // --- Read current group settings ---
  const settings = await getGroupSettings(GROUP_ID);

  console.log('Current group settings:');
  console.log(JSON.stringify(settings, null, 2));

  // --- Update: always get-then-modify to avoid clobbering other fields ---
  // Group settings are nested by resource category: appCommonSettings, kubeSettings,
  // volumeSettings, ecsSettings, serverlessSettings, bucketSettings.
  // Update only the fields you want to change.
  if (settings.volumeSettings) {
    settings.volumeSettings = {
      ...settings.volumeSettings,
      optimization: {
        ...settings.volumeSettings.optimization,
        setting: {
          ...settings.volumeSettings.optimization?.setting,
          configMode: 'DATA_PILOT',
        },
      },
    };
  }

  await updateGroupSettings(GROUP_ID, settings);
  console.log('\nGroup settings updated.');

  // --- Read back to confirm ---
  const updated = await getGroupSettings(GROUP_ID);
  console.log('\nUpdated group settings:');
  console.log(JSON.stringify(updated, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
