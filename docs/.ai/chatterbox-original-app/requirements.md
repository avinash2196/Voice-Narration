# Requirements — chatterbox-original-app

Every item ends with one source label:

- `[User: brief]` or `[User: Qn]` — stated by the user, in the brief or in the answer to clarification question n (see Clarification Log).
- `[Repo: <path>:<line>]` — established by inspecting the current repository during this capture.
- `[Artifact: <work-item>/<file> <ID>]` — an approved requirement of another work item that this work item explicitly depends on; quote it, do not extend it.
- `[Derived from <sources> — confirmed Qn]` — a consequence derived from other items; recorded only after the user confirmed it.
- `[Left to <phase> — non-blocking]` — valid only in Non-Blocking Decisions.

## Goal

In the user's words: "all we wanted was use chatterbox from original FE and get the voice clones." The user records or uploads a voice in the original multi-page app and generates cloned speech with Chatterbox from its TextToSpeech page. [User: brief]

## Status

Approved by Avinash Srivastava on 2026-11-13 (revision recording Q41–Q45; the earlier version was approved on 2026-11-12).

## Relationship to Product-Level Requirements

No product-level `docs/requirements.md` exists in the repository, so no product-level statement is changed. [Repo: docs/ — no requirements.md present]

## Business Context

- **Problem:** the earlier Chatterbox work item was built on a one-page prototype frontend and backend, not on the original app. The user wants Chatterbox voice cloning inside the original app. [User: brief]
- **Actors:** logged-in users of the original app. All logged-in users share one voice list, and any of them may clone any voice in it. [Derived from recommended option — confirmed Q35]
- **Outcome:** the work is done when a voice recorded or uploaded on `/voices`, then picked on `/tts`, produces speech in that voice through the deployed Chatterbox. The user checks this manually against the deployed Cloud Run service. [User: Q1, Q13]
- **Business rules:**
  - A new voice is approved automatically, as today, and can be cloned straight away. [User: Q19]
  - Cloning supports English and Hindi. The language is chosen for each generation on the TTS page. [User: Q4, Q20]
  - Text to be spoken has no length limit, for every provider. [User: Q17, Q41]
  - Each voice and its sample are deleted 5 days after upload and cannot be recovered. [Derived from recommended option — confirmed Q36]

## Repository-Confirmed Facts

Inspected at HEAD `664cee4`, the same commit as `feature/audio-download-persistence-docs`.

