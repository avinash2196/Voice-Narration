# Implementation Plan — chatterbox-original-app OAM-7 (TTS page GREEN)

## Milestone

OAM-7 — TTS page GREEN (`docs/.ai/chatterbox-original-app/Plan.md`, Milestones, OAM-7).

## Milestone Type

GREEN. `Plan.md` records OAM-7 as GREEN, with predecessor OAM-6 (TTS page RED), whose valid RED evidence is recorded (`Plan.md`, Execution Status, "OAM-6 RED evidence (revision 2)").

## Review Summary

- Behavior change: the TTS page offers only Google and Chatterbox. Every generation request names its provider, and a Chatterbox request also carries `en` or `hi` from a new language control, with English preselected. With Chatterbox chosen, only recorded and uploaded voices are listed. The text box has no cap, and its count reads "n characters". The "Max 5000 chars/request" label, the 90% warning and the maximum-reached message are removed.
- Requirements delivered: the page parts of COA-1, COA-3, COA-4, COA-5, COA-7, COA-13 and COA-17 (`Plan.md` OAM-7 Owned), through the page seams T6D-3 to T6D-7 that OAM-6 approved.
- Files: created `frontend/src/components/LanguageSelector.tsx`; modified `frontend/src/types/tts.ts`, `frontend/src/context/TTSContext.tsx`, `frontend/src/services/ttsApi.ts`, `frontend/src/components/ProviderSelector.tsx`, `frontend/src/components/VoiceSelector.tsx`, `frontend/src/components/TextToSpeechInput.tsx` and `frontend/src/components/GenerationSubmitForm.tsx`; deleted none. No test, build, configuration or backend file changes.
- Tests added: none. The 19 OAM-6 tests in `frontend/tests/tts-provider-choice.spec.tsx` and the 4 changed M3.1 tests go from failing to passing, with no test file changed.
- Verification, run one at a time: `npx vitest run tests/tts-provider-choice.spec.tsx`, then `npx vitest run` and the backend suite (OAV-2). Expected / Predicted — Not Yet Verified: `19 passed (19)`; `90 failed | 282 passed (372)`, where the 90 are exactly the named pre-existing failures; `1 failed, 100 passed, 17 skipped`, where the 1 is the accepted backend test.
- Needs attention: question T7Q-1, on how the 90 pre-existing frontend failures are treated, answered (a). Decisions T7D-1 to T7D-6. Risk T7R-1: during planning an unrelated local service began listening on port 8003, and that changes the `tts.spec.tsx` failure causes (Planning-Time Dry Run, steps 6–7).

## Authoritative References

| Document | Status read |
| --- | --- |
| `docs/.ai/chatterbox-original-app/requirements.md` | "Approved by Avinash Srivastava on 2026-11-13 (revision recording Q46–Q48: automated tests no longer fake Chatterbox)" |
| `docs/.ai/chatterbox-original-app/Plan.md` | Status "Approved by Avinash Srivastava on 2026-11-13, as written, …". Execution Status: OAM-1 to OAM-6 complete; OAM-7 `Pending`; OAM-8 `Pending` |
| `docs/.ai/chatterbox-original-app/API-Contract.md` | Contract Review Status "Approved by Avinash Srivastava on 2026-11-13, as written, accepting every resolution marked `Proposed — deferred by Plan OAC-n`". The OAM-1 row in `Plan.md` Execution Status is Complete and points to it. It is the authoritative predecessor for the request body, the provider list and the voice list this milestone implements |
| `docs/.ai/chatterbox-original-app/001_Implementation_Plan_OAM-2.md` | "Executed on 2026-11-13; valid RED established … (Approved … including decisions V2D-1 to V2D-6.)" Review Summary and Carried-Forward Decisions read |
| `docs/.ai/chatterbox-original-app/002_Implementation_Plan_OAM-3.md` | "Revision 4 approved by Avinash Srivastava on 2026-11-13, as written. Executed 2026-11-13". Review Summary and Carried-Forward Decisions read |
| `docs/.ai/chatterbox-original-app/003_Implementation_Plan_OAM-4.md` | "Superseded — not executed … none of its decisions is carried forward" |
| `docs/.ai/chatterbox-original-app/004_Implementation_Plan_OAM-4.md` | "Executed — RED verified 2026-11-13 … (Approved … including decisions N4D-1 to N4D-6.)" Review Summary and Carried-Forward Decisions read |
| `docs/.ai/chatterbox-original-app/005_Implementation_Plan_OAM-5.md` | "Executed 2026-11-13 — GREEN verified … (Approved … including decisions N5D-1 to N5D-8 …)" Review Summary, Carried-Forward Decisions and its backend-suite commands read |
| `docs/.ai/chatterbox-original-app/006_Implementation_Plan_OAM-6.md` | "Executed 2026-11-14 — valid RED established … (Revision 2 approved by Avinash Srivastava on 2026-11-14, as written, including T6D-9 and confirming that the T6Q-1 answer (a) covers the 10 history tests' history-fetch cause. …)" Read in full: its decisions T6D-1 to T6D-9 and T6Q-1, and its test code, which is this milestone's RED evidence |
| `docs/requirements.md` | Does not exist (`ls docs/requirements.md`: "No such file or directory") |

None of the earlier plans' exact code is for a file this milestone changes. Labels this plan introduces use the prefix `T7` (`T7D-` decisions, `T7Q-` questions, `T7C-` criteria, `T7R-` risks). No referenced artifact defines it (`grep -rnoE "\bT7[A-Z]-?[0-9]*" docs/.ai/` found no match).

## Carried-Forward Decisions

From `006_Implementation_Plan_OAM-6.md` (revision 2, approved and executed):

- **T6D-3** (`006:120`): the page offers exactly the backends named `google` and `chatterbox`, as `provider-radio-<name>` / `provider-option-<name>`. Google stays selected first, and display names are derived as today. Delivered by T7D-3.
- **T6D-4** (`006:121`): with Chatterbox chosen, the voice list is exactly the voices with no `provider` field, in list order, with the first preselected. Delivered in `VoiceSelector.tsx` (T7D-4).
- **T6D-5** (`006:122`): `<select data-testid="language-select">` with options `en` "English" and `hi` "Hindi", in that order, English preselected, present when Chatterbox is chosen. It left open whether the control is hidden for Google, which T7D-1 decides.
- **T6D-6** (`006:123`): a Chatterbox request body is exactly `{script, voice_id, provider: "chatterbox", language}`, and a Google request carries `provider: "google"`. It left open whether a Google request carries `language`, which T7D-2 decides.
- **T6D-7** (`006:124`): `char-count` reads exactly "`<n>` characters". The text box has no `maxlength`, and `char-warning` and `max-chars-warning` are absent.
- **T6D-8** (`006:125`): M3.3.2 and M3.3.5 keep their titles, so they stay identifiable as named pre-existing failures. The accepted list below uses those titles.
- **T6D-1** (`006:118`) and the COA-16 test boundary (`004` N4D-2): the new tests answer every request inside the test process. This milestone changes no test, so the boundary holds unchanged.
- **T6D-9** (`006:1007-1012`): vitest commands run one at a time, never two at once. Applied here to every test command, the backend suite included.
- **T6Q-1 (a)** (`006:831-842`): for `tts.spec.tsx`, exactly the 27 named pre-existing failures are accepted, each only for its baseline cause (`006` T6C-6). T7Q-1 asks how this extends to the full suite.
- **V3Q-1 (a)** (`002_Implementation_Plan_OAM-3.md:730-736`), as `005` applied it: in a backend run, only the failing test the plan names is accepted. The one named test is `tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing` (`Plan.md:343`).
- **V3Q-3** (`002:736`): `tests/test_persistence.py`, `tests/test_authentication_consent.py` and `tests/test_voice_enrollment.py` are left out of every backend-suite run (OAV-2, `Plan.md:343`).
- **OAV-3 handling** (`002:596-597`, `Plan.md:344`): after a backend run writes to tracked `audio_storage/`, the output is recorded, then `git checkout -- audio_storage` and `git clean -fd -- audio_storage` restore it.
- **N4D-8** (`004:137`, carried by `005`): the provider list holds exactly `azure`, `chatterbox`, `google` and `mock`, with the contract descriptions. The page filters it (T7D-3), and the service is not changed.

## Preconditions / Predecessor Evidence

