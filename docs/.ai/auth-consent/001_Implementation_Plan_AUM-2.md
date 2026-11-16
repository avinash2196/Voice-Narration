# Implementation Plan

## Milestone

AUM-2 Frontend test request delivery — `docs/.ai/auth-consent/Plan.md`, Milestones, AUM-2. Serves AUM-3 Accounts and storage RED and AUM-7 Consent RED.

## Milestone Type

FOUNDATION

## Review Summary

- Behavior change: none in production. In the frontend test environment, `AbortController` and `AbortSignal` become Node's own, so a request made through the account client with its abort signal reaches the msw request mock.
- Requirements covered: frontend test request delivery (AUM2-Q1), the prerequisite for AUM-3 and AUM-7; known pre-existing failures not made worse (AUM2-Q2).
- Files: created `frontend/tests/environment/jsdom-node-abort.ts`; modified `frontend/vitest.config.ts` (one line); deleted none.
- Tests added: none in the repository. A temporary verification check, created in the git-ignored `frontend/.vitest/aum2-check/` and deleted after the run, proves an `AuthClient.login` request reaches the mock and returns its answer.
- Verification: the check (2 passed; on the baseline 2 failed with the abort-signal `TypeError`), `npm run type-check` (passes), `npx vitest run` (no failure outside the 90 known baseline failures).
- Needs attention: FTD-1 mechanism and FTD-4 constraint on later RED tests; FTD-5 temporary check written inside the frontend folder (git-ignored) because vitest cannot load one from outside it.

## Authoritative References

| Document | Status |
| --- | --- |
| `docs/.ai/auth-consent/requirements.md` | Approved by Avinash Srivastava on 2026-11-16 (revision 2) |
| `docs/.ai/auth-consent/Plan.md` | Approved by Avinash Srivastava on 2026-11-16 (8-milestone revision) |
| `docs/.ai/auth-consent/API-Contract.md` | Contract Review Status: Approved by Avinash Srivastava on 2026-11-16 (reference-only revision for the 8-milestone Plan); CONTRACT milestone AUM-1 Complete in `Plan.md` Execution Status. Authoritative predecessor. It defines no frontend test-environment behavior; AUM-2 uses no part of it. |
| `docs/requirements.md` (product level) | Does not exist (`ls docs` shows no such file) |
| Earlier Implementation Plans of this work item | None exist (the work-item folder holds only `requirements.md`, `Plan.md`, `API-Contract.md`) |

Answers recorded in this plan:

- **AUM2-Q2** [User: AUM2-Q2, 2026-11-16]: "pre-existing failures are recorded as known and must not get worse, not fixed in this work item". Applied in Acceptance / Completion Criterion FTC-5 and Verification step 3.

## Carried-Forward Decisions

None.

## Preconditions / Predecessor Evidence

- Predecessor AUM-1 (CONTRACT): `Plan.md` Execution Status row "Complete — contract approved by Avinash Srivastava on 2026-11-16", pointing to `docs/.ai/auth-consent/API-Contract.md`, whose Contract Review Status records the approval.
- AUM-2 Execution Status: Pending. No Implementation Plan exists for AUM-2 in the work-item folder, approved or otherwise.
- Milestone type: `Plan.md` records AUM-2 as FOUNDATION ("Milestone type: FOUNDATION."). Planned as recorded.
- Repository state: HEAD `f3372ce` on `claude/auth-consent`; `git status --short` prints only `?? docs/.ai/auth-consent/`, which matches `Plan.md` (no milestone executed since a commit).

FOUNDATION questions (`implementation-planning` FOUNDATION):

