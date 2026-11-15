# Job quota and budget period accounting — proposal

## Human Review

Status: **Policy decision approved by avinash2196 on 2026-10-27 (America/Chicago), recorded 2026-10-28T02:54:15Z.** The user approved this exact recommended package in the main conversation. This is authority to capture the decision through the requirements/Plan/contract review sequence, not approval of those revised artifacts or an Implementation Plan. No production, test, configuration, requirements, Plan or contract change is applied by this document. This planning task has not created or finalised a Job Orchestration RED implementation plan while these decisions remain unresolved. Separately appearing unreviewed prototypes are recorded below and are not adopted as authority.

## Why this decision is needed now

The approved contract already specifies maximum-effective-output reservations, UTC epoch-aligned quota windows, a UTC-month budget, one durable settlement, six-place USD arithmetic, and the exact monthly forecast formula. It does not explicitly assign usage when an accepted job crosses a quota/month boundary, define whether `Usage` money fields cover its quota window or the budget month, or define how an unmeasured terminal job releases concurrency without inventing a zero cost. Tests would otherwise select externally visible accounting behavior on the user's behalf.

Repository inspection confirms that Policy currently has retention persistence and Jobs has generic private history persistence; neither implements generation accounting. There is no existing behavior that resolves these questions. Delivered enrollment and all 97 passing regressions remain constraints, not a source of new accounting rules.

## Existing rules retained

- `default_user_quota` is the default policy. A full per-user `Quota` override replaces it, including `window_seconds`. The current Configuration has no separate `system_quota` or system quota window. Existing system concurrency, configured/model output limits and budget bounds still apply; no new field or comparison of raw limits across different periods is proposed.
- Quota/rate/concurrency admission limits apply at submission. Lowering an admission quota does not invent retroactive selection or cancellation of accepted jobs. Existing consent/model fences, absolute output bound, deadlines and ongoing hard budget/kill-switch safety remain.
- Authenticated public requests count, including replay/polling requests. Internal service callbacks do not recursively count as public requests. Replay does not duplicate accepted-job, audio reservation, execution or accounting. Common rate-limit protection remains applicable.
- A reservation holds the maximum effective allowed audio duration, not a script-duration guess. Estimates come from approved model evidence through an explicit trusted collaborator; missing evidence fails closed. No tariff, free execution or actual provider price is invented here.
- Public snapshots, original idempotent Acceptance, job deadlines and retry bounds remain as currently contracted. No production model, natural-voice calibration, always-on GPU or paid provisioning is authorized.

## Recommended coherent policy

### 1. Quantity quotas follow the job's admission time

Use the durable original `Acceptance.created_at` as the accepted job's quota accounting time. Authenticated request counts use each request's authenticated receipt time. With selected quota width `W`, the current interval is `[floor(now/W)*W, floor(now/W)*W + W)` in UTC.

`Usage.window_start` and `reset_at` describe that selected quota interval. `accepted_jobs`, `requests`, `reserved_audio_seconds` and `consumed_audio_seconds` project the corresponding admission/request facts inside that interval. A completed job's measured audio replaces its maximum audio reservation at its original admission time, even if completion arrives in another interval. Cancellation/failure releases unused audio reservation; it does not fabricate successful consumed audio. Replays never add another accepted-job or reservation fact.

`active_jobs` counts all unfinished accepted jobs for the user, across quota intervals. System concurrency likewise includes all unfinished accepted jobs across users and periods. Thus a window boundary does not free concurrency for a job that is still running.

A changed default or override, including a changed `window_seconds`, selects a new current interval and recomputes admission/request projections from the original facts. It does not reset counters, erase old reservations or rewrite job history. Already accepted jobs retain their admission-time limits; future requests are tested against the newly selected policy and existing independent hard-safety rules.

Example: a job accepted at `00:00:59Z` under a 60-second quota and completed at `00:01:02Z` charges its accepted count and final audio to the interval beginning `00:00:00Z`. It consumes concurrency until terminal. The next interval can admit new work only under its quantity limits, live concurrency and budget checks.

### 2. Money follows the current UTC budget month

Define `Usage.estimated_usd` as the sum of outstanding estimated budget holds, including holds carried from earlier months. Define `Usage.measured_cost` as the aggregate known costs first durably recognised by Policy during the current UTC month. These money fields use the budget month; the `window_start`/`reset_at` fields continue to describe the quantity quota interval. This mixed-period distinction must be documented explicitly in the contract and later UI labels.

