# Changelog — TypeScript / JavaScript SDK

Changes to the `sedai-sdk` npm package, newest first.
For the Python SDK, see [CHANGELOG.md](./CHANGELOG.md).

> Version numbers start at 1.1.0. Earlier TypeScript releases all shipped as `1.0.0` and are not
> listed here.

# 1.2.2 - 2026-08-28

### Changed

- **Examples have moved. They are no longer bundled inside the npm package** — they now live only in this repo, under [`examples/typescript/`](./examples/typescript). If you previously copied them out of your `node_modules` with `cp -r node_modules/sedai-sdk/examples ./sedai-examples`, that path no longer exists after upgrading. Clone this repo instead:

      git clone https://github.com/SedaiEngineering/sedai-sdk-releases.git
      cd sedai-sdk-releases/examples/typescript
      npm install

  *Why:* the bundled copy carried a `tsconfig.json` written for the SDK's own build, mapping `sedai-sdk` to a relative `../dist` path that does not exist inside `node_modules`. It could never compile where it was shipped. Keeping a single copy in this repo removes the duplication that let that go unnoticed. The examples themselves are unchanged and the tarball is smaller as a result.
- **Example environment variables now all use the `SEDAI_` prefix.** Rename these in any scripts or CI that run the examples:

  | Old | New |
  |---|---|
  | `RESOURCE_ID` | `SEDAI_RESOURCE_ID` |
  | `PROVIDER_RESOURCE_IDS` | `SEDAI_PROVIDER_RESOURCE_IDS` |
  | `EXECUTE_RESOURCE_ID` | `SEDAI_EXECUTE_RESOURCE_ID` |

  `SEDAI_BASE_URL`, `SEDAI_API_TOKEN`, and `SEDAI_RESOURCE_IDS` are unchanged. This affects the example scripts only — no SDK function reads these.

### Fixed

- Setup instructions now pin `typescript@5`. `ts-node` is not compatible with TypeScript 7, and an unpinned `npm install typescript` resolves to 7.x, so the documented run command failed with `TypeError: Cannot read properties of undefined (reading 'fileExists')` before any of your code ran. `tsx` is documented as an alternative if you want to stay on current TypeScript.
- The README quickstart no longer crashes with a `TypeError` on a tenant that has no cloud accounts set up yet.

### Documented

- How to force a real reinstall when upgrading. The install URL always serves the latest build, so npm can report "up to date" and silently keep your existing copy — see [Upgrading to a new release](./README.md) in the README.

# 1.2.1 - 2026-08-28

### Fixed

- `BulkExecutionSubmission.transactionId` is now typed `string | null`. When none of the submitted resources are recognized, the API returns `submitted: 0` and no transaction ID — there is nothing to poll. Check for `null` before calling `getExecutionStatus()`/`getExecutionItems()`. Type-only change; runtime behaviour is unchanged from 1.2.0.

### Added

- Runnable TypeScript examples under [`examples/typescript/`](./examples/typescript) — accounts, optimizations, settings, and bulk execution, including transaction-level tracking. Each file documents its own environment variables and run command.

# 1.2.0 - 2026-08-28

### Added

- Transaction-level bulk execution tracking: `submitBulkExecutionRequest()`, `getExecutionStatus()`, `getExecutionItems()` — submit a batch of resources and poll a single transaction ID for completion, instead of tracking a resource-ID list yourself.
- `includeItemsWhenComplete` option on `getExecutionStatus()` — get per-resource results back inline once a transaction finishes, without a separate `getExecutionItems()` call.
- `cloudProviderId` field on every execution item — the native cloud identifier (e.g. an Azure resource path or AWS ARN) alongside the Sedai resource ID. Identical to `resourceId` for Kubernetes resources.