- Routes `/auth/login`, `/auth/signup`, `/`, `/voices` and `/tts` exist; `/`, `/voices` and `/tts` are behind `ProtectedRoute`. [Repo: frontend/src/App.tsx:279-304]
- The frontend calls the voice service at `http://localhost:8002` and the TTS (inference) service at `http://localhost:8003` by default. [Repo: frontend/src/utils/api-config.ts:9-10]
- The recorder creates `new MediaRecorder(stream)` with no MIME type, so Chrome records in its default format (WebM). The recording is labelled `audio/wav` and uploaded as `recording.wav`. [Repo: frontend/src/components/VoiceRecorder.tsx:52, :67, :160]
- The upload form accepts MP3, WAV and OGG files. [Repo: frontend/src/components/VoiceUpload.tsx:104-105]
- The running voice service is `voice_narration.simple_voices`. [Repo: start-voice-service.bat:25] It keeps voices in an in-memory dictionary. [Repo: voice_narration/simple_voices/application.py:10] On upload it extracts the audio bytes but keeps only their length, so the sample audio is not stored. [Repo: voice_narration/simple_voices/application.py:102, :111] Every upload is stored with status `approved` and score 95. [Repo: voice_narration/simple_voices/application.py:113-114] A voice can be deleted. [Repo: voice_narration/simple_voices/application.py:186-187]
- The inference service uses one provider, chosen at startup by `INFERENCE_PROVIDER`: `google` or the mock; `azure` falls back to the mock. [Repo: voice_narration/inference/__main__.py:33-58]
- The provider registry registers `mock`, `google` and `azure`. [Repo: voice_narration/inference/registry.py:68-77] Every provider implements `generate(script, voice_id, **kwargs)`. [Repo: voice_narration/inference/providers/base.py:16-21] `GET /inference/backends` lists the registered providers. [Repo: voice_narration/inference/application.py:343-373]
- The frontend's provider list comes from `GET /inference/backends`. [Repo: frontend/src/services/ttsApi.ts:183-200] The infer request body carries only `script` and `voice_id`, so the provider chosen on the page is not sent. [Repo: frontend/src/services/ttsApi.ts:42-51; voice_narration/inference/application.py:463]
- For the `google` provider, a voice id that does not look like a Google voice is replaced with `en-US-Neural2-A`. [Repo: frontend/src/services/ttsApi.ts:7-19] The voice selector shows only Google-pattern voices whenever any exist. [Repo: frontend/src/components/VoiceSelector.tsx:21-33]
- The TTS text box caps text at 5000 characters for every provider: it truncates input and sets `maxLength`. [Repo: frontend/src/components/TextToSpeechInput.tsx:4, :15, :34] It shows the count as "n / 5000" [Repo: frontend/src/components/TextToSpeechInput.tsx:46], a warning at 90% [Repo: frontend/src/components/TextToSpeechInput.tsx:49-53] and "Maximum character limit reached" at the cap. [Repo: frontend/src/components/TextToSpeechInput.tsx:66-70]
- Each provider is listed with "Max 5000 chars/request" [Repo: frontend/src/components/ProviderSelector.tsx:89], a value hard-coded when the provider list is built. [Repo: frontend/src/services/ttsApi.ts:199]
- The Google provider sends the whole text in one request. [Repo: voice_narration/inference/providers/google_tts.py:109-132]
- The Generate button is disabled while a generation is being submitted. [Repo: frontend/src/components/GenerationSubmitForm.tsx:133]
- Generated audio is persisted, with an expiry of `AUDIO_RETENTION_DAYS`, default 30 days. [Repo: voice_narration/inference/application.py:174] Generations can be listed, downloaded and deleted. [Repo: frontend/src/services/ttsApi.ts:102-150]
- Existing tests assert that `mock`, `google` and `azure` are registered [Repo: tests/test_provider_registry.py:15-19], and cover the voice selector. [Repo: frontend/tests/tts.spec.tsx:155-211] Existing tests check the 5000-character cap, counter and warning [Repo: frontend/tests/tts.spec.tsx:83, :113-120, :130, :133-144], and the test mock rejects text over 5000 characters. [Repo: frontend/tests/mocks/tts-handlers.ts:27]
- `.env` and `service-account-key.json` are gitignored. [Repo: .gitignore:5, :8]

## Requirements