1. Why AUM-3 and AUM-7 cannot meaningfully proceed now: both need frontend tests in which requests made through the account client reach the msw request mock (`Plan.md` AUM-3 and AUM-7 Prerequisites). On the unmodified repository every such request is rejected with `TypeError: RequestInit: Expected signal ("AbortSignal {}") to be an instance of AbortSignal.` before the mock sees it (Planning-Time Dry Run, step D2), so their tests would fail for an environment reason, which is not valid RED evidence.
2. Exact prerequisite: in the frontend test environment, the global `AbortSignal` that `HttpClient` attaches (`frontend/src/services/api/httpClient.ts:89-100`) must be one that the global `Request` accepts, so msw's fetch interceptor can build the request and answer it.
3. Files that may change: create `frontend/tests/environment/jsdom-node-abort.ts`; modify `frontend/vitest.config.ts` line 8. Temporarily created and deleted during verification: `frontend/.vitest/aum2-check/account-client-delivery.check.spec.ts` (git-ignored). Plus this milestone's Execution Status update in `Plan.md`.
4. Excluded target behavior: every account, session, token-check, ownership and consent behavior; any change under `frontend/src/`, including the shared HTTP client's timeout; any test added to or changed in the repository; any msw handler; any fix of the known pre-existing failures.
5. Completion verified by: the temporary check passing (it failed on the baseline), the frontend type check passing, and the full frontend suite failing only on tests in the baseline's failure list (Acceptance / Completion Criteria).
6. Readiness evidence for AUM-3 and AUM-7: the check's second case shows `AuthClient.login` — the account client whose sign-up, login, session-check and logout calls AUM-3 tests, and which the protected pages AUM-7 tests depend on after AUM-4 — sending its request with its abort signal through the shared server from `frontend/tests/mocks/setup.ts`, the mock receiving method, path and body, and the client resolving with the mock's answer. Both RED milestones' frontend tests run under the same `vitest.config.ts`, so the change applies to them.

## Current Repository State

- `frontend/vitest.config.ts:8` — `environment: 'jsdom'`; `:10` — `setupFiles: ['./tests/mocks/setup.ts']`. No test file overrides the environment (`grep -rn "vitest-environment\|environmentMatchGlobs" tests vitest.config.ts vite.config.ts` finds nothing).
- `frontend/src/services/api/httpClient.ts:89-100` — every request creates an `AbortController` and passes `controller.signal` to `fetch`. `frontend/src/services/api/authClient.ts:14-20`, `:27-30` — `AuthClient` extends `HttpClient`; `login` posts to `/auth/login` on `API_CONFIG.AUTH_SERVICE` (`frontend/src/utils/api-config.ts:8`).
- `frontend/tests/mocks/setup.ts:1`, `:5-11` — `setupServer()` from `msw/node`, exported as `server`, listening for the whole run.
- `frontend/package-lock.json:8574-8575` vitest 1.6.1; `:6021-6022` msw 1.3.5; `:1166-1167` @mswjs/interceptors 0.17.10; `:5613-5614` jsdom 23.2.0. Node in this environment: v24.14.1 (`node -v`).
- Cause of the rejection, from the installed package sources (`npm ci` of the lock file in the disposable copy):
  - `node_modules/vitest/dist/vendor/index.GVFv9dZ0.js:264-265` lists `AbortController` and `AbortSignal` among the jsdom window keys; `:368-390` (`populateGlobal`) defines each such key on the global to return jsdom's value; `:538` the jsdom environment's `setup` calls it. The global `Request` that rejects the jsdom signal is not jsdom's: the check's first case, which builds `new Request(url, { signal })` directly, fails on the built-in environment with the same `RequestInit: Expected signal` message (dry run D2, D5) and passes once Node's `AbortSignal` is kept (D4).
  - `node_modules/@mswjs/interceptors/src/interceptors/fetch/index.ts:41-42` — the patched `fetch` calls `new Request(input, init)`; the dry-run stack trace points at this line (`:42:23`) for the `TypeError`.
- `node_modules/vitest/dist/worker.js:44` — an `environment` value starting with `.` is resolved as a path relative to the root and loaded; `:45-56` require a default-export object with `transformMode` `"web"` or `"ssr"`. `node_modules/vitest/package.json:74-77` exports `vitest/environments`, which provides `builtinEnvironments` (`dist/environments.d.ts`).
- `frontend/.gitignore:36` — `.vitest` is ignored (`git check-ignore -v .vitest/aum2-check/account-client-delivery.check.spec.ts` → `frontend/.gitignore:36:.vitest`). `frontend/.vitest/` does not exist.
- `frontend/tsconfig.json` — `"include": ["src"]`; the type check (AUV-6) does not cover `frontend/tests/`.
- msw 1.3.5 exports `rest` and no `http` or `HttpResponse` (`node_modules/msw/lib/index.d.ts:365`), so the check uses `rest`. `frontend/tests/mocks/auth-handlers.ts:1` imports `http, HttpResponse` and is imported by no test (repository fact for AUM-3; not changed here).

