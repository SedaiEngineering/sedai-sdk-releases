/**
 * Error handling and retries — what the SDK throws, what it retries for you, and what a caller
 * driving a long-running workflow needs to decide.
 *
 * There are exactly two error types to handle:
 *
 *   APIException  The API rejected the call, or stayed unreachable after the SDK's built-in
 *                 retries. Something outside your process went wrong.
 *   Error         A precondition you control was violated — a missing required argument, an
 *                 invalid enum value. The call never left your process.
 *
 * The SDK never signals failure by returning false, null, or an empty array. If a call returns,
 * it succeeded. That means you never have to inspect a result to find out whether it worked.
 *
 * Run (from the examples directory, after `npm install`):
 *   SEDAI_BASE_URL=https://your-org.sedai.app SEDAI_API_TOKEN=your-token \
 *   npx ts-node -P tsconfig.json error_handling.ts
 */

import {
  configure,
  getAllAccounts,
  getOpportunitiesForResources,
  submitBulkExecutionRequest,
  APIException,
} from 'sedai-sdk';

// --- Retries are built in, and configurable ---------------------------------------------------
// doGet/doPost/doDelete automatically retry on 429, 503, and 504 with exponential backoff
// (1s x 2^attempt, plus jitter). Three retries by default.
//
// This matters for what an APIException *means*: by the time one reaches you, transient failures
// have already been retried and are exhausted. It is not a "try again in a moment" signal — the
// SDK already did that. Treat it as a real failure.
//
// Raise `retries` for a long-running batch job that can afford to wait; lower it for an
// interactive request where a user is watching a spinner.
configure({
  baseUrl: process.env.SEDAI_BASE_URL ?? 'https://your-org.sedai.app',
  apiToken: process.env.SEDAI_API_TOKEN ?? 'your-api-token',
  retries: 3,
});

async function main() {
  // --- 1. The standard shape ------------------------------------------------------------------
  // Catch APIException for anything the API is responsible for; rethrow everything else, because
  // a programming error should not be silently swallowed by a network-error handler.
  console.log('\n--- 1. Standard error handling ---');
  try {
    const accounts = await getAllAccounts();
    console.log(`  Retrieved ${accounts.length} account(s).`);
  } catch (e) {
    if (e instanceof APIException) {
      console.error(`  API error: ${e.message}`);
    } else {
      throw e;
    }
  }

  // --- 2. Reading an APIException -------------------------------------------------------------
  // The message carries the HTTP method, the endpoint, and the underlying cause, for example:
  //
  //   GET /api/site/accounts failed: Request failed with status code 401
  //   GET /api/site/accounts failed: undefined getaddrinfo ENOTFOUND your-org.sedai.app
  //
  // There is no structured `status` property — if you need to branch on the cause, match the
  // message. Keep such matching to logging and alerting decisions rather than control flow, since
  // message text is not part of the SDK's compatibility surface.
  console.log('\n--- 2. Classifying a failure for a workflow ---');
  try {
    await getAllAccounts();
    console.log('  Call succeeded.');
  } catch (e) {
    if (e instanceof APIException) {
      const msg = e.message;
      if (msg.includes('401') || msg.includes('403')) {
        // Credentials are wrong or lack permission. Retrying will not help — fail loudly so
        // somebody rotates the token.
        console.error('  Authentication/authorization failure — check SEDAI_API_TOKEN.');
      } else if (msg.includes('ENOTFOUND') || msg.includes('ECONNREFUSED')) {
        // The host is wrong or unreachable. Also not worth retrying in-process.
        console.error('  Cannot reach the Sedai instance — check SEDAI_BASE_URL and networking.');
      } else {
        // Everything else: the SDK already exhausted its retries.
        console.error(`  API call failed after retries: ${msg}`);
      }
    } else {
      throw e;
    }
  }

  // --- 3. Precondition violations are plain Errors, not APIException --------------------------
  // These are bugs in the calling code. They fail before any network call is made, so no retry
  // configuration affects them, and a catch block that only handles APIException will not catch
  // them. Submitting an execution request with no resources at all is one such case.
  console.log('\n--- 3. Precondition violation (never reaches the network) ---');
  try {
    await submitBulkExecutionRequest({});
    console.log('  No error thrown.');
  } catch (e) {
    if (e instanceof APIException) {
      console.error(`  Unexpected API error: ${e.message}`);
    } else if (e instanceof Error) {
      console.error(`  Precondition violated (a bug to fix, not a failure to retry): ${e.message}`);
    }
  }

  // --- 4. Failing one item without failing the batch ------------------------------------------
  // When you are iterating many resources, decide deliberately whether one failure should abort
  // the run. Collecting failures and continuing is usually right for a scheduled job; aborting is
  // usually right for an interactive request.
  console.log('\n--- 4. Per-item failure handling in a batch ---');
  const resourceIds = ['i-0abc1234567890def', 'vol-0abc1234567890def'];
  const failures: Array<{ id: string; reason: string }> = [];
  let succeeded = 0;

  for (const id of resourceIds) {
    try {
      for await (const _opp of getOpportunitiesForResources([id])) {
        succeeded++;
        break; // first page is enough for this illustration
      }
    } catch (e) {
      // One resource failing should not lose the results for the others.
      failures.push({ id, reason: e instanceof Error ? e.message : String(e) });
    }
  }

  console.log(`  ${succeeded} succeeded, ${failures.length} failed.`);
  for (const f of failures) {
    console.log(`    ${f.id}: ${f.reason}`);
  }

  // Surface a non-zero exit code so a scheduler or CI job notices partial failure.
  if (failures.length > 0) {
    process.exitCode = 1;
  }
}

main().catch(err => {
  if (err instanceof APIException) {
    console.error(`\nSedai API error: ${err.message}`);
  } else {
    console.error('\nUnexpected error:', err);
  }
  process.exit(1);
});
