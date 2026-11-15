# Implementation Plan — chatterbox-original-app OAM-6 (TTS page RED)

## Milestone

OAM-6 — TTS page RED (`docs/.ai/chatterbox-original-app/Plan.md`, Milestones, OAM-6).

## Milestone Type

RED. `Plan.md` records OAM-6 as RED with no preceding FOUNDATION milestone (Milestones, OAM-6, Prerequisites; Milestone boundaries, "No FOUNDATION milestone").

## Review Summary

- Behavior change: tests only.
- Requirements verified, not delivered: the page parts of COA-1, COA-3, COA-4, COA-5, COA-7, COA-13 and COA-17. Owned: COA-17's test-change part (the cap tests and the test mock change to match).
- Files: created `frontend/tests/tts-provider-choice.spec.tsx`; modified `frontend/tests/tts.spec.tsx` (M3.1.2, M3.1.6, M3.1.7, M3.1.8, M3.3.2, M3.3.5) and `frontend/tests/mocks/tts-handlers.ts` (the 5000-character rejection removed); deleted none.
- Tests added: 19 (10 tests, 2 parametrized). They prove that the page offers only Google and Chatterbox and names the provider in the request; that it lists only recorded and uploaded voices for Chatterbox; that it offers and sends English or Hindi; that it shows each of the nine Chatterbox failure messages; that it plays a finished Chatterbox generation; that it keeps Generate disabled while a generation runs; and that it keeps and sends long text whole with a plain count and no limit label. The inference and voice services are mocked; nothing fakes or calls Chatterbox.
- Verification: `npx vitest run tests/tts-provider-choice.spec.tsx`, then `npx vitest run tests/tts.spec.tsx` (in `frontend/`). Expected / Predicted — Not Yet Verified: `19 failed (19)`, then `31 failed | 63 passed (94)`, where the 31 are the 27 named pre-existing failures plus the 4 changed M3.1 tests.
- Needs attention: T6Q-1 is answered (a): exactly the 27 named pre-existing `tts.spec.tsx` failures are accepted. Also decisions T6D-3 to T6D-7, the page seams that bind OAM-7, and T6R-1: three Chatterbox tests fail at RED on the missing Chatterbox voice list, because their display code already exists. Revision 2 (after the stopped run): only the stated baseline cause of the 10 history tests (T6C-6, command 4's last check, Current Repository State) and the order of commands 3 and 4 (Execution Step 5) change; see Revision 2 Changes.

## Authoritative References

| Document | Status read |
| --- | --- |
| `docs/.ai/chatterbox-original-app/requirements.md` | "Approved by Avinash Srivastava on 2026-11-13 (revision recording Q46–Q48 …)" |
| `docs/.ai/chatterbox-original-app/Plan.md` | Status "Approved by Avinash Srivastava on 2026-11-13, as written …". Execution Status: OAM-1 to OAM-5 complete, OAM-6 `Pending`. Re-read for revision 2: OAM-6 is `Blocked`, with "OAM-6 stopped execution evidence" (test files rolled back); Status unchanged |
| `docs/.ai/chatterbox-original-app/API-Contract.md` | Contract Review Status "Approved by Avinash Srivastava on 2026-11-13, as written". The OAM-1 row in `Plan.md` Execution Status is Complete and points to it. It is the authoritative predecessor for the request and answer shapes the tests mock |
| `docs/.ai/chatterbox-original-app/001_Implementation_Plan_OAM-2.md` | "Executed on 2026-11-13; valid RED established … (Approved … including decisions V2D-1 to V2D-6.)" Review Summary and Carried-Forward Decisions read |
| `docs/.ai/chatterbox-original-app/002_Implementation_Plan_OAM-3.md` | "Revision 4 approved … Executed 2026-11-13". Review Summary and Carried-Forward Decisions read |
| `docs/.ai/chatterbox-original-app/003_Implementation_Plan_OAM-4.md` | "Superseded — not executed … none of its decisions is carried forward" |
| `docs/.ai/chatterbox-original-app/004_Implementation_Plan_OAM-4.md` | "Executed — RED verified 2026-11-13 … (Approved … including decisions N4D-1 to N4D-6.)" Review Summary and Carried-Forward Decisions read |
| `docs/.ai/chatterbox-original-app/005_Implementation_Plan_OAM-5.md` | "Executed 2026-11-13 — GREEN verified … (Approved … including decisions N5D-1 to N5D-8 …)" Review Summary and Carried-Forward Decisions read |
| `docs/requirements.md` | Does not exist (`ls docs/requirements.md`: "No such file or directory") |

None of the earlier Implementation Plans' exact code touches a file in this milestone's scope, so none was read for code. Labels this plan introduces use the prefix `T6` (`T6D-` decisions, `T6Q-` questions, `T6C-` criteria, `T6R-` risks). No referenced artifact defines it (`grep -rnoE "\bT6[A-Z]-?[0-9]*" docs/.ai/` found no match).

## Carried-Forward Decisions

- **V3Q-1 (a)** (`002_Implementation_Plan_OAM-3.md:730-736`), as later plans applied it (`005_Implementation_Plan_OAM-5.md`, Carried-Forward Decisions): only the failing tests a plan names are accepted as pre-existing failures, and any other failure fails the milestone. That decision covered backend runs. How it applies to the 27 frontend failures this milestone runs is question T6Q-1, because `Plan.md` (Non-Blocking Open Decisions) gives that choice to the user for each frontend Implementation Plan.
- **COA-16 test boundary** (`004_Implementation_Plan_OAM-4.md`, N4D-2, carried into `005`): no test makes a lookup outside this machine. Applied here as T6D-1: every request the new tests cause is answered in the test process.

No earlier plan decided anything about the frontend, its test tooling or the TTS page.

## Preconditions / Predecessor Evidence

- OAM-5 is complete: "Complete — GREEN verified 2026-11-13" (`Plan.md`, Execution Status). Its evidence records the inference service answering `provider` and `language`, listing `chatterbox`, and the four pre-call `503` messages (`Plan.md`, OAM-5 GREEN evidence, commands 2–3). Those are the answers these tests mock.
- HEAD is `ce598d4` ("Add Chatterbox generation to the inference service (OAM-5)"). `git status --short` printed nothing at planning time. `git diff --stat ce598d4 -- frontend` is empty, so no frontend file has changed since the Plan's Current State, which was inspected at `664cee4` (`Plan.md:46`). Revision 2: HEAD is `b8704a6`, and `git diff --stat ce598d4 b8704a6` lists only this plan; `git status --short -- frontend` printed nothing (2026-11-14).
- OAM-6 is `Pending`, and no Implementation Plan for OAM-6 exists in the folder (`ls docs/.ai/chatterbox-original-app/`: `001`–`005`, `API-Contract.md`, `Plan.md`, `requirements.md`).
- Prerequisites (Plan Content Rule 11) are present. The lockfile installs vitest 1.6.1, jsdom 23.2.0, @testing-library/react 16.3.3, @testing-library/user-event 14.6.8 and msw 1.3.5 (`npm ls`). msw 1.3.5 intercepts `fetch` in Node: `node_modules/msw/lib/node/index.js` uses `FetchInterceptor`. No dependency or configuration change is needed.
- Baseline (planning-time observation on the unmodified tree, HEAD `ce598d4`, 2026-11-13):
  - `npx vitest run` (in `frontend/`): `Test Files 2 failed | 2 passed (4)`, `Tests 90 failed | 263 passed (353)`. The failing names match the lists in `Plan.md:39-40` exactly: 27 in `tts.spec.tsx` and 63 in `voice.spec.tsx`.
  - `npm run type-check`: exit 0.
  - Nothing listens on ports 8002 or 8003 (`netstat -ano | grep LISTENING | grep -E ":(8002|8003) "` printed nothing).

## Current Repository State

The facts the exact code depends on:

- The page renders the error display, the form, the player and the history: `frontend/src/pages/TextToSpeech.tsx:65`, `:70`, `:85`, `:95`. It loads a ready generation's audio from the download operation into an object URL: `TextToSpeech.tsx:36-51`, `frontend/src/services/ttsApi.ts:102-114`.
- The generation request body holds only `script` and `voice_id` (`ttsApi.ts:49-50`). A failure throws the body's `error` text (`ttsApi.ts:56`), which the page shows under "Generation Failed" in `data-testid="error-display"` (`frontend/src/components/GenerationErrorDisplay.tsx:43`, `:48`, `:50`).
- Providers come from `GET /inference/backends`. Each backend becomes a radio, `provider-option-<name>` / `provider-radio-<name>`. The display name is the description before ` (`, and every option carries the "Max 5000 chars/request" label (`ttsApi.ts:182-201`, `:197`, `:199`; `frontend/src/components/ProviderSelector.tsx:73`, `:83`, `:89`). The initial provider is `google` (`frontend/src/context/TTSContext.tsx:12`), and the selector keeps it (`ProviderSelector.tsx:25`). Whenever the provider changes, the selector fetches again and briefly shows "Loading providers..." (`ProviderSelector.tsx:36`, `:42-44`).
- Voices come from `GET /voices/approved` on the voice service (`ttsApi.ts:203-216`). The selector keeps only Google-pattern voices when any exist, and preselects the first (`frontend/src/components/VoiceSelector.tsx:21-39`). It fetches again whenever the selected voice changes (`VoiceSelector.tsx:48`) and renders `data-testid="voice-select"` (`:84`).
- The text box truncates at 5000 characters and sets `maxLength` (`frontend/src/components/TextToSpeechInput.tsx:4`, `:15`, `:34`). It shows "n / 5000" in `char-count` (`:44`, `:46`), `char-warning` at 90% (`:50`) and `max-chars-warning` at 5000 (`:66-67`). Its `data-testid` is `text-input` (`:36`).
- Generate is `data-testid="generate-button"` and is disabled while a submission is pending (`frontend/src/components/GenerationSubmitForm.tsx:133`, `:139`).
- The player sets the audio element's `src` to the object URL (`frontend/src/components/AudioPlayer.tsx:20`, `:68`, `:70`).
- Test setup: one msw server per test file, `server.listen()` with no unhandled-request option (`frontend/tests/mocks/setup.ts:7`), so msw warns about unmatched requests and sends them to the network. `URL.createObjectURL` is stubbed when jsdom lacks it (`setup.ts:107-108`). `tests/` is not covered by `npm run type-check`, because `frontend/tsconfig.json` includes only `src`.
- `tts.spec.tsx` registers only `ttsHandlers` (`frontend/tests/tts.spec.tsx:56-58`). Those serve `/generate`, `/providers` and `/voices` on port 8003 (`frontend/tests/mocks/tts-handlers.ts:18-242`), not the endpoints the page calls. That is the observed cause of the 27 `tts.spec.tsx` failures. In 17 of them a selector renders `provider-error` or `voice-selector-error` "fetch failed" (baseline log, for example M3.3.2 and M3.3.5). In the other 10 (M3.7.1–M3.7.7, M3.11.3, M3.11.5, M3.12.5) the history fetch fails: `GenerationHistory.tsx:35-36` catches it and logs `Failed to fetch history: [TypeError: fetch failed]` (cause `ECONNREFUSED`) on stderr, and the component shows `data-testid="empty-state"` "No generations yet" (`:120-121`) instead of `generation-history-container` (`:130`) (revision 2 baseline, Planning-Time Dry Run). The default handler's 5000-character rejection is at `tts-handlers.ts:27-29`. Only `tts.spec.tsx` imports `tts-handlers.ts` (`grep -rn "tts-handlers" frontend/tests`).
- The contract's provider list is `azure`, `chatterbox`, `google`, `mock`. The page can send only `google` or `chatterbox` as `provider`. The Chatterbox display name is "Chatterbox voice cloning" (`API-Contract.md`, Inference Provider List). The repository's descriptions for the others are at `voice_narration/inference/application.py:384-388`. Preloaded voices carry `"provider": "google"`, and recorded and uploaded voices have no `provider` (`API-Contract.md`, Voice List; `voice_narration/simple_voices/application.py:19-65`).

## Files in Scope

### Files to Create

- `frontend/tests/tts-provider-choice.spec.tsx`

### Files to Modify

- `frontend/tests/tts.spec.tsx`
- `frontend/tests/mocks/tts-handlers.ts`

### Files to Delete

None.

## Proposed Changes

1. **Create `frontend/tests/tts-provider-choice.spec.tsx`** (Plan OAM-6 Scope, bullets 1–7). It renders the whole `TextToSpeech` page inside an authenticated `AuthContext` and a `TTSProvider` (T6D-2). It mocks the inference service and the voice service with msw handlers registered in `beforeEach` (T6D-1):
   - `GET /inference/backends` answers the contract's four backends.
   - `GET /voices/approved` answers two preloaded Google voices, one recorded voice and one uploaded voice.
   - `GET /inference/generations` answers an empty history.
   - `POST /inference/jobs/:jobId/infer` records `{jobId, body}`, optionally waits on a gate, then answers the per-test `inferAnswer`: `200 {job_id, status: "complete", duration_seconds}` by default.
   - `GET /inference/jobs/:jobId/download` records the job id and answers a 4-frame PCM WAV as `audio/wav`.
   - A final `rest.all('*')` records the request and answers `501`. `afterEach` asserts that nothing was recorded.

   Helpers: `renderPage`, `offeredProviders`, `offeredVoiceIds`, `languageOptions`, `waitForChatterboxVoices`, `chooseChatterbox`, `chooseVoice`, `chooseLanguage`, `enterText`, `generate`, `wavFile`, `blobBytes`. Tests:
   - OAM-6.1 (COA-1): the page offers exactly `google` and `chatterbox`. Google is selected first, and the display names show.
   - OAM-6.2 (COA-1): a Google generation request carries `provider: "google"`.
   - OAM-6.3 (COA-3): with Chatterbox chosen, the voice list is exactly the recorded and uploaded voices, the first is preselected, and the request is exactly `{script, voice_id, provider: "chatterbox", language: "en"}` for the voice chosen.
   - OAM-6.4 ×2 (COA-5): with Chatterbox chosen, the language control offers English (`en`) and Hindi (`hi`), with English preselected, and the request carries the language chosen.
   - OAM-6.5 ×9 (COA-7): for each of the contract's nine OAF messages, answered `503`, the error display shows the message. No player is shown and no download is made.
   - OAM-6.6 (COA-4): a finished Chatterbox generation's download (same `job_id`) is loaded into the player: the object URL is created from the downloaded WAV bytes, typed `audio/wav`, and the audio element's `src` is that URL.
   - OAM-6.7 (COA-13): while the Chatterbox request is held open, Generate is disabled. After release the player appears, and exactly one request was sent.
   - OAM-6.8 (COA-17): 6600-character text is kept whole, with no `maxlength`, a count of "6600 characters", and no "/ 5000", 90% warning or maximum-reached message. It is sent whole with `provider: "google"`, and a Google rejection (`500 Inference failed: …`) shows under "Generation Failed".
   - OAM-6.9 (COA-17): the same text is kept whole with Chatterbox chosen and sent whole in a Chatterbox request.
   - OAM-6.10 (COA-17, OAR-6): with the provider list reached, no "chars/request" label shows.
2. **Modify `frontend/tests/tts.spec.tsx`** (Plan OAM-6 Scope bullet 8; requirements COA-17; Plan Current State, `:33`):
   - M3.1.2 (`:83`): the count reads exactly "0 characters".
   - M3.1.6 (`:113-121`): retitled "should keep text exceeding 5000 characters whole". It asserts that all 5001 characters are kept and that there is no `maxlength`.
   - M3.1.7 (`:130`): the count reads exactly "`<length>` characters".
   - M3.1.8 (`:133-144`): retitled "should show no capacity warning or limit message for long text". With 5000 characters the count reads "5000 characters", and neither `char-warning`, the 90% text, `max-chars-warning` nor the maximum-reached text is shown.
   - M3.3.2 (`:255-257`): asserts that no `Max \d+ chars/request` label shows. Its existing wait for "Google Text-to-Speech" is unchanged.
   - M3.3.5 (`:290-293`): waits for `provider-selector-container`, then asserts that no label shows. Titles of M3.3.2 and M3.3.5 are unchanged (T6D-8).
3. **Modify `frontend/tests/mocks/tts-handlers.ts`** (COA-17; `Plan.md:33`): remove the default `POST /generate` handler's `text.length > 5000` rejection (`:27-29`) and the blank line after it. `errorResponses.textTooLong` and `ttsErrorHandlers.textTooLong` stay: no test uses them (`grep -rn textTooLong frontend/tests`), and they are not the rejection `Plan.md` names.

### Decisions for review

Added because these test choices bind OAM-7, and the Plan leaves two of them to this plan (Non-Blocking Open Decisions).

- **T6D-1 Mock boundary and isolation.** The new tests mock the inference service (8003) and the voice service (8002) with msw handlers in the new file. A catch-all answers every other request, and `afterEach` asserts that none was made. So no request leaves the test process, even when local services are running. The page never calls Chatterbox. The "successful Chatterbox result" is the inference service's `200` answer plus a WAV download built in the test (COA-16). Alternatives: (a) add the handlers to the shared `tts-handlers.ts`. Rejected: `Plan.md` limits changes to existing tests and the mock to the cap items (OAM-6 exclusions). (b) `vi.mock` the `ttsApi` module. Rejected: the tests would no longer observe the request body the page actually sends (`testing`: assert what the unit produced).
- **T6D-2 Render the whole page.** The error display and the player exist only at page level (`TextToSpeech.tsx:65`, `:85`). Alternative: render `GenerationSubmitForm` alone. Rejected: it cannot show the failure message or the player.
- **T6D-3 Providers offered (binds OAM-7).** The page offers exactly the backends named `google` and `chatterbox`, as radios `provider-radio-<name>` and `provider-option-<name>` (existing IDs). Google stays selected first (existing `TTSContext.tsx:12`), and the display names are derived as today. Reason: the contract accepts only `google` and `chatterbox` as `provider`, and answers anything else `400` (`API-Contract.md`, Inference Generation failure 3, and "Listing a provider does not make it selectable"). COA-1 names the choice as "Google narration or Chatterbox cloning". Alternative: keep all four listed. Rejected: choosing mock or Azure would always fail with `400`.
- **T6D-4 Voices for Chatterbox (binds OAM-7; Plan Non-Blocking Open Decision 2).** With Chatterbox chosen, the voice list is exactly the voices without a `provider` field, in list order. Google voices are not listed, and the first recorded or uploaded voice is preselected. Reason: a Google voice has no sample, so Chatterbox would answer OAF-3 ("voice sample … could not be read") for it (`API-Contract.md`, Voice Sample failure 2, OAF-3). Alternative: list Google voices as well. Not chosen: the user could only get an OAF-3 failure from them.
- **T6D-5 Language control (binds OAM-7; Plan Non-Blocking Open Decision 1).** A `<select data-testid="language-select">` with options `en` "English" and `hi` "Hindi", in that order, with English preselected, present when Chatterbox is chosen. Whether it is hidden for Google is not asserted, and OAM-7 decides it. Alternatives: Hindi preselected; nothing preselected, with Generate disabled until a language is chosen; radio buttons.
- **T6D-6 Request body (binds OAM-7).** A Chatterbox request body is exactly `{script, voice_id, provider: "chatterbox", language}`. A Google request carries `provider: "google"`; whether it also carries `language` is not asserted, because the contract ignores it for Google. Alternative: send no `provider` for Google, which the contract treats the same. Rejected: Plan OAM-6 scope requires that "the generation request names the chosen provider".
- **T6D-7 Count and long text (binds OAM-7).** `char-count` reads exactly "`<n>` characters". The text box has no `maxlength`, and `char-warning` and `max-chars-warning` are absent. The long text is 6600 characters.
- **T6D-8 Titles of changed existing tests.** M3.1.6 and M3.1.8 are retitled to describe their new assertions. M3.3.2 and M3.3.5 keep their titles, so they stay identifiable as two of the named pre-existing failures (`Plan.md:39`). Alternative: retitle M3.3.5, whose title mentions "max chars". Then the named-failure list would no longer match it.

## Proposed Code / Tests

The content below is for review only. It was not applied to the repository during planning.

### `frontend/tests/tts-provider-choice.spec.tsx` (create, complete content)

SHA-256 of this block's content, with LF line endings: `de6f2493c63f319ec9c6a71eab2b1988b069d35b222211f3a361058c3fd22a24`.

```tsx
// ============================================================================
// OAM-6 RED: TTS page provider, voice and language per generation, and no text cap
// (chatterbox-original-app; requirements COA-1, COA-3, COA-4, COA-5, COA-7, COA-13, COA-17).
//
// The inference service (port 8003) and the voice service (port 8002) are mocked with msw.
// The page never talks to Chatterbox; no test fakes or calls Chatterbox (COA-16).
// A catch-all handler answers every other request, so no request leaves the test process.
// ============================================================================

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';
import { rest } from 'msw';

import { server } from './mocks/setup';
import { TextToSpeech } from '../src/pages/TextToSpeech';
import { TTSProvider } from '../src/context/TTSContext';
import { AuthContext } from '../src/context/AuthContext';

const INFERENCE = 'http://localhost:8003';
const VOICES = 'http://localhost:8002';

// Inference Provider List as the approved contract defines it (API-Contract.md, Inference Provider List).
const BACKENDS = [
  {
    name: 'azure',
    provider_class: 'AzureSpeechProvider',
    description: 'Azure Cognitive Services Speech (requires AZURE_SPEECH_KEY + AZURE_SPEECH_REGION)',
  },
  {
    name: 'chatterbox',
    provider_class: 'ChatterboxClient',
    description: 'Chatterbox voice cloning (deployed Cloud Run service)',
  },
  {
    name: 'google',
    provider_class: 'GoogleTextToSpeechProvider',
    description: 'Google Cloud Text-to-Speech (requires GOOGLE_APPLICATION_CREDENTIALS)',
  },
  {
    name: 'mock',
    provider_class: 'MockInferenceProvider',
    description: 'Deterministic mock for testing (no external deps)',
  },
];

// Approved Voice List as the approved contract defines it: preloaded Google voices carry
// "provider": "google"; recorded and uploaded voices carry no provider field.
const GOOGLE_VOICE = {
  id: 'en-US-Neural2-A',
  name: 'Google Neural2-A (US English)',
  provider: 'google',
  language: 'en-US',
  gender: 'Female',
  approvalScore: 100,
  status: 'approved',
};
const GOOGLE_HINDI_VOICE = {
  id: 'hi-IN-Neural2-A',
  name: 'Google Neural2-A (Hindi)',
  provider: 'google',
  language: 'hi-IN',
  gender: 'Female',
  approvalScore: 100,
  status: 'approved',
};
const RECORDED_VOICE = {
  id: 'voice-1a2b3c4d',
  name: 'My Chrome recording',
  format: 'WAV',
  duration: 45,
  fileSize: 48213,
  uploadedAt: '2026-11-13T10:00:00.000000',
  status: 'approved',
  approvalScore: 95,
};
const UPLOADED_VOICE = {
  id: 'voice-5e6f7a8b',
  name: 'Uploaded WAV voice',
  format: 'WAV',
  duration: 45,
  fileSize: 96044,
  uploadedAt: '2026-11-13T10:05:00.000000',
  status: 'approved',
  approvalScore: 95,
};
const APPROVED_VOICES = [GOOGLE_VOICE, GOOGLE_HINDI_VOICE, RECORDED_VOICE, UPLOADED_VOICE];

// The nine Chatterbox failure messages of the approved contract (Chatterbox Failure Causes,
// OAF-1 to OAF-9), with <N> = 1200 and <status> = 403 and 500.
const CHATTERBOX_FAILURE_MESSAGES = [
  'Chatterbox voice cloning is not configured. Please retry, or choose another provider.',
  'The Chatterbox time limit setting CHATTERBOX_TIMEOUT_SECONDS is invalid; it must be a positive whole number of seconds. Please retry, or choose another provider.',
  'The voice sample for the selected voice could not be read. Please retry, or choose another provider.',
  'Could not obtain an identity token for Chatterbox. Please retry, or choose another provider.',
  'Chatterbox did not respond within 1200 seconds. Please retry, or choose another provider.',
  'Could not connect to Chatterbox. Please retry, or choose another provider.',
  'Access to Chatterbox was denied (HTTP 403). Please retry, or choose another provider.',
  'Chatterbox returned an error (HTTP 500). Please retry, or choose another provider.',
  'Chatterbox returned a response that is not audio. Please retry, or choose another provider.',
];

// Text longer than the removed 5000-character cap (COA-17): 6600 characters.
const LONG_TEXT = 'Chatterbox long text. '.repeat(300);

// A short, valid PCM WAV file: 16-bit mono, 24000 Hz, four silent frames.
function wavFile(): ArrayBuffer {
  const frames = 4;
  const dataSize = frames * 2;
  const buffer = new ArrayBuffer(44 + dataSize);
  const view = new DataView(buffer);
  const ascii = (offset: number, text: string) => {
    for (let i = 0; i < text.length; i += 1) view.setUint8(offset + i, text.charCodeAt(i));
  };
  ascii(0, 'RIFF');
  view.setUint32(4, 36 + dataSize, true);
  ascii(8, 'WAVE');
  ascii(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, 24000, true);
  view.setUint32(28, 48000, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  ascii(36, 'data');
  view.setUint32(40, dataSize, true);
  return buffer;
}
const CLONED_WAV_FILE = wavFile();
const CLONED_WAV = new Uint8Array(CLONED_WAV_FILE);

// Reads a jsdom Blob, which has no arrayBuffer() method in this test environment.
function blobBytes(blob: Blob): Promise<Uint8Array> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(new Uint8Array(reader.result as ArrayBuffer));
    reader.onerror = () => reject(reader.error);
    reader.readAsArrayBuffer(blob);
  });
}

type InferAnswer = { status: number; body: Record<string, unknown> };
type InferRequest = { jobId: string; body: Record<string, unknown> };

let inferRequests: InferRequest[] = [];
let downloadRequests: string[] = [];
let unexpectedRequests: string[] = [];
let inferAnswer: InferAnswer = { status: 200, body: {} };
let inferGate: Promise<void> | null = null;

function completeAnswer(): InferAnswer {
  return { status: 200, body: { status: 'complete', duration_seconds: 4 / 24000 } };
}

beforeEach(() => {
  inferRequests = [];
  downloadRequests = [];
  unexpectedRequests = [];
  inferAnswer = completeAnswer();
  inferGate = null;
  server.use(
    rest.get(`${INFERENCE}/inference/backends`, (req, res, ctx) =>
      res(ctx.status(200), ctx.json({ backends: BACKENDS }))
    ),
    rest.get(`${VOICES}/voices/approved`, (req, res, ctx) =>
      res(ctx.status(200), ctx.json({ data: APPROVED_VOICES }))
    ),
    rest.get(`${INFERENCE}/inference/generations`, (req, res, ctx) =>
      res(ctx.status(200), ctx.json({ items: [], total: 0, skip: 0, limit: 100 }))
    ),
    rest.post(`${INFERENCE}/inference/jobs/:jobId/infer`, async (req, res, ctx) => {
      const jobId = String(req.params.jobId);
      const body = (await req.json()) as Record<string, unknown>;
      inferRequests.push({ jobId, body });
      if (inferGate) {
        await inferGate;
      }
      const answerBody = inferAnswer.status === 200 ? { job_id: jobId, ...inferAnswer.body } : inferAnswer.body;
      return res(ctx.status(inferAnswer.status), ctx.json(answerBody));
    }),
    rest.get(`${INFERENCE}/inference/jobs/:jobId/download`, (req, res, ctx) => {
      downloadRequests.push(String(req.params.jobId));
      return res(ctx.status(200), ctx.set('Content-Type', 'audio/wav'), ctx.body(CLONED_WAV_FILE));
    }),
    rest.all('*', (req, res, ctx) => {
      unexpectedRequests.push(`${req.method} ${req.url.href}`);
      return res(ctx.status(501), ctx.json({ error: 'unexpected request in test' }));
    })
  );
});

afterEach(() => {
  expect(unexpectedRequests).toEqual([]);
});

function AuthenticatedPage() {
  const [authState] = React.useState({
    user: null,
    token: 'mock-test-token',
    refreshToken: 'mock-refresh-token',
    isAuthenticated: true,
    isLoading: false,
    error: null,
  });

  return (
    <AuthContext.Provider value={{ ...authState, dispatch: () => {} }}>
      <TTSProvider>
        <TextToSpeech />
      </TTSProvider>
    </AuthContext.Provider>
  );
}

// Renders the TTS page and waits until its provider list and voice list have loaded.
async function renderPage() {
  render(<AuthenticatedPage />);
  await waitFor(() => {
    expect(screen.getByTestId('provider-radio-google')).toBeInTheDocument();
    expect(screen.getByTestId('provider-radio-chatterbox')).toBeInTheDocument();
  });
  await waitFor(() => {
    expect(screen.getByTestId('voice-select')).toHaveValue(GOOGLE_VOICE.id);
  });
}

function offeredProviders(): string[] {
  return screen.getAllByRole('radio').map((radio) => (radio as HTMLInputElement).value);
}

function offeredVoiceIds(): string[] {
  return within(screen.getByTestId('voice-select'))
    .getAllByRole('option')
    .map((option) => (option as HTMLOptionElement).value)
    .filter((value) => value !== '');
}

function languageOptions(): Array<[string, string]> {
  return within(screen.getByTestId('language-select'))
    .getAllByRole('option')
    .map((option) => [(option as HTMLOptionElement).value, option.textContent ?? '']);
}

type User = ReturnType<typeof userEvent.setup>;

// Waits until Chatterbox is chosen and the voice list shows exactly the recorded and uploaded voices.
async function waitForChatterboxVoices() {
  await waitFor(() => {
    expect(screen.getByTestId('provider-radio-chatterbox')).toBeChecked();
    expect(offeredVoiceIds()).toEqual([RECORDED_VOICE.id, UPLOADED_VOICE.id]);
  });
}

async function chooseChatterbox(user: User) {
  await user.click(screen.getByTestId('provider-radio-chatterbox'));
  await waitForChatterboxVoices();
}

async function chooseVoice(user: User, voiceId: string) {
  await user.selectOptions(screen.getByTestId('voice-select'), voiceId);
  await waitFor(() => {
    expect(screen.getByTestId('voice-select')).toHaveValue(voiceId);
  });
}

async function chooseLanguage(user: User, language: string) {
  await waitFor(() => {
    expect(screen.getByTestId('language-select')).toBeInTheDocument();
  });
  await user.selectOptions(screen.getByTestId('language-select'), language);
  await waitFor(() => {
    expect(screen.getByTestId('language-select')).toHaveValue(language);
  });
}

function enterText(text: string) {
  fireEvent.change(screen.getByTestId('text-input'), { target: { value: text } });
}

async function generate(user: User) {
  await waitFor(() => {
    expect(screen.getByTestId('generate-button')).not.toBeDisabled();
  });
  await user.click(screen.getByTestId('generate-button'));
  await waitFor(() => {
    expect(inferRequests).toHaveLength(1);
  });
}

describe('OAM-6: provider chosen per generation (COA-1)', () => {
  it('OAM-6.1: offers exactly Google and Chatterbox from the provider list, Google first selected', async () => {
    await renderPage();

    expect(offeredProviders().sort()).toEqual(['chatterbox', 'google']);
    expect(screen.getByTestId('provider-radio-google')).toBeChecked();
    expect(screen.getByTestId('provider-radio-chatterbox')).not.toBeChecked();
    expect(screen.getByText('Google Cloud Text-to-Speech')).toBeInTheDocument();
    expect(screen.getByText('Chatterbox voice cloning')).toBeInTheDocument();
  });

  it('OAM-6.2: a Google generation request names provider google', async () => {
    const user = userEvent.setup();
    await renderPage();

    enterText('Hello from Google narration.');
    await generate(user);

    expect(inferRequests[0].body).toMatchObject({
      script: 'Hello from Google narration.',
      voice_id: GOOGLE_VOICE.id,
      provider: 'google',
    });
    await waitFor(() => {
      expect(downloadRequests).toEqual([inferRequests[0].jobId]);
    });
  });
});

describe('OAM-6: recorded and uploaded voices for Chatterbox (COA-3)', () => {
  it('OAM-6.3: with Chatterbox chosen, lists only recorded and uploaded voices and sends the one chosen', async () => {
    const user = userEvent.setup();
    await renderPage();

    await chooseChatterbox(user);
    expect(screen.getByTestId('voice-select')).toHaveValue(RECORDED_VOICE.id);
    expect(screen.getByRole('option', { name: /My Chrome recording/ })).toBeInTheDocument();
    expect(screen.getByRole('option', { name: /Uploaded WAV voice/ })).toBeInTheDocument();

    await chooseVoice(user, UPLOADED_VOICE.id);
    enterText('Speak in my uploaded voice.');
    await generate(user);

    expect(inferRequests[0].body).toEqual({
      script: 'Speak in my uploaded voice.',
      voice_id: UPLOADED_VOICE.id,
      provider: 'chatterbox',
      language: 'en',
    });
  });
});

describe('OAM-6: English or Hindi for Chatterbox (COA-5)', () => {
  it.each([
    ['English', 'en'],
    ['Hindi', 'hi'],
  ])('OAM-6.4: with Chatterbox chosen, %s can be chosen and is sent', async (_name, language) => {
    const user = userEvent.setup();
    await renderPage();

    await user.click(screen.getByTestId('provider-radio-chatterbox'));
    await waitFor(() => {
      expect(languageOptions()).toEqual([
        ['en', 'English'],
        ['hi', 'Hindi'],
      ]);
    });
    expect(screen.getByTestId('language-select')).toHaveValue('en');

    await waitForChatterboxVoices();
    await chooseLanguage(user, language);
    enterText('Namaste and hello.');
    await generate(user);

    expect(inferRequests[0].body).toEqual({
      script: 'Namaste and hello.',
      voice_id: RECORDED_VOICE.id,
      provider: 'chatterbox',
      language,
    });
  });
});

describe('OAM-6: Chatterbox failure messages shown (COA-7)', () => {
  it.each(CHATTERBOX_FAILURE_MESSAGES)('OAM-6.5: shows the failure message "%s"', async (message) => {
    const user = userEvent.setup();
    inferAnswer = { status: 503, body: { error: message } };
    await renderPage();

    await chooseChatterbox(user);
    enterText('This clone will fail.');
    await generate(user);

    expect(inferRequests[0].body).toMatchObject({ provider: 'chatterbox', voice_id: RECORDED_VOICE.id });
    await waitFor(() => {
      expect(within(screen.getByTestId('error-display')).getByText(message)).toBeInTheDocument();
    });
    expect(screen.queryByTestId('audio-player-container')).not.toBeInTheDocument();
    expect(downloadRequests).toEqual([]);
  });
});

describe('OAM-6: cloned speech plays on the page (COA-4)', () => {
  it('OAM-6.6: loads the audio of a finished Chatterbox generation into the player', async () => {
    const createObjectURL = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:cloned-speech');
    try {
      const user = userEvent.setup();
      await renderPage();

      await chooseChatterbox(user);
      enterText('Hello in my own voice.');
      await generate(user);

      expect(inferRequests[0].body).toMatchObject({ provider: 'chatterbox', voice_id: RECORDED_VOICE.id });
      await waitFor(() => {
        expect(downloadRequests).toEqual([inferRequests[0].jobId]);
      });
      await waitFor(() => {
        const player = screen.getByTestId('audio-player-container');
        expect((within(player).getByTestId('audio-element') as HTMLAudioElement).src).toBe('blob:cloned-speech');
      });
      expect(createObjectURL).toHaveBeenCalledTimes(1);
      const loaded = createObjectURL.mock.calls[0][0] as Blob;
      expect(loaded.type).toBe('audio/wav');
      expect(await blobBytes(loaded)).toEqual(CLONED_WAV);
    } finally {
      createObjectURL.mockRestore();
    }
  });
});

describe('OAM-6: Generate disabled during a Chatterbox generation (COA-13)', () => {
  it('OAM-6.7: keeps the Generate button disabled while the Chatterbox generation is running', async () => {
    let release: () => void = () => {};
    inferGate = new Promise<void>((resolve) => {
      release = resolve;
    });
    try {
      const user = userEvent.setup();
      await renderPage();

      await chooseChatterbox(user);
      enterText('A long clone that takes a while.');
      await generate(user);

      expect(inferRequests[0].body).toMatchObject({ provider: 'chatterbox', voice_id: RECORDED_VOICE.id });
      expect(screen.getByTestId('generate-button')).toBeDisabled();

      release();
      await waitFor(() => {
        expect(screen.getByTestId('audio-player-container')).toBeInTheDocument();
      });
      expect(inferRequests).toHaveLength(1);
    } finally {
      release();
    }
  });
});

describe('OAM-6: no text length limit for any provider (COA-17)', () => {
  function expectLongTextKeptWhole() {
    const textInput = screen.getByTestId('text-input') as HTMLTextAreaElement;
    expect(textInput.value.length).toBe(LONG_TEXT.length);
    expect(textInput).toHaveValue(LONG_TEXT);
    expect(textInput).not.toHaveAttribute('maxlength');
    expect(screen.getByTestId('char-count')).toHaveTextContent(/^6600 characters$/);
    expect(screen.queryByText(/\/ 5000/)).not.toBeInTheDocument();
    expect(screen.queryByTestId('char-warning')).not.toBeInTheDocument();
    expect(screen.queryByText(/90% capacity/i)).not.toBeInTheDocument();
    expect(screen.queryByTestId('max-chars-warning')).not.toBeInTheDocument();
    expect(screen.queryByText(/maximum character limit/i)).not.toBeInTheDocument();
  }

  it('OAM-6.8: sends text over 5000 characters whole to Google and shows the failed-generation error when Google rejects it', async () => {
    const user = userEvent.setup();
    const rejection = 'Inference failed: 400 Either `input.text` or `input.ssml` is longer than the limit of 5000 bytes.';
    inferAnswer = { status: 500, body: { error: rejection } };
    await renderPage();

    expect(LONG_TEXT).toHaveLength(6600);
    enterText(LONG_TEXT);
    expectLongTextKeptWhole();
    await generate(user);

    expect(inferRequests[0].body).toMatchObject({ script: LONG_TEXT, provider: 'google' });
    await waitFor(() => {
      const errorDisplay = screen.getByTestId('error-display');
      expect(within(errorDisplay).getByText('Generation Failed')).toBeInTheDocument();
      expect(within(errorDisplay).getByText(rejection)).toBeInTheDocument();
    });
    expect(downloadRequests).toEqual([]);
  });

  it('OAM-6.9: sends text over 5000 characters whole to Chatterbox', async () => {
    const user = userEvent.setup();
    await renderPage();

    enterText(LONG_TEXT);
    expectLongTextKeptWhole();
    await chooseChatterbox(user);
    expectLongTextKeptWhole();
    await generate(user);

    expect(inferRequests[0].body).toEqual({
      script: LONG_TEXT,
      voice_id: RECORDED_VOICE.id,
      provider: 'chatterbox',
      language: 'en',
    });
    await waitFor(() => {
      expect(downloadRequests).toEqual([inferRequests[0].jobId]);
    });
  });

  it('OAM-6.10: shows no "Max 5000 chars/request" label on the providers it offers', async () => {
    await renderPage();

    expect(screen.getByTestId('provider-option-google')).toBeInTheDocument();
    expect(screen.getByTestId('provider-option-chatterbox')).toBeInTheDocument();
    expect(screen.queryAllByText(/chars\/request/)).toHaveLength(0);
  });
});
```

### `frontend/tests/tts.spec.tsx` (modify, complete unified diff against `HEAD` `ce598d4`)

SHA-256 of this block's content, with LF line endings: `9caf63cbd00ce1cbac9abe22328f4146d06acd89c347be5139e95ceb07caeb8e`. Content after applying it, with CR removed: `b7ba4cadaadfa89a18b9e4d631a9ad2e97b60f98fb36a4b67a20fbb087b44952`. Some context lines in this diff are blank except for trailing spaces, and they must be kept.

```diff
diff --git a/frontend/tests/tts.spec.tsx b/frontend/tests/tts.spec.tsx
index bfb3f97..13dbec6 100644
--- a/frontend/tests/tts.spec.tsx
+++ b/frontend/tests/tts.spec.tsx
@@ -80,7 +80,7 @@ describe('M3.1: Text Input Validation', () => {
     const textarea = screen.getByRole('textbox', { name: /text to convert/i });
     expect(textarea).toHaveValue('');
     const charCount = screen.getByTestId('char-count');
-    expect(charCount).toHaveTextContent('0 / 5000');
+    expect(charCount).toHaveTextContent(/^0 characters$/);
   });
 
   it('M3.1.3: should accept text with standard characters', async () => {
@@ -110,14 +110,16 @@ describe('M3.1: Text Input Validation', () => {
     expect(textarea).toHaveValue(textSamples.utf8);
   });
 
-  it('M3.1.6: should reject text exceeding 5000 characters', async () => {
+  it('M3.1.6: should keep text exceeding 5000 characters whole', async () => {
     renderWithProvider(<TextToSpeechInput />);
     const textarea = screen.getByRole('textbox', { name: /text to convert/i }) as HTMLTextAreaElement;
     
     // Use fireEvent to set value directly to avoid long typing timeout
     fireEvent.change(textarea, { target: { value: textSamples.exceedsMaxLength } });
-    // Component should cap at 5000 chars
-    expect(textarea.value.length).toBeLessThanOrEqual(5000);
+    // No text cap for any provider (COA-17): all 5001 characters stay in the text box
+    expect(textarea.value.length).toBe(textSamples.exceedsMaxLength.length);
+    expect(textarea).toHaveValue(textSamples.exceedsMaxLength);
+    expect(textarea).not.toHaveAttribute('maxlength');
   });
 
   it('M3.1.7: should display character count', async () => {
@@ -127,20 +129,22 @@ describe('M3.1: Text Input Validation', () => {
     const charCount = screen.getByTestId('char-count');
     
     await user.type(textarea, textSamples.medium);
-    expect(charCount).toHaveTextContent(`${textSamples.medium.length} / 5000`);
+    expect(charCount).toHaveTextContent(new RegExp(`^${textSamples.medium.length} characters$`));
   });
 
-  it('M3.1.8: should show warning at 90% of character limit', async () => {
+  it('M3.1.8: should show no capacity warning or limit message for long text', async () => {
     renderWithProvider(<TextToSpeechInput />);
     const textarea = screen.getByRole('textbox', { name: /text to convert/i }) as HTMLTextAreaElement;
     
-    // Type text that exceeds 90% (4500 chars)
-    const longText = 'a'.repeat(4500);
+    // 5000 characters: the old cap showed both the 90% warning and the maximum-reached message here
+    const longText = 'a'.repeat(5000);
     fireEvent.change(textarea, { target: { value: longText } });
     
-    const warning = screen.getByTestId('char-warning');
-    expect(warning).toBeInTheDocument();
-    expect(warning).toHaveTextContent(/90% capacity reached/i);
+    expect(screen.getByTestId('char-count')).toHaveTextContent(/^5000 characters$/);
+    expect(screen.queryByTestId('char-warning')).not.toBeInTheDocument();
+    expect(screen.queryByText(/90% capacity/i)).not.toBeInTheDocument();
+    expect(screen.queryByTestId('max-chars-warning')).not.toBeInTheDocument();
+    expect(screen.queryByText(/maximum character limit/i)).not.toBeInTheDocument();
   });
 });
 
@@ -252,9 +256,8 @@ describe('M3.3: Provider Selection', () => {
     await waitFor(() => {
       expect(screen.getByText('Google Text-to-Speech')).toBeInTheDocument();
     });
-    // Multiple providers show max chars, so use getAllByText or check individual text
-    const maxCharsElements = screen.getAllByText(/Max \d+ chars\/request/);
-    expect(maxCharsElements.length).toBeGreaterThan(0);
+    // No provider shows a "Max 5000 chars/request" label (COA-17)
+    expect(screen.queryAllByText(/Max \d+ chars\/request/)).toHaveLength(0);
   });
 
   it('M3.3.3: should allow selecting a provider', async () => {
@@ -288,9 +291,10 @@ describe('M3.3: Provider Selection', () => {
   it('M3.3.5: should show provider capabilities (rate limit, max chars)', async () => {
     renderWithProvider(<ProviderSelector />);
     await waitFor(() => {
-      const maxCharsTexts = screen.getAllByText(/Max \d+ chars\/request/);
-      expect(maxCharsTexts.length).toBeGreaterThan(0);
+      expect(screen.getByTestId('provider-selector-container')).toBeInTheDocument();
     });
+    // No provider shows a "Max 5000 chars/request" label (COA-17)
+    expect(screen.queryAllByText(/Max \d+ chars\/request/)).toHaveLength(0);
   });
 
   it('M3.3.6: should default to first available provider', async () => {
```

### `frontend/tests/mocks/tts-handlers.ts` (modify, complete unified diff against `HEAD` `ce598d4`)

SHA-256 of this block's content, with LF line endings: `c40a40590f11f7ed2b38f4f4a0207789796e12053bc2928a3403f9c4eec84982`. Content after applying it, with CR removed: `4c6c32e5f406076e80011235fbdb95349a16352e6a59591e06b73eac437c5049`.

```diff
diff --git a/frontend/tests/mocks/tts-handlers.ts b/frontend/tests/mocks/tts-handlers.ts
index cd1aabf..a253748 100644
--- a/frontend/tests/mocks/tts-handlers.ts
+++ b/frontend/tests/mocks/tts-handlers.ts
@@ -24,10 +24,6 @@ export const ttsHandlers = [
       return res(ctx.status(400), ctx.json(errorResponses.emptyText));
     }
 
-    if (text.length > 5000) {
-      return res(ctx.status(400), ctx.json(errorResponses.textTooLong));
-    }
-
     // Validate voice
     if (!voiceId) {
       return res(ctx.status(400), ctx.json(errorResponses.invalidVoice));
```

### Contract rule coverage

Added because `implementation-planning` RED requires each contract rule this milestone verifies to be mapped to a test.

| Contract rule (`API-Contract.md`) | Test |
| --- | --- |
| Inference Generation: `provider` `"google"` or `"chatterbox"`; any other value `400` (so only those two are offered) | OAM-6.1, OAM-6.2, OAM-6.3 |
| Inference Generation: `language` exactly `"en"` or `"hi"`, required for Chatterbox | OAM-6.3, OAM-6.4 |
| Inference Generation: `script` has no length limit and is used whole | OAM-6.8, OAM-6.9 |
| Inference Generation: `voice_id` for Chatterbox is a recorded or uploaded voice's `id` | OAM-6.3 |
| Inference Provider List: four entries; display name is the description before ` (`, "Chatterbox voice cloning" | OAM-6.1 |
| Voice List: recorded and uploaded voices are told apart by the absence of `provider` | OAM-6.3 |
| Chatterbox Failure Causes: `503 {"error": <message>}` with the nine messages; clients tell causes apart by `error` text | OAM-6.5 |
| Inference Generation, failure 7: Google rejecting long text answers `500 Inference failed: …` | OAM-6.8 |
| Inference Generation, Result delivery (OAC-9): the result is the answer to the same request | OAM-6.6, OAM-6.7 |
| Inference Generation Download: `audio/wav` bytes for the `job_id` the client chose | OAM-6.6 |

Not tested here: `provider` `null` or `""`, which the page never sends after OAM-7 (T6D-6). Every rule the services themselves enforce was verified at OAM-4 or is checked at OAM-8. History, download and delete of a cloned generation (COA-10) are not page-side scope of OAM-6 (`Plan.md` traceability: verified at OAM-8).

## Execution Steps

Run in Git Bash from the repository root unless a step says `frontend/`. Logs go to `$TEMP`, outside the repository.

1. Confirm that the Human Review status below records the user's approval, and that it records the user's answer to T6Q-1. If either is missing, stop.
2. Run command 1. Stop if `git status --short` shows anything other than work-item records under `docs/.ai/chatterbox-original-app/`, or if the port check prints a listening line.
3. Extract the three code blocks of this plan with CR removed. The new file is lines 136-648, the `tts.spec.tsx` diff lines 656-743, and the `tts-handlers.ts` diff lines 751-765:
   `P=docs/.ai/chatterbox-original-app/006_Implementation_Plan_OAM-6.md`
   `sed -n '136,648p' "$P" | tr -d '\r' > frontend/tests/tts-provider-choice.spec.tsx`
   `sed -n '656,743p' "$P" | tr -d '\r' > "$TEMP/oam6-spec.diff"`
   `sed -n '751,765p' "$P" | tr -d '\r' > "$TEMP/oam6-handlers.diff"`
   `sha256sum frontend/tests/tts-provider-choice.spec.tsx "$TEMP/oam6-spec.diff" "$TEMP/oam6-handlers.diff"` must print `de6f2493c63f319ec9c6a71eab2b1988b069d35b222211f3a361058c3fd22a24`, `9caf63cbd00ce1cbac9abe22328f4146d06acd89c347be5139e95ceb07caeb8e` and `c40a40590f11f7ed2b38f4f4a0207789796e12053bc2928a3403f9c4eec84982`. Otherwise delete the new file and stop.
4. `git apply --check "$TEMP/oam6-spec.diff" && git apply "$TEMP/oam6-spec.diff"`, then the same for `"$TEMP/oam6-handlers.diff"`. If a check fails, revert this milestone's files (Rollback / Recovery) and stop.
5. Run commands 2–6 in order, one at a time. Commands 3 and 4 may run in the background, but command 4 starts only after command 3 has exited and its log has been read. No two commands run at the same time (T6D-9, Revision 2 Changes).
6. Record the evidence in `Plan.md` below the Execution Status table, and set the OAM-6 row. Change nothing else in `Plan.md`.

## Acceptance / Completion Criteria

Criteria limiting which files may change exclude this milestone's Execution Status update in `Plan.md`.

- **T6C-1 Files.** Exactly `frontend/tests/tts-provider-choice.spec.tsx` is created and `frontend/tests/tts.spec.tsx` and `frontend/tests/mocks/tts-handlers.ts` are modified, each matching the hash above with CR removed. No production, build or configuration file and no other test file changes. Only work-item records under `docs/.ai/chatterbox-original-app/` change besides.
- **T6C-2 Compile.** `npm run type-check` exits 0. Production source is unchanged, and `tests/` is outside that check (Current Repository State). vitest compiles both test files, so neither run reports a collection or transform error.
- **T6C-3 New tests fail for the missing behavior.** All 19 tests in the new file fail. Each fails on an assertion or a missing element that the missing page behavior explains, in these classes:
  - (A) the page offers providers other than Google and Chatterbox (OAM-6.1);
  - (B) the Google request names no provider (OAM-6.2);
  - (C) with Chatterbox chosen, the voice list is not exactly the recorded and uploaded voices (OAM-6.3, OAM-6.5 ×9, OAM-6.6, OAM-6.7);
  - (D) there is no language control (OAM-6.4 ×2);
  - (E) long text is truncated (OAM-6.8, OAM-6.9);
  - (F) the "chars/request" label shows (OAM-6.10).

  No failure comes from an import, a transform, an unhandled request (the `afterEach` check), or an msw warning.
- **T6C-4 Changed cap tests fail for the missing behavior.** In `tts.spec.tsx`, M3.1.2, M3.1.7 and M3.1.8 fail because the count is not "`<n>` characters", and M3.1.6 fails because the text is truncated.
- **T6C-5 M3.3.2 and M3.3.5 keep their pre-existing failure.** Each fails because the provider selector shows `provider-error` "fetch failed", as on the baseline. They are recorded as pre-existing, not as RED evidence (`Plan.md` OAM-6 Success criteria, OAR-6).
- **T6C-6 Other `tts.spec.tsx` tests keep their baseline result.** Per T6Q-1 (a), the 27 named pre-existing failures (Answered Questions) are accepted only when each fails for its baseline cause; any other failure fails the milestone. The baseline cause is one of two, re-observed on the unmodified tree at HEAD `b8704a6` (revision 2 baseline, Planning-Time Dry Run):
  - the selectors' "fetch failed", for M3.2.1–M3.2.7, M3.3.1–M3.3.6, M3.11.1, M3.11.2, M3.12.1 and M3.12.7 (17): the test's `FAIL` section shows `fetch failed` and `data-testid="provider-error"` or `data-testid="voice-selector-error"`;
  - the history fetch's "fetch failed", for M3.7.1–M3.7.7, M3.11.3, M3.11.5 and M3.12.5 (10): the test's first error is `Unable to find an element by: [data-testid="generation-history-container"]`, its `FAIL` section shows `data-testid="empty-state"` ("No generations yet"), and the test logs `Failed to fetch history: [TypeError: fetch failed]` on stderr. The history component catches the error (`GenerationHistory.tsx:35-36`), so `fetch failed` does not appear in these tests' `FAIL` sections.

  Every other `tts.spec.tsx` test passes, as on the baseline.
- **T6C-7 No test fakes or calls Chatterbox, and no request leaves the test process** (COA-16). Shown by the code (no handler for any Chatterbox URL, and the catch-all) and by the `afterEach` check passing, so no failure names `unexpected request`.

## Answered Questions

Asked because `implementation-planning` Pre-existing Failures requires asking the user before approval.

- **T6Q-1 — answered by Avinash Srivastava on 2026-11-14: "Accept the 27", option (a).** How the 27 pre-existing `tts.spec.tsx` failures are treated.** This milestone must run all of `tts.spec.tsx`, because it uses `tts-handlers.ts`, which this milestone changes (`prompt-driven-development` Test Scope: "plus tests that use a shared test file the milestone changes"). On the unmodified baseline (HEAD `ce598d4`, 2026-11-13, one full run) these 27 fail. Their observed cause is that `tts-handlers.ts` does not serve the endpoints the page calls, so the selectors show "fetch failed" (`Plan.md:39`). They are:
  - M3.2: `M3.2.1: should display list of approved voices`, `M3.2.2: should show voice name for each option`, `M3.2.3: should show language for each voice`, `M3.2.4: should allow selecting a voice`, `M3.2.5: should persist selected voice in form`, `M3.2.6: should exclude pending and rejected voices`, `M3.2.7: should show preview for each voice`;
  - M3.3: `M3.3.1: should display available TTS providers`, `M3.3.2: should show provider name for each option`, `M3.3.3: should allow selecting a provider`, `M3.3.4: should disable unavailable providers`, `M3.3.5: should show provider capabilities (rate limit, max chars)`, `M3.3.6: should default to first available provider`;
  - M3.7: `M3.7.1: should fetch and display generation history`, `M3.7.2: should display generation text for each item`, `M3.7.3: should display voice name used for each generation`, `M3.7.4: should display provider used for each generation`, `M3.7.5: should display creation timestamp for each generation`, `M3.7.6: should display audio duration for ready generations`, `M3.7.7: should allow pagination through history`;
  - M3.11: `M3.11.1: should persist selected voice in context`, `M3.11.2: should persist selected provider in context`, `M3.11.3: should persist generation history in context`, `M3.11.5: should update context when generation is deleted`;
  - M3.12: `M3.12.1: should render text input, voice selector, and provider selector together`, `M3.12.5: should render history list with playback controls`, `M3.12.7: should handle full workflow: input → submit → poll → play → history`.

  The 63 `voice.spec.tsx` failures (M2.2.4, M2.3.2, M2.3.5, M2.6.7, M2.8.2–M2.8.8, M2.9.1–M2.9.8, M2.10.1–M2.10.10, M2.11.1–M2.11.9, M2.12.1–M2.12.9, M2.13.1–M2.13.8, M2.14.1–M2.14.8) are not run by this milestone: `voice.spec.tsx` uses no file this milestone changes. They come up again at OAM-7, which runs the full suite.

  Options:
  - (a) Accept exactly these 27 names as the only pre-existing failures. Each is recorded in the milestone evidence, and the `tts.spec.tsx` run is accepted only when its failures are exactly these 27 plus the 4 changed M3.1 tests (T6C-4). Any other failure, or one of the 27 failing for a different cause than the selectors' "fetch failed", fails the milestone. This is the only non-blocking form `implementation-planning` Pre-existing Failures allows.
  - (b) Another treatment you state. Repairing these tests is not in this work item's requirements (`Plan.md`, Non-Blocking Open Decisions), so it would need replanning.

## Verification

### Commands

1. Preconditions (repository root):
   `git status --short`
   `netstat -ano | grep LISTENING | grep -E ":(8002|8003) "; echo "ports-check exit $?"` → must print only `ports-check exit 1`
   `test -d frontend/node_modules && echo "node_modules present" || (cd frontend && npm ci)` (OAV-4)
   `tasklist //FI "IMAGENAME eq node.exe" //NH > "$TEMP/oam6-node-before.txt"`
2. After Execution Steps 3–4 (repository root):
   `for f in frontend/tests/tts-provider-choice.spec.tsx frontend/tests/tts.spec.tsx frontend/tests/mocks/tts-handlers.ts; do tr -d '\r' < "$f" | sha256sum; done` → `de6f2493c63f319ec9c6a71eab2b1988b069d35b222211f3a361058c3fd22a24`, `b7ba4cadaadfa89a18b9e4d631a9ad2e97b60f98fb36a4b67a20fbb087b44952`, `4c6c32e5f406076e80011235fbdb95349a16352e6a59591e06b73eac437c5049` (T6C-1)
   `(cd frontend && npm run type-check > "$TEMP/oam6-tsc.log" 2>&1; echo "type-check exit $?")` (OAV-6, T6C-2)
3. New tests (in `frontend/`; OAV-5 scoped; T6C-3, T6C-7):
   `npx vitest run tests/tts-provider-choice.spec.tsx > "$TEMP/oam6-red-new.log" 2>&1; sed 's/\x1b\[[0-9;]*m//g' "$TEMP/oam6-red-new.log" > "$TEMP/oam6-red-new.txt"; grep -E "^ +Tests " "$TEMP/oam6-red-new.txt"`
   `for p in "to deeply equal \[ 'chatterbox', 'google' \]" "to match object" "to deeply equal \[ 'voice-1a2b3c4d', 'voice-5e6f7a8b' \]" 'Unable to find an element by: \[data-testid="language-select"\]' "expected 5000 to be 6600" "to have a length of \+0 but got"; do printf '%s => ' "$p"; grep -cE "^(AssertionError|TestingLibraryElementError): .*$p" "$TEMP/oam6-red-new.txt"; done`
   `printf 'afterEach => '; grep -cE "to deeply equal \[\]" "$TEMP/oam6-red-new.txt"; printf 'MSW => '; grep -c "\[MSW\]" "$TEMP/oam6-red-new.txt"; grep -ciE "(Transform|Syntax|Reference)Error|Failed to load|Cannot find module" "$TEMP/oam6-red-new.txt"`
   Then read each `FAIL` section's first error line, and map it to its class in T6C-3.
4. `tts.spec.tsx` (in `frontend/`; T6C-4 to T6C-6):
   `npx vitest run tests/tts.spec.tsx > "$TEMP/oam6-red-tts.log" 2>&1; sed 's/\x1b\[[0-9;]*m//g' "$TEMP/oam6-red-tts.log" > "$TEMP/oam6-red-tts.txt"; grep -E "^ +Tests " "$TEMP/oam6-red-tts.txt"`
   `grep -E "^ FAIL " "$TEMP/oam6-red-tts.txt" | sed -E 's/.*> //' | LC_ALL=C sort > "$TEMP/oam6-tts-failed.txt"`
   Write the accepted list (T6Q-1 answered (a)). The heredoc lines start at column 0:

```bash
cat > "$TEMP/oam6-tts-accepted.txt" <<'LIST'
M3.1.2: should reject empty text submission
M3.1.6: should keep text exceeding 5000 characters whole
M3.1.7: should display character count
M3.1.8: should show no capacity warning or limit message for long text
M3.11.1: should persist selected voice in context
M3.11.2: should persist selected provider in context
M3.11.3: should persist generation history in context
M3.11.5: should update context when generation is deleted
M3.12.1: should render text input, voice selector, and provider selector together
M3.12.5: should render history list with playback controls
M3.12.7: should handle full workflow: input → submit → poll → play → history
M3.2.1: should display list of approved voices
M3.2.2: should show voice name for each option
M3.2.3: should show language for each voice
M3.2.4: should allow selecting a voice
M3.2.5: should persist selected voice in form
M3.2.6: should exclude pending and rejected voices
M3.2.7: should show preview for each voice
M3.3.1: should display available TTS providers
M3.3.2: should show provider name for each option
M3.3.3: should allow selecting a provider
M3.3.4: should disable unavailable providers
M3.3.5: should show provider capabilities (rate limit, max chars)
M3.3.6: should default to first available provider
M3.7.1: should fetch and display generation history
M3.7.2: should display generation text for each item
M3.7.3: should display voice name used for each generation
M3.7.4: should display provider used for each generation
M3.7.5: should display creation timestamp for each generation
M3.7.6: should display audio duration for ready generations
M3.7.7: should allow pagination through history
LIST
```

   `LC_ALL=C sort -o "$TEMP/oam6-tts-accepted.txt" "$TEMP/oam6-tts-accepted.txt"; wc -l < "$TEMP/oam6-tts-accepted.txt"` → `31`
   `echo "unexpected:"; LC_ALL=C comm -13 "$TEMP/oam6-tts-accepted.txt" "$TEMP/oam6-tts-failed.txt"; echo "accepted, not failing:"; LC_ALL=C comm -23 "$TEMP/oam6-tts-accepted.txt" "$TEMP/oam6-tts-failed.txt"`
   `for t in "M3.3.2:" "M3.3.5:"; do printf '%s fetch failed => ' "$t"; awk -v t="$t" '$0 ~ "^ FAIL .*> "t {p=1;n=0} p{print;n++} n>60{p=0}' "$TEMP/oam6-red-tts.txt" | grep -c "fetch failed"; done` → each at least `1`
   `for t in "M3.1.2:" "M3.1.6:" "M3.1.7:" "M3.1.8:"; do printf '%s => ' "$t"; awk -v t="$t" '$0 ~ "^ FAIL .*> "t {getline; print; exit}' "$TEMP/oam6-red-tts.txt" | cut -c1-80; done`
   Then check the other 25 named failures for their baseline cause (T6C-6). The 15 that fail on a selector's fetch:
   `for t in M3.2.1 M3.2.2 M3.2.3 M3.2.4 M3.2.5 M3.2.6 M3.2.7 M3.3.1 M3.3.3 M3.3.4 M3.3.6 M3.11.1 M3.11.2 M3.12.1 M3.12.7; do s=$(awk -v t="$t:" '/^ FAIL / {p=(index($0,"> " t)>0); next} /Test Files/ {p=0} p' "$TEMP/oam6-red-tts.txt"); printf '%s: fetch-failed=%s error-id=%s\n' "$t" "$(printf '%s\n' "$s" | grep -c 'fetch failed')" "$(printf '%s\n' "$s" | grep -cE 'data-testid="(provider|voice-selector)-error"')"; done` → 15 lines, each with `fetch-failed` and `error-id` at least `1`
   The 10 that fail on the history fetch:
   `for t in M3.7.1 M3.7.2 M3.7.3 M3.7.4 M3.7.5 M3.7.6 M3.7.7 M3.11.3 M3.11.5 M3.12.5; do s=$(awk -v t="$t:" '/^ FAIL / {p=(index($0,"> " t)>0); next} /Test Files/ {p=0} p' "$TEMP/oam6-red-tts.txt"); printf '%s: container-missing=%s empty-state=%s history-log=%s\n' "$t" "$(printf '%s\n' "$s" | grep -m1 -E '^(AssertionError|TestingLibraryElementError)' | grep -c 'Unable to find an element by: \[data-testid="generation-history-container"\]')" "$(printf '%s\n' "$s" | grep -c 'data-testid="empty-state"')" "$(awk -v t="$t:" '/^(stderr|stdout) \| / {p=(index($0,"> " t)>0); next} /^ (FAIL|✓|×|❯) / {p=0} p && /^Failed to fetch history: \[TypeError: fetch failed\]/ {c++} END {print c+0}' "$TEMP/oam6-red-tts.txt")"; done` → 10 lines, each with `container-missing=1`, and `empty-state` and `history-log` at least `1`
   Any other value fails T6C-6.
5. Repository state (repository root): `git status --short`, then `git status --short -- audio_storage` (OAV-3; no backend test runs here, so it must print nothing).
6. Processes: `tasklist //FI "IMAGENAME eq node.exe" //NH > "$TEMP/oam6-node-after.txt"; diff "$TEMP/oam6-node-before.txt" "$TEMP/oam6-node-after.txt"`. Any `node.exe` line present only in the after file belongs to this run and must be stopped before reporting.

### Affected Tests

- `frontend/tests/tts.spec.tsx`, all 94 tests. It is changed by this milestone, and it is the only importer of the changed `frontend/tests/mocks/tts-handlers.ts` (`grep -rn "tts-handlers" frontend/tests` → `tts.spec.tsx:11` only).
- No other test file imports a changed file. `voice.spec.tsx`, `auth.spec.tsx` and `auth-api.spec.tsx` import neither changed file (same grep), so they are not run (`prompt-driven-development` Test Scope, RED).

### Expected Evidence

Expected / Predicted — Not Yet Verified.

- Command 2: `type-check exit 0`.
- Command 3: `Tests  19 failed (19)`. The six pattern counts, in order, are 1, 1, 12, 2, 2, 1, for classes (A) to (F). Then `afterEach => 0`, `MSW => 0`, and `0` for the transform and load-error grep.
- Command 4: `Tests  31 failed | 63 passed (94)`. The comparison prints `unexpected:` and `accepted, not failing:` with nothing under either. M3.3.2 and M3.3.5 each show `provider-error` with "fetch failed". The 15 selector-fetch lines show `fetch-failed=2 error-id=2`, except M3.12.1 and M3.12.7 with `4` and `4`. The 10 history lines show `container-missing=1 empty-state=2 history-log=1`.
- Command 5: `?? frontend/tests/tts-provider-choice.spec.tsx`, ` M frontend/tests/mocks/tts-handlers.ts`, ` M frontend/tests/tts.spec.tsx`, plus work-item records under `docs/.ai/chatterbox-original-app/`. `git status --short -- audio_storage` prints nothing.
- Command 6: no `node.exe` process started by this run is still running.
- Repeat run: none. These tests touch no persistent state and override no configuration (`implementation-planning` Repeatable, Isolated Verification). Each test resets its recorded requests in `beforeEach`, and setup resets the handlers after each test (`setup.ts:9`).
- Preserved-behavior tests (expected to pass at RED): none. `Plan.md` assigns no preserved row to OAM-6.

### Planning-Time Dry Run

Planning-time dry run, not milestone evidence. Disposable copy: `git archive HEAD frontend | tar -x -C <scratchpad>/dry`, then `npm ci` there (exit 0). The repository was not modified. The copy was deleted afterwards.

| # | Command (in the copy's `frontend/`) | Result |
| --- | --- | --- |
| 1 | Applied the three files above. Hashes of the copy's files with CR removed: new file `de6f2493c63f319ec9c6a71eab2b1988b069d35b222211f3a361058c3fd22a24`, `tts.spec.tsx` `b7ba4cadaadfa89a18b9e4d631a9ad2e97b60f98fb36a4b67a20fbb087b44952`, `tts-handlers.ts` `4c6c32e5f406076e80011235fbdb95349a16352e6a59591e06b73eac437c5049` | Match the blocks above |
| 2 | `git apply --check <diff>` for both diffs, run against the real worktree (writes nothing) | `spec diff applies`, `handlers diff applies` |
| 3 | `npx tsc -p <scratch tsconfig extending tsconfig.json, adding vitest/globals and jest-dom types, including src and the new file>` | Only `tests/mocks/setup.ts(145,3): error TS2322`, which is existing code outside this milestone. No error in the new file. The scratch tsconfig was deleted before the runs |
| 4 | `npx vitest run tests/tts-provider-choice.spec.tsx` (production source as `HEAD`) | `Tests  19 failed (19)`. Classes: (A) `expected [ 'azure', 'chatterbox', …(2) ] to deeply equal [ 'chatterbox', 'google' ]` 1; (B) `expected { …(2) } to match object { …(3) }` (missing `provider`) 1; (C) `to deeply equal [ 'voice-1a2b3c4d', 'voice-5e6f7a8b' ]` (received the two Google voices) 12; (D) `Unable to find an element by: [data-testid="language-select"]` 2; (E) `expected 5000 to be 6600` 2; (F) `to have a length of +0 but got 4` 1. `[MSW]` warnings 0; no `unexpected request` failure |
| 5 | `npx vitest run tests/tts.spec.tsx` (production source as `HEAD`) | `Tests  31 failed | 63 passed (94)`. Compared with the baseline 27: added exactly M3.1.2, M3.1.6 (`expected 5000 to be 5001`), M3.1.7 and M3.1.8 (`toHaveTextContent`); none removed. M3.3.2 fails on "Google Text-to-Speech" and M3.3.5 on `provider-selector-container`, each with `provider-error` "fetch failed" in the DOM, as on the baseline |
| 6 | Scratch-only GREEN probe in the copy's `src/`. It filters the backends to `google` and `chatterbox`, removes the label and the text cap, adds a `SELECT_LANGUAGE` state with `language-select`, sends `provider` and `language`, and lists voices without `provider` for Chatterbox. Then `npm run type-check` | exit 0 |
| 7 | `npx vitest run tests/tts-provider-choice.spec.tsx` with the probe | `Tests  19 passed (19)` |
| 8 | `npx vitest run tests/tts.spec.tsx` with the probe | `Tests  27 failed | 67 passed (94)`. The failing names equal the baseline 27 exactly (`diff` printed nothing), and the 4 changed M3.1 tests pass |
| 9 | Corrections the dry run caused. The jsdom `Blob` had no `arrayBuffer()` (`TypeError: loaded.arrayBuffer is not a function`), so it is read with `FileReader`. `ctx.body(Uint8Array)` failed type-check (TS2345), so an `ArrayBuffer` is passed. Length assertions were added before `toHaveValue`, to keep failure output short | Applied in the code above; runs 4–8 are the reruns after the corrections |

Created during the dry run, all under the session scratchpad and deleted afterwards: `dry/` (the copy with its `node_modules`), `orig/`, `final/`, `draft/`, and the logs. The probe never entered the repository.

#### Revision 2 baseline check (2026-11-14)

Planning-time observation, not milestone evidence. It ran on the real worktree's untouched frontend at HEAD `b8704a6` (`git status --short -- frontend` printed nothing; only this plan and `Plan.md` were modified, under `docs/`). No file was applied. The ports check printed only `ports-check exit 1`. Logs went to the session scratchpad and were deleted afterwards.

| # | Command (in `frontend/`) | Result |
| --- | --- | --- |
| R1 | `npx vitest run tests/tts.spec.tsx` | `Tests  27 failed | 67 passed (94)`. The 27 failing names equal T6Q-1's list |
| R2 | Per-test listing of the 27: first error line, `fetch failed` and `*-error` count in the `FAIL` section, `empty-state` and "No generations yet" count, and stderr count of `Failed to fetch history: [TypeError: fetch failed]` | 17 (M3.2.1–M3.2.7, M3.3.1–M3.3.6, M3.11.1, M3.11.2, M3.12.1, M3.12.7): `fetch failed` and `provider-error` or `voice-selector-error` in the section, no history log line. 10 (M3.7.1–M3.7.7, M3.11.3, M3.11.5, M3.12.5): first error `Unable to find an element by: [data-testid="generation-history-cont…`, `empty-state` and "No generations yet" twice each, `fetch failed` 0 times in the section, history log line once each, cause `code: 'ECONNREFUSED'`. This matches the stopped run's command 4 observation |
| R3 | The two loops of command 4's revised last check, run on a copy of the R1 log named `oam6-red-tts.txt` | 15 lines `fetch-failed=2 error-id=2` (M3.12.1 and M3.12.7: `4` and `4`); 10 lines `container-missing=1 empty-state=2 history-log=1` |
| R4 | `tasklist` of `node.exe` before and after R1, then `diff` | `diff exit 0` |
| R5 | `sed -n` / `tr -d '\r'` / `sha256sum` of lines 136-648, 656-743 and 751-765 of this revised plan | `de6f2493…2a24`, `9caf63cb…eb8e`, `c40a4059…4982`, unchanged, so Execution Step 3 still extracts the same code |

Not re-run: the new file and the diffs, which revision 2 does not change. The stopped run's commands 2 and 3 matched this plan's expectations (`Plan.md`, OAM-6 stopped execution evidence), and the first dry run covers them.

## Risks

- **T6R-1 Three Chatterbox tests fail at RED one step before what they verify.** OAM-6.5 (COA-7), OAM-6.6 (COA-4) and OAM-6.7 (COA-13) fail at RED in class (C), because Chatterbox voices are not offered. Showing the response's `error` text, loading a ready generation's audio and disabling Generate already exist for any request (`GenerationErrorDisplay.tsx:50`, `TextToSpeech.tsx:36-51`, `GenerationSubmitForm.tsx:133`). What the page lacks is making a Chatterbox generation. Their RED evidence therefore shows that the page cannot reach a Chatterbox generation, and dry-run step 7 shows they pass once it can. The mocks supply the message and the WAV, and the tests assert what the page did with them: the message shown, and the downloaded bytes used for the player (`testing`).
- **T6R-2 `tts.spec.tsx` sends unmocked requests to the real `localhost:8002` and `localhost:8003`.** This follows from `setup.ts:7` and the unmatched endpoints, as the baseline's "fetch failed" shows. If a local service were running, the 27 results could change. Mitigation: command 1 stops execution when either port is listening. The new file is not affected, because its catch-all answers every request (T6D-1).
- **T6R-3 The page seams in T6D-3 to T6D-7 bind OAM-7.** They are decided here for review. OAM-7 cannot change them without the user's approval (`implementation-planning` Carried-Forward Decisions).
- **T6R-4 Timing.** The tests wait with `waitFor` at its default 1000 ms timeout. In the dry run the new file's 19 tests took about 13 s in total with the probe, and no wait came near the limit (hypothesis: slower machines keep that margin; not measured).
- **T6R-5 Duplicate React key warning.** A successful generation logs "Encountered two children with the same key" (seen in dry-run step 7). `GENERATION_COMPLETE` and `ADD_TO_HISTORY` both prepend the same generation (`TTSContext.tsx:48`, `:62`; `GenerationSubmitForm.tsx:47-48`). It is existing behavior, fails no test, and is not in scope.
- **T6R-6 Code quality, Medium RU1, kept.** The new file's `AuthenticatedPage` resembles `tts.spec.tsx`'s `AuthenticatedWrapper` (`tts.spec.tsx:28-44`). That helper is not exported, and `Plan.md` allows no other change to `tts.spec.tsx`. No High finding is open.
- Security: no authentication or authorization requirement is owned or verified by this milestone. The tests pass a fixed bearer token that no mock checks, as the contract states (Out of Scope: neither service checks `Authorization`).

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Reverse only this milestone's files:

- `rm frontend/tests/tts-provider-choice.spec.tsx`
- `git checkout -- frontend/tests/tts.spec.tsx frontend/tests/mocks/tts-handlers.ts`

## Explicitly Out of Scope

- Any production, build or configuration change, including everything T6D-3 to T6D-7 describe, which is OAM-7's work.
- Backend tests, and any change to the backend.
- Any change to `tts.spec.tsx` other than the six tests listed, and to `tts-handlers.ts` other than `:27-29`. This includes the `/providers` mock's `maxCharsPerRequest` values (`tts-handlers.ts:194`, `:200`, `:206`) and `fixtures/tts.ts`, which `Plan.md` does not name.
- Repairing any pre-existing failure, including the cause of M3.3.2 and M3.3.5 (`Plan.md` OAM-6 exclusions).
- Any test that fakes, stands in for or calls Chatterbox (COA-16); any Docker or `gcloud` command (CON-2).
- Page behavior the requirements do not ask for: hiding the language control for Google, history display of cloned generations, and duplicate prevention beyond the disabled button (COA-13).

## Revision 2 Changes

Revision of the approved plan after the stopped run (`Plan.md`, OAM-6 stopped execution evidence). It is not a fresh draft. No test code, diff, hash, line range, Files in Scope entry, decision T6D-1 to T6D-8, T6Q-1 or its answer (a), or the 27 accepted names changed.

- **T6C-6** now states both baseline causes. The 17 selector tests fail on the selectors' "fetch failed". The 10 history tests fail on the history fetch's `TypeError: fetch failed`, which is logged on stderr, with the empty state and no `generation-history-container`. The criterion's rule is unchanged: only the 27 named failures plus the 4 changed M3.1 tests are accepted, each for its baseline cause.
- **Command 4's last check**, a prose instruction before, is now two commands with stated pass values (Verification, command 4), dry-run on the baseline log (R3).
- **Current Repository State**: the cause sentence for the 27 now names both causes. That sentence made the same claim as T6C-6, so it is updated with it.
- **Expected Evidence, command 4**: the values the two new loops are predicted to print are added.
- **Execution Step 5 and T6D-9**: commands now run one at a time (below).
- **Review Summary, Authoritative References, Preconditions**: one sentence each, recording this revision, the `Blocked` status that was re-read and HEAD `b8704a6`. These edits stay on their existing lines, so lines 136-648, 656-743 and 751-765 still hold the code blocks (R5).
- **Planning-Time Dry Run**: Revision 2 baseline check added.

Not changed, for review: T6Q-1's recorded text, including option (a)'s phrase "a different cause than the selectors' 'fetch failed'", is kept as answered. T6C-6 now spells out that, for the 10 history tests, the baseline "fetch failed" is the history fetch's. Re-approval confirms that answer (a) covers this.

**T6D-9 Commands run one at a time.** The stopped run ran commands 3 and 4 in the background at the same time (its Deviations). Its results still matched this plan, except T6C-6 as written, so running them together caused no observed difference. They still run one after the other, for three reasons:
- Both start vitest in the same `frontend/`, and every wait uses the default 1000 ms `waitFor` timeout (T6R-4). CPU contention could push a wait past that limit. That is a hypothesis; it was not measured.
- Command 6's `node.exe` before/after comparison is clearest when only one run's processes exist at a time.
- Each command's evidence then comes from a run that had the machine to itself.

Alternative: allow commands 3 and 4 to run in parallel. They write separate logs, and the stopped run showed no interference. Not chosen, because a timing failure in a parallel run could not be told apart from a real failure without re-running, and `implementation-planning` Pre-existing Failures forbids re-running until a check passes.

## Human Review

Status: Executed 2026-11-14 — valid RED established; see `Plan.md`, OAM-6 RED evidence (revision 2). (Revision 2 approved by Avinash Srivastava on 2026-11-14, as written, including T6D-9 and confirming that the T6Q-1 answer (a) covers the 10 history tests' history-fetch cause. The earlier approval covered revision 1, whose execution stopped at the T6C-6 blocker recorded in `Plan.md`.)