## Files in Scope

### Files to Create

- `frontend/tests/environment/jsdom-node-abort.ts`

### Files to Modify

- `frontend/vitest.config.ts`

### Files to Delete

None. (The temporary check `frontend/.vitest/aum2-check/account-client-delivery.check.spec.ts` is created and deleted within Execution Steps; it is never part of the repository.)

## Proposed Changes

1. Create `frontend/tests/environment/jsdom-node-abort.ts`: a vitest `Environment` object, default export, `name: 'jsdom-node-abort'`, `transformMode: 'web'`, and `async setup(global, options)` that reads Node's `global.AbortController` and `global.AbortSignal`, calls `builtinEnvironments.jsdom.setup(global, options)`, assigns the two saved Node values back to `global.AbortController` and `global.AbortSignal`, and returns the jsdom environment's result (its `teardown` is unchanged). Required so the `AbortSignal` `HttpClient` attaches is one that `Request` accepts (FOUNDATION question 2). No `setupVM` is defined: `frontend/vitest.config.ts` sets no `pool`, so the default non-VM pool calls `setup`.
2. Modify `frontend/vitest.config.ts` line 8: `environment: 'jsdom'` → `environment: './tests/environment/jsdom-node-abort.ts'`. Required so every frontend test file, including those AUM-3 and AUM-7 add or change, runs in that environment. No other setting changes.

## Proposed Code / Tests

### `frontend/tests/environment/jsdom-node-abort.ts` (create — complete content)

```ts
import type { Environment } from 'vitest';
import { builtinEnvironments } from 'vitest/environments';

// The built-in jsdom environment replaces the global AbortController and
// AbortSignal with jsdom's own, but keeps Node's fetch and Request. Node's
// Request accepts only Node's AbortSignal, so a fetch given a jsdom signal is
// rejected before the request mock sees it. This environment is the built-in
// jsdom environment with Node's AbortController and AbortSignal kept, so a
// request carrying an abort signal reaches the request mock.
const jsdomWithNodeAbort: Environment = {
  name: 'jsdom-node-abort',
  transformMode: 'web',
  async setup(global, options) {
    const NodeAbortController = global.AbortController;
    const NodeAbortSignal = global.AbortSignal;
    const jsdomEnvironment = await builtinEnvironments.jsdom.setup(global, options);
    global.AbortController = NodeAbortController;
    global.AbortSignal = NodeAbortSignal;
    return jsdomEnvironment;
  },
};

export default jsdomWithNodeAbort;
```

Note: assigning after `setup` works because `populateGlobal` defines each key with a setter that stores the assigned value and a getter that returns it (`node_modules/vitest/dist/vendor/index.GVFv9dZ0.js:377-389`); the jsdom `teardown` deletes the keys and restores the originals (`:541-548`).

### `frontend/vitest.config.ts` (modify — complete unified diff)

```diff
--- a/frontend/vitest.config.ts
+++ b/frontend/vitest.config.ts
@@ -5,7 +5,7 @@ import path from 'path'
 export default defineConfig({
   plugins: [react()],
   test: {
-    environment: 'jsdom',
+    environment: './tests/environment/jsdom-node-abort.ts',
     globals: true,
     setupFiles: ['./tests/mocks/setup.ts'],
     coverage: {
```

### Temporary verification check — `frontend/.vitest/aum2-check/account-client-delivery.check.spec.ts` (created in Execution Step 4, deleted in Step 8; complete content)

