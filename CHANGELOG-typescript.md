# Changelog — TypeScript / JavaScript SDK

Changes to the `sedai-sdk` npm package, newest first.
For the Python SDK, see [CHANGELOG.md](./CHANGELOG.md).

> Version numbers start at 1.1.0. Earlier TypeScript releases all shipped as `1.0.0` and are not
> listed here.

# 1.2.4 - 2026-08-28

### Fixed

- **`getCloudProviderIds()` returns unresolved IDs mapped to themselves, not omitted.** Every ID you pass is always present in the result, so checking for a missing key never detects a failed lookup. To find unresolved ones, compare each value against its key: `ids.filter(id => map[id] === id)`. Kubernetes resources are the exception — they have no separate provider ID, so theirs legitimately equals the Sedai resource ID. This is existing backend behaviour; only the documentation changed.
- **`resourceId` is not an opaque UUID.** It was documented as `res_abc123`. Real IDs are slash-delimited composite paths that embed the account, region and resource kind — e.g. `tjab5onf/eastus2/Instance/23b2be14-.../US6WVDCP200253`. Any validation pattern written from the old documented shape would reject every real ID. Treat the value as opaque; the structure is not a published contract.

### Changed

- **Source maps are no longer published.** The package shipped 26 `.js.map` files whose sources pointed at a `src/` directory that is not included, so stack traces referenced paths that do not exist. The tarball drops from 83 KB to 56 KB. Compiled `.js` and `.d.ts` are unaffected.

### Added

- **[REFERENCE-typescript.md](./REFERENCE-typescript.md)** — the SDK's full reference (key concepts, typical workflow, authentication, pagination, error handling, and every function by area) is now published in this repo. It previously shipped only inside the package at `node_modules/sedai-sdk/README.md`, so nothing linked to it and it was invisible until after installing.
- **A `401` entry in the README's [Troubleshooting](./README.md#troubleshooting) section**, including how to read the JWT `exp` claim to tell an expired token from a wrong one without calling the API.

# 1.2.3 - 2026-08-28

### Fixed

- **`start` in `PaginationConfig` is a 1-based page number, not a record offset.** The documentation said the opposite, and advised passing `start: 50` with `pageSize: 50` to reach page 2. That actually requests **page 50** — record 2,450 — and returns plausible-looking data from the wrong part of the result set **with no error**. If you followed the old guidance, your offsets were multiplied by `pageSize`. To start at page 2, pass `start: 2`, whatever `pageSize` is. `numPages` is likewise a count of pages, not records.
- **The clone-and-run flow for examples now works.** v1.2.2 moved the examples out of the npm package and pointed you at this repo, but `examples/typescript/` had no `package.json`, so `sedai-sdk` never resolved and every example failed with `TS2307`. That directory is now a self-contained npm project — `npm install` there is all you need, and it pins `typescript@5` for you.
- **Example run commands now use paths that exist.** Every example header printed `npx ts-node -P examples/tsconfig.json examples/<file>` — paths from the SDK's own repo layout, not this one. Commands are now relative to `examples/typescript/`, and each header says to run from there.

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