- **COA-1 Provider per generation.** On the TTS page the user chooses the provider for each generation, Google narration or Chatterbox cloning. The chosen provider is the one used for that generation. [User: Q5; Derived from Q5 and the provider-not-sent fact — confirmed Q30]
- **COA-2 Sample kept.** The voice service keeps the audio of each recorded or uploaded voice sample. [Derived from Q1 and the sample-discarded fact — confirmed Q29]
- **COA-3 Voices selectable for cloning.** When Chatterbox is chosen, the user's recorded and uploaded voices are listed and selectable on `/tts`. [Derived from Q1 and Q5 — confirmed Q37]
- **COA-4 Cloned speech.** A Chatterbox generation produces speech in the selected voice, for the entered text and chosen language, through the deployed Chatterbox service, and the user can play it on the TTS page. [User: Q1]
- **COA-5 Language.** For a Chatterbox generation, the user chooses English or Hindi on the TTS page. [User: Q4, Q20]
- **COA-6 Sample formats.** Voices recorded in Chrome and voices uploaded as WAV must clone. MP3 and OGG uploads stay accepted but are not required to clone. [User: Q6, Q21] Chrome recordings must reach the unchanged deployed Chatterbox in a format it can read; how is left to the Plan. [Derived from Q6 and Q8 — confirmed Q37]
- **COA-7 Failure messages.** When cloning fails, the user sees one message per cause. The causes are: not configured, invalid time-limit setting, voice sample unreadable, identity token unavailable, timed out, cannot connect, access denied, service error, and a response that is not audio. Each message ends with "Please retry, or choose another provider." [User: Q10, Q23]
- **COA-8 No fallback.** When Chatterbox is unavailable, the app shows the error and does not fall back to Google. [User: Q18]
- **COA-9 Time limit.** A Chatterbox call is bounded by a configurable time limit, default 1200 seconds. Reaching it produces the timed-out message. [User: Q17, Q26]
- **COA-10 History.** Cloned generations appear in generation history and can be downloaded and deleted like Google generations. [User: Q11] They keep the existing 30-day retention. [Derived from recommended option — confirmed Q36]
- **COA-11 Voice durability and retention.** Voices and their samples survive a restart of the local services. Each voice and its sample are deleted 5 days after upload and cannot be recovered. [Derived from recommended option — confirmed Q36]
- **COA-12 Automatic approval kept.** A new voice is approved automatically, as today, and can be cloned straight away. [User: Q19]
- **COA-13 Waiting and duplicates.** A generation request that arrives while another is generating waits. [User: Q25] The Generate button stays disabled during a generation, and no other duplicate prevention is added. [User: Q38]
- **COA-14 Preserved behavior.** The mock, Google and Azure providers and the tests that check them stay unchanged. Google narration with Google voices keeps working as now, except that its text is no longer capped (COA-17). [User: Q12, Q33; Derived from Q41 — confirmed Q45]
- **COA-15 Shared voice list.** All logged-in users share one voice list, and any of them may clone any voice in it. [Derived from recommended option — confirmed Q35]
- **COA-16 Testing.** Automated tests use a fake Chatterbox with no network. The final check is the user's manual test against the deployed Cloud Run service. [User: Q13, Q24]
- **COA-17 No text length limit.** The TTS page accepts text of any length for every provider; the 5000-character cap is removed. [User: Q17, Q41] The text is sent as entered, without splitting; if Google rejects long text, the user sees the error the app shows for a failed Google generation. [User: Q42] The "Max 5000 chars/request" label is removed. [User: Q43] The text box shows a plain count, "n characters", and the 90% warning and the maximum-reached message are removed. [User: Q44] The frontend tests and test mock that check the cap change to match. [Derived from Q41 — confirmed Q45]

### Constraints

- **CON-1** Only Chatterbox runs on GCP; everything else runs locally. [User: brief]
- **CON-2** No local Docker build or container, and no `gcloud` command, during planning or execution. The user deploys manually on Cloud Run and tests there. [User: brief]
- **CON-3** The deployed Chatterbox service is used unchanged. [User: Q8]
- **CON-4** Chatterbox stays a separate service. [User: Q9, Q34]
- **CON-5** The deployed service is at `https://chatterbox-model-api-177206684903.asia-southeast1.run.app` (project `project-84eb579f-1f7b-4f87-838`, region `asia-southeast1`, NVIDIA L4). Only `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` may call it, with a Google identity token whose audience is exactly that URL. `POST /v1/synthesize` takes `multipart/form-data` with `text`, `language` and the file part `sample_audio`, and returns WAV (24 kHz float). Cold starts take about 80–100 s. [User: brief]
- **CON-6** Voice samples and key files are private. `service-account-key.json` and `.env` must never be committed. [User: brief]

## Scenarios

- **S-1 Record and clone.** The user records a voice in Chrome on `/voices`, opens `/tts`, chooses Chatterbox, selects that voice, chooses English or Hindi, enters text and generates. They hear the text in the recorded voice. [User: Q1, Q4, Q5, Q6, Q20] → AC-1, AC-2, AC-3, AC-4, AC-5
- **S-2 Upload and clone.** As S-1, but the voice is uploaded as a WAV file. [User: Q1, Q21] → AC-2, AC-3, AC-4, AC-5
- **S-3 Google narration.** The user chooses Google on `/tts` with a Google voice and generates, with the same result as today apart from the removed text cap. [User: Q5, Q12, Q33; Derived from Q41 — confirmed Q45] → AC-1, AC-11
- **S-4 Chatterbox fails.** Chatterbox is unreachable, denies access, errors, returns something other than audio, or exceeds the time limit. The user sees the message for that cause, and no Google audio is produced. [User: Q10, Q18, Q23, Q26] → AC-6, AC-7, AC-8
- **S-5 History.** After a cloned generation, the user finds it in history, downloads it and deletes it. [User: Q11] → AC-9
- **S-6 Restart and expiry.** After the local services restart, the user's voices are still listed and still clone. A voice uploaded more than 5 days ago is gone. [Derived from recommended option — confirmed Q36] → AC-10
- **S-7 Second request.** A second generation is requested while one is generating. It waits and then completes. [User: Q25] → AC-12
- **S-8 Long text.** The user enters text longer than 5000 characters on `/tts`. All of it stays in the text box, the count shows its length, and all of it is sent with the generation. [User: Q41, Q44] → AC-13

