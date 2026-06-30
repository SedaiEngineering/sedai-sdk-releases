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

**2. TypeScript project setup**

```bash
npm install --save-dev typescript ts-node @types/node
```

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

**Full API reference** — type signatures, all functions, pagination, and examples:
https://sedaiengineering.github.io/sedai-sdk-typescript/