```ts
// AUM-2 verification check (docs/.ai/auth-consent/001_Implementation_Plan_AUM-2.md).
// Temporary: created in the git-ignored frontend/.vitest/aum2-check/ folder for
// the verification run and deleted afterwards. It is not a repository test.
import { describe, it, expect } from 'vitest';
import { rest } from 'msw';
import { server } from '@/../tests/mocks/setup';
import { AuthClient } from '@/services/api/authClient';
import { API_CONFIG } from '@/utils/api-config';

describe('AUM-2 check: account client requests reach the request mock', () => {
  it('the abort signal in force is one that Request accepts', () => {
    const controller = new AbortController();
    const request = new Request(`${API_CONFIG.AUTH_SERVICE}/auth/login`, { signal: controller.signal });
    controller.abort();
    expect(request.signal.aborted).toBe(true);
  });

  it('delivers an account client request, with its abort signal, to the mock and returns the mock answer', async () => {
    let received: { method: string; path: string; body: unknown } | null = null;
    server.use(
      rest.post(`${API_CONFIG.AUTH_SERVICE}/auth/login`, async (req, res, ctx) => {
        received = { method: req.method, path: req.url.pathname, body: await req.json() };
        return res(ctx.status(200), ctx.json({ token: 'aum2-check-token' }));
      })
    );

    const answer = await new AuthClient().login({ email: 'aum2@example.com', password: 'Passw0rdA' });

    expect(received).toEqual({
      method: 'POST',
      path: '/auth/login',
      body: { email: 'aum2@example.com', password: 'Passw0rdA' },
    });
    expect(answer).toEqual({ token: 'aum2-check-token' });
  });
});
```

The first case asserts the effective value in force (the global `AbortSignal` is accepted by `Request` and its abort propagates), as the environment overrides globals (`implementation-planning` Repeatable, Isolated Verification). The `@/` alias resolves to `frontend/src` (`frontend/vitest.config.ts:18-19`), so `@/../tests/mocks/setup` is the same setup module the setup file loads.

## Execution Steps

All commands run in `frontend/` unless stated, in one Git Bash shell. Logs go to a temporary folder outside the repository; only summaries and failing tests are recorded.

1. From the repository root: `LOGS="$(mktemp -d)"`, then `git status --short` — expect only `?? docs/.ai/auth-consent/`. Anything else: stop and report.
2. AUV-4: `npm ci > "$LOGS/aum2-npm-ci.log" 2>&1` — expect exit 0.
3. Baseline (unmodified repository), AUV-5: `npx vitest run > "$LOGS/aum2-baseline-full.log" 2>&1`. Record the summary and the list of failing tests (the ` FAIL ` lines). Expected / Predicted — Not Yet Verified: `Tests  90 failed | 282 passed (372)`, 27 in `tests/tts.spec.tsx`, 63 in `tests/voice.spec.tsx` (`Plan.md` Current State). If the failing tests are not 90 tests within those two files, stop and report the difference before changing any file.
4. Create `frontend/.vitest/aum2-check/account-client-delivery.check.spec.ts` with the exact content above. Run `npx vitest run .vitest/aum2-check > "$LOGS/aum2-check-baseline.log" 2>&1` — expect exit 1, `Tests  2 failed (2)`, each with `TypeError: RequestInit: Expected signal ("AbortSignal {}") to be an instance of AbortSignal.`
5. Create `frontend/tests/environment/jsdom-node-abort.ts` with the exact content above. Write the `frontend/vitest.config.ts` diff above, exactly, to `"$LOGS/vitest.config.diff"` (outside the repository); from the repository root run `git apply --check "$LOGS/vitest.config.diff"` and then `git apply "$LOGS/vitest.config.diff"`.
6. `npx vitest run .vitest/aum2-check > "$LOGS/aum2-check-after.log" 2>&1` — expect exit 0, `Tests  2 passed (2)`, and no `Expected signal` text in the log (`grep -c "Expected signal" "$LOGS/aum2-check-after.log"` → `0`).
7. Second run of only the check, without cleaning: `npx vitest run .vitest/aum2-check > "$LOGS/aum2-check-after-2.log" 2>&1` — expect the same result.
8. Delete the check: `rm -rf .vitest` (the folder did not exist before step 4). Confirm `ls -a` shows no `.vitest`.
9. AUV-6: `npm run type-check > "$LOGS/aum2-typecheck.log" 2>&1` — expect exit 0.
10. AUV-5: `npx vitest run > "$LOGS/aum2-full-after.log" 2>&1`. Compare its failing-test list with step 3's.
11. From the repository root: `git status --short` — expect exactly ` M frontend/vitest.config.ts`, `?? docs/.ai/auth-consent/`, `?? frontend/tests/environment/`; and `git diff --stat -- frontend/src frontend/tests frontend/package.json frontend/package-lock.json` prints nothing.
12. Record the evidence in `Plan.md` Execution Status for AUM-2.