## Operational Characteristics

| Characteristic | Answer | Source |
|----------------|--------|--------|
| Scale | Not required for this work item | [User: Q39] |
| Deployment | Each local service runs as one instance; Chatterbox runs on Cloud Run | [User: Q15, brief] |
| Availability and latency | Availability: not required for this work item. Latency: a Chatterbox call may take up to the configurable limit, default 1200 s; cold starts take about 80–100 s | [User: Q40, Q26, brief] |
| Consistency and concurrency | A request that arrives while another is generating waits. The Generate button stays disabled during a generation; no other duplicate prevention | [User: Q25, Q38] |
| Dependency failure | When Chatterbox is unavailable, show the error for that cause; no fallback to Google. Automated tests run without Chatterbox, using a fake | [User: Q18, Q24] |
| Observability | Not required for this work item | [User: Q28] |
| Data durability and retention | Voices and samples survive a restart; each voice and its sample are deleted 5 days after upload, unrecoverable. Generated clips keep the existing 30-day retention | [Derived from recommended option — confirmed Q36] |

## Decisions Deferred to Later Milestones

- How a Chrome recording reaches Chatterbox in a format it can read (COA-6) is decided by the Plan. [Derived from Q6 and Q8 — confirmed Q37]

## Explicit Exclusions

- Copying the Chatterbox service source (`voice_narration/chatterbox_api/`, `cloudrun/chatterbox-service/`, the `setuptools==80.10.2` pin) into this branch. Putting the service on `main` is a separate PR outside this work item. [User: Q34]
- Changing or redeploying the deployed Chatterbox service. [User: Q8]
- Per-user voice separation. [Derived from recommended option — confirmed Q35]
- A consent step or manual approval before cloning. [User: Q19]
- Falling back to Google when Chatterbox fails. [User: Q18]

## Non-Blocking Decisions

None.

## Acceptance Criteria

- **AC-1** On `/tts` the user can choose Google or Chatterbox for a generation, and the generation uses the chosen provider. → COA-1
- **AC-2** A voice recorded in Chrome or uploaded as WAV has its sample audio stored by the voice service. → COA-2, COA-6
- **AC-3** With Chatterbox chosen, the user's recorded and uploaded voices are listed and selectable on `/tts`. → COA-3, COA-15
- **AC-4** A Chatterbox generation for a recorded (Chrome) or WAV-uploaded voice returns speech that plays on the TTS page; the user hears the selected voice in the manual check against Cloud Run. → COA-4, COA-6, COA-12, COA-16
- **AC-5** For a Chatterbox generation the user can choose English or Hindi, and the chosen language is used. → COA-5
- **AC-6** Each of the nine failure causes in COA-7 produces its own message ending "Please retry, or choose another provider.", shown by automated tests against a fake Chatterbox. → COA-7, COA-16
- **AC-7** When Chatterbox fails, no Google audio is produced for that generation. → COA-8
- **AC-8** The time limit is configurable with a default of 1200 s; a call exceeding it produces the timed-out message. → COA-9
- **AC-9** A cloned generation appears in history, can be downloaded and deleted, and has a 30-day retention. → COA-10
- **AC-10** Voices and their samples are still present after the local services restart; a voice and its sample are deleted 5 days after upload. → COA-11
- **AC-11** The mock, Google and Azure providers and their existing tests pass unchanged, and Google narration with a Google voice behaves as before apart from the removed text cap. → COA-14
- **AC-12** A request made while another generation is running waits and then completes; the Generate button is disabled during a generation. → COA-13
- **AC-13** For every provider, text longer than 5000 characters is kept whole in the text box and sent whole, unsplit, with the generation; the count reads "n characters"; no "/ 5000", 90% warning, maximum-reached message or "Max 5000 chars/request" label is shown. → COA-17