The immutable per-job `estimated_cost_usd` and original reported `Cost.measured_at` remain job metadata. The latter is the time the authorised source actually measured that cost; it is preserved as evidence and is not rewritten to the callback receipt time. The separate recognition time is Policy's trusted clock at first durable acceptance of that settlement. This defines application budget accounting and prevents a late or backdated report from silently removing current exposure. The aggregate `Usage.measured_cost.measured_at` is the time that aggregate is observed. With no known costs for the current month, a measured aggregate of zero represents an empty ledger, not a fabricated measurement for an unmeasured job. No new timestamp-validation rule or caller-selectable period field is proposed here.

At a UTC-month boundary, monthly spend selects the new month's projection, but every unresolved estimated hold remains effective exactly once in the new month's budget exposure. A boundary never makes accepted unfinished or unmeasured work free. Budget exposure remains current-month known cost plus all outstanding estimated holds. Existing stop/kill-switch admission and ongoing safety rules still apply.

When a known settlement is first accepted, remove its outstanding hold once and recognise its actual compute/storage cost in that acceptance's UTC month. A late report is recognised when first durably received, while the original `Cost.measured_at` remains unchanged. Identical duplicate/replayed reports do not add charges, release another hold, move an already recognised cost to another month or duplicate forecast alerts. Conflicting final cost payloads retain the existing conflict behavior.

Forecast remains the already approved formula: current-month measured spend multiplied by UTC-month duration divided by elapsed month duration (at the start, measured spend). Outstanding estimates are budget protection, not measured spend for that forecast.

Example: a January job still holding an estimate of `0.200000` when February starts contributes that hold to February's protection. Its actual `0.120000` report first accepted in February removes the hold and adds `0.120000` to February recognised spend once. A January `Cost.measured_at` remains January in the per-job evidence. Repeating that report in March does not charge March. An alternative measurement-month attribution would require explicit late-arrival/historical-budget rules; it is not silently assumed.

### 3. Unknown terminal cost is explicit, never zero

A failed/cancelled/deadline-expired job must be able to stop occupying concurrency and unused audio while its actual incurred cost is not yet known. Keep `Job.measured_cost = null` until a trusted measurement exists. Retain that job's estimated budget hold across month boundaries until reconciliation, and fail closed when accounting/protection is unavailable.

Recommended narrow internal contract amendments:

| Existing operation | Proposed input change / semantics |
| --- | --- |
| Jobs `POST /jobs/{job_id}/fail` | `cost: Cost-or-null`; null explicitly means measurement is unavailable. Failure/deadline must not be kept indefinitely unfinished merely to manufacture a Cost. |
| Policy `POST /quotas/reserve` | Add required `command_id: ID`. Preserve one reservation per owner/job even across different command IDs. An identical semantic reservation reuses it; changed bound/estimate for the bound job conflicts. |
| Policy `POST /quotas/commit-usage` | Add required `command_id: ID`. Known Cost and actual successful duration remain required; matching repeats never settle or charge again, including a new command ID carrying the same settlement. A different known Cost or measured duration for the already settled reservation conflicts. |
| Policy `POST /quotas/release-reservation` | Add required `command_id: ID` and allow `cost: Cost-or-null`; null releases unfinished-job concurrency and unused audio, but retains the estimated money hold. All three Policy mutations currently omit `command_id` despite the generic internal command rule; these are explicit consistent schema amendments. Queries do not gain command IDs. |
| Policy same release operation with later known Cost | Permit one null-to-known reconciliation for the same owner/reservation/job, using a **fresh command_id**. It replaces the hold with one actual cost without releasing quantity/concurrency twice. A repeated command ID requires the original semantic payload and returns its original result; changing its cost still conflicts. A new command with an identical already-known final Cost is a no-charge semantic repeat; a different known final Cost conflicts. Null replay never downgrades known settlement or restores a released hold. |

Successful completion and `commit-usage` continue to require known Cost, available output and the durable terminal winner. Ordinary command-ID payload conflicts remain; reusing a Jobs failure command ID with a different payload is not the late-cost reporting mechanism. After a job is terminal, or its history/profile/consent content has been purged, reconciliation goes to Policy's release operation and returns `Usage`, not a recreated full Job. Add a narrow accounting-only exception to unfinished/current-context rules: configured accounting-authorised service identity, the original authorised owner/work reference, matching reservation/job and valid metering evidence may settle incurred cost after terminal state, revocation or content purge. It cannot infer, publish, read voice content, restore a grant, resume execution or bypass consent for any other purpose.

Policy's existing `usage.recorded` fact with known Cost updates permitted operational `Job.measured_cost` if a history record is retained. If the job was purged, the consumer acknowledges the legitimate accounting fact without recreating it: public Job GET remains `404`, and prior idempotency replay restores only the already contracted original Acceptance. The exact trusted measurement/reconciliation collaborator is an Implementation Plan decision; it may supply raw cost evidence, never final Job/Usage decisions or fake zero measurements.

