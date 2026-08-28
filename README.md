What's new in each release:
[Python SDK changelog](./CHANGELOG.md) · [TypeScript / JavaScript SDK changelog](./CHANGELOG-typescript.md)

---

## Python SDK

Create a virtual environment and activate it:

    python3 -m venv venv
    . ./venv/bin/activate

Install the SDK:

    pip install https://github.com/SedaiEngineering/sedai-sdk-releases/raw/main/sedai_sdk-latest.tar.gz

Go to a sample example dir and update the .env file and run the examples

API Documentation at https://sedaiengineering.github.io/sedai-sdk-python/

---

## JavaScript / TypeScript SDK

Requires Node.js ≥ 16.

**1. Install**

    npm install https://github.com/SedaiEngineering/sedai-sdk-releases/raw/main/sedai-sdk-typescript-latest.tgz

*Already installed and upgrading to a newer release? See [Troubleshooting](#troubleshooting).*

**2. TypeScript project setup**

```bash
npm install --save-dev typescript@5 ts-node @types/node
```

> **Pin `typescript@5`.** `ts-node` is not compatible with TypeScript 7, and installing `typescript`
> unpinned resolves to 7.x — every `ts-node` run then fails with
> `TypeError: Cannot read properties of undefined (reading 'fileExists')` before your code runs.
> To stay on current TypeScript instead, use [`tsx`](https://www.npmjs.com/package/tsx)
> (`npx tsx exercise.ts`) in place of `ts-node`.

Add a `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "types": ["node"],
    "strict": true,
    "esModuleInterop": true,
    "outDir": "dist"
  }
}
```

**3. Get an API token** — log in to your Sedai instance → Settings → API Keys → Create New Key

**4. Use it**

Create a file `exercise.ts`:

```typescript
import { configure, getAllAccounts, getRecommendations, APIException } from 'sedai-sdk';

configure({
  baseUrl: 'https://your-org.sedai.app',
  apiToken: 'your-api-token',
});

async function main() {
  try {
    // List accounts
    const accounts = await getAllAccounts();
    if (accounts.length === 0) {
      console.error('No cloud accounts are set up in this Sedai tenant yet.');
      return;
    }
    const accountId = accounts[0].id;
    console.log('Account:', accounts[0].name, accountId);

    // Key functions return a PageIterator<T> — iterate with for await
    for await (const rec of getRecommendations({ accountIds: [accountId] })) {
      console.log(rec.resourceId, rec.actionName);
    }
  } catch (e) {
    if (e instanceof APIException) {
      console.error('API error:', e.message);
    } else {
      throw e;
    }
  }
}

main();
```

**5. Run**

    npx ts-node exercise.ts

**Full SDK reference** — [REFERENCE-typescript.md](./REFERENCE-typescript.md). Key concepts, the
typical workflow, authentication, pagination, error handling, and every function by area. This is
the same document that ships inside the package as `node_modules/sedai-sdk/README.md`; read it here
without installing first.

**Generated API docs** — type signatures for every export:
https://sedaiengineering.github.io/sedai-sdk-typescript/

**What changed in this release** — see the
[TypeScript / JavaScript SDK changelog](./CHANGELOG-typescript.md).

**More examples** — see [examples/typescript](./examples/typescript) for runnable examples
covering accounts, optimizations, settings, and bulk execution (including transaction-level
tracking — [examples/typescript/execute/bulk_execution_transaction_tracking.ts](./examples/typescript/execute/bulk_execution_transaction_tracking.ts)).
Each file documents its own env vars and run command at the top.

---

## Troubleshooting

### npm says "up to date" but I still have the old version

The install URL always serves the latest build, so the same URL returns different bytes over time.
npm skips the network entirely when your `package-lock.json` already has a `resolved` entry for that
URL and the package is present in `node_modules` — it reports "up to date" and keeps your existing
copy. Force a real refetch:

```bash
rm -rf node_modules/sedai-sdk
npm cache clean --force
npm install https://github.com/SedaiEngineering/sedai-sdk-releases/raw/main/sedai-sdk-typescript-latest.tgz
```

Then confirm you got what you expected:

```bash
cat node_modules/sedai-sdk/package.json | grep version
```

Deleting the installed package is what forces the refetch; the cache clean is needed because npm
also caches HTTP responses by URL independently of `node_modules`.

### `npm ci` fails with an integrity/checksum error

Same root cause. Your lockfile recorded an integrity hash for a previous build served from this URL,
and the bytes have since changed. Follow the steps above to refresh the install, then commit the
updated `package-lock.json`.

### `ts-node` fails with `Cannot read properties of undefined (reading 'fileExists')`

`ts-node` is not compatible with TypeScript 7, and `npm install typescript` resolves to 7.x by
default. Either pin TypeScript 5:

```bash
npm install --save-dev typescript@5
```

or switch to [`tsx`](https://www.npmjs.com/package/tsx), which works with current TypeScript:

```bash
npm install --save-dev tsx
npx tsx exercise.ts
```

### `error TS5102: Option 'baseUrl' has been removed`

`baseUrl` was removed in TypeScript 7. Delete it from your `tsconfig.json` — the SDK resolves from
`node_modules` and needs no path mapping.