## Clarification Log

| Q | Question | Answer |
|---|----------|--------|
| Q1 | Is it done when a voice recorded or uploaded on `/voices`, picked on `/tts`, produces speech in that voice through the deployed Chatterbox? Any other check? | yes |
| Q2 | Must each user see only their own voices, or does the shared list stay? (recommended: shared list) | ok — confirmed in Q35 |
| Q3 | Must something happen before cloning (consent, real approval), or does automatic approval stay? | yes — clarified in Q19 |
| Q4 | English, Hindi or both? How is it chosen? | both — clarified in Q20 |
| Q5 | Google and Chatterbox both in one running app, chosen per generation, or one provider at startup? | user choice |
| Q6 | Which browsers must produce recordings that clone? | Chrome |
| Q7 | Must MP3, OGG and WAV uploads all clone? | keep it simple now — clarified in Q21 |
| Q8 | May the deployed Chatterbox be changed and redeployed? | use the deployed one |
| Q9 | Should the Chatterbox service source move into this app? | Chatterbox should be a separate service — clarified in Q22/Q34 |
| Q10 | One message per failure cause? What wording? | use recommended — proposal given and accepted in Q23 |
| Q11 | Cloned generations in history, downloadable, deletable? | yes |
| Q12 | Mock, Google, Azure and their tests unchanged? | yes |
| Q13 | Automated tests with a fake Chatterbox, manual test on Cloud Run? | I will test manually — clarified in Q24 |
| Q14 | Anything else out of scope? | no |
| Q15 | One instance per local service? | yes |
| Q16 | One request at a time acceptable? Prevent double-click duplicates? | keep it simple — clarified in Q25/Q38 |
| Q17 | How long to wait before failure? Text length limit? | no limit — wait clarified in Q26 |
| Q18 | Samples survive restart, how long kept? Chatterbox down: error or fall back to Google? Logs or metrics? | 5 days; show error — clarified in Q27/Q28 |
| Q19 | (Q3) Keep automatic approval (a), or add a step (b)? | (a) |
| Q20 | (Q4) Language chosen on the TTS page (a), or per voice (b)? | (a) |
| Q21 | (Q7) Only Chrome recordings and WAV uploads must clone; MP3/OGG accepted but not required to clone? | yes |
| Q22 | (Q9) Source stays on `feature/voice-cloning`, this work item only calls the deployed service? | keep it a separate service, but also put it on `main` — any issues? (answered in Q34) |
| Q23 | (Q10) One message per cause for nine causes, ending "Please retry, or choose another provider."? | yes |
| Q24 | (Q13) Automated tests with a fake Chatterbox, then manual test on Cloud Run? | yes |
| Q25 | (Q16) A request arriving during a generation waits; nothing stops a double-click making two clips? | another should wait |
| Q26 | (Q17) Configurable limit, default 600 s (a), or no limit (b)? | configurable, 1200 s |
| Q27 | (Q18) Voices and samples survive restart, deleted 5 days after upload; clips keep 30-day retention? | recommended — confirmed in Q36 |
| Q28 | (Q18) Logs and metrics not required? | not required |
| Q29 | Confirm: the voice service must keep the sample audio. | yes |
| Q30 | Confirm: the provider picked on the TTS page is the one used. | yes |
| Q31 | Confirm: with Chatterbox chosen, recorded and uploaded voices are listed and selectable on `/tts`. | use recommended — confirmed in Q37 |
| Q32 | Confirm: Chrome recordings must reach the unchanged Chatterbox in a readable format; how left to the Plan. | recommended — confirmed in Q37 |
| Q33 | Confirm: Google narration with Google voices keeps working exactly as now. | yes |
| Q34 | Putting the service on `main`: (a) separate PR outside this work item, or (b) copy into this branch? | (a) |
| Q35 | Confirm: all logged-in users share one voice list and any may clone any voice. | yes |
| Q36 | Confirm: voices and samples survive restart; deleted 5 days after upload, unrecoverable; clips keep 30-day retention. | yes |
| Q37 | Confirm Q31 and Q32 as stated. | yes |
| Q38 | Confirm: keep the Generate button disabled during a generation; no other duplicate prevention. | yes |
| Q39 | Scale: expected users and generations, or not required? | not required |
| Q40 | Availability: uptime or downtime expectation, or not required? | not required |
| Q41 | The TTS page caps text at 5000 characters for every provider, against the no-length-limit rule. (a) no cap for Chatterbox only, (b) remove the cap for every provider, (c) keep the cap? | no cap for any service (b) |
| Q42 | Long text for Google: (a) send unchanged, Google's rejection shown as an error, Google provider unchanged, or (b) split and join the audio? | use recommended (a) |
| Q43 | The "Max 5000 chars/request" label: (a) remove, or (b) keep? | use recommended (a) |
| Q44 | The text-box counter: (a) plain "n characters", warnings removed, or (b) no counter? | use recommended (a) |
| Q45 | Confirm: the cap tests and test mock change to match; COA-14 reads "as before, except that text is no longer capped". | use recommended (yes) |