## Acceptance / Completion Criteria

- **FTC-1** With the change applied, the temporary check's second case passes: a request made by `AuthClient.login`, carrying the abort signal `HttpClient` attaches, is received by the msw handler with method `POST`, path `/auth/login` and the sent body, and `login` resolves with the handler's answer; the check log contains no `Expected signal` rejection.
- **FTC-2** With the change applied, the check's first case passes: the global `AbortSignal` in force is accepted by the global `Request`, and aborting its controller aborts the request's signal. Both cases pass on a second run without cleaning.
- **FTC-3** On the unmodified repository, the same check fails, both cases with the `RequestInit: Expected signal` `TypeError` (the prerequisite was missing).
- **FTC-4** `npm run type-check` (AUV-6) exits 0.
- **FTC-5** (AUM2-Q2) The full frontend suite (AUV-5) after the change has no failing test that is not in step 3's baseline failure list, which itself matches the 90 known failures named in `Plan.md` Current State. A baseline-listed test that now passes is recorded by name; it is not a failure. The known failures are not fixed here.
- **FTC-6** The only repository changes are the created `frontend/tests/environment/jsdom-node-abort.ts` and the one-line change to `frontend/vitest.config.ts`, apart from `docs/.ai/auth-consent/` and this milestone's Execution Status update in `Plan.md`. No file under `frontend/src/` changes; no test file or msw handler is added or changed; `frontend/package.json` and `frontend/package-lock.json` are unchanged; `frontend/.vitest/` does not exist after execution.

## Verification

### Commands

| Step | Command (in `frontend/`) | Demonstrates |
| --- | --- | --- |
| 3 | `npx vitest run` on the unmodified repository (AUV-5) | baseline for FTC-5 |
| 4 | `npx vitest run .vitest/aum2-check` before the change | FTC-3 |
| 6, 7 | `npx vitest run .vitest/aum2-check` after the change, twice | FTC-1, FTC-2 |
| 9 | `npm run type-check` (AUV-6) | FTC-4 |
| 10 | `npx vitest run` (AUV-5) | FTC-5 |
| 1, 8, 11 | `git status --short`; `git diff --stat -- frontend/src frontend/tests frontend/package.json frontend/package-lock.json`; `ls -a` | FTC-6 |

### Affected Tests

All five frontend test files: `frontend/tests/auth-api.spec.tsx`, `frontend/tests/auth.spec.tsx`, `frontend/tests/tts-provider-choice.spec.tsx`, `frontend/tests/tts.spec.tsx`, `frontend/tests/voice.spec.tsx` (372 tests). Found by: the changed `environment` setting in `frontend/vitest.config.ts` applies to every test file, and no file overrides it (Current Repository State). Tests that reach `HttpClient` (and so the changed signal path): none found — `grep` for `authClient|AuthClient|httpClient|HttpClient|tokenInterceptor` in `frontend/tests` finds only comments in `auth-api.spec.tsx`, and `AuthProvider` (used by `tts.spec.tsx:25` and `voice.spec.tsx:22`) makes no account-client call (`frontend/src/context/AuthContext.tsx`, `grep` for `authClient|fetch` finds none). `frontend/src/components/VoiceUpload.tsx:30`, `:261`, `:314` create and abort an `AbortController` without passing its signal anywhere.

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- Step 4: `Tests  2 failed (2)`, `TypeError: RequestInit: Expected signal ("AbortSignal {}") to be an instance of AbortSignal.`
- Steps 6 and 7: `Tests  2 passed (2)`; `grep -c "Expected signal"` → `0`.
- Step 9: `tsc --noEmit` exit 0.
- Step 3 and step 10: `Tests  90 failed | 282 passed (372)`, the same 90 tests (27 `tests/tts.spec.tsx`, 63 `tests/voice.spec.tsx`).
- Step 11: ` M frontend/vitest.config.ts`, `?? docs/.ai/auth-consent/`, `?? frontend/tests/environment/`; empty `git diff --stat`.