- OAM-6 is complete: "Complete — valid RED established 2026-11-14" (`Plan.md`, Execution Status). Its evidence (revision 2) records `Tests  19 failed (19)` for `tts-provider-choice.spec.tsx`, in classes (A) to (F), and `Tests  31 failed | 63 passed (94)` for `tts.spec.tsx`. The 31 were the 27 named pre-existing failures plus M3.1.2, M3.1.6, M3.1.7 and M3.1.8, each failing on the missing behavior.
- HEAD is `a909fd2` ("Add OAM-6 TTS page RED tests for chatterbox-original-app"). It commits the three OAM-6 test files, and `git status --short` printed nothing (2026-11-14). With CR removed, their hashes equal the OAM-6 evidence: `de6f2493…2a24`, `b7ba4cad…4952`, `4c6c32e5…5049`. The OAM-6 row has no `Committed as` entry, and neither does any earlier row. The commit holds only the OAM-6 files and this work item's records, so no unrecorded change is present.
- The backend is unchanged since OAM-5's verified state: `git diff --stat ce598d4 HEAD -- voice_narration tests requirements-dev.txt .gitignore` printed nothing.
- OAM-7 is `Pending`, and no Implementation Plan for OAM-7 exists (`ls docs/.ai/chatterbox-original-app/`: `001`–`006`, `API-Contract.md`, `Plan.md`, `requirements.md`). This plan is numbered `007`.
- `frontend/node_modules` is present in this worktree (installed from the lockfile, OAV-4). No dependency changes.
- Baseline, observed during planning on the unmodified tree at HEAD `a909fd2` (2026-11-14; planning observation, not milestone evidence). `netstat` showed nothing listening on 8002 or 8003 before each run:
  - `npx vitest run tests/voice.spec.tsx`: `Tests  63 failed | 43 passed (106)`. The 63 failing names equal `Plan.md:40` exactly. First error per failure group: 60 `Error: Test timed out in 5000ms.`, 1 `AssertionError: expected "spy" to be called with arguments: [ Any<Blob> ]`, 1 `TypeError: Cannot convert undefined or null to object`, 1 `Error: expect(element).toHaveClass("frozen")`. Duration 316.70 s.
  - `npx vitest run` (started 20:24:27): `Test Files  3 failed | 2 passed (5)`, `Tests  113 failed | 259 passed (372)`, Duration 318.84 s. Per file: `auth-api.spec.tsx` (80 tests) and `auth.spec.tsx` (73 tests) pass; `tts-provider-choice.spec.tsx` 19 of 19 fail; `tts.spec.tsx` 31 of 94 fail; `voice.spec.tsx` 63 of 106 fail. The 113 are the 90 names in the accepted list below, the 19 new tests and the 4 changed M3.1 tests. The `voice.spec.tsx` names equal the voice-only run's. On this log, the T6C-6 cause checks for the 27 `tts.spec.tsx` failures (command 4d) print exactly the OAM-6 values.
  - `npm run type-check` passed at OAM-6 (`Plan.md`, OAM-6 RED evidence, command 2), and production source has not changed since.

## Current Repository State

The facts the exact code depends on:

- The generation request body holds only `script` and `voice_id` (`frontend/src/services/ttsApi.ts:48-51`). `submitGeneration(text, voiceId, provider, token)` (`ttsApi.ts:32-37`) is called only from `frontend/src/components/GenerationSubmitForm.tsx:36-41` (`grep -rn submitGeneration frontend/src frontend/tests`). `normalizeVoiceIdForProvider` passes a non-Google voice identifier through unchanged (`ttsApi.ts:7-19`).
- The provider list maps every backend and adds `maxCharsPerRequest: 5000` (`ttsApi.ts:195-200`). The selector renders the "Max … chars/request" label (`frontend/src/components/ProviderSelector.tsx:88-90`). `maxCharsPerRequest` is read nowhere else in `src` (`grep -rn maxCharsPerRequest frontend/src`: `types/tts.ts:24`, `ttsApi.ts:199`, `ProviderSelector.tsx:89`). The test files that also name it (`frontend/tests/fixtures/tts.ts:90-114`, `frontend/tests/mocks/tts-handlers.ts:190-202`) do not use the `TTSProvider` type.
- The TTS state holds `selectedProvider`, initially `'google'`, set by `SELECT_PROVIDER` (`frontend/src/types/tts.ts:36-46`, `:48-62`; `frontend/src/context/TTSContext.tsx:10-20`, `:30-31`). `TTSGeneration.provider` is `'google' | 'elevenlabs' | 'azure'` (`types/tts.ts:7`), and `ttsApi.ts:39` casts the chosen provider to it.
- The voice selector keeps Google voices only, preselects the first, and fetches again only when the token or the selected voice changes (`frontend/src/components/VoiceSelector.tsx:9`, `:20-39`, `:48`). `Voice.provider` is optional (`frontend/src/types/voice.ts:7`).
- The text box truncates at `MAX_CHARS` 5000 and sets `maxLength` (`frontend/src/components/TextToSpeechInput.tsx:4-5`, `:15`, `:34`). It shows "n / 5000" and the 90% warning (`:40-53`) and the maximum-reached message (`:66-70`).
- The form renders the text box, the voice selector and the provider selector, in that order (`GenerationSubmitForm.tsx:87-91`). Generate is disabled while `isSubmitting` is true, and that holds for the whole request (`:27-78`, `:133`).
- What the page already does for any generation, which OAM-6 found reachable once a Chatterbox generation can be made (`006` T6R-1): it shows a failed request's `error` text (`frontend/src/components/GenerationErrorDisplay.tsx:50`), and it loads a ready generation's download into the player (`frontend/src/pages/TextToSpeech.tsx:36-51`).
- `GenerationSubmitForm` is also rendered by the TTS tab of `/voices` (`frontend/src/pages/VoiceManagement.tsx:162`).
- Working-tree line endings: these seven files are `i/lf w/crlf` (`git ls-files --eol`), like `frontend/tests/tts.spec.tsx`, to which OAM-6 applied an LF diff with `git apply`.

## Files in Scope

### Files to Create

- `frontend/src/components/LanguageSelector.tsx`

### Files to Modify

- `frontend/src/types/tts.ts`
- `frontend/src/context/TTSContext.tsx`
- `frontend/src/services/ttsApi.ts`
- `frontend/src/components/ProviderSelector.tsx`
- `frontend/src/components/VoiceSelector.tsx`
- `frontend/src/components/TextToSpeechInput.tsx`
- `frontend/src/components/GenerationSubmitForm.tsx`

### Files to Delete

None.

## Proposed Changes

Each change names the OAM-6 tests it makes pass. COA-4 (playback), COA-7 (message shown) and COA-13 (Generate disabled) need no new code: once a Chatterbox generation can be made, the existing code above delivers them. OAM-6.5, OAM-6.6 and OAM-6.7 pass through changes 3 and 5 (`006` T6R-1).

1. **Create `frontend/src/components/LanguageSelector.tsx`** (COA-5; T6D-5; OAM-6.4). `export function LanguageSelector()` reads `selectedLanguage` and `dispatch` from `useTTS()`. It renders a labelled `<select id="language-select-field" data-testid="language-select">`, with the options `en` "English" and `hi` "Hindi" in that order, from a `LANGUAGES` constant. A change dispatches `SELECT_LANGUAGE` with the chosen code.
2. **Modify `frontend/src/types/tts.ts`** (COA-5, COA-17):
   - `TTSGeneration.provider` adds `'chatterbox'` (T7D-6).
   - `TTSProvider` loses `maxCharsPerRequest` (T7D-5).
   - Adds `export type ChatterboxLanguage = 'en' | 'hi'`.
   - Adds `selectedLanguage: ChatterboxLanguage` to `TTSState`.
   - Adds the action `{ type: 'SELECT_LANGUAGE'; payload: ChatterboxLanguage }` to `TTSAction`.
3. **Modify `frontend/src/context/TTSContext.tsx`** (COA-5; T6D-5 English preselected; OAM-6.3, OAM-6.4, OAM-6.9): `initialState.selectedLanguage` is `'en'`, and the reducer handles `SELECT_LANGUAGE`.
4. **Modify `frontend/src/services/ttsApi.ts`** (COA-1, COA-5, COA-17):
   - Adds `SELECTABLE_PROVIDERS = ['google', 'chatterbox']`.
   - `getAvailableProviders` keeps only backends with those names, in the order the service lists them, and no longer adds `maxCharsPerRequest` (T6D-3, T7D-3, T7D-5; OAM-6.1, OAM-6.10).
   - `submitGeneration` gains a `language: ChatterboxLanguage` parameter, placed before `token`. The body adds `provider`, and `language` only when the provider is `chatterbox` (T6D-6, T7D-2; OAM-6.2, OAM-6.3, OAM-6.4, OAM-6.8, OAM-6.9).
