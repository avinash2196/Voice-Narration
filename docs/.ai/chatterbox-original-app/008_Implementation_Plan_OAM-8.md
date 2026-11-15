# Implementation Plan — OAM-8 Cloud Run manual validation

## Milestone

OAM-8 — Cloud Run manual validation (`Plan.md:257-278`).

## Milestone Type

OTHER (validation protocol), as `Plan.md:261` records. No requirement it owns changes behavior: it owns COA-16's manual part and the deployment characteristic, which check the behavior OAM-5 and OAM-7 delivered (`Plan.md:272`, `:276`).

- Baseline evidence: the OAM-7 backend suite (`1 failed, 100 passed, 17 skipped`, the one accepted failure) and full frontend suite (`90 failed | 282 passed (372)`, exactly the accepted 90) (`Plan.md:555-559`), plus the user's confirmation in case M8-1 that the deployed service is unchanged.
- Preserved tests: the OAV-2 backend suite and the full frontend suite as recorded at OAM-7. OAM-8 changes no file they cover (M8C-5), so they are not rerun (`prompt-driven-development` Test Scope and Output: the full suite runs only when production or build files change).

## Review Summary

- Behavior change: none. The user runs a manual protocol against the deployed Chatterbox and records the results in `Plan.md`.
- Requirements covered: COA-16's manual part, which checks COA-4, COA-5, COA-6, COA-7 and COA-8 (call-time), COA-9, COA-10, COA-12, COA-17 (inference part) and CON-5; AC-1, AC-4–AC-9 and AC-13; and the deployment characteristic.
- Files: modified `docs/.ai/chatterbox-original-app/Plan.md` (Execution Status row, and an evidence section with the result table); created none; deleted none.
- Tests added: none. There are 12 manual cases (M8-1 to M8-12) with met / not met rules, and a not verified result for the five call-time causes.
- Verification: the pre-check commands, then the user's table, then the final checks. Expected / Predicted — Not Yet Verified: M8-1 to M8-7 met; M8-8 to M8-12 each met or not verified; only `docs/.ai/` changed.
- Needs attention: M8Q-1, answered (a) (a baseline finding: the default database account cannot write the `generations` table, so a clone's 30-day expiry is not recorded). Decisions M8D-1 (a browser session without an auth service) and M8D-6 (how each failure cause is reproduced, partly a hypothesis). Risk M8R-1 (long text and the deployed service).

## Question Before Approval

Added because a baseline finding must be answered before approval (`implementation-planning` Pre-existing Failures).

- **M8Q-1 How is the 30-day retention of a cloned generation observed (case M8-7)? Answered by Avinash Srivastava on 2026-11-14: "Approve with (a)", option (a).** The expiry is recorded only in the database row that `persist_generation` writes, inside a block that ignores database errors (`voice_narration/inference/application.py:170-198`, `:193`; contract `API-Contract.md:298`). The inference service's default database URL connects as `voice_narration` to `localhost:5432` (`voice_narration/inference/db.py:19-28`). Planning observed, read-only, on 2026-11-14: a PostgreSQL server is listening on 5432 and the connection succeeds. The `generations`, `voices` and `generation_audit` tables exist, owned by `postgres`, and `voice_narration` has no SELECT, INSERT or DELETE privilege on `generations` or `voices` (`has_table_privilege` printed `[False, False, False]` for both). A count query failed with `InsufficientPrivilege: permission denied for table generations`. So with the default settings no expiry is written, and M8-7 cannot be met (Plan OAR-2 then means not met, reported for replanning).
  - (a) **Proposed:** you type a `DATABASE_URL` for an account that can write those tables (for example the owner `postgres`) into the inference terminal and the check terminal with `Read-Host`. It is held only in those terminals, never in a file (M8P-4, M8P-6). No database change is needed.
  - (b) You grant `voice_narration` SELECT, INSERT and DELETE on `generations` and `voices` in your local PostgreSQL. M8P-4 and M8P-6 then set no `DATABASE_URL`. This changes your local database, outside the repository.
  - (c) Keep the defaults. The retention part of M8-7 is then recorded as not met and goes back to planning.
  - The protocol below is written for (a). If you answer (b) or (c), this plan is revised before approval.

## Authoritative References

| Document | Status |
| --- | --- |
| `docs/.ai/chatterbox-original-app/requirements.md` | Approved by Avinash Srivastava on 2026-11-13 |
| `docs/.ai/chatterbox-original-app/Plan.md` | Approved by Avinash Srivastava on 2026-11-13 (`Plan.md:5`) |
| `docs/.ai/chatterbox-original-app/API-Contract.md` | Approved by Avinash Srivastava on 2026-11-13 (`API-Contract.md:527`); OAM-1 Complete (`Plan.md:355`) |
| `001_Implementation_Plan_OAM-2.md`, `002_…OAM-3.md`, `004_…OAM-4.md`, `005_…OAM-5.md`, `006_…OAM-6.md`, `007_…OAM-7.md` | Approved and executed (each Human Review status) |
| `003_Implementation_Plan_OAM-4.md` | Superseded, not executed; nothing carried forward |
| Reference contract on `feature/voice-cloning` at `abbe387`, `docs/.ai/chatterbox-cloud-run/API-Contract.md` | Approved 2026-11-09, cited through `API-Contract.md:14`; not read again, because CON-5 and the contract's Chatterbox Call section give everything this protocol uses |
| Product-level `docs/requirements.md` | Does not exist (`ls docs` on 2026-11-14) |
| Cloud Run service-to-service authentication, `https://docs.cloud.google.com/run/docs/authenticating/service-to-service` | External docs, read 2026-11-14 for M8D-6; they do not say whether an audience with a path is accepted |

## Carried-Forward Decisions

- **N4D-3** (`004`, applied in `005`): settings are read when the app is created (`voice_narration/inference/application.py:100`). So each setting change in M8-8 to M8-11 needs the inference service restarted.
- **N5D-2** (`005:123`): the identity token comes only from the service-account key file, with no metadata-server fallback (`voice_narration/inference/chatterbox.py:76-95`).
- **N5D-8** (`005:158`): a failure answer carries only the contract text, so the page shows exactly the OAF message.
- **N5R-3** (`005:611`): google-auth limits the token request to 120 s; a token request that runs longer is OAF-4.
- **T6D-4 / T7D-4** (`006:121`, `007:135`): with Chatterbox chosen, the voice list shows only recorded and uploaded voices, in list order, with the first one preselected.
- **T6D-5 / T7D-1** (`006:122`, `007:132`): the language select (English, Hindi) appears only for Chatterbox, with English preselected.
- **T6D-7** (`006:124`): the count reads "`n` characters", and there is no cap.
- **OAS-1 / OAV-3** (`Plan.md:83`, `:344`, `:600`): tracked `audio_storage/` stays unchanged. M8D-4 keeps generated audio out of it.

## Preconditions / Predecessor Evidence

- OAM-7 is Complete, GREEN verified 2026-11-14 (`Plan.md:361`, `:544-568`). OAM-8 is `Pending` (`Plan.md:362`). No earlier OAM-8 Implementation Plan exists (folder listing: `001`–`007` only).
- Repository on 2026-11-14: HEAD `60a9192`, branch `claude/chatterbox-original-app-client-a3ef0e`, `git status --short` printed nothing. Current `Plan.md` SHA-256 (CRLF working copy): `e401dd722d441a186b2b8f1b01afbd5e0c400b563e72c991ba5b8aa7c5c4c7d4`.
- The OAM-5 code that OAM-8 checks is in the tree: `voice_narration/inference/chatterbox.py` and the `submit_for_cloning` path (`application.py:317-320`).

## Current Repository State

- Chatterbox settings and the order of causes: `chatterbox.py:67-73` reads `CHATTERBOX_URL`, `CHATTERBOX_TIMEOUT_SECONDS`, `VOICE_SERVICE_URL` and `GOOGLE_APPLICATION_CREDENTIALS`. Then `:131-137` checks the URL, then the time limit, fetches the sample, gets the token and calls. `:170-182` sends the call bounded by the time limit, with timeout as OAF-5 and transport errors as OAF-6. `:186-193` maps 401/403 to OAF-7, any other non-200 to OAF-8, and a non-`audio/wav` answer to OAF-9.
- The key file must be a service-account key: `chatterbox.py:84-88`.
- Startup provider: `INFERENCE_PROVIDER`, default `mock`, printed at start (`voice_narration/inference/__main__.py:35-37`).
- Audio storage: `AUDIO_STORAGE_PATH`, default the tracked `audio_storage/` (`application.py:106-108`).
- The inference service also loads `.env`, `.env.local` and `.env.production` from the repository root (`db.py:14-16`). Only `/.env` is gitignored (`.gitignore:5`). `git check-ignore` printed `NOT-IGNORED` for `.env.local` and `.env.production`.
- Voice storage: `voice_storage/` at the repository root (`voice_narration/simple_voices/application.py:15`), gitignored (`.gitignore:11`). The upload form sends only the file (`frontend/src/components/VoiceUpload.tsx:265`), so the voice is named `Unnamed Voice` (`simple_voices/application.py:107`, `:128`). The recorder sends a name (`VoiceRecorder.tsx:160-161`). After an upload the page polls the evaluation service at `:9000` (`VoiceUpload.tsx:286`, `voiceApi.ts:83`, `api-config.ts:11`).
- Login: the login page posts `/auth/login` to `http://localhost:9000` (`authClient.ts:27-30`, `api-config.ts:8`). No repository service answers that path; `voice_narration/auth/application.py:39` serves `/api/v1/auth/login`. The session is restored from `localStorage` whenever `auth_token` and `refresh_token` exist (`AuthContext.tsx:111-138`, `constants.ts:43-44`).
- Launchers: `start-inference-service.bat:11-12` sets `INFERENCE_PROVIDER=google` and `GOOGLE_APPLICATION_CREDENTIALS=.\service-account-key.json`, and `:22` runs `cd voice_narration`; `start-voice-service.bat:18` does the same `cd`.
- The TTS page history fetches on mount, plays with `play-button-…` and deletes with `delete-button-…` through `DELETE /inference/generations/{job_id}` (`GenerationHistory.tsx:24-42`, `:63-67`, `:188`, `ttsApi.ts:123`). It has no download button. Download is `GET /inference/jobs/{job_id}/download` (`API-Contract.md:366-382`).
- Frontend dev server port 5173 (`frontend/vite.config.ts:18`). `frontend/node_modules` is present in this worktree.

## Files in Scope

### Files to Create

None.

### Files to Modify

- `docs/.ai/chatterbox-original-app/Plan.md`

### Files to Delete

None.

## Proposed Changes

1. `Plan.md` Execution Status, the OAM-8 row: `Pending` becomes `Waiting — manual check from user`, pointing to this plan and to the evidence section (`Plan.md:278` success criteria).
2. `Plan.md`, a new section `### OAM-8 manual validation evidence` after the OAM-7 GREEN evidence and before `## Risks`. It holds the result table the user fills in (cases M8-1 to M8-12). The executor's pre-check and final-check evidence is appended below the table during execution.
3. No other repository change. The Validation Protocol below is the exact set of steps the user runs. It writes only outside the repository (`$HOME\oam8-private`) and into the gitignored `voice_storage/`.

## Proposed Code / Tests

### Plan.md diff

Generated against the current `Plan.md` and applied in a dry run (`git apply --check` passed). Resulting SHA-256 (CRLF working copy): `bf4dc09f81de33e467ba49330396777a1b95715a19ba4c770ebb8987b9ddedf9`.

```diff
diff --git a/docs/.ai/chatterbox-original-app/Plan.md b/docs/.ai/chatterbox-original-app/Plan.md
index 9c6f75e..f46527f 100644
--- a/docs/.ai/chatterbox-original-app/Plan.md
+++ b/docs/.ai/chatterbox-original-app/Plan.md
@@ -359,7 +359,7 @@ No verification command uses Docker or `gcloud` (CON-2), and no automated test f
 | OAM-5 Inference service GREEN | Complete — GREEN verified 2026-11-13 | `005_Implementation_Plan_OAM-5.md`; see OAM-5 GREEN evidence below (the behavior that needs a Chatterbox call is not claimed; its evidence comes from OAM-8) |
 | OAM-6 TTS page RED | Complete — valid RED established 2026-11-14 | `006_Implementation_Plan_OAM-6.md` revision 2; see OAM-6 RED evidence (revision 2) below (the earlier stopped run is kept below) |
 | OAM-7 TTS page GREEN | Complete — GREEN verified 2026-11-14 | `007_Implementation_Plan_OAM-7.md`; see OAM-7 GREEN evidence below |
-| OAM-8 Cloud Run manual validation (OTHER) | Pending | — |
+| OAM-8 Cloud Run manual validation (OTHER) | Waiting — manual check from user | `008_Implementation_Plan_OAM-8.md`; see OAM-8 manual validation evidence below |
 
 ### OAM-2 RED evidence
 
@@ -567,6 +567,25 @@ Executed 2026-11-14 at HEAD `cb394ab`, which differs from the plan's `a909fd2` o
 - Deviations: none in the planned commands, which ran as written, one at a time, in order. Commands 4a and 5b ran in the background. Each next command started only after the previous one had exited and its output had been read. Two read-only checks were added: `git diff --stat a909fd2 HEAD`, because HEAD is `cb394ab`, and a `grep` of the backend log for the accepted failure's `ImportError` line, because the raw `FAILED` line carries no reason suffix.
 - Processes: both background jobs exited. No process started by this run is still running.
 
+### OAM-8 manual validation evidence
+
+Protocol: `008_Implementation_Plan_OAM-8.md`, Validation Protocol. The user runs it by hand and fills in the last three columns. A Result is `met` or `not met`; for M8-8 to M8-12 it may also be `not verified`. Message text is written exactly as the page shows it. Nothing in this table holds a key, a password, a token, a database URL or a voice sample.
+
+| Case | Checked | Setting change from the start settings (M8P-4) | Voice on `/tts` | Language | What the user saw or heard | History total before → after | Result |
+| --- | --- | --- | --- | --- | --- | --- | --- |
+| M8-1 | One instance of each local service; the deployed service is the unchanged one at the CON-5 URL and was not redeployed for this check | none | — | — | | — | |
+| M8-2 | S-1: Chrome recording, English | none | OAM8 Chrome | English | | | |
+| M8-3 | S-1: Chrome recording, Hindi | none | OAM8 Chrome | Hindi | | | |
+| M8-4 | S-2: WAV upload, English | none | Unnamed Voice (newest) | English | | | |
+| M8-5 | S-2: WAV upload, Hindi | none | Unnamed Voice (newest) | Hindi | | | |
+| M8-6 | Text over 5000 characters, spoken whole | none | OAM8 Chrome | English | | | |
+| M8-7 | Cloned generation in history, downloaded, 30-day retention, deleted | none | OAM8 Chrome | English | | | |
+| M8-8 | OAF-5 timed out | `CHATTERBOX_TIMEOUT_SECONDS` = `3` | OAM8 Chrome | English | | | |
+| M8-9 | OAF-6 cannot connect | `CHATTERBOX_URL` = `https://127.0.0.1:1` | OAM8 Chrome | English | | | |
+| M8-10 | OAF-7 access denied | `GOOGLE_APPLICATION_CREDENTIALS` = `$HOME\oam8-private\other-account-key.json` | OAM8 Chrome | English | | | |
+| M8-11 | OAF-8 service error | `CHATTERBOX_URL` = the CON-5 URL followed by `/oam8-no-such-path` | OAM8 Chrome | English | | | |
+| M8-12 | OAF-9 not audio | none (M8D-6) | — | — | | — | |
+
 ## Risks
 
 - **OAR-1 Tests write to tracked `audio_storage/`.** `tests/test_generation_history_download.py:18` builds an app over the default storage root (`voice_narration/inference/application.py:87-89`). The planning run modified `audio_storage/generation_index.json` and added a folder. Mitigation: OAV-3 after every backend run; new tests in OAM-2 and OAM-4 keep their own storage out of `audio_storage/`.
```

### Validation Protocol

You do every step by hand on this machine, in Windows PowerShell, from this worktree: `C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.claude\worktrees\chatterbox-original-app-client-a3ef0e` (called "the repo" below). No Docker, no `gcloud`, and no change to the deployed service (CON-2, CON-3).

**Inputs (all supplied by you, all kept outside the repository, never committed — CON-6):**

| ID | Input | Where it goes |
| --- | --- | --- |
| M8I-1 | Service-account key of `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com` | `$HOME\oam8-private\test-850-key.json` |
| M8I-2 | A WAV recording of a voice, 5–20 s | `$HOME\oam8-private\sample.wav` |
| M8I-3 | A voice recorded in Chrome on `/voices` | Recorded in M8P-8; stored by the voice service in the gitignored `voice_storage/` |
| M8I-4 | `DATABASE_URL` for an account that can write `generations` (M8Q-1 (a)) | Typed at the `Read-Host` prompts in M8P-4 and M8P-6; held only in those terminals |
| M8I-5 | Optional: a service-account key of any account other than test-850 | `$HOME\oam8-private\other-account-key.json`; without it M8-10 is not verified |

**M8P-1 Private folder (once).** Any PowerShell window:

```powershell
New-Item -ItemType Directory -Force "$HOME\oam8-private" | Out-Null
(Get-Content "$HOME\oam8-private\test-850-key.json" -Raw | ConvertFrom-Json).client_email
```

Put M8I-1 and M8I-2 in that folder first. Expected: `test-850@project-84eb579f-1f7b-4f87-838.iam.gserviceaccount.com`.

**M8P-2 Pre-checks. Terminal D** (this terminal stays open for checks):

```powershell
Set-Location "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.claude\worktrees\chatterbox-original-app-client-a3ef0e"
git diff --stat 60a9192 HEAD -- . ":(exclude)docs/.ai"
git status --short
Test-Path .env, .env.local, .env.production
Get-NetTCPConnection -LocalPort 8002,8003,5173 -State Listen -ErrorAction SilentlyContinue
```

Expected: the `git diff` prints nothing (the code is the OAM-7 code). `git status` lists only `docs/.ai/` paths, or nothing. `Test-Path` prints `False` three times. The port check prints nothing. If a `.env*` file exists, move it to `$HOME\oam8-private` for the session and move it back at the end. Do not rename it inside the repo, because `.env.local` and `.env.production` are not gitignored.

**M8P-3 Voice service. Terminal A:**

```powershell
Set-Location "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.claude\worktrees\chatterbox-original-app-client-a3ef0e"
python -m voice_narration.simple_voices
```

Expected: `Uvicorn running on http://0.0.0.0:8002`.

**M8P-4 Inference service, start settings. Terminal B:**

```powershell
Set-Location "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.claude\worktrees\chatterbox-original-app-client-a3ef0e"
$env:CHATTERBOX_URL = "https://chatterbox-model-api-177206684903.asia-southeast1.run.app"
$env:GOOGLE_APPLICATION_CREDENTIALS = "$HOME\oam8-private\test-850-key.json"
$env:CHATTERBOX_TIMEOUT_SECONDS = "1200"
$env:VOICE_SERVICE_URL = "http://localhost:8002"
$env:INFERENCE_PROVIDER = "mock"
$env:AUDIO_STORAGE_PATH = "$HOME\oam8-private\audio_storage"
$env:DATABASE_URL = Read-Host "DATABASE_URL"
python -m voice_narration.inference
```

Expected: `[Inference] Using provider: mock`, then `Uvicorn running on http://0.0.0.0:8003`. **To change a setting** (M8-8 to M8-11): press Ctrl+C, set the one variable the case names, and run `python -m voice_narration.inference` again. The other variables stay set in that terminal. Settings are read only at start (N4D-3).

**M8P-5 Frontend. Terminal C:**

```powershell
Set-Location "C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.claude\worktrees\chatterbox-original-app-client-a3ef0e\frontend"
npm run dev
```

Expected: `Local:   http://localhost:5173/`.

**M8P-6 Running checks. Terminal D:**

```powershell
Get-NetTCPConnection -LocalPort 8002,8003,5173 -State Listen | Select-Object LocalAddress, LocalPort, OwningProcess
Invoke-RestMethod http://localhost:8002/health | ConvertTo-Json -Compress
(Invoke-RestMethod http://localhost:8003/inference/backends).backends.name -join ' '
$env:DATABASE_URL = Read-Host "DATABASE_URL"
function Get-HistoryTotal { (Invoke-RestMethod "http://localhost:8003/inference/generations?limit=1").total }
Get-HistoryTotal
```

Expected: one `OwningProcess` per port; `{"status":"ok","service":"voice-management"}`; `azure chatterbox google mock`; `0`, because the audio storage folder is new.

**M8P-7 Browser session (M8D-1).** In Chrome, open `http://localhost:5173/auth/login` and press F12, then Console. If Chrome asks, type `allow pasting`. Run:

```javascript
localStorage.setItem('auth_token', 'oam8-local'); localStorage.setItem('refresh_token', 'oam8-local'); location.href = '/voices';
```

Expected: the Voice Management page.

**M8P-8 Record.** On `/voices`, under "Record Your Voice", allow the microphone, speak for 10–20 s, stop, name the voice `OAM8 Chrome`, and upload it. Go straight on to M8-2 without restarting anything: M8-2 then also shows that a new voice clones straight away (COA-12).

**M8P-9 Upload.** Under "Upload Voice File", choose `$HOME\oam8-private\sample.wav` and upload it. An evaluation error may appear afterwards, because no evaluation service runs on `:9000`; it does not affect the voice. Check in Terminal D:

```powershell
(Invoke-RestMethod http://localhost:8002/voices).data | Select-Object -Last 2 id, name
```

Expected: the last two entries are `OAM8 Chrome` and `Unnamed Voice`. The newest `Unnamed Voice` is the last one in the `/tts` voice list.

**M8P-10 One generation on `/tts`.** Run `Get-HistoryTotal` in Terminal D and note it ("before"). On `/tts`, choose Chatterbox, pick the voice and the language the case names, paste the case's text, and click Generate once. The first call can take 2 minutes or more (a cold start is about 80–100 s), and Generate stays disabled while you wait. Then run `Get-HistoryTotal` again ("after").

**Texts:**

- T-EN: `OAM8 English check. Hello, this is my cloned voice reading a short English sentence on the text to speech page.`
- T-HI: `नमस्ते। यह क्लोन की गई आवाज़ में हिंदी की एक छोटी जाँच है।`
- T-LONG, built and copied in Terminal D:

```powershell
$long = ((1..80 | ForEach-Object { "This is sentence $_ of the long text check, read by the cloned voice." }) -join " ") + " This is the final sentence of the long text check."
$long.Length
Set-Clipboard -Value $long
```

Expected: `5641`.

**Rules for M8-2 to M8-6 (a clone).** **Met:** an audio player appears with no error message. When played, you hear the case's text in the selected voice (the recorded or uploaded speaker, not a Google voice) and in the chosen language, and the history total goes up by 1. **Not met:** anything else, including any error message, no audio, a different voice or language, or missing words.

| Case | Steps | Extra for met |
| --- | --- | --- |
| M8-1 | After M8P-6: write down what the port check showed. State whether the service at the CON-5 URL is the deployment you made, unchanged and not redeployed for this check, and that you ran no Docker or `gcloud` command | Met: one process per port, and you confirm both. Otherwise not met |
| M8-2 | M8P-10 with `OAM8 Chrome`, English, T-EN | — |
| M8-3 | M8P-10 with `OAM8 Chrome`, Hindi, T-HI | — |
| M8-4 | M8P-10 with the newest `Unnamed Voice`, English, T-EN | — |
| M8-5 | M8P-10 with the newest `Unnamed Voice`, Hindi, T-HI | — |
| M8-6 | M8P-10 with `OAM8 Chrome`, English, T-LONG (paste with Ctrl+V). Then in Terminal D: `(Invoke-RestMethod "http://localhost:8003/inference/generations?search=final%20sentence%20of%20the%20long").items[0].text.Length` | The command prints `5641`. When played: you hear sentence 1, then near the middle sentence numbers in order around 40, and the clip ends with "This is the final sentence of the long text check." If the page loses the request, play the entry from the history list instead (Plan OAR-3) |
| M8-7 | Uses the M8-2 generation. Reload `/tts`: the history lists an entry starting "OAM8 English check"; press Play. Then run commands M8-7a, M8-7b and M8-7c below in Terminal D. Press Delete on that entry and reload `/tts`. Then run M8-7b and M8-7c again | Play sounds like M8-2. M8-7a saves a file you can play, the same clip. M8-7b prints `retention_days 30.0`. After the delete: the entry is gone after the reload, M8-7c prints `404`, and M8-7b prints `NO RECORD` |

M8-7 commands (Terminal D, after M8P-6, with the same `DATABASE_URL` as Terminal B):

```powershell
$job = (Invoke-RestMethod "http://localhost:8003/inference/generations?search=OAM8%20English%20check").items[0].job_id
$job
$retention = @'
import sys
from voice_narration.inference.db import SessionLocal
from voice_narration.inference.models import Generation
with SessionLocal() as db:
    g = db.query(Generation).filter(Generation.job_id == sys.argv[1]).first()
    if g is None:
        print("NO RECORD")
    else:
        print("created_at", g.created_at, "expires_at", g.expires_at, "retention_days", (g.expires_at - g.created_at).total_seconds() / 86400)
'@
# M8-7a download
Invoke-WebRequest "http://localhost:8003/inference/jobs/$job/download" -OutFile "$HOME\oam8-private\m8-7.wav" -UseBasicParsing
(Get-Item "$HOME\oam8-private\m8-7.wav").Length
# M8-7b retention
$retention | python - $job
# M8-7c download status
try { Invoke-WebRequest "http://localhost:8003/inference/jobs/$job/download" -UseBasicParsing | Out-Null; "200" } catch { $_.Exception.Response.StatusCode.value__ }
```

Before the delete, M8-7c prints `200`.

**Rules for M8-8 to M8-12 (a call-time cause).** Before each case, restart Terminal B with the case's setting change (M8P-4). Use M8P-10 with `OAM8 Chrome`, English and T-LONG, which is long enough that the 3 s limit in M8-8 is surely reached. After each case, set the variable back to its M8P-4 value before the next case.

- **Met:** the page shows exactly the expected message, every character, ending "Please retry, or choose another provider.". No audio player appears for it, and the history total is unchanged (no Google audio, no entry; COA-8).
- **Not met:** a message that is not one of the nine contract messages (`API-Contract.md:336-346`), any audio, a higher history total, or the right message with the wrong number.
- **Not verified:** the setting change did not produce the cause. That means another of the nine contract messages appears (write it down), or the generation succeeds (write it down, then delete that history entry), or, for M8-10, you have no M8I-5 key. COA-16 and AC-6 allow this result.

| Case | Setting change in Terminal B | Expected message |
| --- | --- | --- |
| M8-8 OAF-5 | `$env:CHATTERBOX_TIMEOUT_SECONDS = "3"` | `Chatterbox did not respond within 3 seconds. Please retry, or choose another provider.` |
| M8-9 OAF-6 | `$env:CHATTERBOX_URL = "https://127.0.0.1:1"` | `Could not connect to Chatterbox. Please retry, or choose another provider.` |
| M8-10 OAF-7 | `$env:GOOGLE_APPLICATION_CREDENTIALS = "$HOME\oam8-private\other-account-key.json"` | `Access to Chatterbox was denied (HTTP 403). Please retry, or choose another provider.` or the same with `HTTP 401` |
| M8-11 OAF-8 | `$env:CHATTERBOX_URL = "https://chatterbox-model-api-177206684903.asia-southeast1.run.app/oam8-no-such-path"` | `Chatterbox returned an error (HTTP <status>). Please retry, or choose another provider.`, with any status other than 200, 401 or 403 (404 expected, a hypothesis). If the OAF-7 message appears instead, M8-11 is not verified |
| M8-12 OAF-9 | none: no setting change produces it without changing the deployed service, or without sending the token and sample somewhere other than Chatterbox (M8D-6) | `Chatterbox returned a response that is not audio. Please retry, or choose another provider.`. Not verified, unless this message appeared in any case; then write down where |

**M8P-11 Record.** Fill in the table in `Plan.md`, section "OAM-8 manual validation evidence". Use the last three columns, plus the voice column for M8-4 and M8-5 if you used a different voice. Write no key, password, token, database URL or sample there.

**M8P-12 Finish.** Press Ctrl+C in Terminals A, B and C. In Terminal D, run `Get-NetTCPConnection -LocalPort 8002,8003,5173 -State Listen -ErrorAction SilentlyContinue` (expected: nothing) and `git status --short` (expected: only `docs/.ai/` paths). Optional: delete the two test voices on `/voices` (they are removed 5 days after upload anyway); run `localStorage.clear()` in the Chrome console; delete `$HOME\oam8-private`, which holds the key. Then tell the executor the table is filled in.

## Execution Steps

1. Confirm that this plan's Human Review status records approval, and that M8Q-1 is answered in this plan. If either is missing, stop.
2. Run M8V-1 and M8V-2 (M8C-1). If either differs from its expected result, stop.
3. Check that `Plan.md`'s SHA-256 is `e401dd722d441a186b2b8f1b01afbd5e0c400b563e72c991ba5b8aa7c5c4c7d4`; any other value is a plan difference, so stop. Apply the diff with `git apply` from the repository root, then run M8V-3.
4. Append the M8V-1 to M8V-3 output, trimmed, below the result table in `Plan.md`. Report `Waiting — manual check from user` and stop. The executor does not start the services and does not run the protocol.
5. When the user reports that the table is filled in: run M8V-1, M8V-4 and M8V-5, append their output, and check M8C-2 to M8C-6 against the table. If every criterion holds, set the OAM-8 row to `Complete — manual validation recorded <date>`. If any case is `not met`, set it to `Blocked — <case IDs> not met; replanning required`: such a case is not fixed here (`Plan.md:277`). Update this plan's Human Review status.

## Acceptance / Completion Criteria

- **M8C-1** Before the user starts: the code is the OAM-7 code (M8V-1 prints nothing), no root `.env`, `.env.local` or `.env.production` exists, and ports 8002, 8003 and 5173 are free (M8V-2).
- **M8C-2** Cases M8-1 to M8-7 are each recorded `met`, and M8-2 to M8-7 also record the voice and the language used.
- **M8C-3** Cases M8-8 to M8-12 are each recorded `met` or `not verified`, with the message seen. None is `not met`.
- **M8C-4** The table holds no key, password, token, database URL or sample (read by the executor).
- **M8C-5** After the protocol, `git status --short --untracked-files=all` lists only paths under `docs/.ai/chatterbox-original-app/`; `git status --short -- audio_storage` prints nothing; and M8V-1 still prints nothing. This milestone's Execution Status update and the evidence section are excluded from this file limit.
- **M8C-6** The user confirms in M8-1 that no Docker or `gcloud` command ran and the deployed service was not changed or redeployed. After M8P-12, no listener remains on 8002, 8003 or 5173 (M8V-5).

## Verification

### Commands

Run by the executor in Git Bash from the repository root. Expected results are Expected / Predicted — Not Yet Verified.

```bash
# M8V-1 — expected: prints nothing
git diff --stat 60a9192 HEAD -- . ':(exclude)docs/.ai'; git diff --stat -- . ':(exclude)docs/.ai'
# M8V-2 — expected: no .env line; "ports exit 1"
ls -a | grep -E '^\.env(\.local|\.production)?$'; netstat -ano | grep -E ':(8002|8003|5173) .*LISTEN'; echo "ports exit $?"
# M8V-3 — expected: bf4dc09f81de33e467ba49330396777a1b95715a19ba4c770ebb8987b9ddedf9; "20<TAB>1<TAB>docs/.ai/chatterbox-original-app/Plan.md"
sha256sum docs/.ai/chatterbox-original-app/Plan.md; git diff --numstat -- docs/.ai/chatterbox-original-app/Plan.md
# M8V-4 — expected: only docs/.ai/chatterbox-original-app/ paths; nothing; ".gitignore:11:/voice_storage/	voice_storage/x"
git status --short --untracked-files=all; git status --short -- audio_storage; git check-ignore -v voice_storage/x
# M8V-5 — expected: "ports exit 1"
netstat -ano | grep -E ':(8002|8003|5173) .*LISTEN'; echo "ports exit $?"
```

M8V-3 runs right after the diff is applied, before any evidence is appended. M8V-1 is run again at step 5 (M8C-5).

### Affected Tests

None. The only modified file is `Plan.md`, under `docs/.ai/`. No test reads it: `grep -rln "docs/.ai\|Plan.md" tests frontend/tests` found only contract citations in the docstrings of `tests/test_inference_provider_choice_red.py:3` and `tests/test_voice_sample_persistence_red.py:3`.

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- M8V-1 to M8V-5 as stated in the comments of the command block above.
- The user's table: M8-1 to M8-7 `met`. M8-8 and M8-9 `met`. M8-10 `met` if the user has an M8I-5 key, otherwise `not verified`. M8-11 `met` or `not verified`, depending on M8D-6's hypothesis. M8-12 `not verified`.
- Preserved-behavior tests (expected to pass at RED): not applicable (OTHER). The preserved suites are not rerun, because no file they cover changes (M8C-5); their OAM-7 results stand (`Plan.md:555-559`).

### Planning-Time Dry Run

Planning-time dry run, 2026-11-14. This is not milestone evidence. It ran in a disposable copy made with `git archive HEAD` into the session scratchpad, with `frontend/node_modules` linked by a junction. The private folder was a scratchpad folder standing in for `$HOME\oam8-private`, and the commands ran through PowerShell 5.1 scripts. No key, Chatterbox call, browser or real database password was used.

| Step | Command (as run) | Result |
| --- | --- | --- |
| M8P-2 | `Test-Path .env, .env.local, .env.production`; port check | `False` ×3; nothing listening |
| M8P-3 | `python -m voice_narration.simple_voices` | `Uvicorn running on http://0.0.0.0:8002` |
| M8P-4 | the M8P-4 block, without the `DATABASE_URL` line, with no key file present | `Uvicorn running on http://0.0.0.0:8003` |
| M8P-5 | `npm run dev` | `VITE v5.4.21 ready`, `Local: http://localhost:5173/` (listening on `[::1]:5173`) |
| M8P-6 | port check; health; backends; history total | one process per port; `{"status":"ok","service":"voice-management"}`; `azure chatterbox google mock`; `0` |
| M8P-9 stand-in | `curl.exe -s -F "file=@…\sample.wav" http://localhost:8002/voice/upload`, then `GET /voices/<id>/sample` | name `Unnamed Voice`; `200`; the last listed voice was the upload |
| Pre-call path | `POST /inference/jobs/oam8-dry-1/infer` with `provider` `chatterbox`, `language` `en` and no key file | `503 {"error":"Could not obtain an identity token for Chatterbox. Please retry, or choose another provider."}`; history total stayed `0`. No network call (`chatterbox.py:86` fails on the missing file) |
| T-LONG | the `$long` command | `5641` |
| M8P-1 | the `client_email` command on a dummy JSON file | printed the dummy's `client_email` |
| M8-7 retention, default DB | the `$retention` script | `psycopg2.errors.InsufficientPrivilege: permission denied for table generations` (M8Q-1) |
| M8-7 path, scratch SQLite DB | inference restarted with `DATABASE_URL=sqlite:///<scratch>/dry.db`; one mock generation (`provider` `google`, `job_id` `oam8-dry-3`); then the M8-7 commands, then `DELETE /inference/generations/oam8-dry-3` | search found `oam8-dry-3`; `retention_days 30.0`; download `32044` bytes; delete `{"job_id":"oam8-dry-3","deleted":true}`; then `NO RECORD`, download `404`, total `0` |
| Diff | `git apply --check` then `git apply` of the Plan.md diff, in a scratch git repo with `core.autocrlf=true` holding the current CRLF `Plan.md` | check OK; SHA-256 `bf4dc09f…ddedf9`; numstat `20 1` |
| Cleanup | `taskkill /T /F` of each started process; junction removed with `rmdir`; scratch folders deleted | ports 8002, 8003 and 5173 free; the worktree's `node_modules` intact; `git status --short` printed nothing |

Not run, because each needs your input: M8P-1 with the real key, M8P-4 and M8P-6 `Read-Host` with a real `DATABASE_URL`, M8P-7 to M8P-9 in Chrome, every case that calls Chatterbox (M8-2 to M8-11), the Hindi paste and `Set-Clipboard`.

## Risks

- **M8R-1 Long text against the deployed service (hypothesis).** The repository does not show whether the deployed Chatterbox speaks 5641 characters in one call, or how long that takes. If it stops early, or runs past 1200 s (OAF-5), M8-6 is not met and goes back to planning, because the service cannot be changed (CON-3).
- **M8R-2 Failure-cause reproduction rests on hypotheses (M8D-6).** Three things are not established. First, that Google issues a token for the audience `https://127.0.0.1:1` (needed for M8-9; otherwise OAF-4 appears). Second, that Cloud Run answers another account's token with 401 or 403 (the contract states it is rejected, `API-Contract.md:321`; the status is not established). Third, that a path in the audience is accepted, so M8-11 gives 404 (the Cloud Run docs do not say). Each outcome is covered by the not verified rule.
- **M8R-3 An abandoned call keeps running.** After M8-8's 3 s limit, the inference service stops waiting, but the deployed service may finish the call. Nothing is saved locally. Cloud Run usage is outside this plan.
- **M8R-4 Settings files at the root.** `.env.local` and `.env.production` are loaded (`db.py:15-16`) and not gitignored. The protocol creates neither, and M8P-2 requires that none exists.
- **M8R-5 Identity checks.** The protocol compares no identity, role or ownership itself. Which account may call is decided by Cloud Run (CON-5). The bearer token goes only over HTTPS to the configured Chatterbox URL, or nowhere: the connection in M8-9 is refused before anything is sent.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Reverse only this milestone's change: `git checkout -- docs/.ai/chatterbox-original-app/Plan.md` only if it holds nothing but this milestone's change since the hash check in step 3. Otherwise, edit back the OAM-8 row and remove the OAM-8 evidence section by hand. Outside the repository, the user may delete `$HOME\oam8-private` and the test voices.

## Explicitly Out of Scope

- Any code, test, build, configuration or launcher change; the `.bat` launchers stay as they are (M8D-2).
- Docker and `gcloud` (CON-2); changing or redeploying the deployed Chatterbox, including to reproduce a cause (CON-3).
- Faking Chatterbox, or sending the token or a sample to any server other than the deployed service (COA-16, CON-6).
- Committing keys, samples, generated audio, `DATABASE_URL` or `.env` files (CON-6).
- Fixing a `not met` case: it is reported for replanning (`Plan.md:277`).
- Re-running the backend and frontend suites (M8C-5); S-3, S-6 and S-7, which are verified elsewhere (`Plan.md` Requirement Traceability).

## Decisions for Review

Added because a validation protocol needs these choices reviewed (`implementation-planning` OTHER).

- **M8D-1 Browser session from `localStorage`.** Reason: no repository service answers `/auth/login` on `:9000`, and the app restores a session from any stored tokens (Current Repository State). The voice and inference services check no token. Alternative: log in through an auth service you run on `:9000`, if you have one; then skip M8P-7.
- **M8D-2 Start the services with direct commands, not the `.bat` launchers.** Reason: the inference launcher sets `INFERENCE_PROVIDER=google` and a different key path (`start-inference-service.bat:11-12`), and both launchers `cd voice_narration` first. Alternative: edit the launchers, which is a file change outside this scope.
- **M8D-3 `INFERENCE_PROVIDER=mock`.** Reason: Chatterbox generations do not use the startup provider (`API-Contract.md:278-281`), and this keeps the test-850 key out of Google Text-to-Speech. The no-fallback check is the unchanged history total and the absence of audio. Alternative: `google`, which is not needed by any case.
- **M8D-4 `AUDIO_STORAGE_PATH=$HOME\oam8-private\audio_storage`.** Reason: it keeps tracked `audio_storage/` unchanged (OAS-1) and clips of your voice out of a tracked folder, and history starts at `0`. Alternative: the default folder, then restored with OAV-3.
- **M8D-5 One private folder outside the repository** for the key, the WAV, the download and the audio storage. Alternative: the repository root, where only `service-account-key.json` is ignored (`.gitignore:8`).
- **M8D-6 How each call-time cause is reproduced, using local settings only:**
  - OAF-5: a 3 s limit with T-LONG.
  - OAF-6: `https://127.0.0.1:1`, a refused local port.
  - OAF-7: another account's key, which the contract says Cloud Run rejects (`API-Contract.md:321`).
  - OAF-8: the CON-5 URL with a path that does not exist.
  - OAF-9: none.

  Rejected alternatives: an echo service such as a public request inspector, which would receive the token and the sample (CON-6); a local stand-in server, which fakes Chatterbox (Q46); and an `http://` URL, which would send the bearer token unencrypted.
- **M8D-7 Long text.** 80 numbered sentences and a final marker, 5641 characters. "Sent whole" is checked by the history entry's text length. "Spoken whole" is checked by hearing the first sentence, ordered numbers in the middle, and the final marker.

## Human Review

Status: Approved by Avinash Srivastava on 2026-11-14, as written, including decisions M8D-1 to M8D-6 and the M8Q-1 answer (a).