FOUNDATION decisions binding AUM-3 and AUM-7, for review:

- **FTD-1 Mechanism: a custom vitest environment that is the built-in jsdom environment with Node's `AbortController` and `AbortSignal` kept.** Chosen because it changes no production code, adds no dependency, and keeps the abort signal working. Alternatives: (a) a `fetch` wrapper in `tests/mocks/setup.ts` that drops the signal — requests could no longer be aborted in tests, so the timeout path would differ from production; (b) the `happy-dom` environment — a new dependency and a different DOM for all 372 tests; (c) a `fetch` polyfill over XMLHttpRequest (for example `whatwg-fetch`) — a new dependency replacing Node's `fetch` for all tests; (d) upgrading vitest or msw — version changes for every test; that either upgrade alone removes the rejection is an unverified hypothesis; (e) changing `HttpClient` — excluded by `Plan.md` AUM-2 and AUR-7.
- **FTD-2 Scope: every frontend test file, through `vitest.config.ts`.** Alternative: a per-file `// @vitest-environment ./tests/environment/jsdom-node-abort.ts` comment in each AUM-3 and AUM-7 test file — would leave existing files AUM-7 changes (for example `tests/voice.spec.tsx`) under a different environment from new ones, and every RED file would have to remember it.
- **FTD-3 Location: `frontend/tests/environment/jsdom-node-abort.ts`,** next to the existing test setup `tests/mocks/setup.ts`. It contains no test cases and does not match vitest's test-file pattern (`*.{test,spec}.*`), so it is test infrastructure, not a test. Alternative: a local `vitest-environment-<name>` package (more files and a `package.json` entry).
- **FTD-4 Constraint on AUM-3 and AUM-7 tests: the global `AbortController` and `AbortSignal` are Node's.** A RED test that passes such a signal to a jsdom DOM API (for example `addEventListener(type, listener, { signal })`) may be rejected by jsdom — a hypothesis from jsdom's type checks, not exercised: no frontend source or test does this (`grep` for `signal|AbortController|AbortSignal` finds only `httpClient.ts:89-100` and `VoiceUpload.tsx:30`, `:261`, `:314`).
- **FTD-5 Verification check location: a temporary file in the git-ignored `frontend/.vitest/aum2-check/`, deleted after the run.** `Plan.md` AUM-2 excludes writing tests, and vitest 1.6.1 with this config could not load a check placed outside `frontend/` (dry run D1). Alternative: keep it as a permanent repository test — excluded by the Plan.

- Preserved-behavior tests (expected to pass at RED): not applicable — FOUNDATION milestone.

### Planning-Time Dry Run

Planning-time dry run — not milestone evidence. Disposable copy: `git archive HEAD frontend` extracted to `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/dry-aum2/` (outside the repository), `npm ci` there (exit 0). The baseline full-suite result reused is the AUM-2 planning dry run of 2026-11-16 at the same HEAD (`Tests  90 failed | 282 passed (372)`; 27 `tts.spec.tsx`, 63 `voice.spec.tsx`), not rerun.