### 4. Retain only the metadata needed for honest reprojection

Supporting a later larger configured window after voice/job-content purge requires complete accounting facts. Recommend explicit **account-lifetime retention of minimum Policy usage/request metadata**, analogous in duration to the already approved minimum retry record, while keeping it account-scoped and access-controlled.

Only facts needed for counting, reservation protection and duplicate-safe settlement are retained: owner/job/reservation and original actor/request/command/message identifiers needed to verify accounting authority; admission/request/measurement/settlement times or equivalent exact aggregate counts; reserved/consumed audio quantities; active/terminal and settlement deduplication state; estimated holds and known compute/storage amounts. Jobs may keep a minimum accounting-fact receipt/deduplication reference after history purge, without restoring the history record. Retain no script, audio, embedding, waveform, filename, profile/consent identity or text, model material, credentials, tokens, request bodies, URLs or private listening annotations. This does not extend voice/history-content retention, restore purged GET results, or introduce account deletion.

Content purge and minimal idempotency replay do not erase or recreate those counting facts. A later quota/window change therefore recomputes honest counters rather than silently resetting or treating unavailable history as zero. If complete required metadata is unavailable, protection fails closed; it does not guess. Physical bucketing/indexing remains an implementation choice provided it preserves exact projections for the contract's integer-second windows.

An alternative bounded-retention design would require an explicit retained-history horizon and rules restricting later window changes or reporting unavailable history. Neither exists in the current contract. It is not silently selected here.

## Required review and scope of a subsequent amendment

Approve this coherent policy, or provide the desired changes, before the Job RED plan types these expectations. Approval would need to be recorded through the normal requirements clarification, Plan/CONTRACT review and exact RED Implementation Plan sequence; this document does not authorize executing any of them.

Affected approved requirements: R-GEN-001, FR-044, FR-045, NFR-008, AC-QUOTA-001 and the existing privacy/purge constraints. A requirements clarification must record period attribution, minimum metadata retention and unknown-cost handling rather than presenting them as previously explicit requirements.

Affected contract sections: Shared `Usage`/`Cost` meaning; operator quota/budget rules; minimum metadata retention; Policy reserve/commit/release accounting and all three required `command_id` inputs; Jobs fail nullable-cost input; the narrowly authorised terminal/purged accounting exception; idempotence and existing `usage.recorded` consumption. Public field names/types, quota/configuration shape, `$20` target, forecast formula, model/calibration gates and successful-completion Cost requirement remain unchanged. Completed artifacts and evidence remain history; no tests or existing implementation are rewritten by this proposal.

The later RED scope should cover boundary-crossing completion, default/override window changes, carried concurrency/holds, late known cost, unknown-to-known reconciliation, duplicate/crash replay, content purge plus larger-window reprojection and complete preservation of existing 97 regressions. This list is a test target, not typed tests or claimed evidence.

## Inspection and non-execution record

Sources inspected: approved `requirements.md` Q12 (including Q6/Q8/Q9 and AC-QUOTA-001); approved calibration-deferral `Plan.md` (approval recorded `2026-10-28T02:10:48Z`, Job RED milestone 16); approved Q12 `contract/API-Contract.md` Shared schemas, Jobs/history, durable idempotency, operator configuration, internal APIs, facts and common rules; delivered `jobs/persistence.py`, `policy/persistence.py`, owner SQL/HTTP helpers and current enrollment/Auth/persistence test fixtures; relevant approved prior Implementation Plans and model-cost protocol references. The 015 actual two-pass result is completed predecessor evidence, not a new run here.

This task created only this proposal. It created no Implementation Plan, test file, scratch production stub, runtime resource, dependency installation or model/audio asset. No pytest, Docker command or planning dry run was executed: the blocking choice is the undefined target accounting semantics, so there is no approved behavior against which to type or validate these new tests yet. A Windows wildcard-form `rg` read failed before search and was corrected to `rg -g`; no executable artifact was changed by that helper correction.

During inspection, external `016_Implementation_Plan_Job_Orchestration_RED.md` and `tests/test_job_orchestration.py` appeared and HEAD was observed at `d45d103`. They were not created or modified by this task, have no human approval recorded in this conversation, and are preserved as unreviewed inputs. Their assertions, approval-history claims and proposed fixture/API assumptions are not adopted as requirements, valid RED or passing evidence. The existing 016 filename is occupied and must not be overwritten or reused for a later artifact. Other external working files are likewise retained.