5. **Modify `frontend/src/components/ProviderSelector.tsx`** (COA-17; OAM-6.10, M3.3.2 and M3.3.5's new assertion): removes the "Max {provider.maxCharsPerRequest} chars/request" paragraph (`:88-90`).
6. **Modify `frontend/src/components/VoiceSelector.tsx`** (COA-3; T6D-4, T7D-4; OAM-6.3, OAM-6.5 ×9, OAM-6.6, OAM-6.7, OAM-6.9):
   - It reads `selectedProvider`.
   - When the provider is `chatterbox`, it lists exactly the approved voices with no `provider`. It keeps the selection if that voice is listed, otherwise it selects the first listed voice, or none when the list is empty.
   - The effect also runs when `selectedProvider` changes.
   - The Google branch is unchanged.
7. **Modify `frontend/src/components/TextToSpeechInput.tsx`** (COA-17; T6D-7; OAM-6.8, OAM-6.9, M3.1.2, M3.1.6, M3.1.7, M3.1.8):
   - Removes `MAX_CHARS`, `WARNING_THRESHOLD`, the truncation, `maxLength`, the 90% warning and the maximum-reached message.
   - `char-count` reads `{charCount} characters` with the plain style.
8. **Modify `frontend/src/components/GenerationSubmitForm.tsx`** (COA-5; T7D-1; OAM-6.3, OAM-6.4, OAM-6.9): imports `LanguageSelector`, passes `selectedLanguage` to `submitGeneration`, and renders `<LanguageSelector />` after the provider selector only when the provider is `chatterbox`.

### Decisions for review

Added because T6D-5 and T6D-6 leave two choices to OAM-7, and these choices bind the page.

- **T7D-1 The language control appears only when Chatterbox is chosen.** Reason: the contract ignores `language` for Google, which takes the language from the voice name (`API-Contract.md`, Inference Generation, `language`). A control shown for Google would suggest a choice that has no effect. Alternative: always show it. Not chosen, for that reason.
- **T7D-2 A Google request carries no `language`.** The body is `{script, voice_id, provider: "google"}`. Reason: the request then carries only the fields the contract uses for that provider. Alternative: always send `language`, which the contract ignores for Google. Not chosen: it would send a value the service discards.
- **T7D-3 The provider list is filtered in `ttsApi.getAvailableProviders`, in the service's order.** Chatterbox is listed above Google (`API-Contract.md`, Inference Provider List ordering), and Google stays selected (`TTSContext.tsx:12`). Reason: the mapping from the contract's backend list to page providers already lives there (`ttsApi.ts:195-200`). Alternatives: filter in `ProviderSelector`; reorder Google first. Not chosen: OAM-6.1 sorts the offered values, so order is not part of T6D-3, and keeping the service's order needs no extra code.
- **T7D-4 An empty Chatterbox voice list shows the existing empty state and clears the selection.** It does not fall back to every voice, as the Google branch does (`VoiceSelector.tsx:33`). Reason: T6D-4 lists exactly the voices with no `provider`; a fallback would offer Google voices, which answer OAF-3 for Chatterbox. Clearing the selection keeps Generate disabled (`GenerationSubmitForm.tsx:21-25`), so a Google voice is never sent to Chatterbox. Alternative: keep the previous selection. Not chosen, for the same reason.
- **T7D-5 `maxCharsPerRequest` is removed from the `TTSProvider` type and the mapping, not only from the label.** Reason: COA-17 removes the limit, and no other `src` code reads the field (Current Repository State). Alternative: keep the field and stop rendering it. Not chosen: it would keep a 5000 value that no longer means anything.
- **T7D-6 The chosen language is held in the TTS context as `selectedLanguage`, initially `'en'`, set by `SELECT_LANGUAGE`, and `TTSGeneration.provider` adds `'chatterbox'`.** Reason: the voice and the provider are already held there (`TTSContext.tsx:11-12`, `:27-31`), and a generation's provider may now be `chatterbox` (`ttsApi.ts:39`, `:67`). Alternative: local state in `GenerationSubmitForm`. Not chosen: the choice would then not survive the form remounting, unlike the voice and provider. The type change is type-only.

## Proposed Code / Tests

The content below is for review only. It was not applied to the repository during planning. Each diff is against `HEAD` `a909fd2`, with LF line endings. Blank context lines hold one space, which must be kept. Hashes are SHA-256 of the block's content with LF line endings, and of the resulting file with CR removed.

### `frontend/src/components/LanguageSelector.tsx` (create, complete content)

Block and resulting file: `a37b0d071d452a662d8405a753b065f67de28e7160deebe3e789a4cf76b4b51d`.

```tsx
import React from 'react';
import { useTTS } from '@/hooks/useTTS';
import { ChatterboxLanguage } from '@/types/tts';

const LANGUAGES: Array<{ code: ChatterboxLanguage; label: string }> = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'Hindi' },
];

export function LanguageSelector() {
  const { selectedLanguage, dispatch } = useTTS();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const language = LANGUAGES.find((option) => option.code === e.target.value);
    if (language) {
      dispatch({ type: 'SELECT_LANGUAGE', payload: language.code });
    }
  };

  return (
    <div className="w-full" data-testid="language-selector-container">
      <label htmlFor="language-select-field" className="block text-sm font-medium text-gray-700 mb-2">
        Language
      </label>

      <select
        id="language-select-field"
        value={selectedLanguage}
        onChange={handleChange}
        className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        data-testid="language-select"
      >
        {LANGUAGES.map((language) => (
          <option key={language.code} value={language.code}>
            {language.label}
          </option>
        ))}
      </select>
    </div>
  );
}
```

### `frontend/src/types/tts.ts` (modify, complete unified diff)

Block: `051b068ef867c1f3f2cef019c9b0571e0cf274417f122c0c186ea01aa920931d`. Resulting file: `044050d6d99d0f6394915dbf8fd99bedb127c41bded9dc33aeda504bc31dbe8b`.

```diff
diff --git a/frontend/src/types/tts.ts b/frontend/src/types/tts.ts
index 4ab5b9b..3878609 100644
--- a/frontend/src/types/tts.ts
+++ b/frontend/src/types/tts.ts
@@ -4,7 +4,7 @@ export interface TTSGeneration {
   id: string;
   text: string;
   voiceId: string;
-  provider: 'google' | 'elevenlabs' | 'azure';
+  provider: 'google' | 'elevenlabs' | 'azure' | 'chatterbox';
   status: 'processing' | 'ready' | 'failed';
   audioFormat?: string;
   audioSize?: number;
@@ -21,9 +21,11 @@ export interface TTSProvider {
   id: string;
   name: string;
   available: boolean;
-  maxCharsPerRequest: number;
 }
 
+// The languages a Chatterbox generation accepts (API-Contract.md, Inference Generation, `language`).
+export type ChatterboxLanguage = 'en' | 'hi';
+
 export interface RateLimit {
   provider: string;
   totalLimit: number;
@@ -36,6 +38,7 @@ export interface RateLimit {
 export interface TTSState {
   selectedVoice: Voice | null;
   selectedProvider: string;
+  selectedLanguage: ChatterboxLanguage;
   generationText: string;
   isGenerating: boolean;
   currentGeneration: TTSGeneration | null;
@@ -49,6 +52,7 @@ export type TTSAction =
   | { type: 'SET_TEXT'; payload: string }
   | { type: 'SELECT_VOICE'; payload: Voice | null }
   | { type: 'SELECT_PROVIDER'; payload: string }
+  | { type: 'SELECT_LANGUAGE'; payload: ChatterboxLanguage }
   | { type: 'START_GENERATION' }
   | { type: 'UPDATE_GENERATION'; payload: TTSGeneration }
   | { type: 'GENERATION_COMPLETE'; payload: TTSGeneration }
```

### `frontend/src/context/TTSContext.tsx` (modify, complete unified diff)

Block: `ad4aa873d5a212ddfc0a25781d054d2b80b2f863144983a8d418e42ce81bc7d1`. Resulting file: `f18d45a03c273a2b068c8153a4b02d7ac5f9fc3e7bf92c3fb24b7074fb57487a`.

```diff
diff --git a/frontend/src/context/TTSContext.tsx b/frontend/src/context/TTSContext.tsx
index 2eefe16..3375c45 100644
--- a/frontend/src/context/TTSContext.tsx
+++ b/frontend/src/context/TTSContext.tsx
@@ -10,6 +10,7 @@ export const TTSContext = createContext<{
 const initialState: TTSState = {
   selectedVoice: null,
   selectedProvider: 'google',
+  selectedLanguage: 'en',
   generationText: '',
   isGenerating: false,
   currentGeneration: null,
@@ -30,6 +31,9 @@ function ttsReducer(state: TTSState, action: TTSAction): TTSState {
     case 'SELECT_PROVIDER':
       return { ...state, selectedProvider: action.payload };
 
+    case 'SELECT_LANGUAGE':
+      return { ...state, selectedLanguage: action.payload };
+
     case 'START_GENERATION':
       return { ...state, isGenerating: true, error: null };
 
```

### `frontend/src/services/ttsApi.ts` (modify, complete unified diff)

Block: `40007dd46d35e0b51e1798891f44c31dfffcbca4618a76c2800455d727a47e3f`. Resulting file: `6fe06e7b3896fc41a059ef71c2766590b1539bc1f082048ebe51044f55583c55`.

```diff
diff --git a/frontend/src/services/ttsApi.ts b/frontend/src/services/ttsApi.ts
index 8d64294..a56ef42 100644
--- a/frontend/src/services/ttsApi.ts
+++ b/frontend/src/services/ttsApi.ts
@@ -1,9 +1,12 @@
 import { API_CONFIG } from '@/utils/api-config';
-import { TTSGeneration, TTSProvider, RateLimit } from '@/types/tts';
+import { TTSGeneration, TTSProvider, RateLimit, ChatterboxLanguage } from '@/types/tts';
 import { Voice } from '@/types/voice';
 
 const VALID_GOOGLE_VOICE_PATTERN = /^[a-z]{2,3}-[A-Z]{2,}[-A-Za-z0-9]+$/;
 
+// The only providers a generation may name (API-Contract.md, Inference Generation, `provider`).
+const SELECTABLE_PROVIDERS = ['google', 'chatterbox'];
+
 export function normalizeVoiceIdForProvider(provider: string, voiceId?: string): string {
   const candidate = (voiceId || '').trim();
   if (!candidate) return 'en-US-Neural2-A';
@@ -33,6 +36,7 @@ export class TTSApiClient {
     text: string,
     voiceId: string,
     provider: string,
+    language: ChatterboxLanguage,
     token: string
   ): Promise<TTSGeneration> {
     const jobId = `gen-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
@@ -48,6 +52,8 @@ export class TTSApiClient {
       body: JSON.stringify({
         script: text,
         voice_id: normalizedVoiceId,
+        provider: normalizedProvider,
+        ...(normalizedProvider === 'chatterbox' ? { language } : {}),
       }),
     });
 