| ID | Command (in the copy's `frontend/`) | Result |
| --- | --- | --- |
| D1 | `npx vitest run --dir ../check` with a one-assertion spec `t.spec.ts` in `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/dry-aum2/check/` (beside, not inside, the copy's `frontend/`) | `Error: Failed to load url C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/dry-aum2/check/t.spec.ts (resolved id: the same path). Does the file exist?` (the same for `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/aum2-trivial/`); the same spec in `frontend/.vitest/aum2-check/` → `Tests 1 passed (1)`. Why vitest refuses a file outside the root is not established (hypothesis: Vite's file-access restriction to the project root) |
| D2 | check file in `.vitest/aum2-check/`, unmodified config: `npx vitest run .vitest/aum2-check` | exit 1, `Tests 2 failed (2)`, both `TypeError: RequestInit: Expected signal ("AbortSignal {}") to be an instance of AbortSignal.`, thrown at `@mswjs/interceptors/src/interceptors/fetch/index.ts:42:23` |
| D3 | create `tests/environment/jsdom-node-abort.ts`; `git apply --check -v` then `git apply` of the `vitest.config.ts` diff | `Checking patch frontend/vitest.config.ts...`; applied; line 8 now `environment: './tests/environment/jsdom-node-abort.ts',` |
| D4 | `npx vitest run .vitest/aum2-check` | exit 0, `Tests 2 passed (2)` |
| D5 | `npx vitest run .vitest/aum2-check --environment jsdom` (built-in environment forced, change otherwise applied) | exit 1, `Tests 2 failed (2)`, same `TypeError` |
| D6 | `rm -rf .vitest`; `npm run type-check` | exit 0 |
| D7 | `npx tsc --noEmit --skipLibCheck --module esnext --moduleResolution bundler --target es2020 --strict --types node tests/environment/jsdom-node-abort.ts` (extra check; the file is outside AUV-6's `include`) | exit 0, no output |
| D8 | `npx vitest run` | DRY_RUN_FULL_RESULT |

Created during planning, all outside the repository: the disposable copy `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/dry-aum2/`, the drafts `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/aum2-check/` and `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/aum2-exact/`, and a one-assertion spec folder `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/aum2-trivial/` — all deleted afterwards. Logs kept: `C:/Users/avina/AppData/Local/Temp/claude/149227430f0b9316/d6411997-208c-4ff0-8720-e5a1ae00f5c7/scratchpad/logs/aum2-npm-ci.log`, `aum2-probe-baseline.log`, `aum2-check-after.log`, `aum2-check-builtin-jsdom.log`, `aum2-typecheck.log`, `aum2-tsc-env.log`, `aum2-full-after.log`, `aum2-baseline-fails.txt` in that folder.

## Risks

- **FTD-4 constraint** (above): a later RED test that passes a Node abort signal to a jsdom DOM API may be rejected. Mitigation within scope: recorded here as a binding decision so AUM-3 and AUM-7 plans avoid it; none of the current code does it.
- **Unsupported test-tool versions.** vitest 1.6.1 and msw 1.3.5 are older major versions; this plan relies on vitest 1.x's `vitest/environments` export and environment loader (`node_modules/vitest/dist/worker.js:44-56`). No version is changed here. A later upgrade would need to re-check this file.
- Identity, role or ownership comparisons: none — this milestone touches no authentication or authorization code.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Reverse only this milestone's changes: delete `frontend/tests/environment/jsdom-node-abort.ts` and the then-empty `frontend/tests/environment/`; reverse the diff with `git apply -R "$LOGS/vitest.config.diff"` from the repository root; delete `frontend/.vitest/` if it exists.

## Explicitly Out of Scope

- Any change under `frontend/src/`, including `HttpClient`'s timeout and abort signal (Plan AUM-2 exclusions, AUR-7).
- Writing, changing or deleting any test, test mock or msw handler, including `frontend/tests/mocks/auth-handlers.ts` and its msw 2 imports (AUM-3 scope).
- Any account, session, token-check, ownership or consent behavior (AUM-3–AUM-8).
- Fixing the known pre-existing failures in `tts.spec.tsx` and `voice.spec.tsx`, the backend run's exit-code-127 abort, or `test_production_inference_module_missing` (AUM2-Q2).
- Any dependency, version or `package.json` change; any backend change; AX-1–AX-5.

## Human Review

Status: Executed — approved by Avinash Srivastava on 2026-11-16; executed and verified 2026-11-16, see `Plan.md` Execution Status, "AUM-2 evidence".
