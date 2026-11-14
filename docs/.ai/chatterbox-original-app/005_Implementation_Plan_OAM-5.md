# Implementation Plan

## Milestone

OAM-5 — Inference service GREEN (`docs/.ai/chatterbox-original-app/Plan.md`, Milestones, OAM-5, `Plan.md:197-216`).

## Milestone Type

GREEN

## Review Summary

- Behavior change: each generation uses the provider it names (`google` or `chatterbox`), with `400` answers for an unsupported provider or Chatterbox language. Chatterbox is listed among the providers. Generations run one at a time, and later requests wait. A Chatterbox generation fetches the voice's sample from the voice service, obtains an identity token from the service-account key, and calls the deployed Chatterbox, bounded by `CHATTERBOX_TIMEOUT_SECONDS` (default 1200). It answers `503` with the contract message for each of OAF-1 to OAF-9, and a successful clone is saved to history like any other generation.
- Requirements delivered: COA-1, COA-5, COA-7 and COA-17 (inference parts), COA-4, COA-8, COA-9, COA-10, COA-13 (waiting), CON-5; contract OAC-1 to OAC-9 and OAC-11 for the inference service.
- Files: created `voice_narration/inference/chatterbox.py`; modified `voice_narration/inference/application.py`; deleted none.
- Tests added: none. The 36 OAM-4 tests in `tests/test_inference_provider_choice_red.py` go from failing to passing, unchanged. The Chatterbox call itself (the token request, the call, the time limit, OAF-5 to OAF-9, cloned-clip history) has no automated test and is checked only at OAM-8 (COA-16, Plan OAR-9).
- Verification: the OAM-4 file twice, then OAV-2 once. Expected / Predicted — Not Yet Verified: `36 passed` twice, then `1 failed, 100 passed, 17 skipped` from 118 collected tests, whose one failure is the accepted `test_production_inference_module_missing`.
- Needs attention: N5D-2 (the token through google-auth, honoring N4D-2), N5D-3 (google-auth and requests used but not declared, Plan OAR-4), N5D-4 (outbound client settings), N5D-6 (the WAV reader), N5R-3 (google-auth's own 120 s limit on the token request), and the call-time code reviewed under Contract Rule Coverage with no automated test.

## Authoritative References

| Document | Status read |
| --- | --- |
| `docs/.ai/chatterbox-original-app/requirements.md` | Approved by Avinash Srivastava on 2026-11-13, revision recording Q46–Q48 (`requirements.md:17`) |
| `docs/.ai/chatterbox-original-app/Plan.md` | Approved by Avinash Srivastava on 2026-11-13, as written (`Plan.md:5`), including the planning call "OAM-5 call behavior with no RED test, OAR-9". OAM-5 row: `Pending` (`Plan.md:359`) |
| `docs/.ai/chatterbox-original-app/API-Contract.md` (OAM-1 deliverable, authoritative predecessor) | Approved by Avinash Srivastava on 2026-11-13 (`API-Contract.md:527`); OAM-1 row Complete (`Plan.md:355`) |
| `docs/.ai/chatterbox-original-app/001_Implementation_Plan_OAM-2.md` | Approved, executed (`:669`). Read: Review Summary, Carried-Forward Decisions |
| `docs/.ai/chatterbox-original-app/002_Implementation_Plan_OAM-3.md` | Revision 4 approved, executed (`:801`). Read: Review Summary, Carried-Forward Decisions, V3Q-1 to V3Q-3 (`:730-740`), Verification commands |
| `docs/.ai/chatterbox-original-app/003_Implementation_Plan_OAM-4.md` | Superseded, not executed (`Plan.md:358`). Not used |
| `docs/.ai/chatterbox-original-app/004_Implementation_Plan_OAM-4.md` | Approved by Avinash Srivastava on 2026-11-13, including N4D-1 to N4D-6; executed (`:760`). Read in full, since this milestone makes its tests pass |
| Reference contract `feature/voice-cloning@abbe387:docs/.ai/chatterbox-cloud-run/API-Contract.md` | Contract Review Status: Approved 2026-11-09. Read only its Chatterbox Synthesize (`:75-110`) and Chatterbox Caller Identity (`:148-154`) sections, the fixed constraint `Plan.md:82` adopts |
| Product-level `docs/requirements.md` | Does not exist (checked `docs/`) |
| create-implementation-plan arguments, 2026-11-13 | User context for this run: no automated test fakes or calls Chatterbox, and neither does the dry run; honor N4D-2 and N4D-5; full-suite checks use OAV-2 with the three V3Q-3 files ignored; no local Docker and no `gcloud`. No question IDs were answered, so none is recorded |

## Carried-Forward Decisions

- **N4D-2** (`004_Implementation_Plan_OAM-4.md:104-113`): no lookup of a host outside this machine while the four pre-call causes are answered. In particular, no google-auth `fetch_id_token` metadata-server fallback. Applied in N5D-2 and N5R-7.
- **N4D-3** (`004:114-119`): the settings are read from the process environment no earlier than `create_app`. Applied: `ChatterboxSettings.from_environment()` runs in `InferenceState.__init__`, which `create_app` calls (`application.py:427`).
- **N4D-4** (`004:120`): the startup provider is injected with `create_app(provider=…)` and is used for `google`, absent, `null` and `""`. Kept unchanged.
- **N4D-5** (`004:121-127`): the database is reached only through the module names `SessionLocal` and `create_all_tables` (`application.py:22`). Kept: the diff does not touch them, and the Chatterbox path saves through the existing `persist_generation`.
- **N4D-8** (`004:137`): the provider list is exactly `azure`, `chatterbox`, `google`, `mock`, with the contract descriptions.
- **V3Q-1 (a)** (`002_Implementation_Plan_OAM-3.md:730-736`), as applied for this milestone by the Plan's OAM-5 success criteria (`Plan.md:216`): only the failing tests named in the plan are accepted as pre-existing failures, and any other failure fails the milestone. The one named test is `tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing` (`Plan.md:343`, `:446`).
- **V3Q-3** (`002:736`): `tests/test_persistence.py`, `tests/test_authentication_consent.py` and `tests/test_voice_enrollment.py` are left out of every backend-suite run (OAV-2, `Plan.md:343`).
- **OAV-3 handling** (`002:596-597`, `Plan.md:344`): after a backend run writes to tracked `audio_storage/`, the output is recorded, then restored with `git checkout -- audio_storage` and `git clean -fd -- audio_storage`.
- **V2D-1 / V3D-1** (`001:99-106`, `002:124-130`): the voice service and its `GET /voices/{voice_id}/sample` are unchanged; the inference service only calls that operation.

## Preconditions / Predecessor Evidence

- `Plan.md` records approval (`Plan.md:5`). OAM-5 is recorded as GREEN (`Plan.md:201`), with predecessor OAM-4 (`Plan.md:202`).
- OAM-4 is `Complete — valid RED established 2026-11-13` (`Plan.md:358`). In both runs, the 36 tests failed in exactly four classes: 22 `assert 200 == 503`, 12 `assert 200 == 400`, 1 no-waiting, 1 provider list. There were no errors, and the 29 preserved tests passed (`Plan.md:457-477`). Each failure is an assertion on contracted behavior that is missing, which is valid RED evidence for every behavior this milestone must make pass.
- OAM-5 Execution Status is `Pending` (`Plan.md:359`). No earlier OAM-5 Implementation Plan exists. The folder holds `001` to `004`, so this plan is `005`.
- Repository state, inspected 2026-11-13: HEAD `598d9eb`, branch `claude/chatterbox-original-app-client-a3ef0e`, and `git status --short` printed nothing. Commit `598d9eb` adds `tests/test_inference_provider_choice_red.py`; with CR removed, its SHA-256 is `f0f8ab986f603c79bd52a81f4826d3fac6e4da77d9a75ab7eeff32fe7c892365`, the N4C-1 value. `git diff --stat 059102c HEAD -- voice_narration tests .gitignore` lists only that test file. `Plan.md` records no `Committed as` entries, but the tree is clean, so nothing is unrecorded.
- No `.env`, `.env.local` or `.env.production` exists (only `.env.example`).
- Python on PATH: `finnie-chat\venv`, Python 3.14.3. httpx 0.28.1, fastapi 0.162.0 and uvicorn 0.54.0 are pinned in `requirements-dev.txt:1-5`. google-auth 2.62.1, requests 2.33.1 and cryptography 50.0.2 are installed but not declared (N5D-3).

## Current Repository State

- `voice_narration/inference/application.py:22`: `from .db import SessionLocal, create_all_tables` (N4D-5). `:26` is the last import, followed by two blank lines before `get_default_provider_name` (`:29`).
- `application.py:83-85`: `InferenceState.__init__` sets `self.provider`, `self.jobs_app`, `self.job_repository`. `create_app` builds `InferenceState` at `:427`, so settings read in `__init__` are read when `create_app` runs.
- `application.py:286-304`: `submit_for_inference` calls the startup provider (`:292`), then stores the output in `_pending_inferences` and saves it with `persist_generation` (`:296-298`). `persist_generation` (`:130-181`) writes the audio file and history entry, and writes the database record with expiry `AUDIO_RETENTION_DAYS`, default 30 (`:174`), inside a block that ignores database errors (`:151-179`).
- `application.py:343-373`: `list_backends` returns the registry's providers in name order (`registry.py:60`), with the baseline descriptions.
- `application.py:460-479`: the generation route reads only `script` and `voice_id` (`:462-463`), answers check 2 (`:465-469`), calls `submit_for_inference` with no lock (`:471`), and maps `ValueError` to `400` and any other exception to `500` (`:473-479`).
- `application.py:623`: `app = create_app()` runs at import, so `InferenceState.__init__` also runs at import.
- `voice_narration/inference/db.py:14-16`: `.env` files are loaded once, at import. The new code does not load them again (N4D-2, Plan OAR-8).
- `voice_narration/inference/providers/google_tts.py:59`: the Google provider imports its client library inside a method, so the service starts without it (precedent for N5D-3).
- `voice_narration/simple_voices/application.py:184-197`: `GET /voices/{voice_id}/sample` answers `404 {"error": "Voice not found"}` or `404 {"error": "Voice sample not found"}`, or the sample bytes.
- Installed google-auth: `google/oauth2/service_account.py:559` defines `IDTokenCredentials`, and `:687-705` defines `from_service_account_info(info, **kwargs)`, which requires `client_email` and `token_uri`. `google/auth/transport/requests.py:49` sets `_DEFAULT_TIMEOUT = 120`.
- Installed uvicorn `protocols/http/h11_impl.py:459-460`: `send` returns without error once the client has disconnected (N5D-7). `httptools` is not installed, so uvicorn uses h11.
- Deployed Chatterbox response: `abbe387:voice_narration/chatterbox_api/application.py:65-73`, `:135` converts the output to a float32 tensor, writes it with `torchaudio.save(…, format="wav")` and answers `media_type="audio/wav"` (N5D-6).
- Working-tree line endings: `application.py` is `i/lf w/crlf` (`git ls-files --eol`), and `core.autocrlf` is `true`. The diff below is LF, and the dry run showed that `git apply` applies it to the CRLF file (Planning-Time Dry Run).

## Files in Scope

### Files to Create

- `voice_narration/inference/chatterbox.py`

### Files to Modify

- `voice_narration/inference/application.py`

### Files to Delete

None.

## Proposed Changes

1. **Create `voice_narration/inference/chatterbox.py`.** It holds the Chatterbox call behind one boundary (N5D-1):
   - **Message constants:** `CLOSING`, and the nine OAF messages, exactly as in `API-Contract.md:338-346`: `NOT_CONFIGURED`, `INVALID_TIME_LIMIT`, `SAMPLE_UNREADABLE`, `TOKEN_UNAVAILABLE`, `TIMED_OUT` (`{seconds}`), `CANNOT_CONNECT`, `ACCESS_DENIED` (`{status}`), `SERVICE_ERROR` (`{status}`), `NOT_AUDIO`.
   - **Other constants:** `DESCRIPTION` (`API-Contract.md:451`), `LANGUAGES = ("en", "hi")` (`:290`), `DEFAULT_TIME_LIMIT_SECONDS = 1200` (`:474`, COA-9), `DEFAULT_VOICE_SERVICE_URL = "http://localhost:8002"` (`:476`).
   - **`class ChatterboxFailure(Exception)`:** its message is the contract text. It is not a `ValueError`, so the route's existing `ValueError → 400` mapping does not catch it.
   - **`trimmed_url(value) -> str`:** strips surrounding whitespace and trailing `/` (`:473`, `:476`).
   - **`parse_time_limit(value) -> Optional[int]`:** absent or blank gives `1200`; ASCII digits with value ≥ 1 after trimming give that value; anything else gives `None`, which is invalid (`:474`).
   - **`@dataclass(frozen=True) ChatterboxSettings(url, time_limit, voice_service_url, credentials_path)` with `from_environment()`:** reads `CHATTERBOX_URL`, `CHATTERBOX_TIMEOUT_SECONDS`, `VOICE_SERVICE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` (`:471-476`).
   - **`service_account_identity_token(credentials_path, audience) -> str`:** blank path, unreadable file, non-JSON content or a `type` other than `service_account` each raise before google-auth is imported. Otherwise it calls `IDTokenCredentials.from_service_account_info(info, target_audience=audience)` and `refresh(Request())` (N5D-2, N5D-3).
   - **`wav_duration(audio) -> float`:** reads the RIFF chunks and returns sample frames divided by sample rate; raises `ValueError` when the bytes are not a readable WAV file (N5D-6, `:329`).
   - **`class ChatterboxClient`**, with `generate(script, voice_id, language) -> dict`. It runs these steps in contract order, each raising `ChatterboxFailure`:
     - OAF-1, OAF-2;
     - `_fetch_sample` (OAF-3);
     - `_obtain_identity_token` in a worker thread (OAF-4);
     - `_synthesize` under `asyncio.wait_for(…, timeout=limit)` (OAF-5, OAF-6);
     - `_read_audio` (OAF-7, OAF-8, OAF-9);
     - `wav_duration` (OAF-9).
     It returns the provider output shape `{"output_seconds", "audio_bytes", "format": "wav"}` that `persist_generation` already reads (`application.py:134-144`).
2. **Modify `voice_narration/inference/application.py`** (diff below):
   - a. Add `import asyncio`.
   - b. Import `DESCRIPTION as CHATTERBOX_DESCRIPTION`, `LANGUAGES as CHATTERBOX_LANGUAGES`, `ChatterboxClient`, `ChatterboxFailure` and `ChatterboxSettings` from `.chatterbox`.
   - c. Add the module constants `UNSUPPORTED_PROVIDER` and `UNSUPPORTED_LANGUAGE`, the exact `400` strings (`API-Contract.md:289-290`).
   - d. Add `unsupported_choice_error(provider, language) -> Optional[str]`. It returns `UNSUPPORTED_PROVIDER` when `provider` is not `None`, `""`, `"google"` or `"chatterbox"` (exact, case-sensitive, any type), and `UNSUPPORTED_LANGUAGE` when `provider == "chatterbox"` and `language` is not exactly `"en"` or `"hi"`; otherwise it returns `None` (`:282-283`, `:289-290`, `:495`).
   - e. In `InferenceState.__init__`, add `self.chatterbox = ChatterboxClient(ChatterboxSettings.from_environment())` and `self.generation_lock = asyncio.Lock()` (N4D-3, N5D-5).
   - f. In `submit_for_inference`, replace the store-and-return lines (`:296-304`) with `return self._store_output(job_id, script, voice_id, output)`. Add `_store_output(job_id, script, voice_id, output) -> dict`, which holds those same lines unchanged. Add `async submit_for_cloning(job_id, script, voice_id, language) -> dict`, which calls `self.chatterbox.generate` and then `_store_output`. A `ChatterboxFailure` propagates before anything is stored (`:297`, `:300`, OAC-11).
   - g. In `list_backends`, append `{"name": "chatterbox", "provider_class": ChatterboxClient.__name__, "description": CHATTERBOX_DESCRIPTION}` and return the list sorted by `name` (`:449-454`).
   - h. Update the generation route's docstring with `provider` and `language`.
   - i. In the generation route, read `provider` and `language`. After check 2, answer `unsupported_choice_error` with `400`. Then, inside `async with state.generation_lock`, call `submit_for_cloning` for `"chatterbox"` and `submit_for_inference` otherwise. Add `except ChatterboxFailure as e:` → `503 {"error": str(e)}`, ahead of the existing `except ValueError` (`:286-293`, `:306-308`).
3. No other file changes: no test, no build or dependency file, no `.env.example`, no launcher, and nothing in the voice service, frontend or `audio_storage/`.

### Decisions for Review

- **N5D-1 Chatterbox is a separate module, not a registered provider.** `chatterbox.py` holds the settings, messages, token, call and WAV reading. `application.py` keeps the HTTP mapping, the waiting, the listing and the saving.
  - Alternatives:
    - (a) A `ChatterboxProvider(InferenceProvider)` registered in `ProviderRegistry`. Rejected: the registry builds providers from a config dict (`registry.py:49-50`) and requires `estimate_cost` and `list_voices`, which Chatterbox does not offer. Registering would also change the registry contents that `tests/test_provider_registry.py` checks, which COA-14 keeps unchanged. And `generate(script, voice_id)` has no language.
    - (b) All the code in `application.py`. Rejected: it is already 623 lines (code-quality SZ1).
- **N5D-2 The identity token comes only from the key file (CON-5, N4D-2).**
  - The key file named by `GOOGLE_APPLICATION_CREDENTIALS` is read at each Chatterbox generation (`API-Contract.md:475`). It must be JSON with `"type": "service_account"`. Then `service_account.IDTokenCredentials.from_service_account_info(info, target_audience=<Chatterbox URL in effect>)` is refreshed through `google.auth.transport.requests.Request()`, inside `asyncio.to_thread`, so the event loop is not blocked.
  - Every exception becomes OAF-4, including an import failure.
  - For the OAM-4 OAF-4 cases (absent, blank, missing file, not JSON, authorized-user key), it raises before importing google-auth or opening a connection.
  - Alternatives:
    - (a) `google.oauth2.id_token.fetch_id_token`. Rejected: it pings the metadata server when the key is absent or not a service-account key (installed `google/oauth2/id_token.py:297-349`), which N4D-2 forbids.
    - (b) Signing the JWT and exchanging it by hand. Rejected: that re-implements google-auth.
- **N5D-3 Libraries: google-auth and requests are used but not declared; no dependency file changes (Plan OAR-4).**
  - Used: google-auth (`google.oauth2.service_account`, `google.auth.transport.requests`), installed 2.62.1, and requests, installed 2.33.1, which that transport needs. Both are already in the environment as dependencies of the Google provider's client library, which is itself undeclared (Plan Current State `:51`). Also used: httpx, pinned at 0.28.1 (`requirements-dev.txt:5`).
  - Support check (PyPI JSON, read 2026-11-13): google-auth's latest release is 2.62.2, `requires_python >=3.10`, with a `requests` extra. requests' latest is 2.34.2, `requires_python >=3.10`. The installed versions are in those current release lines. The two calls used exist in the installed source (Current Repository State).
  - google-auth is imported inside the token function, as `google_tts.py:59` imports its library, so the service starts without it and its absence is OAF-4.
  - Alternative: add `google-auth[requests]==2.62.2` to `requirements-dev.txt`. Not proposed: OAM-5's scope names no dependency or build change (`Plan.md:203-215`), and the Google provider's libraries stay undeclared. If you want this alternative, the plan must be revised to add that line.
- **N5D-4 Outbound HTTP clients.**
  - Each call creates its own `httpx.AsyncClient`.
  - Sample fetch: `timeout=None, trust_env=False`. The voice service is local, so no proxy applies. The contract sets no limit on this fetch (`API-Contract.md:296`, `:320`).
  - Chatterbox call: `timeout=None, follow_redirects=False` (redirects not followed, `:327`), and the default `trust_env`, so the machine's proxy and CA settings apply to the outbound HTTPS call. The only bound is `asyncio.wait_for(client.send(request), timeout=limit)`. It runs from sending the request to reading the complete body, because `send` without `stream=True` reads the body (`:328`).
  - Alternatives:
    - (a) `httpx.AsyncClient(timeout=limit)`. Rejected: httpx applies its timeout per connect, read and write operation, not to the whole call, so a slow response could exceed the limit.
    - (b) One shared client. Rejected: `app = create_app()` runs at import (`application.py:623`), so the client would be created at import and never closed.
- **N5D-5 Waiting: one `asyncio.Lock` on `InferenceState`, for every provider.**
  - The route enters it after checks 1–4, so rejected requests do not wait (`API-Contract.md:308`).
  - The OAF checks run inside it (`:291-292`), so waiting does not count toward the time limit, which starts at `wait_for` (`:309`).
  - The lock is created in `__init__`, which also runs at import (`application.py:623`). In Python 3.10 and later, `asyncio.Lock()` binds to no event loop until it is contended.
  - Alternative: a `threading.Lock`. Rejected: it would block the event loop, so rejected requests could not be answered during a generation, which the OAM-4 waiting test checks.
- **N5D-6 Reading the returned WAV.**
  - `wav_duration` reads the RIFF/WAVE chunks itself. A readable WAV has a `fmt ` chunk of at least 16 bytes, with a non-zero sample rate and block alignment, before a `data` chunk. Frames are `min(declared data size, bytes present) // block_align`.
  - Reason: the deployed Chatterbox writes float32 audio with torchaudio (`abbe387:voice_narration/chatterbox_api/application.py:65-73`), and the standard `wave` module rejects IEEE-float WAV. In the dry run it raised `unknown format: 3` on a float WAV, which `wav_duration` read as 1.5 s.
  - That the deployed service's WAV uses format tag 3 or the extensible tag is a hypothesis. The reader accepts any format tag.
  - Alternatives:
    - (a) The `wave` module. Rejected, as shown above.
    - (b) Reject a `data` chunk whose declared size exceeds the bytes received, as not audio. Not chosen: the contract requires only "a readable WAV file" (`:329`), and the bytes present are still playable.
- **N5D-7 OAC-9 needs no new code.**
  - The result is the answer to the same request (carried over). In the dry run, a client gave up after 0.5 s during a 2 s generation. The generation still completed, with the lock in place, and its history entry read `complete` afterwards.
  - The cause is uvicorn's `send`, which returns without error once the client has disconnected (`h11_impl.py:459-460`), so the route runs to the end.
  - This was observed for a startup-provider generation. That it holds the same way for a Chatterbox generation, which goes through the same route, is a hypothesis checked at OAM-8.
- **N5D-8 Failure answers carry only the contract text.** No exception text, token, key path or sample byte appears in an OAF answer. Nothing new is printed or logged, because observability is not required (requirements Operational Characteristics). The existing `print` calls in `submit_for_inference` are unchanged and do not run for Chatterbox generations.

### Contract Rule Coverage

| Contract rule (`API-Contract.md`) | Code | Verified by |
| --- | --- | --- |
| `provider` absent, `null`, `""`, `"google"` → startup provider; `language` ignored otherwise (`:279-283`) | `unsupported_choice_error`; route `else` branch | OAM-4 `test_each_generation_uses_the_provider_it_names` |
| Failure 3 and failure 4, after check 2 (`:286-290`) | `unsupported_choice_error`, called after check 2 | OAM-4 rejection tests (12) |
| Waiting after checks 1–4, for every provider (`:291`, `:306-308`) | `generation_lock` around both branches | OAM-4 waiting test |
| OAF-1, OAF-2 (`:338-339`, `:473-474`) | `ChatterboxClient.generate`, `parse_time_limit`, `trimmed_url` | OAM-4 pre-call tests |
| Step 2 and OAF-3: `GET <voice service URL>/voices/<voice_id>/sample`; only a non-empty `200` (`:320`, `:340`, `:476`) | `_fetch_sample` | OAM-4 pre-call tests (unknown, preloaded, deleted, unreachable, padded URL) |
| Step 3 and OAF-4: token for the key's service account, audience equal to the Chatterbox URL in effect (`:321`, `:341`, `:475`) | `service_account_identity_token`, `_obtain_identity_token` | Failure cases: OAM-4 pre-call tests. A token actually issued, and its audience: OAM-8 only (COA-16) |
| Step 4: `POST <url>/v1/synthesize`, multipart `text` (whole), `language`, `sample_audio`, `Authorization: Bearer`, no redirects (`:322-327`) | `_synthesize` | OAM-8 only (COA-16) |
| Time limit, from sending to the complete response; OAF-5 with `<N>` (`:328`, `:342`) | `_synthesize`, `asyncio.wait_for` | OAM-8 only |
| OAF-6 for any transport failure (`:343`) | `_synthesize`, `except (httpx.RequestError, httpx.InvalidURL)` | OAM-8 only. Dry-run scratch check: port 0 gave the OAF-6 message |
| OAF-7 (`401`, `403`), OAF-8 (any other status but `200`, redirects included) (`:344-345`) | `_read_audio` | OAM-8 only |
| Success and OAF-9: `audio/wav`, case-insensitive with parameters ignored; non-empty readable WAV; `duration_seconds` = frames / rate (`:329`, `:346`) | `_read_audio`, `wav_duration` | OAM-8 only. Dry-run scratch check of `wav_duration` on PCM, float and bad bytes |
| A Chatterbox success is saved like any other generation: history, download, output, 30-day database expiry (`:298`, OAC-11) | `submit_for_cloning` → `_store_output` → `persist_generation` (unchanged) | OAM-8 only (COA-10) |
| No fallback; a failure saves nothing and leaves an existing entry unchanged (`:297`, `:300`) | `ChatterboxFailure` raised before `_store_output`; route → `503` | OAM-4 pre-call tests. Call-time causes: OAM-8 |
| Provider list adds `chatterbox`, always, in name order (`:449-454`) | `list_backends` | OAM-4 provider-list test |
| Settings read at `create_app` (`:469`) | `InferenceState.__init__` | OAM-4 tests (settings set before `create_app`); command 6 shows the defaults in force |
| Result on the same request; a client that leaves does not cancel the generation (`:296`, OAC-9) | No change (N5D-7) | Dry-run scratch check; OAM-8 |

## Proposed Code / Tests

### `voice_narration/inference/chatterbox.py` (new file, complete content)

```python
"""Voice cloning through the deployed Chatterbox service.

Contract: docs/.ai/chatterbox-original-app/API-Contract.md, Inference Service Chatterbox
Call, Chatterbox Failure Causes (OAF-1 to OAF-9) and Inference Service Settings.
"""

from __future__ import annotations

import asyncio
import json
import os
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import quote

import httpx

CLOSING = "Please retry, or choose another provider."
NOT_CONFIGURED = f"Chatterbox voice cloning is not configured. {CLOSING}"
INVALID_TIME_LIMIT = (
    "The Chatterbox time limit setting CHATTERBOX_TIMEOUT_SECONDS is invalid; "
    f"it must be a positive whole number of seconds. {CLOSING}"
)
SAMPLE_UNREADABLE = f"The voice sample for the selected voice could not be read. {CLOSING}"
TOKEN_UNAVAILABLE = f"Could not obtain an identity token for Chatterbox. {CLOSING}"
TIMED_OUT = "Chatterbox did not respond within {seconds} seconds. " + CLOSING
CANNOT_CONNECT = f"Could not connect to Chatterbox. {CLOSING}"
ACCESS_DENIED = "Access to Chatterbox was denied (HTTP {status}). " + CLOSING
SERVICE_ERROR = "Chatterbox returned an error (HTTP {status}). " + CLOSING
NOT_AUDIO = f"Chatterbox returned a response that is not audio. {CLOSING}"

DESCRIPTION = "Chatterbox voice cloning (deployed Cloud Run service)"
LANGUAGES = ("en", "hi")
DEFAULT_TIME_LIMIT_SECONDS = 1200
DEFAULT_VOICE_SERVICE_URL = "http://localhost:8002"


class ChatterboxFailure(Exception):
    """A Chatterbox generation failed; the message is the contract's text for its cause."""


def trimmed_url(value: Optional[str]) -> str:
    """The URL in effect: surrounding whitespace and trailing slashes removed."""
    return (value or "").strip().rstrip("/")


def parse_time_limit(value: Optional[str]) -> Optional[int]:
    """Seconds from CHATTERBOX_TIMEOUT_SECONDS: 1200 when absent or blank, None when invalid."""
    text = (value or "").strip()
    if not text:
        return DEFAULT_TIME_LIMIT_SECONDS
    if text.isascii() and text.isdigit() and int(text) >= 1:
        return int(text)
    return None


@dataclass(frozen=True)
class ChatterboxSettings:
    url: str
    time_limit: Optional[int]
    voice_service_url: str
    credentials_path: str

    @classmethod
    def from_environment(cls) -> "ChatterboxSettings":
        return cls(
            url=trimmed_url(os.getenv("CHATTERBOX_URL")),
            time_limit=parse_time_limit(os.getenv("CHATTERBOX_TIMEOUT_SECONDS")),
            voice_service_url=trimmed_url(os.getenv("VOICE_SERVICE_URL")) or DEFAULT_VOICE_SERVICE_URL,
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or "",
        )


def service_account_identity_token(credentials_path: str, audience: str) -> str:
    """A Google-signed identity token for the service account whose key file is credentials_path.

    Only a service-account key file is used. google-auth's fetch_id_token is not used,
    because it falls back to the metadata server when the key is absent or of another type.
    google-auth is imported here, as the Google provider imports its client library, so the
    inference service starts without it; its absence then means no token (OAF-4).
    """
    if not credentials_path.strip():
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is not set")
    info = json.loads(Path(credentials_path).read_text(encoding="utf-8"))
    if not isinstance(info, dict) or info.get("type") != "service_account":
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS does not name a service-account key")

    from google.auth.transport.requests import Request
    from google.oauth2 import service_account

    credentials = service_account.IDTokenCredentials.from_service_account_info(info, target_audience=audience)
    credentials.refresh(Request())
    return credentials.token


def wav_duration(audio: bytes) -> float:
    """Sample frames divided by sample rate, read from the RIFF chunks of a WAV file.

    The chunks are read directly because Chatterbox returns IEEE-float WAV, which the
    standard wave module rejects. Raises ValueError when the bytes are not a readable WAV file.
    """
    if len(audio) < 12 or audio[:4] != b"RIFF" or audio[8:12] != b"WAVE":
        raise ValueError("not a RIFF/WAVE file")
    sample_rate = block_align = 0
    offset = 12
    while offset + 8 <= len(audio):
        chunk_id = audio[offset:offset + 4]
        (size,) = struct.unpack_from("<I", audio, offset + 4)
        start = offset + 8
        if chunk_id == b"fmt ":
            if size < 16 or start + 16 > len(audio):
                raise ValueError("truncated fmt chunk")
            _, _, sample_rate, _, block_align = struct.unpack_from("<HHIIH", audio, start)
        elif chunk_id == b"data":
            if not sample_rate or not block_align:
                raise ValueError("no usable fmt chunk before the data chunk")
            return (min(size, len(audio) - start) // block_align) / sample_rate
        offset = start + size + (size % 2)
    raise ValueError("no data chunk")


class ChatterboxClient:
    """Produces a cloned generation from the deployed Chatterbox, or raises ChatterboxFailure."""

    def __init__(self, settings: ChatterboxSettings):
        self.settings = settings

    async def generate(self, script: str, voice_id: str, language: str) -> dict:
        if not self.settings.url:
            raise ChatterboxFailure(NOT_CONFIGURED)
        if self.settings.time_limit is None:
            raise ChatterboxFailure(INVALID_TIME_LIMIT)
        sample = await self._fetch_sample(voice_id)
        token = await self._obtain_identity_token()
        response = await self._synthesize(script, language, sample, token)
        audio = self._read_audio(response)
        try:
            seconds = wav_duration(audio)
        except ValueError:
            raise ChatterboxFailure(NOT_AUDIO) from None
        return {"output_seconds": seconds, "audio_bytes": audio, "format": "wav"}

    async def _fetch_sample(self, voice_id: str) -> bytes:
        url = f"{self.settings.voice_service_url}/voices/{quote(voice_id, safe='')}/sample"
        try:
            # The voice service is local; no proxy applies. The contract sets no limit on this fetch.
            async with httpx.AsyncClient(timeout=None, trust_env=False) as client:
                response = await client.get(url)
        except (httpx.RequestError, httpx.InvalidURL):
            raise ChatterboxFailure(SAMPLE_UNREADABLE) from None
        if response.status_code != 200 or not response.content:
            raise ChatterboxFailure(SAMPLE_UNREADABLE)
        return response.content

    async def _obtain_identity_token(self) -> str:
        try:
            return await asyncio.to_thread(
                service_account_identity_token, self.settings.credentials_path, self.settings.url
            )
        except Exception:
            # Every way of not getting a token is the one cause OAF-4.
            raise ChatterboxFailure(TOKEN_UNAVAILABLE) from None

    async def _synthesize(self, script: str, language: str, sample: bytes, token: str) -> httpx.Response:
        limit = self.settings.time_limit
        try:
            # httpx applies no limit of its own; the one bound is the time limit, from sending to the full response.
            async with httpx.AsyncClient(timeout=None, follow_redirects=False) as client:
                request = client.build_request(
                    "POST",
                    f"{self.settings.url}/v1/synthesize",
                    data={"text": script, "language": language},
                    files={"sample_audio": ("sample", sample, "application/octet-stream")},
                    headers={"Authorization": f"Bearer {token}"},
                )
                return await asyncio.wait_for(client.send(request), timeout=limit)
        except asyncio.TimeoutError:
            raise ChatterboxFailure(TIMED_OUT.format(seconds=limit)) from None
        except (httpx.RequestError, httpx.InvalidURL):
            raise ChatterboxFailure(CANNOT_CONNECT) from None

    @staticmethod
    def _read_audio(response: httpx.Response) -> bytes:
        status = response.status_code
        if status in (401, 403):
            raise ChatterboxFailure(ACCESS_DENIED.format(status=status))
        if status != 200:
            raise ChatterboxFailure(SERVICE_ERROR.format(status=status))
        media_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
        if media_type != "audio/wav" or not response.content:
            raise ChatterboxFailure(NOT_AUDIO)
        return response.content
```

### `voice_narration/inference/application.py` (unified diff against HEAD `598d9eb`)

```diff
diff --git a/voice_narration/inference/application.py b/voice_narration/inference/application.py
index 0e801e3..e6daad5 100644
--- a/voice_narration/inference/application.py
+++ b/voice_narration/inference/application.py
@@ -8,6 +8,7 @@ M020: Mock Inference Adapter GREEN
 M022: Approved Model Test Prerequisites (provider registry)
 """
 
+import asyncio
 import json
 import os
 import uuid
@@ -19,12 +20,27 @@ from fastapi import FastAPI, Request, Depends, Response
 from fastapi.responses import JSONResponse
 from fastapi.middleware.cors import CORSMiddleware
 
+from .chatterbox import DESCRIPTION as CHATTERBOX_DESCRIPTION
+from .chatterbox import LANGUAGES as CHATTERBOX_LANGUAGES
+from .chatterbox import ChatterboxClient, ChatterboxFailure, ChatterboxSettings
 from .db import SessionLocal, create_all_tables
 from .models import Generation, Voice
 from .providers import InferenceProvider, MockInferenceProvider
 from .registry import ProviderRegistry
 from .storage import AudioStorage
 
+UNSUPPORTED_PROVIDER = "Unsupported provider. Choose google or chatterbox."
+UNSUPPORTED_LANGUAGE = "language must be en or hi for a chatterbox generation."
+
+
+def unsupported_choice_error(provider, language) -> Optional[str]:
+    """The 400 error for an unsupported provider, or for a Chatterbox language other than en or hi."""
+    if provider not in (None, "", "google", "chatterbox"):
+        return UNSUPPORTED_PROVIDER
+    if provider == "chatterbox" and language not in CHATTERBOX_LANGUAGES:
+        return UNSUPPORTED_LANGUAGE
+    return None
+
 
 def get_default_provider_name() -> str:
     """
@@ -81,6 +97,9 @@ class InferenceState:
             job_repository: Job repository for persistence
         """
         self.provider = provider
+        self.chatterbox = ChatterboxClient(ChatterboxSettings.from_environment())
+        # One generation at a time, for every provider; a request that arrives during one waits.
+        self.generation_lock = asyncio.Lock()
         self.jobs_app = jobs_app
         self.job_repository = job_repository
         self._pending_inferences = {}
@@ -293,6 +312,14 @@ class InferenceState:
         
         print(f"[TTS] Generated audio: {len(output.get('audio_bytes', b''))} bytes, {output['output_seconds']:.2f} seconds")
 
+        return self._store_output(job_id, script, voice_id, output)
+
+    async def submit_for_cloning(self, job_id: str, script: str, voice_id: str, language: str) -> dict:
+        """Generate with the deployed Chatterbox; ChatterboxFailure leaves nothing stored."""
+        output = await self.chatterbox.generate(script, voice_id, language)
+        return self._store_output(job_id, script, voice_id, output)
+
+    def _store_output(self, job_id: str, script: str, voice_id: str, output: dict) -> dict:
         # Store the output for later retrieval
         self._pending_inferences[job_id] = output
         self.persist_generation(job_id, script, voice_id, output)
@@ -370,7 +397,12 @@ class InferenceState:
             except Exception:
                 pass
 
-        return backends
+        backends.append({
+            "name": "chatterbox",
+            "provider_class": ChatterboxClient.__name__,
+            "description": CHATTERBOX_DESCRIPTION,
+        })
+        return sorted(backends, key=lambda backend: backend["name"])
 
     async def run_pending(self) -> int:
         """
@@ -447,7 +479,9 @@ def create_app(
         Request body JSON:
         {
             "script": "Text to synthesize",
-            "voice_id": "voice-identifier"
+            "voice_id": "voice-identifier",
+            "provider": "google" | "chatterbox" (optional),
+            "language": "en" | "hi" (required for chatterbox)
         }
 
         Returns:
@@ -461,15 +495,26 @@ def create_app(
             body = await request.json()
             script = body.get("script")
             voice_id = body.get("voice_id")
+            provider = body.get("provider")
+            language = body.get("language")
 
             if not script or not voice_id:
                 return JSONResponse(
                     content={"error": "Missing required fields: script, voice_id"},
                     status_code=400,
                 )
+            choice_error = unsupported_choice_error(provider, language)
+            if choice_error:
+                return JSONResponse(content={"error": choice_error}, status_code=400)
 
-            result = await state.submit_for_inference(job_id, script, voice_id)
+            async with state.generation_lock:
+                if provider == "chatterbox":
+                    result = await state.submit_for_cloning(job_id, script, voice_id, language)
+                else:
+                    result = await state.submit_for_inference(job_id, script, voice_id)
             return JSONResponse(content=result, status_code=200)
+        except ChatterboxFailure as e:
+            return JSONResponse(content={"error": str(e)}, status_code=503)
         except ValueError as e:
             return JSONResponse(content={"error": str(e)}, status_code=400)
         except Exception as e:
```

## Execution Steps

1. Confirm that this plan's Human Review status records approval. Confirm that `git status --short` prints nothing outside `docs/.ai/chatterbox-original-app/`, that `git diff --stat 598d9eb HEAD -- voice_narration tests requirements-dev.txt .gitignore` prints nothing, and that no `.env`, `.env.local` or `.env.production` exists. If any check fails, stop and report.
2. Create `voice_narration/inference/chatterbox.py` with exactly the content of the first code block above (plan lines 186–379), with LF line endings: `sed -n '186,379p' docs/.ai/chatterbox-original-app/005_Implementation_Plan_OAM-5.md | tr -d '\r' > voice_narration/inference/chatterbox.py`.
3. Extract the diff block (plan lines 385–502): `sed -n '385,502p' docs/.ai/chatterbox-original-app/005_Implementation_Plan_OAM-5.md | tr -d '\r' > "$TEMP/oam5-application.diff"`. Its `sha256sum` must print `6284d9e818104c9a597f183f23ad19a511606e320e7e864c72289b5ebe9c928e`; if it does not, stop and report. Then run `git apply --check "$TEMP/oam5-application.diff"`, and only if that succeeds, `git apply "$TEMP/oam5-application.diff"`.
4. Run the commands under Verification in order, writing each log to `$TEMP`, outside the repository. Do not start, stop or check the Docker engine, run no `gcloud` command (CON-2), create no `.env` or key file, and call no Chatterbox.
5. Record the evidence in `Plan.md` Execution Status for OAM-5, and update this plan's Human Review status.

## Acceptance / Completion Criteria

- **N5C-1** The repository changes are exactly these two:
  - `voice_narration/inference/chatterbox.py` is created; with CR removed, its SHA-256 is `0f9119817868c690295ceeeb11c0148b6436d1e94864c3ee96f9db7c2e3eedb9`;
  - `voice_narration/inference/application.py` is changed by the diff above; with CR removed, its SHA-256 is `d18e1b430e965472c3d6dce90795ded0de5d1456b9c4ca7ab82bbe1fc9489532`.

  No other file changes, including tests, `requirements-dev.txt`, `.env.example` and `audio_storage/`. This excludes the OAM-5 Execution Status update in `Plan.md` and this plan's Human Review status.
- **N5C-2** The OAM-4 file, unchanged, reports `36 passed`, with 0 failed and 0 errors (command 2).
- **N5C-3** A second run of the OAM-4 file, with no cleanup between runs, again reports `36 passed`, 0 failed, 0 errors (command 3). Those tests override settings and write under `tmp_path`. They assert the storage root and the database refusal in force (Repeatable, Isolated Verification).
- **N5C-4** After commands 2–3, `git status --short -- audio_storage` prints nothing, and no `voice_storage/` folder exists.
- **N5C-5** The backend suite (OAV-2, without the three V3Q-3 files) collects 118 tests, none from the ignored files, with no collection error and no interruption. The only `FAILED` or `ERROR` line is `tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing` (V3Q-1 (a)). The 29 preserved tests (`Plan.md:193`) are among those that pass. Any other failing or erroring test fails the milestone. It is not rerun, skipped or weakened.
- **N5C-6** After the suite, OAV-3 holds: anything the suite wrote under `audio_storage/` is recorded and restored, and `git status --short -- audio_storage` then prints nothing.
- **N5C-7** With the four Chatterbox settings unset, the settings in force are `url=''`, `time_limit=1200`, `voice_service_url='http://localhost:8002'` and `credentials_path=''` (command 6, COA-9 default).
- **N5C-8** No test was added or changed (COA-16). `chatterbox.py` and `application.py` contain no `load_dotenv` and no `fetch_id_token(` call (N4D-2). No Docker, `gcloud`, `.env` or Chatterbox call was used.
- **N5C-9** No process started by the runs is left running.

Completing OAM-5 does not claim the behavior that needs a Chatterbox call. Its evidence comes from OAM-8 (`Plan.md:216`).

## Verification

### Commands

Run from the repository root in Git Bash. `$TEMP` is outside the repository.

1. `python -m compileall -q voice_narration/inference && echo compiled; tr -d '\r' < voice_narration/inference/chatterbox.py | sha256sum; tr -d '\r' < voice_narration/inference/application.py | sha256sum`
2. `python -m pytest tests/test_inference_provider_choice_red.py -q > "$TEMP/oam5-green-run1.log" 2>&1; tail -1 "$TEMP/oam5-green-run1.log"; grep -cE "^(FAILED|ERROR) " "$TEMP/oam5-green-run1.log"` (OAV-1)
3. The same as command 2, with `run2` in place of `run1` (the second run, with no cleanup).
4. `git status --short -- audio_storage; test ! -e voice_storage && echo absent`
5. Backend suite and the V3Q-1 (a) check (OAV-2; run in the background with a completion notice):
   - 5a. `printf '%s\n' 'tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing' > "$TEMP/oam5-accepted.txt"; wc -l < "$TEMP/oam5-accepted.txt"`
   - 5b. `python -m pytest -q --ignore=tests/test_persistence.py --ignore=tests/test_authentication_consent.py --ignore=tests/test_voice_enrollment.py > "$TEMP/oam5-full.log" 2>&1; tail -1 "$TEMP/oam5-full.log"; grep -cE "^!+ (Interrupted|KeyboardInterrupt)" "$TEMP/oam5-full.log"`
   - 5c. `grep -E "^(FAILED|ERROR) " "$TEMP/oam5-full.log" | sed -E 's/^(FAILED|ERROR) //; s/ - .*$//' | LC_ALL=C sort -u > "$TEMP/oam5-failing.txt"; echo "unexpected:"; LC_ALL=C comm -23 "$TEMP/oam5-failing.txt" "$TEMP/oam5-accepted.txt"; echo "accepted, not failing:"; LC_ALL=C comm -13 "$TEMP/oam5-failing.txt" "$TEMP/oam5-accepted.txt"; grep -E "^(FAILED|ERROR) " "$TEMP/oam5-full.log"`
   - 5d. `python -m pytest --collect-only -q -p no:cacheprovider --ignore=tests/test_persistence.py --ignore=tests/test_authentication_consent.py --ignore=tests/test_voice_enrollment.py > "$TEMP/oam5-collect.log" 2>&1; tail -1 "$TEMP/oam5-collect.log"; grep -cE "^tests/(test_persistence|test_authentication_consent|test_voice_enrollment)\.py::" "$TEMP/oam5-collect.log"`
   - 5e. `git status --short -- audio_storage`. Only if it prints anything: record it, run `git checkout -- audio_storage` and `git clean -fd -- audio_storage`, and repeat `git status --short -- audio_storage`, which must print nothing (OAV-3).
6. `env -u CHATTERBOX_URL -u CHATTERBOX_TIMEOUT_SECONDS -u VOICE_SERVICE_URL -u GOOGLE_APPLICATION_CREDENTIALS python -c "from voice_narration.inference.chatterbox import ChatterboxSettings; print(ChatterboxSettings.from_environment())" 2>&1 | tail -1`, then `git status --short -- audio_storage`, which must print nothing. (Importing the package runs `create_app()`, `application.py:623`.)
7. `grep -nE "load_dotenv|fetch_id_token\(" voice_narration/inference/chatterbox.py voice_narration/inference/application.py; echo "matches: $?"; git status --short; git diff --stat`
8. Process check: in PowerShell, `Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId, CreationDate, CommandLine`. No process from this run may remain.

### Affected Tests

Found as the tests that import `voice_narration.inference` (`grep -rln "voice_narration.inference" tests --include=*.py`), checked for what each uses:

- `tests/test_inference_provider_choice_red.py` (36): the RED evidence. It uses `create_app`, the route, the provider list and the settings this milestone changes.
- `tests/test_inference.py`, `tests/test_provider_registry.py`, `tests/test_generation_history_download.py`, `tests/test_generation_persistence_red.py`, `tests/test_generation_delete_search_red.py` (29): the preserved tests (`Plan.md:193`). They use `create_app`, `InferenceState`, `submit_for_inference`, the route and `list_backends`.
- `tests/test_real_model_inference.py`, `tests/test_linguistic_chunking_and_controls.py`: they import only `production.py` and `providers.mock`. Both still import the changed `application.py` through the package `__init__` (`voice_narration/inference/__init__.py:3`), so they are affected by import only. Dry run: `1 failed, 17 passed, 10 skipped` before and after the change, and the one failure is the accepted test.
- Every other backend test runs in command 5 (OAV-2). No test file changes.

### Expected Evidence

Expected / Predicted — Not Yet Verified:

- Command 1: `compiled`, `0f9119817868c690295ceeeb11c0148b6436d1e94864c3ee96f9db7c2e3eedb9 *-`, `d18e1b430e965472c3d6dce90795ded0de5d1456b9c4ca7ab82bbe1fc9489532 *-`.
- Commands 2 and 3: `36 passed, … in …` (dry run: 29.91 s); `0`.
- Command 4: no output, then `absent`.
- Command 5a: `1`.
- Command 5b: `1 failed, 100 passed, 17 skipped, … warnings in …` (OAM-3: `1 failed, 64 passed, 17 skipped`, `Plan.md:445`, plus the 36 OAM-4 tests), then `0`.
- Command 5c: `unexpected:` empty, `accepted, not failing:` empty. The one `FAILED` line is the accepted test, with `ImportError: cannot import name 'ProductionInferenceProvider'`.
- Command 5d: `118 tests collected …`, then `0`.
- Command 5e: predicted ` M audio_storage/generation_index.json` and `?? audio_storage/generations/<UTC date>/`, written by `tests/test_generation_history_download.py` (Plan OAR-1). After the restore, nothing.
- Command 6: `ChatterboxSettings(url='', time_limit=1200, voice_service_url='http://localhost:8002', credentials_path='')`, then no `audio_storage` change.
- Command 7: no match lines, `matches: 1`. Then ` M voice_narration/inference/application.py`, `?? voice_narration/inference/chatterbox.py`, plus `docs/.ai/chatterbox-original-app/` changes; and `1 file changed, 48 insertions(+), 3 deletions(-)`.
- Command 8: no `python.exe` from this run.

### Planning-Time Dry Run

This is a planning-time dry run, not milestone evidence. It ran on 2026-11-13 at HEAD `598d9eb`, in disposable copies under `C:/Users/avina/AppData/Local/Temp/claude/75d22e5e94aa85f8/7c785373-79e0-4451-8aab-0a1437282b97/scratchpad/oam5/`:

- `copy/`: made with `git -c core.autocrlf=false archive HEAD | tar -x`, then `git init`. The exact `chatterbox.py` above was placed in it, and the exact diff above was applied.
- `base/`: unmodified, made the same way.
- `crlf/`: a scratch repository holding the working tree's CRLF `application.py`.

The repository was not modified. Nothing fakes Chatterbox, Google's token endpoint or the voice service, and nothing contacted the deployed Chatterbox or Google.

| Step | Command (in the copy) | Result |
| --- | --- | --- |
| Compile (`copy/`) | `python -m compileall -q voice_narration/inference && echo compiled` | `compiled` |
| OAM-4 tests (`copy/`) | `python -m pytest tests/test_inference_provider_choice_red.py -q -p no:cacheprovider --tb=short` | `36 passed, 128 warnings in 29.91s`; no `FAILED` or `ERROR` line |
| Preserved tests (`copy/`) | `python -m pytest tests/test_inference.py tests/test_provider_registry.py tests/test_generation_history_download.py tests/test_generation_persistence_red.py tests/test_generation_delete_search_red.py -q -p no:cacheprovider` | `29 passed, 42 warnings in 1.37s`; then `git status --short` showed ` M audio_storage/generation_index.json` and `?? audio_storage/generations/2026-11-14/` in the copy (Plan OAR-1) |
| Affected by import (`base/` and `copy/`) | `python -m pytest tests/test_real_model_inference.py tests/test_linguistic_chunking_and_controls.py -q -p no:cacheprovider` | Both `1 failed, 17 passed, 10 skipped`; the one failure is `test_production_inference_module_missing` |
| Accepted failure on the baseline (`base/`, twice) | `python -m pytest "tests/test_real_model_inference.py::TestRealModelInferenceRED::test_production_inference_module_missing" -q -p no:cacheprovider` | `1 failed` each time, `ImportError: cannot import name 'ProductionInferenceProvider'`; the same in `copy/` |
| Collection (`copy/`) | command 5d | `118 tests collected in 1.02s` |
| Settings in force (`copy/`) | command 6 | `ChatterboxSettings(url='', time_limit=1200, voice_service_url='http://localhost:8002', credentials_path='')` |
| Static check (`copy/`) | `grep -nE "load_dotenv\|fetch_id_token\(" …; echo "matches: $?"` | `matches: 1` |
| Diff on a CRLF file (`crlf/`) | `git apply --check app.diff`, `git apply app.diff`, then `cmp` of both files with CR removed | `check-ok`, `applied`, the result keeps CRLF, `identical` |
| Hashes, and extraction from this plan | `tr -d '\r' < … \| sha256sum`; the `sed -n` commands of Execution Steps 2–3 run on this file; `git apply --check` of the extracted diff on the worktree, which changes nothing | `chatterbox.py` `0f9119817868c690295ceeeb11c0148b6436d1e94864c3ee96f9db7c2e3eedb9`; `application.py` `d18e1b430e965472c3d6dce90795ded0de5d1456b9c4ca7ab82bbe1fc9489532`; diff block `6284d9e818104c9a597f183f23ad19a511606e320e7e864c72289b5ebe9c928e` |
| Scratch checks (`probe/checks.py`, run in `copy/` under a lookup guard like N4D-2) | `python checks.py` | `wav_duration`: PCM 0.5 s → `0.5`; PyAV `pcm_f32le` WAV at 24 kHz (format tag `3`) → `1.5`, which `wave` rejects with `unknown format: 3`; `b""`, `b"not audio"`, a header with no chunks and a truncated header → `ValueError`. `parse_time_limit`: `None`, `""`, `"   "` → `1200`; `" 7 "` → `7`; `"0"`, `"-5"`, `"10.5"`, `"ten"` → `None`. `trimmed_url("  https://x.run.app//  ")` → `'https://x.run.app'`. `IDTokenCredentials.from_service_account_info` with a scratch RSA key and `target_audience`: built, audience kept, not refreshed. `_synthesize` to `http://127.0.0.1:0` (no server): the OAF-6 message. `asyncio.TimeoutError is TimeoutError` → `True`. Client gave up after 0.5 s during a 2 s generation; 3 s later `GET /inference/generations/left` → `200 complete` (N5D-7). Blocked lookups: `[]` |

Corrections from the dry run, made before this plan was written:

- The first scripted edit read `application.py` with the platform's default encoding, which corrupted the en dash in its docstring (line 2). The edit was redone in UTF-8, and the diff above no longer touches line 2.
- `follow_redirects=False` was made explicit in `_synthesize`. It is httpx's default, and the explicit setting records the contract rule (`API-Contract.md:327`).

Created during planning, all under the scratchpad's `oam5/` folder: `copy/`, `base/`, `crlf/`, `probe/checks.py`, `app.diff`, `plan_skeleton.md`, `x_cb.py` and `x.diff` (the blocks extracted from this plan with Execution Steps 2–3), and the logs `green1.log`, `preserved.log`, `accepted.log`, `base-accepted1.log`, `base-accepted2.log`, `base-import.log`, `copy-import.log` and `collect.log`. Also the scratchpad file `refc.md`, the reference contract extracted with `git show`. All of them are deleted once this plan is written. Pytest temporary directories went under the system pytest temp root. The scratchpad files `oam45.md`, `oam8.md`, `ref-contract.md` and `trace.md` predate this run and were left untouched.

## Risks

- **N5R-1 The call-time behavior has no automated test (Plan OAR-9, COA-16).** That covers `_synthesize`, `_read_audio`, the token refresh, the time limit and saving a cloned clip, reviewed here as exact code under Contract Rule Coverage. A defect shows only at OAM-8, and a later regression would not be caught automatically. The scratch checks above exercised only `wav_duration`, the settings parsers, building the token credentials and the port-0 mapping.
- **N5R-2 Blocking the event loop** (python-fastapi "Do not block the async event loop", Medium, justified). Creating each `httpx.AsyncClient` loads CA certificates synchronously. A synchronous client took 0.3–0.6 s in the OAM-4 planning (N4D-7); that the asynchronous one costs the same is a hypothesis. `persist_generation`'s file I/O is synchronous, as before. Justification: generations already run one at a time (N5D-5), the service is a single local instance (requirements Operational Characteristics), and the contract makes no statement about other operations during a generation (`API-Contract.md:310`).
- **N5R-3 google-auth limits its token request to 120 s** (`google/auth/transport/requests.py:49`). A token request that exceeds it fails, which is OAF-4. The contract states no limit for this step other than not counting it toward the Chatterbox limit (`API-Contract.md:296`, `:321`). This is the library's own bound, not a setting. It is listed for your review.
- **N5R-4 Authentication and identity (CON-5; `security`).**
  - The inference service makes no identity, role or ownership comparison. It does not check which account the key belongs to: a key for another account is rejected by Cloud Run, which is OAF-7 (`API-Contract.md:321`). It authenticates no caller (`:58`).
  - The token audience is the Chatterbox URL in effect, the same trimmed string used as the call's base URL (`trimmed_url`). The CON-5 URL has no trailing slash, so the audience equals it exactly.
  - The token is sent only in the `Authorization` header of the Chatterbox call, and is never printed, saved or put in an answer.
  - The key file is read once per generation and not copied. The sample is sent only to the configured `CHATTERBOX_URL`. TLS verification is httpx's default (on).
  - `voice_id` is percent-encoded with `quote(…, safe='')`, so it cannot reach a different voice-service path.
- **N5R-5 Long requests (Plan OAR-3).** A generation may hold its request open for the wait plus up to 1200 s, plus the sample fetch and the token request. If the browser gives up, the generation still completes and is saved (N5D-7). OAM-8 exercises real cold starts.
- **N5R-6 One lock across event loops.** The preserved tests use `TestClient` without a context manager, which may run each request on a new event loop. An uncontended `asyncio.Lock` binds to no loop, and the preserved tests passed in the dry run. A contended lock binds to the loop it waits on. That only happens under uvicorn's single loop, as in the OAM-4 waiting test.
- **N5R-7 No outside lookup on the pre-call paths (N4D-2, Plan OAR-8).**
  - OAF-1 and OAF-2 are answered before any I/O.
  - The OAF-3 fetch goes only to `VOICE_SERVICE_URL`, which is loopback in the OAM-4 tests.
  - For every OAM-4 OAF-4 case, the token function raises before importing google-auth or opening a connection.
  - No code loads `.env` again (command 7). The OAM-4 guard recorded no lookup in the dry run.
- **N5R-8 Size** (code-quality SZ1, Medium, justified). `application.py` grows from 623 to 668 lines. It was already above 400 before this milestone. The new behavior is in `chatterbox.py` (194 lines), and `application.py` gains only the HTTP mapping, the waiting and the listing.
- **N5R-9 The three V3Q-3 files are not run (Plan OAR-10).** None of them references `voice_narration.inference` (`Plan.md:49`).

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Run `git apply -R "$TEMP/oam5-application.diff"`; if that file is gone, extract it again with Execution Step 3. Then delete `voice_narration/inference/chatterbox.py`. Nothing else is changed.

## Explicitly Out of Scope

- Any test change or new test, including any test that fakes, stands in for or calls Chatterbox or Google's token endpoint (COA-16, `Plan.md:215`).
- Changes to the mock, Google or Azure providers, the provider registry or their tests (COA-14).
- A Google fallback, duplicate prevention, text splitting or a text limit (COA-8, COA-13, COA-17).
- Changing the deployed Chatterbox, copying its source, Docker and `gcloud` (CON-2, CON-3, Explicit Exclusions).
- Logging or metrics (observability not required).
- Voice-service and TTS-page changes (OAM-3, OAM-7).
- Dependency declarations (N5D-3), `.env.example` and launcher changes, and creating a `.env` or key file (CON-6).
- Deleting generations when their expiry passes (`API-Contract.md:66`).
- Changes to tracked `audio_storage/` files.

## Human Review

Status: Executed 2026-11-13 — GREEN verified; see `Plan.md`, OAM-5 GREEN evidence. (Approved by Avinash Srivastava on 2026-11-13, as written, including decisions N5D-1 to N5D-8; google-auth and requests stay undeclared, N5D-3.)