@@ -192,12 +198,13 @@ export class TTSApiClient {
 
     const data = await response.json();
 
-    return (data.backends || []).map((backend: any) => ({
-      id: backend.name,
-      name: backend.description.split(' (')[0],
-      available: true,
-      maxCharsPerRequest: 5000,
-    }));
+    return (data.backends || [])
+      .filter((backend: any) => SELECTABLE_PROVIDERS.includes(backend.name))
+      .map((backend: any) => ({
+        id: backend.name,
+        name: backend.description.split(' (')[0],
+        available: true,
+      }));
   }
 
   static async getApprovedVoices(token: string): Promise<Voice[]> {
```

### `frontend/src/components/ProviderSelector.tsx` (modify, complete unified diff)

Block: `11355d21751f9382a0e0c90608c2765866e440932b8dced70932152a5c718999`. Resulting file: `7313d6f8cd0623cdb714add095577795830b6ea7e842b17bfcba3f20c6978c9d`.

```diff
diff --git a/frontend/src/components/ProviderSelector.tsx b/frontend/src/components/ProviderSelector.tsx
index 7563cc5..da4ab77 100644
--- a/frontend/src/components/ProviderSelector.tsx
+++ b/frontend/src/components/ProviderSelector.tsx
@@ -85,9 +85,6 @@ export function ProviderSelector() {
 
             <div className="flex-1">
               <p className="font-medium text-gray-900">{provider.name}</p>
-              <p className="text-xs text-gray-600">
-                Max {provider.maxCharsPerRequest} chars/request
-              </p>
             </div>
 
             {!provider.available && (
```

### `frontend/src/components/VoiceSelector.tsx` (modify, complete unified diff)

Block: `2344dbc75a0af262d458e251a8298b16b498b125061651c3ed3939c3c96bfe19`. Resulting file: `fc0217f2c838e6420035eea47e84d44107a6d2db0d5acbd8577d1e867542fff2`.

```diff
diff --git a/frontend/src/components/VoiceSelector.tsx b/frontend/src/components/VoiceSelector.tsx
index 637fb8e..7b3064d 100644
--- a/frontend/src/components/VoiceSelector.tsx
+++ b/frontend/src/components/VoiceSelector.tsx
@@ -6,7 +6,7 @@ import { Voice } from '@/types/voice';
 
 export function VoiceSelector() {
   const auth = useAuth();
-  const { selectedVoice, dispatch } = useTTS();
+  const { selectedVoice, selectedProvider, dispatch } = useTTS();
   const [voices, setVoices] = useState<Voice[]>([]);
   const [loading, setLoading] = useState(false);
   const [error, setError] = useState<string | null>(null);
@@ -18,6 +18,19 @@ export function VoiceSelector() {
       setLoading(true);
       try {
         const approvedVoices = await ttsApi.getApprovedVoices(auth.token);
+
+        if (selectedProvider === 'chatterbox') {
+          // Recorded and uploaded voices carry no provider field (API-Contract.md, Voice List).
+          const cloningVoices = approvedVoices.filter((voice) => !voice.provider);
+          setVoices(cloningVoices);
+
+          const keepsSelection = cloningVoices.some((voice) => voice.id === selectedVoice?.id);
+          if (!keepsSelection && (selectedVoice || cloningVoices.length > 0)) {
+            dispatch({ type: 'SELECT_VOICE', payload: cloningVoices[0] ?? null });
+          }
+          return;
+        }
+
         const providerVoices = approvedVoices.filter((voice) => {
           const voiceId = (voice.id || '').trim();
           const provider = (voice as any).provider?.toLowerCase?.() || '';
@@ -45,7 +58,7 @@ export function VoiceSelector() {
     };
 
     fetchVoices();
-  }, [auth.token, dispatch, selectedVoice]);
+  }, [auth.token, dispatch, selectedVoice, selectedProvider]);
 
   const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
     const voiceId = e.target.value;
```

### `frontend/src/components/TextToSpeechInput.tsx` (modify, complete unified diff)

Block: `e671d740b786b1a77b59462b61b353ace2fb7fe6f004f0be29e3f3c7b0d8dbe7`. Resulting file: `470a93ae9000403d10da888514a87bd3f86ddf2b06ca22d54cec37b69e71485e`.

```diff
diff --git a/frontend/src/components/TextToSpeechInput.tsx b/frontend/src/components/TextToSpeechInput.tsx
index c8d1780..b22f461 100644
--- a/frontend/src/components/TextToSpeechInput.tsx
+++ b/frontend/src/components/TextToSpeechInput.tsx
@@ -1,19 +1,13 @@
 import React from 'react';
 import { useTTS } from '@/hooks/useTTS';
 
-const MAX_CHARS = 5000;
-const WARNING_THRESHOLD = 0.9;
-
 export function TextToSpeechInput() {
   const { generationText, dispatch } = useTTS();
 
   const charCount = generationText.length;
-  const percentage = charCount / MAX_CHARS;
-  const isWarning = percentage >= WARNING_THRESHOLD;
 
   const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
-    const text = e.target.value.slice(0, MAX_CHARS);
-    dispatch({ type: 'SET_TEXT', payload: text });
+    dispatch({ type: 'SET_TEXT', payload: e.target.value });
   };
 
   const handleClear = () => {
@@ -31,27 +25,15 @@ export function TextToSpeechInput() {
         value={generationText}
         onChange={handleChange}
         placeholder="Enter text to convert to speech..."
-        maxLength={MAX_CHARS}
         className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
         data-testid="text-input"
       />
 
       <div className="flex justify-between items-center mt-2">
-        <span
-          className={`text-sm ${
-            isWarning ? 'text-red-600 font-semibold' : 'text-gray-500'
-          }`}
-          data-testid="char-count"
-        >
-          {charCount} / {MAX_CHARS}
+        <span className="text-sm text-gray-500" data-testid="char-count">
+          {charCount} characters
         </span>
 
-        {isWarning && (
-          <span className="text-sm text-red-600 font-semibold" data-testid="char-warning">
-            ⚠️ 90% capacity reached
-          </span>
-        )}
-
         {charCount > 0 && (
           <button
             onClick={handleClear}
@@ -62,12 +44,6 @@ export function TextToSpeechInput() {
           </button>
         )}
       </div>
-
-      {charCount >= MAX_CHARS && (
-        <p className="text-xs text-red-500 mt-1" data-testid="max-chars-warning">
-          Maximum character limit reached
-        </p>
-      )}
     </div>
   );
 }
```

### `frontend/src/components/GenerationSubmitForm.tsx` (modify, complete unified diff)

Block: `9658d43c8d370896c3101196fc447e1a8892fa62748f2c7b160a7b6c6e9bf811`. Resulting file: `63767877568f61f0762ef4d8e21c52e500f71d1588de6f58db422278a5faa134`.

```diff
diff --git a/frontend/src/components/GenerationSubmitForm.tsx b/frontend/src/components/GenerationSubmitForm.tsx
index 1443ff8..8c790fb 100644
--- a/frontend/src/components/GenerationSubmitForm.tsx
+++ b/frontend/src/components/GenerationSubmitForm.tsx
@@ -6,6 +6,7 @@ import { TTSPollingService } from '@/services/ttsPollingService';
 import { TextToSpeechInput } from './TextToSpeechInput';
 import { VoiceSelector } from './VoiceSelector';
 import { ProviderSelector } from './ProviderSelector';
+import { LanguageSelector } from './LanguageSelector';
 
 export function GenerationSubmitForm() {
   const auth = useAuth();
@@ -13,6 +14,7 @@ export function GenerationSubmitForm() {
     generationText,
     selectedVoice,
     selectedProvider,
+    selectedLanguage,
     rateLimit,
     dispatch,
   } = useTTS();
@@ -37,6 +39,7 @@ export function GenerationSubmitForm() {
         generationText,
         selectedVoice.id,
         selectedProvider,
+        selectedLanguage,
         auth.token
       );
 
@@ -90,6 +93,8 @@ export function GenerationSubmitForm() {
 
       <ProviderSelector />
 
+      {selectedProvider === 'chatterbox' && <LanguageSelector />}
+
       {/* Rate Limit Display */}
       {rateLimit && (
         <div
```

### Accepted pre-existing frontend failures (verification input, T7Q-1 (a))

This is not a repository file. Execution Step 6 extracts it to `$TEMP` and command 4c compares the full-suite failures against it. Each line is `<test file> :: <test title>`, sorted with `LC_ALL=C`. These are the 27 `tts.spec.tsx` names of T6Q-1 and the 63 `voice.spec.tsx` names of `Plan.md:40`. Block: `0757f7d18f6e5264eb192cdf4e743291ad447629c727750bbe5056f7b269fa75`.

```text
tests/tts.spec.tsx :: M3.11.1: should persist selected voice in context
tests/tts.spec.tsx :: M3.11.2: should persist selected provider in context
tests/tts.spec.tsx :: M3.11.3: should persist generation history in context
tests/tts.spec.tsx :: M3.11.5: should update context when generation is deleted
tests/tts.spec.tsx :: M3.12.1: should render text input, voice selector, and provider selector together
tests/tts.spec.tsx :: M3.12.5: should render history list with playback controls
tests/tts.spec.tsx :: M3.12.7: should handle full workflow: input → submit → poll → play → history
tests/tts.spec.tsx :: M3.2.1: should display list of approved voices
tests/tts.spec.tsx :: M3.2.2: should show voice name for each option
tests/tts.spec.tsx :: M3.2.3: should show language for each voice
tests/tts.spec.tsx :: M3.2.4: should allow selecting a voice
tests/tts.spec.tsx :: M3.2.5: should persist selected voice in form
tests/tts.spec.tsx :: M3.2.6: should exclude pending and rejected voices
tests/tts.spec.tsx :: M3.2.7: should show preview for each voice
tests/tts.spec.tsx :: M3.3.1: should display available TTS providers
tests/tts.spec.tsx :: M3.3.2: should show provider name for each option
tests/tts.spec.tsx :: M3.3.3: should allow selecting a provider
tests/tts.spec.tsx :: M3.3.4: should disable unavailable providers
tests/tts.spec.tsx :: M3.3.5: should show provider capabilities (rate limit, max chars)
tests/tts.spec.tsx :: M3.3.6: should default to first available provider
tests/tts.spec.tsx :: M3.7.1: should fetch and display generation history
tests/tts.spec.tsx :: M3.7.2: should display generation text for each item
tests/tts.spec.tsx :: M3.7.3: should display voice name used for each generation
tests/tts.spec.tsx :: M3.7.4: should display provider used for each generation
tests/tts.spec.tsx :: M3.7.5: should display creation timestamp for each generation
tests/tts.spec.tsx :: M3.7.6: should display audio duration for ready generations
tests/tts.spec.tsx :: M3.7.7: should allow pagination through history
tests/voice.spec.tsx :: M2.10.10: should sort voices by upload date (newest first)
tests/voice.spec.tsx :: M2.10.1: should fetch and display all user voices
tests/voice.spec.tsx :: M2.10.2: should display voice name for each voice
tests/voice.spec.tsx :: M2.10.3: should display voice status (approved/pending/rejected)
tests/voice.spec.tsx :: M2.10.4: should display approval score when available
tests/voice.spec.tsx :: M2.10.5: should display upload date for each voice
tests/voice.spec.tsx :: M2.10.6: should display audio format (MP3/WAV/OGG)
tests/voice.spec.tsx :: M2.10.7: should display audio duration
tests/voice.spec.tsx :: M2.10.8: should display file size
tests/voice.spec.tsx :: M2.10.9: should show empty state when no voices exist
tests/voice.spec.tsx :: M2.11.1: should show play button for each voice
tests/voice.spec.tsx :: M2.11.2: should play audio when play button clicked
tests/voice.spec.tsx :: M2.11.3: should show pause button during playback
tests/voice.spec.tsx :: M2.11.4: should pause audio when pause button clicked
tests/voice.spec.tsx :: M2.11.5: should resume audio when play clicked after pause
tests/voice.spec.tsx :: M2.11.6: should show playback progress bar
tests/voice.spec.tsx :: M2.11.7: should show current time / total duration
tests/voice.spec.tsx :: M2.11.8: should allow seeking via progress bar click
tests/voice.spec.tsx :: M2.11.9: should stop playback when voice is deleted
tests/voice.spec.tsx :: M2.12.1: should show edit button for each voice
tests/voice.spec.tsx :: M2.12.2: should show rename dialog when edit clicked
tests/voice.spec.tsx :: M2.12.3: should prefill current name in rename dialog
tests/voice.spec.tsx :: M2.12.4: should update voice name on rename confirm
tests/voice.spec.tsx :: M2.12.5: should show delete button for each voice
tests/voice.spec.tsx :: M2.12.6: should show confirmation dialog before delete
tests/voice.spec.tsx :: M2.12.7: should delete voice when confirmed
tests/voice.spec.tsx :: M2.12.8: should not delete voice when cancelled
tests/voice.spec.tsx :: M2.12.9: should disable edit/delete during network request
tests/voice.spec.tsx :: M2.13.1: should persist voice list in context across navigation
tests/voice.spec.tsx :: M2.13.2: should update voice list when voice added
tests/voice.spec.tsx :: M2.13.3: should update voice list when voice deleted
tests/voice.spec.tsx :: M2.13.4: should update voice when renamed
tests/voice.spec.tsx :: M2.13.5: should update voice status when approval changes
tests/voice.spec.tsx :: M2.13.6: should track loading state during async operations
tests/voice.spec.tsx :: M2.13.7: should track errors in context state
tests/voice.spec.tsx :: M2.13.8: should clear errors when user dismisses
tests/voice.spec.tsx :: M2.14.1: should retry failed upload
tests/voice.spec.tsx :: M2.14.2: should retry failed delete
tests/voice.spec.tsx :: M2.14.3: should retry failed rename
tests/voice.spec.tsx :: M2.14.4: should retry failed evaluation polling
tests/voice.spec.tsx :: M2.14.5: should recover from network timeout
tests/voice.spec.tsx :: M2.14.6: should recover from rate limit temporarily
tests/voice.spec.tsx :: M2.14.7: should validate JWT token before upload
tests/voice.spec.tsx :: M2.14.8: should refresh token if expired during upload
tests/voice.spec.tsx :: M2.2.4: should stop recording and save blob on Stop button click
tests/voice.spec.tsx :: M2.3.2: should animate waveform during recording
tests/voice.spec.tsx :: M2.3.5: should freeze waveform after stop
tests/voice.spec.tsx :: M2.6.7: should hide progress bar after completion
tests/voice.spec.tsx :: M2.8.2: should poll every 2 seconds during evaluation
tests/voice.spec.tsx :: M2.8.3: should stop polling when status is ready
tests/voice.spec.tsx :: M2.8.4: should timeout after 300 poll attempts
tests/voice.spec.tsx :: M2.8.5: should show "Evaluating..." status during polling
tests/voice.spec.tsx :: M2.8.6: should show progress indicator during polling
tests/voice.spec.tsx :: M2.8.7: should handle polling error gracefully
tests/voice.spec.tsx :: M2.8.8: should allow user to cancel polling
tests/voice.spec.tsx :: M2.9.1: should show score after evaluation complete
tests/voice.spec.tsx :: M2.9.2: should show feedback message with score
tests/voice.spec.tsx :: M2.9.3: should auto-approve when score >= 60
tests/voice.spec.tsx :: M2.9.4: should auto-reject when score < 60
tests/voice.spec.tsx :: M2.9.5: should show approval status badge
tests/voice.spec.tsx :: M2.9.6: should allow user to manually approve voice
tests/voice.spec.tsx :: M2.9.7: should allow user to manually reject voice
tests/voice.spec.tsx :: M2.9.8: should show rejection reason field when rejecting
```

### Contract rule coverage

Added because this milestone implements the page side of contract rules; each maps to the code and the test that shows it.

| Contract rule (`API-Contract.md`) | Code | Test |
| --- | --- | --- |
| Inference Generation: `provider` is `"google"` or `"chatterbox"`, and any other value is answered `400` | `SELECTABLE_PROVIDERS` filter; `provider` in the body | OAM-6.1, OAM-6.2, OAM-6.3 |
| Inference Generation: `language` is exactly `"en"` or `"hi"`, required for Chatterbox, ignored otherwise | `ChatterboxLanguage`; `language` only for `chatterbox` | OAM-6.3, OAM-6.4 |
| Inference Generation: `script` has no length limit and is used whole | no truncation, no `maxLength` | OAM-6.8, OAM-6.9, M3.1.6 |
| Inference Provider List: display name is the description before ` (` | unchanged `split(' (')[0]` | OAM-6.1 |
| Voice List: recorded and uploaded voices have no `provider` | `!voice.provider` filter | OAM-6.3 |
| Chatterbox Failure Causes: `503 {"error": <message>}` | unchanged error display | OAM-6.5 |
| Inference Generation, Result delivery: the answer to the same request | unchanged `await` in `submitGeneration` | OAM-6.6, OAM-6.7 |

## Execution Steps

Run in Git Bash, from the repository root unless a step says `frontend/`. Logs go to `$TEMP`, outside the repository.

1. Confirm that the Human Review status below records the user's approval, and that it records the user's answer to T7Q-1. If either is missing, stop. If the answer is not (a), stop: T7C-4 and commands 4b–4d implement (a), and another answer needs a revised plan.
2. Run command 1. Stop if:
   - `git status --short` shows anything other than work-item records under `docs/.ai/chatterbox-original-app/`;
   - the backend diff prints anything;
   - the port check prints a listening line. In that case record OAM-7 in `Plan.md` Execution Status as `Waiting — ports 8002 and 8003 free from user` (T7R-1), and do not start or stop any process.
3. Set `P=docs/.ai/chatterbox-original-app/007_Implementation_Plan_OAM-7.md`. Extract the code blocks with CR removed:
   - `sed -n '148,188p' "$P" | tr -d '\r' > frontend/src/components/LanguageSelector.tsx`
   - `sed -n '196,237p' "$P" | tr -d '\r' > "$TEMP/oam7-tts.diff"`
   - `sed -n '245,266p' "$P" | tr -d '\r' > "$TEMP/oam7-context.diff"`
   - `sed -n '274,328p' "$P" | tr -d '\r' > "$TEMP/oam7-api.diff"`
   - `sed -n '336,349p' "$P" | tr -d '\r' > "$TEMP/oam7-provider.diff"`
   - `sed -n '357,398p' "$P" | tr -d '\r' > "$TEMP/oam7-voice.diff"`
   - `sed -n '406,473p' "$P" | tr -d '\r' > "$TEMP/oam7-input.diff"`
   - `sed -n '481,517p' "$P" | tr -d '\r' > "$TEMP/oam7-form.diff"`
   - `sha256sum frontend/src/components/LanguageSelector.tsx "$TEMP"/oam7-tts.diff "$TEMP"/oam7-context.diff "$TEMP"/oam7-api.diff "$TEMP"/oam7-provider.diff "$TEMP"/oam7-voice.diff "$TEMP"/oam7-input.diff "$TEMP"/oam7-form.diff` must print, in order, `a37b0d071d452a662d8405a753b065f67de28e7160deebe3e789a4cf76b4b51d`, `051b068ef867c1f3f2cef019c9b0571e0cf274417f122c0c186ea01aa920931d`, `ad4aa873d5a212ddfc0a25781d054d2b80b2f863144983a8d418e42ce81bc7d1`, `40007dd46d35e0b51e1798891f44c31dfffcbca4618a76c2800455d727a47e3f`, `11355d21751f9382a0e0c90608c2765866e440932b8dced70932152a5c718999`, `2344dbc75a0af262d458e251a8298b16b498b125061651c3ed3939c3c96bfe19`, `e671d740b786b1a77b59462b61b353ace2fb7fe6f004f0be29e3f3c7b0d8dbe7` and `9658d43c8d370896c3101196fc447e1a8892fa62748f2c7b160a7b6c6e9bf811`. Otherwise delete the new file and stop.
4. For each diff, in the order above: `git apply --check "$TEMP/oam7-<name>.diff" && git apply "$TEMP/oam7-<name>.diff"`. If a check fails, reverse this milestone's files (Rollback / Recovery) and stop.
5. Run command 2.
6. Extract the accepted list: `sed -n '525,614p' "$P" | tr -d '\r' > "$TEMP/oam7-accepted.txt"; sha256sum "$TEMP/oam7-accepted.txt"` must print `0757f7d18f6e5264eb192cdf4e743291ad447629c727750bbe5056f7b269fa75`. Then `wc -l < "$TEMP/oam7-accepted.txt"` must print `90`, and `LC_ALL=C sort -c "$TEMP/oam7-accepted.txt"` must print nothing.
7. Run commands 3, 4, 5, 6 and 7 in order, one at a time (T6D-9). Commands 4 and 5 run in the background with a completion notice, without polling. Each starts only after the previous command has exited and its output has been read.
8. Record the evidence in `Plan.md` below the Execution Status table, and set the OAM-7 row. Change nothing else in `Plan.md`. Update this plan's Human Review status.

## Acceptance / Completion Criteria

Criteria that limit which files may change exclude this milestone's Execution Status update in `Plan.md`.

- **T7C-1 Files.** Exactly `frontend/src/components/LanguageSelector.tsx` is created, and the seven files in Files to Modify are modified. Each matches its resulting-file hash above with CR removed. No test, mock, fixture, build, configuration, dependency or backend file changes. Only work-item records under `docs/.ai/chatterbox-original-app/` change besides.
- **T7C-2 Compile.** `npm run type-check` exits 0.
- **T7C-3 The OAM-6 RED tests pass.** `npx vitest run tests/tts-provider-choice.spec.tsx` reports `Tests  19 passed (19)`, with no `FAIL` line, no `[MSW]` warning and no `unexpected request`. The test file is unchanged (T7C-1).
- **T7C-4 The full frontend suite fails only on the named pre-existing failures** (`Plan.md` OAM-7 success criteria; T7Q-1 (a)). The run reports `Test Files  2 failed | 3 passed (5)` and `Tests  90 failed | 282 passed (372)`. Its failing tests are exactly the 90 names in the accepted list, so the comparison prints nothing under `unexpected:` and nothing under `accepted, not failing:`. In particular:
  - M3.1.2, M3.1.6, M3.1.7 and M3.1.8 pass. They are not in the list, so a failure of any of them shows under `unexpected:`.
  - Each of the 27 `tts.spec.tsx` failures shows its baseline cause, as `006` T6C-6 defines it and command 4d checks. This includes M3.3.2 and M3.3.5, each with `provider-error` "fetch failed" (`Plan.md` OAM-7: "apart from M3.3.2 and M3.3.5 keeping their pre-existing failure").
  - The 63 `voice.spec.tsx` failures are accepted by name. `voice.spec.tsx` imports none of the eight files this milestone changes (Affected Tests).
  - `auth-api.spec.tsx`, `auth.spec.tsx` and `tts-provider-choice.spec.tsx` pass.
- **T7C-5 The backend is unchanged, and the backend suite keeps its result** (`Plan.md` OAM-7: "The backend is unchanged"; OAS-2; OAV-2):
  - No file under `voice_narration/`, `tests/`, `requirements-dev.txt` or `.gitignore` changes.
  - The OAV-2 run collects `118` tests, with none from the three V3Q-3 files, and fails only on `tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing` (V3Q-1 (a)).
  - Afterwards `git status --short -- audio_storage` prints nothing (OAV-3, OAS-1).
- **T7C-6 No test fakes or calls Chatterbox, and no process started by this run is left running** (COA-16, CON-2). No test file changes (T7C-1). No Docker or `gcloud` command runs. Command 7 shows no `node.exe` or `python.exe` process started by this run.

## Answered Questions

Added because `implementation-planning` Pre-existing Failures requires the user to decide, before approval, how the criteria treat failures seen on the unmodified baseline.

- **T7Q-1 — answered by Avinash Srivastava on 2026-11-14: "Approve with (a)", option (a).** How are the 90 pre-existing frontend failures treated in OAM-7's full-suite run? `Plan.md` OAM-7 requires the full frontend suite, so all 90 run. Each was established on the unmodified baseline at HEAD `a909fd2` (Preconditions; Planning-Time Dry Run). They are the 90 lines of the accepted list above:
  - `tts.spec.tsx`, 27, accepted under T6Q-1 (a) at OAM-6:
    - M3.2.1–M3.2.7 and M3.3.1–M3.3.6;
    - M3.7.1–M3.7.7;
    - M3.11.1, M3.11.2, M3.11.3 and M3.11.5;
    - M3.12.1, M3.12.5 and M3.12.7.

    Baseline cause: the test mock does not serve the endpoints the page calls. 17 of them show a selector's "fetch failed", and 10 show the history fetch's `TypeError: fetch failed` on stderr (`006` T6C-6).
  - `voice.spec.tsx`, 63, named in `Plan.md:40` and in `006:838`:
    - M2.2.4, M2.3.2, M2.3.5 and M2.6.7;
    - M2.8.2–M2.8.8 and M2.9.1–M2.9.8;
    - M2.10.1–M2.10.10, M2.11.1–M2.11.9 and M2.12.1–M2.12.9;
    - M2.13.1–M2.13.8 and M2.14.1–M2.14.8.

    Baseline first errors: 60 time out at 5000 ms, and 3 fail on assertions (Preconditions).

  Options:
  - **(a) Recommended. Accept exactly these 90 names, consistent with T6Q-1 (a).** Each is recorded in the milestone evidence. The run is accepted only when its failures are exactly these 90: nothing under `unexpected:` and nothing under `accepted, not failing:`. The 27 `tts.spec.tsx` failures must also each show their T6C-6 baseline cause. The 63 `voice.spec.tsx` failures are checked by name only, because that file imports no file this milestone changes. Any other failure, or a named one that passes or changes cause, stops the milestone without a rerun. This is the only non-blocking form `implementation-planning` Pre-existing Failures allows. T7C-4 and commands 4b–4d are written for it.
  - (b) As (a), except that a named test that passes is recorded but does not stop the milestone. This matters for the 60 time-outs (T7R-2). It needs a revised T7C-4 and command 4c before approval.
  - (c) Another treatment you state. Repairing these tests is not in this work item's requirements (`Plan.md`, Non-Blocking Open Decisions), so it would need replanning.

## Verification

### Commands

1. Preconditions (repository root):
   `git status --short; git log --oneline -1`
   `git diff --stat ce598d4 HEAD -- voice_narration tests requirements-dev.txt .gitignore` → must print nothing
   `netstat -ano | grep LISTENING | grep -E ":(8002|8003) "; echo "ports-check exit $?"` → must print only `ports-check exit 1`
   `test -d frontend/node_modules && echo "node_modules present" || (cd frontend && npm ci)` (OAV-4)
   `tasklist //FI "IMAGENAME eq node.exe" //NH > "$TEMP/oam7-node-before.txt"; tasklist //FI "IMAGENAME eq python.exe" //NH > "$TEMP/oam7-python-before.txt"`
2. Files and compile, after Execution Steps 3–4 (repository root; T7C-1, T7C-2):
   `for f in types/tts.ts context/TTSContext.tsx services/ttsApi.ts components/ProviderSelector.tsx components/VoiceSelector.tsx components/TextToSpeechInput.tsx components/GenerationSubmitForm.tsx components/LanguageSelector.tsx; do printf '%s ' "$f"; tr -d '\r' < "frontend/src/$f" | sha256sum; done` → the eight resulting-file hashes above, in that order (`LanguageSelector.tsx`: its block hash)
   `git status --short`
   `(cd frontend && npm run type-check > "$TEMP/oam7-tsc.log" 2>&1; echo "type-check exit $?")` (OAV-6)
3. The OAM-6 RED tests (in `frontend/`; OAV-5 scoped; T7C-3):
   `npx vitest run tests/tts-provider-choice.spec.tsx > "$TEMP/oam7-new.log" 2>&1; sed 's/\x1b\[[0-9;]*m//g' "$TEMP/oam7-new.log" > "$TEMP/oam7-new.txt"; grep -E "^ +Tests " "$TEMP/oam7-new.txt"; printf 'FAIL => '; grep -cE "^ FAIL " "$TEMP/oam7-new.txt"; printf 'MSW => '; grep -c "\[MSW\]" "$TEMP/oam7-new.txt"; printf 'unexpected => '; grep -c "unexpected request" "$TEMP/oam7-new.txt"`
4. The full frontend suite (OAV-5; T7C-4). It runs in the background; it took about 320 s at baseline.
   - 4a, in `frontend/`: `npx vitest run > "$TEMP/oam7-full.log" 2>&1; sed 's/\x1b\[[0-9;]*m//g' "$TEMP/oam7-full.log" > "$TEMP/oam7-full.txt"; grep -E "^ +(Test Files|Tests) " "$TEMP/oam7-full.txt"; grep -E "^ (✓|❯) +tests/[^ ]+ +\(" "$TEMP/oam7-full.txt"`. Then, from the repository root, `netstat -ano | grep LISTENING | grep -E ":(8002|8003) "; echo "ports-check exit $?"`.
   - 4b: the accepted list was extracted in Execution Step 6.
   - 4c: `grep -E "^ FAIL " "$TEMP/oam7-full.txt" | sed -E 's/^ FAIL +([^ ]+) .*> /\1 :: /' | LC_ALL=C sort > "$TEMP/oam7-full-failed.txt"; wc -l < "$TEMP/oam7-full-failed.txt"; echo "unexpected:"; LC_ALL=C comm -13 "$TEMP/oam7-accepted.txt" "$TEMP/oam7-full-failed.txt"; echo "accepted, not failing:"; LC_ALL=C comm -23 "$TEMP/oam7-accepted.txt" "$TEMP/oam7-full-failed.txt"`
   - 4d: the baseline causes of the 27 `tts.spec.tsx` failures (`006` T6C-6), on `T="$TEMP/oam7-full.txt"`:
     `for t in "M3.3.2:" "M3.3.5:"; do printf '%s fetch failed => ' "$t"; awk -v t="$t" '$0 ~ "^ FAIL .*> "t {p=1;n=0} p{print;n++} n>60{p=0}' "$T" | grep -c "fetch failed"; done` → each at least `1`
     `for t in M3.2.1 M3.2.2 M3.2.3 M3.2.4 M3.2.5 M3.2.6 M3.2.7 M3.3.1 M3.3.3 M3.3.4 M3.3.6 M3.11.1 M3.11.2 M3.12.1 M3.12.7; do s=$(awk -v t="$t:" '/^ FAIL / {p=(index($0,"> " t)>0); next} /Test Files/ {p=0} p' "$T"); printf '%s: fetch-failed=%s error-id=%s\n' "$t" "$(printf '%s\n' "$s" | grep -c 'fetch failed')" "$(printf '%s\n' "$s" | grep -cE 'data-testid="(provider|voice-selector)-error"')"; done` → 15 lines, each with `fetch-failed` and `error-id` at least `1`
     `for t in M3.7.1 M3.7.2 M3.7.3 M3.7.4 M3.7.5 M3.7.6 M3.7.7 M3.11.3 M3.11.5 M3.12.5; do s=$(awk -v t="$t:" '/^ FAIL / {p=(index($0,"> " t)>0); next} /Test Files/ {p=0} p' "$T"); printf '%s: container-missing=%s empty-state=%s history-log=%s\n' "$t" "$(printf '%s\n' "$s" | grep -m1 -E '^(AssertionError|TestingLibraryElementError)' | grep -c 'Unable to find an element by: \[data-testid="generation-history-container"\]')" "$(printf '%s\n' "$s" | grep -c 'data-testid="empty-state"')" "$(awk -v t="$t:" '/^(stderr|stdout) \| / {p=(index($0,"> " t)>0); next} /^ (FAIL|✓|×|❯) / {p=0} p && /^Failed to fetch history: \[TypeError: fetch failed\]/ {c++} END {print c+0}' "$T")"; done` → 10 lines, each with `container-missing=1`, and `empty-state` and `history-log` at least `1`

     Any other value fails T7C-4.
5. The backend suite and the V3Q-1 (a) check (repository root; OAV-2, OAV-3; T7C-5). It runs in the background.
   - 5a: `printf '%s\n' 'tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing' > "$TEMP/oam7-backend-accepted.txt"; wc -l < "$TEMP/oam7-backend-accepted.txt"`
   - 5b: `python -m pytest -q --ignore=tests/test_persistence.py --ignore=tests/test_authentication_consent.py --ignore=tests/test_voice_enrollment.py > "$TEMP/oam7-backend.log" 2>&1; tail -1 "$TEMP/oam7-backend.log"; grep -cE "^!+ (Interrupted|KeyboardInterrupt)" "$TEMP/oam7-backend.log"`
   - 5c: `grep -E "^(FAILED|ERROR) " "$TEMP/oam7-backend.log" | sed -E 's/^(FAILED|ERROR) //; s/ - .*$//' | LC_ALL=C sort -u > "$TEMP/oam7-backend-failing.txt"; echo "unexpected:"; LC_ALL=C comm -23 "$TEMP/oam7-backend-failing.txt" "$TEMP/oam7-backend-accepted.txt"; echo "accepted, not failing:"; LC_ALL=C comm -13 "$TEMP/oam7-backend-failing.txt" "$TEMP/oam7-backend-accepted.txt"; grep -E "^(FAILED|ERROR) " "$TEMP/oam7-backend.log"`
   - 5d: `python -m pytest --collect-only -q -p no:cacheprovider --ignore=tests/test_persistence.py --ignore=tests/test_authentication_consent.py --ignore=tests/test_voice_enrollment.py > "$TEMP/oam7-collect.log" 2>&1; tail -1 "$TEMP/oam7-collect.log"; grep -cE "^tests/(test_persistence|test_authentication_consent|test_voice_enrollment)\.py::" "$TEMP/oam7-collect.log"`
   - 5e: `git status --short -- audio_storage`. Only if it prints anything: record it, run `git checkout -- audio_storage` and `git clean -fd -- audio_storage`, and repeat `git status --short -- audio_storage`, which must print nothing.
6. Repository state (repository root; T7C-1, T7C-5):
   `git status --short`
   `git diff --stat -- voice_narration tests requirements-dev.txt .gitignore frontend/tests frontend/package.json frontend/package-lock.json frontend/tsconfig.json frontend/vitest.config.ts` → must print nothing
   `git status --short -- audio_storage` → must print nothing
7. Processes (T7C-6): `tasklist //FI "IMAGENAME eq node.exe" //NH > "$TEMP/oam7-node-after.txt"; tasklist //FI "IMAGENAME eq python.exe" //NH > "$TEMP/oam7-python-after.txt"; diff "$TEMP/oam7-node-before.txt" "$TEMP/oam7-node-after.txt"; diff "$TEMP/oam7-python-before.txt" "$TEMP/oam7-python-after.txt"`. For each PID present only in an after file, read its command line (`powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'ProcessId=<pid>' | Select-Object CommandLine,CreationDate"`). Stop it before reporting only if this run started it. Record any other process and leave it alone.

### Affected Tests

- `frontend/tests/tts-provider-choice.spec.tsx` (19 tests): the RED evidence. It renders the `TextToSpeech` page, whose form imports every changed file.
- `frontend/tests/tts.spec.tsx` (94 tests): it imports `TextToSpeechInput`, `VoiceSelector`, `ProviderSelector`, `GenerationSubmitForm` and `TTSContext` (`tts.spec.tsx:16-24`).
- Found by `grep -rln "ttsApi\|types/tts\|TTSContext\|ProviderSelector\|VoiceSelector\|TextToSpeechInput\|GenerationSubmitForm\|useTTS\|pages/TextToSpeech" frontend/src frontend/tests`. Among test files, it lists only these two and `tests/fixtures/tts.ts`, which imports only `src/types/voice` (`fixtures/tts.ts:5`).
- Not affected: `frontend/tests/voice.spec.tsx`, `frontend/tests/auth.spec.tsx` and `frontend/tests/auth-api.spec.tsx`. Their imports reach `VoiceRecorder`, `VoiceUpload`, `VoiceLibrary`, `AuthContext`, `VoiceContext`, `voiceApi`, `useAuth`, `useVoice`, `types/voice`, `utils/constants` and their own mocks and fixtures. None of these is in that grep's list. They run only as part of the full suite (command 4).
- Backend tests: none affected. No backend file changes, and the backend suite runs once as `Plan.md` OAV-2 requires at OAM-7.

### Expected Evidence

Expected / Predicted — Not Yet Verified.

- Command 1: `git status --short` prints nothing apart from work-item records under `docs/.ai/chatterbox-original-app/`; `a909fd2` (or a later commit holding only this work item's records); the backend diff prints nothing; `ports-check exit 1`; `node_modules present`.
- Command 2: the eight hashes above, in order. `git status --short` shows seven ` M frontend/src/…` lines and `?? frontend/src/components/LanguageSelector.tsx`, plus work-item records under `docs/.ai/chatterbox-original-app/`. Then `type-check exit 0`.
- Command 3: `Tests  19 passed (19)`; `FAIL => 0`; `MSW => 0`; `unexpected => 0`.
- Command 4a: `Test Files  2 failed | 3 passed (5)` and `Tests  90 failed | 282 passed (372)`. The per-file lines:
  - `✓ tests/auth-api.spec.tsx  (80 tests)`;
  - `✓ tests/auth.spec.tsx  (73 tests)`;
  - `✓ tests/tts-provider-choice.spec.tsx  (19 tests)`;
  - `❯ tests/tts.spec.tsx  (94 tests | 27 failed)`;
  - `❯ tests/voice.spec.tsx  (106 tests | 63 failed)`.

  Then `ports-check exit 1`.
- Command 4c: `90`, then nothing under `unexpected:` and nothing under `accepted, not failing:`.
- Command 4d: as at baseline and in dry-run step 7:
  - `M3.3.2: fetch failed => 3` and `M3.3.5: fetch failed => 3`;
  - 15 lines `fetch-failed=2 error-id=2`, except M3.12.1 and M3.12.7 with `4` and `4`;
  - 10 lines `container-missing=1 empty-state=2 history-log=1`.
- Command 5: `1`. Then `1 failed, 100 passed, 17 skipped, … warnings in …` and `0`. Then `unexpected:` and `accepted, not failing:` with nothing under either, and the one `FAILED` line is the accepted test with `ImportError: cannot import name 'ProductionInferenceProvider'`. Then `118 tests collected …` and `0`. Command 5e, predicted from OAM-5's run: ` M audio_storage/generation_index.json` and `?? audio_storage/generations/<UTC date>/` (Plan OAR-1); after the restore, nothing.
- Command 6: the same `git status --short` as command 2, and nothing from the other two.
- Command 7: no `node.exe` or `python.exe` process started by this run is running.
- Repeat run: none. These tests touch no persistent state and override no configuration. The backend suite's `audio_storage/` writes are restored by OAV-3, as at OAM-3 and OAM-5 (`implementation-planning` Repeatable, Isolated Verification).
- Preserved-behavior tests (expected to pass at RED): not applicable; this is a GREEN milestone. `Plan.md` assigns OAM-7 the COA-14 preserved row through the full frontend suite (T7C-4).

### Planning-Time Dry Run

Planning-time dry run, not milestone evidence.

Disposable copy: `git archive HEAD frontend | tar -x -C <scratchpad>/oam7/dry`, then `npm ci` there (exit 0). The diffs were made in a second scratch repository, `<scratchpad>/oam7/diffrepo` (`core.autocrlf=false`). Its base was the `HEAD` blobs of the seven files (LF), and the same scripted edits were applied there and to the copy. The repository was not modified. The real worktree was used only for `git apply --check`, which writes nothing.

| # | Command | Result |
| --- | --- | --- |
| 1 | Scripted edits applied to the copy's `src/` and to `diffrepo`. Then `tr -d '\r' \| sha256sum` of each of the eight files in both | All eight equal: the resulting-file hashes above |
| 2 | `git diff -- <file>` in `diffrepo` for each modified file; `git apply --check <diff>` of each against the real worktree; then `git status --short` there | Seven `applies:` lines. `git status --short` printed nothing |
| 3 | `npm run type-check` (copy) | exit 0 |
| 4 | `npx vitest run tests/tts-provider-choice.spec.tsx` (copy) | `Tests  19 passed (19)`, Duration 11.04 s; `FAIL` 0; `[MSW]` 0; `unexpected request` 0 |
| 5 | (step 4 ran while an unrelated listener was on 8003, see step 6) | Unaffected: every request the file causes is answered by its own handlers, and the catch-all recorded none (T6D-1) |
| 6 | `npx vitest run tests/tts.spec.tsx` (copy) | `Tests  27 failed \| 67 passed (94)`. The 27 names equal T6Q-1's, and M3.1.2/6/7/8 pass. But the causes differed from the baseline: `provider-error` read `Failed to get providers: 401`, the history fetch logged `Failed to get generation history: 401`, and the 4d loops printed `fetch failed => 0` for M3.3.2/M3.3.5 and `history-log=0`. Cause, established: `netstat` showed `127.0.0.1:8003 LISTENING 302696`, created 20:28:19. That is after the baseline full run's `tts.spec.tsx` had finished: it started at 20:24:27 and the file took 34.9 s. The listener was started by a PowerShell session of the unrelated `v11\Traffic` project ("Testing AUTH SERVICE (port 8003)", created 20:28:17). It was left alone |
| 7 | `VITE_TTS_API_BASE_URL=http://localhost:54934 npx vitest run tests/tts.spec.tsx` (copy; a loopback port found free with a bound-then-closed socket) | `Tests  27 failed \| 67 passed (94)`, the same 27 names. The 4d loops print the baseline values exactly: `fetch failed => 3` twice; 15 lines `fetch-failed=2 error-id=2` (M3.12.1, M3.12.7: `4`/`4`); 10 lines `container-missing=1 empty-state=2 history-log=1`. `Failed to get providers: 401` 0 times. This is a planning-only probe; execution uses no such override (T7R-1) |
| 8 | `sed -n` / `tr -d '\r'` / `sha256sum` of every line range in Execution Steps 3 and 6, on this plan | Each prints the hash Execution Step 3 or 6 requires |
| 9 | Commands 4c and 4d, run on the baseline full-suite log with the accepted list extracted from this plan | 4c: `113`; `unexpected:` lists exactly the 19 `tts-provider-choice.spec.tsx` tests and `tts.spec.tsx` M3.1.2, M3.1.6, M3.1.7 and M3.1.8; `accepted, not failing:` is empty. 4d prints the baseline values. So the commands select what T7C-4 needs |
| 10 | `tasklist` of `node.exe` before the baseline runs and after step 7, then `diff` | No `node.exe` PID that this planning run started is still running |

Not run during planning (`prompt-driven-development` Test Scope: the full suite runs once, at execution): the full frontend suite with the GREEN code, and the backend suite. The backend is unchanged since OAM-5, whose run is the predicted result (`Plan.md`, OAM-5 GREEN evidence, command 5b).

Created during planning, all under the session scratchpad and deleted afterwards: `oam7/dry/` (the copy with its `node_modules`), `oam7/diffrepo/`, `oam7/diffs/`, the baseline and dry-run logs, `oam7-tools/apply_green.py`, `oam7-tools/build_plan.py` and `oam7-tools/plan_template.md`.

## Risks

- **T7R-1 A local listener on 8002 or 8003 changes the `tts.spec.tsx` causes.** `tts.spec.tsx` sends unmocked requests to the real ports (`006` T6R-2). During planning, an unrelated service began listening on 8003 and answered `401`. The 27 names still failed, but with different causes (dry run, step 6). Mitigation: command 1 stops execution, as `Waiting — ports 8002 and 8003 free from user`, while either port is listening. Command 4a checks the ports again after the run. If a listener appeared during the run, the 4d check shows it, and the milestone stops without a rerun. Execution does not start, stop or redirect any service. Redirecting with `VITE_TTS_API_BASE_URL`, as in dry-run step 7, would also redirect `tts-provider-choice.spec.tsx`, whose mocks are fixed to port 8003. So it is not offered as a contingency.
- **T7R-2 60 of the `voice.spec.tsx` failures are 5000 ms time-outs.** Whether a timed-out test can finish in time under different load is a hypothesis; it was not measured. Under T7Q-1 (a), a named test that passes stops the milestone; option (b) avoids that. Both baseline runs failed the same 63 names.
- **T7R-3 Overlapping voice-list fetches.** The voice selector's effect has no cancellation (`VoiceSelector.tsx:14-48`), and switching providers now also starts a fetch. If the user switches twice before a fetch answers, a stale answer can set the list. Hypothesis, from the code and not tested: any answer that changes the selection runs the effect again with the current provider (`:48`, and the new dependency), so the list converges. A cancellation guard is not added, because no approved test or requirement asks for it, and GREEN stays minimal.
- **T7R-4 The `/voices` TTS tab changes too.** It renders the same `GenerationSubmitForm` (`VoiceManagement.tsx:162`), so it gains the provider filter, the language control and the uncapped text box. That is consistent with COA-17 "for every provider", but no test covers that tab.
- **T7R-5 Duplicate React key warning** (`006` T6R-5): `GENERATION_COMPLETE` and `ADD_TO_HISTORY` both prepend the same generation (`TTSContext.tsx:48`, `:62`). It is existing behavior, fails no test, and is out of scope.
- **T7R-6 Code quality, Medium findings kept** (`code-quality`):
  - `getAvailableProviders` keeps the existing `(backend: any)`. Typing the backend list is outside the smallest change.
  - `SELECTABLE_PROVIDERS` restates the contract's two accepted values on the client. That is the one place the page needs them.
  - "1 characters" reads oddly, but T6D-7 fixes the wording as "`<n>` characters".

  No High finding is open.
- **T7R-7 Run time.** The full suite took about 320 s at baseline, mostly `voice.spec.tsx`, and the backend suite took 145 s at OAM-5. Both run in the background with a completion notice (`prompt-driven-development` Test Scope and Output).
- Security: no authentication or authorization requirement is owned or verified by this milestone. The page keeps sending the existing bearer token unchanged, and no identity, role or ownership comparison is added (`API-Contract.md`, Out of Scope: neither service checks `Authorization`).

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Reverse only this milestone's files, from the repository root:

- `rm frontend/src/components/LanguageSelector.tsx`
- `git checkout -- frontend/src/types/tts.ts frontend/src/context/TTSContext.tsx frontend/src/services/ttsApi.ts frontend/src/components/ProviderSelector.tsx frontend/src/components/VoiceSelector.tsx frontend/src/components/TextToSpeechInput.tsx frontend/src/components/GenerationSubmitForm.tsx`
- After a backend run only: `git checkout -- audio_storage` and `git clean -fd -- audio_storage` (OAV-3).

## Explicitly Out of Scope

- Any change to a test, mock or fixture, including `frontend/tests/tts-provider-choice.spec.tsx`, `frontend/tests/tts.spec.tsx`, `frontend/tests/mocks/tts-handlers.ts` and `frontend/tests/fixtures/tts.ts`.
- Any backend, build, configuration or dependency change (`Plan.md` OAM-7 exclusions).
- The recorder and the upload form (OAD-1).
- Per-user voice filtering, a Google fallback, text splitting, any new limit, and any duplicate prevention beyond the existing disabled button (`Plan.md` OAM-7 exclusions; COA-13).
- Repairing any pre-existing failure, including M3.3.2 and M3.3.5 (`Plan.md` OAM-7 exclusions).
- Showing a cloned generation's provider in history (`getGenerationHistory` keeps `'google'`, `ttsApi.ts:160`). COA-10 is verified at OAM-8, and no OAM-6 test asks for it.
- Any test or code that fakes or calls Chatterbox (COA-16), and any Docker or `gcloud` command (CON-2).

## Human Review

Status: Executed 2026-11-14 — GREEN verified; see `Plan.md`, Execution Status, "OAM-7 GREEN evidence". (Approved by Avinash Srivastava on 2026-11-14, as written, including decisions T7D-1 to T7D-6 and the T7Q-1 answer (a).)