## Provenance Check

- Every item above carries a source label: checked Goal, Business Context, Repository-Confirmed Facts, COA-1–COA-17, CON-1–CON-6, S-1–S-8, the Operational Characteristics table, Deferred, Exclusions and AC-1–AC-13.
- `Derived` items, each with its confirming `Qn`: COA-1 (Q30), COA-2 (Q29), COA-3 (Q37), COA-6 format path (Q37), COA-10 retention (Q36), COA-11 (Q36), COA-14 cap exception (Q45), S-3 cap exception (Q45), COA-15 (Q35), COA-17 test changes (Q45), Business Context actors (Q35) and retention rule (Q36), S-6 (Q36), durability row (Q36), the deferred decision (Q37), the per-user exclusion (Q35).
- `Left to` items: none.
- `Repo` citations verified at HEAD `664cee4`: App.tsx:279-304; api-config.ts:9-10; VoiceRecorder.tsx:52, :67, :160; VoiceUpload.tsx:104-105; start-voice-service.bat:25; simple_voices/application.py:10, :102, :111, :113-114, :186-187; inference/__main__.py:33-58; registry.py:68-77; providers/base.py:16-21; inference/application.py:174, :343-373, :463; ttsApi.ts:7-19, :42-51, :102-150, :183-200; VoiceSelector.tsx:21-33; GenerationSubmitForm.tsx:133; tests/test_provider_registry.py:15-19; frontend/tests/tts.spec.tsx:155-211; .gitignore:5, :8; the absence of docs/requirements.md (verified in the 2026-11-12 capture at the same HEAD). Verified during this revision on 2026-11-13: TextToSpeechInput.tsx:4, :15, :34, :46, :49-53, :66-70; ProviderSelector.tsx:89; ttsApi.ts:199; google_tts.py:109-132; frontend/tests/tts.spec.tsx:83, :113-120, :130, :133-144; frontend/tests/mocks/tts-handlers.ts:27.
- Requirements without an acceptance criterion: none (COA-1 AC-1; COA-2 AC-2; COA-3 AC-3; COA-4 AC-4; COA-5 AC-5; COA-6 AC-2, AC-4; COA-7 AC-6; COA-8 AC-7; COA-9 AC-8; COA-10 AC-9; COA-11 AC-10; COA-12 AC-4; COA-13 AC-12; COA-14 AC-11; COA-15 AC-3; COA-16 AC-4, AC-6; COA-17 AC-13). Constraints CON-1–CON-6 bound the work and have no criterion of their own.
- Scenarios without an acceptance criterion: none.
- Statements that contradict each other: none found. The no-length-limit rule, COA-17, S-8 and AC-13 agree. COA-14 and AC-11 state the cap removal as their one exception; the cap tests that change are frontend tests named in COA-17, so the provider tests in AC-11 still pass unchanged. COA-12 and the auto-approval fact agree. COA-1 (provider sent) does not change Google narration with Google voices.
- Answers taken from a recommended option, each with its confirming `Qn`: shared voice list (Q2 → Q35); retention (Q27 → Q36); voices selectable and format path (Q31, Q32 → Q37); Q42–Q45 ("use recommended", answering the stated options). Q19 (a), Q20 (a), Q21, Q23, Q24, Q34 (a) and Q41 (b) were chosen explicitly by the user.
- Nothing is copied from another work item's artifacts.
