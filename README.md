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

Install the SDK:

    npm install https://github.com/SedaiEngineering/sedai-sdk-releases/raw/main/sedai-sdk-latest.tgz

Configure and use:

```typescript
import { configure, getAllAccounts } from 'sedai-sdk';

configure({
  baseUrl: 'https://your-org.sedai.app',
  apiToken: 'your-api-token',
});

const accounts = await getAllAccounts();
```

API Documentation at https://sedaiengineering.github.io/sedai-sdk-typescript/
