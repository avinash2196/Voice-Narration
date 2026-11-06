# API Contract — initial-build

## Contract Scope

Defines public HTTP and stable internal service/message behavior only. [Plan.md](../Plan.md) remains authoritative for scope, milestones and ownership. Concrete schemas/configuration names exercise the user delegation recorded after Q10 in [requirements.md](../requirements.md), and return for human review.

## Baseline

- Baseline source: the complete approved Q12 contract in this same artifact, approved by avinash2196 on 2026-10-26T17:39:41Z, raw SHA256 `d1ccccaee8073f75f9987a137d85319afb28271dd882d1f40d28b4de437060b4`. Exact pre-Q13 bytes are retained at `C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/Q13-contract-20261029-003231/API-Contract-Q12-before-Q13.md`. This snapshot, not an unreviewed prototype, is the normative starting point.
- Verified against: the actual current artifact matched that raw hash before editing; approved requirements Q13, the approved accounting proposal and approved Plan milestone 16 were reread. Current source/test/prototype inspection is recorded under Compatibility Notes. No alternate published OpenAPI/Swagger contract was found in this workspace inspection; no assertion is made about inaccessible deployments or remote publications.
- Current authority: requirements Q13 approved 2026-10-28T23:42:55Z; Plan Q13 approved 2026-10-29T00:32:31Z; Job-Period-Accounting-Proposal.md approved 2026-10-28T02:54:15Z. Completed milestone 15 satisfies the predecessor. First pending milestone 16, Job Accounting Contract Amendment, owns this document; human review is still required.
- Historical provenance: the Q12 amendment began from approved Q11 raw SHA256 `A749DE7C796449F1F6AD4F1321BEF9041EA013D1EEADC857554BD56D0A082281`, with the pre-Q12 copy at `C:/Users/avina/.codex/visualizations/2026/10/24/01a16f65-73ce-7d12-81f7-d277e8480e46/API-Contract-Q11-before-Q12.md`. The original contract's Q11 baseline SHA256 was `90D69B916F55960F2868064BDD556C49478119E30651C6607A7D39EABD5206CC`. Earlier approvals and completed milestone evidence remain history.

## Changes in This Work Item

Only the following Q13 delta and its necessary consistency references are under review. Every other approved Q12 behavior, including Q11/Q12 enrollment rules, is carried forward.

| Change | Added / Changed / Removed | Requirement / Plan Reference |
| --- | --- | --- |
| Quantity usage attributed to original Acceptance.created_at; selected-window reprojection, authenticated request-time counts and cross-period unfinished-job concurrency | Clarified | requirements.md Q13 quantity rules; R-GEN-001/AC-QUOTA-001; Plan milestone 16 |
| Usage monetary views use current UTC budget month; first durable Policy recognition, carried unresolved holds, preserved original Cost.measured_at and unchanged forecast formula | Changed / clarified | requirements.md Q13 budget rules; FR-044/NFR-008; approved proposal section 2 |
| Jobs fail and Policy release require explicitly nullable cost; complete and commit still require known Cost | Changed internal input types | requirements.md Q13 terminal unknown cost; approved proposal section 3 |
| Required command_id on all three Policy mutations; one reservation/settlement and fresh-command null-to-known reconciliation, including narrow terminal/purge accounting authority | Changed internal input/command semantics | requirements.md Q13 reconciliation; FR-045; Plan milestone 16 |
| Policy reserve carries required internal acceptance_created_at from trusted Jobs, exactly the immutable public Acceptance.created_at; no caller-selected period or shared-owner database | Added internal representation of approved fact | requirements.md Q13 admission time; Q10 schema-drafting delegation; Plan milestone 16 |
| Minimum account-lifetime content-free accounting/request facts and purged-history fact acknowledgement without resurrection | Changed / clarified retention and consumption rules | requirements.md Q13 metadata rules; R-RET/R-DEL/AC-HIST/AC-RET; approved proposal section 4 |

## Out of Scope

Requirements Explicit Exclusions apply. Advanced emotion/per-line pronunciation and P1 history search/rename excluded from this delivery. Q11 approves acoustic calibration candidates and evaluator mechanism, not final calibrated thresholds or production-model clearance; delivered runtime prerequisites remain as recorded in Plan.md. No paid environment is selected by this amendment. Model values follow approved feasibility; failure to support P0 stops that gate.

## Requirement Traceability

| Capability | Source |
| --- | --- |
| Accounts/private grants | R-ACCT-001–003;Q10 |
| Consent/sample/enrollment/quality | R-CONS-001/002;FR-010–013;Q5;Q11 configuration/readiness/stream/provenance/reassessment;Q12 selected-model upload/guidance/reuse and listing;Plan milestones 8/12 |
| Revocation/cleanup/retention | R-REV-001;R-DEL-001;R-RET-001/002;Q9;Q13 content-free accounting exception |
| Text/style/controls/chunks | FR-020/021/025–028;R-EXP-001 |
| Jobs/history/retries/cancellation | FR-022/023/045;Q6/Q9;Q13 terminal unknown cost/reconciliation |
| Preview/export/regeneration | FR-024/028;Q9 |
| Quota/cost/configuration | R-GEN-001;FR-044;NFR-008;AC-QUOTA-001;Q8/Q13;Q11 enrollment_quality subsection;Plan milestones 8/16 |
| Model/mock/local/cloud | FR-040–043;R-LIC-001;Plan model gate |
| Service authorization/artifacts/audit | FR-046;AC-CONS-001;Plan nine-service integration |

## Interfaces

### Shared HTTP schemas

Public paths relative to configured public_base_url plus `/api/v1`; internal paths relative to service plus `/internal/v1`. Each row is an operation with exhaustive input, success and specific failures; common rules below apply to all rows. Required unless `?`; optional does not mean nullable. `none` means no body/parameters. Closed JSON objects; no persistence entities exposed.

Primitives: ID=canonical lowercase UUID;Time=RFC3339 UTC Z;Text=nonblank UTF-8;Nat/Pos=nonnegative/positive JSON integer≤9007199254740991;Decimal=finite base10 string,no exponent,at most six fractional digits;USD=nonnegative string with exactly six fractional digits;Lang=hi|en;Model={model_id:ID,version:Text}.

| Schema | Exact fields |
| --- | --- |
| Account | user_id:ID,email:Text,name:Text,role:User-or-Administrator,email_verified:boolean,created_at:Time |
| Token | access_token:Text,token_type:Bearer,expires_at:Time,account:Account |
| Consent | consent_id:ID,owner_id:ID,consenting_identity:Text,text:Text,version:Text,assisted:boolean,authorization:Text-or-null,status:active-or-revoked,created_at:Time,revoked_at:Time-or-null |
| Artifact | artifact_id:ID,owner_id:ID,kind:sample-or-generated-or-joined_preview,consent_id:ID-or-null,profile_id:ID-or-null,job_id:ID-or-null,format:wav-or-mp3-or-m4a,size_bytes:Nat,duration_seconds:Decimal,sample_rate_hz:Pos,created_at:Time,expires_at:Time,availability:available-or-deleting-or-deleted |
| Finding | check:duration-or-clipping-or-silence-or-noise-or-level-or-speech_presence,severity:pass-or-warning-or-failure,measured:Decimal-or-null,unit:Text-or-null,message:Text,action:Text |
| Quality | assessment_id:ID,findings:Finding[],override_allowed:boolean,override_acknowledged:boolean |
| Failure | code:Text,message:Text,action:Text |
| Profile | profile_id:ID,owner_id:ID,name:Text,language:Lang,consent_id:ID,samples:Artifact[],model:Model,status:ProfileState,quality:Quality-or-null,failure:Failure-or-null,created_at:Time,updated_at:Time |
| Controls | pause_strength:Decimal,speech_pace:Decimal |
| Generation | profile_id:ID,script:Text,language:Lang,style:Text,controls?:Controls |
| Acceptance | job_id:ID,status:queued,created_at:Time |
| Cost | compute_usd:USD,storage_usd:USD,total_usd:USD,measured_at:Time |
| Job | job_id:ID,owner_id:ID,profile_id:ID,model:Model,script_snapshot:Text,language:Lang,style:Text,controls:Controls-or-null,parent_job_id:ID-or-null,regenerated_chunk_ids:ID[],status:JobState,created_at:Time,updated_at:Time,completed_at:Time-or-null,output_artifact_id:ID-or-null,joined_preview_artifact_id:ID-or-null,duration_seconds:Decimal-or-null,estimated_cost_usd:USD,measured_cost:Cost-or-null,failure:Failure-or-null,mapping_available:boolean |
| Chunk | chunk_id:ID,index:Nat,text_start:Nat,text_end:Nat,audio_start_seconds:Decimal,audio_end_seconds:Decimal |
| Cleanup | cleanup_id:ID,status:pending-or-running-or-completed-or-failed,requested_at:Time,deadline_at:Time,completed_at:Time-or-null,failure:Failure-or-null |
| Link | url:Text,expires_at:Time,artifact:Artifact |
| Range | min:Decimal,max:Decimal,step:Decimal,default:Decimal |
| Capability | model:Model,languages:Lang[],mixed_language:boolean,styles:Text[],pause_strength:Range-or-null,speech_pace:Range-or-null,section_regeneration:boolean,mapping:boolean,max_script_characters:Pos,max_output_seconds:Decimal,sample_min_seconds:Decimal,sample_max_seconds:Decimal,formats:(wav-or-mp3)[],enrollment_materials:(reference_audio-or-embeddings-or-weights)[],recording_guidance:Text[] |
| Grant | grant_id:ID,owner_id:ID,administrator_id:ID,scopes:(profiles:read-or-samples:read-or-jobs:read-or-audio:read-or-consents:read)[],created_at:Time,expires_at:Time,revoked_at:Time-or-null |
| Quota | window_seconds:Pos,generation_count:Pos,audio_seconds:Decimal,request_count:Pos,concurrent_jobs:Pos |
| Usage | window_start:Time,reset_at:Time,accepted_jobs:Nat,reserved_audio_seconds:Decimal,consumed_audio_seconds:Decimal,requests:Nat,active_jobs:Nat,policy:Quota,estimated_usd:USD,measured_cost:Cost,budget_stopped:boolean |
| Audit | event_id:ID,type:Text,actor_id:ID-or-null,owner_id:ID-or-null,resource_id:ID-or-null,occurred_at:Time,outcome:Text |

`A-or-B` denotes the named JSON string enum alternatives, except `-or-null` permits literal JSON null. `Page<T>={items:T[],next_cursor:Text-or-null}`; `List` query=`cursor?:Text,limit?:Pos`. Configured default/max page size comes from existing Configuration.limits.page_default/page_max (positive integers, default≤max); no hidden page default. Missing/invalid dependent configuration fails closed under existing configuration errors. Opaque authenticated cursor binds principal/filters/stable snapshot fixed on first page; altered/incompatible cursor400 INVALID_CURSOR. All pages descending created_at then resource ID (Audit occurred_at/event_id;models approval timestamp then model_id/version from Approval); Chunk pages ascending index. Empty `{items:[],next_cursor:null}`. No offset/arbitrary sort. Model approval timestamp is the persisted approval time,not an additional Capability input. The trusted catalog provider supplies enabled/approved Capability records in this existing persisted Approval-time/model-identity order; the listing handler preserves that order through authenticated pagination/snapshots. No public Capability timestamp is added. Internal factory/callable signatures remain Implementation Plan detail (Q12 A/B).

### Q13 Usage period and measurement meanings

Quantity fields use the selected full per-user Quota override, or default_user_quota when there is none. There is no separate system quota period. For width W=window_seconds, the current quantity interval is [floor(now/W)*W, floor(now/W)*W+W) in UTC; window_start/reset_at identify its boundaries. accepted_jobs, reserved_audio_seconds and consumed_audio_seconds project each job's original durable Acceptance.created_at inside that interval; requests projects each authenticated public request's receipt time. This includes replay/polling requests, not internal service callbacks. A completed job's measured successful audio replaces its maximum reservation at its original admission time even if completion is later. Failure/cancellation releases unused audio without fabricating successful consumed audio. Replays add no generation or reservation fact.

active_jobs counts all unfinished accepted jobs for that user across quantity windows. system_concurrent_jobs likewise covers all unfinished accepted jobs across users/windows. A default/override change, including window_seconds, reprojects original facts under the newly selected interval; it never resets counters, erases old reservations or rewrites history. Accepted jobs retain admission-time limits; new requests use current selected policy. Existing consent/model fences, output cap, deadlines and hard budget/kill-switch safety remain. Admission-limit changes do not invent retroactive cancellation selection.

Usage.estimated_usd is the user's outstanding estimated monetary holds, including carried earlier-month and unknown-terminal-cost holds. Usage.measured_cost aggregates that user's known costs first durably recognised by Policy during the current UTC budget month. These money fields use the budget month, not window_start/reset_at. The system budget applies the corresponding system-wide recognised costs and all outstanding holds; the per-user Usage view is not a separate $20 allowance.

Per-job estimated_cost_usd remains immutable. Original reported Cost.measured_at is the authorised source's actual measurement time and remains unchanged, including late reports. Budget recognition time is Policy's trusted clock at first durable acceptance of the known settlement, not a caller-selected/backdated period. Aggregate Usage.measured_cost.measured_at is when that aggregate is observed. An empty known-cost monthly ledger aggregates to zero; this is not a zero measurement for any unmeasured job. No new timestamp-validation bound is introduced.

At month rollover, select the new month's recognised-cost projection and carry every unresolved estimated hold exactly once. On first known settlement, replace that hold with actual compute/storage cost recognised in that settlement-acceptance UTC month. Duplicates neither recharge, release another hold, move an existing recognition to another month nor duplicate forecast alerts. For example, a January job's 0.200000 unresolved estimate protects February; its first 0.120000 settlement accepted in February removes the hold and recognises 0.120000 in February, retaining its original measurement timestamp. A March duplicate does not charge March. Exact Decimal/USD arithmetic and forecast formula below are unchanged.

### Accounts/grants (HTTP)

First three rows unauthenticated; all others require unexpired Bearer and verified account. Tokens opaque; no JWT format promised. Public registration User only.

| Method/path | Input | Success | Specific failures |
| --- | --- | --- | --- |
| POST /auth/register | JSON {email:Text,password:Text,name:Text} | 202 {verification_required:true};send verification | 400 INVALID_INPUT;503 DEPENDENCY_UNAVAILABLE |
| POST /auth/verify-email | JSON {token:Text} | 200 Token;consume credential | 400 INVALID_TOKEN;409 TOKEN_CONSUMED |
| POST /auth/login | JSON {email:Text,password:Text} | 200 Token | 401 INVALID_CREDENTIALS;403 EMAIL_UNVERIFIED |
| GET /auth/me | none | 200 Account | common |
| POST /access-grants | JSON {administrator_id:ID,scopes:Grant.scopes,expires_at:Time} | 201 Grant | 400 INVALID_INPUT;404 NOT_FOUND |
| GET /access-grants | List | 200 Page<Grant>,owner only | common |
| DELETE /access-grants/{grant_id} | none | 200 Grant revoked | common |

Email trim/lowercase for lookup; exactly one @, nonblank local/domain,no whitespace. Duplicate registration same202 without existing account change. Password preserved within configured lengths. Consumed verification409 until expiry; expired/unknown400. Grant target must Administrator; expiry future; scopes distinct/nonempty. Owner alone creates/revokes; immutable otherwise. Repeat revocation preserves timestamp. Grant scope/expiry/revocation checked live on every private read/link access; role alone never grants private content or defeats consent revocation.

### Consent/enrollment (HTTP)

| Method/path | Input | Success | Specific failures |
| --- | --- | --- | --- |
| POST /consent/record | JSON {consenting_identity:Text,text:Text,version:Text,assisted:boolean,authorization?:Text} | 201 Consent | 400 INVALID_INPUT |
| GET /consent/{consent_id} | owner_id?:ID for granted admin | 200 Consent | common |
| DELETE /consent/{consent_id} | none | 202 Cleanup | common |
| POST /artifacts/upload | multipart/form-data consent_id:ID,model_id:ID,model_version:Text,file:binary | 201 sample Artifact | 400 INVALID_AUDIO/LIMIT_EXCEEDED;409 CONSENT_REVOKED;503 MODEL_NOT_READY |
| POST /voices | JSON {name:Text,language:Lang,consent_id:ID,sample_artifact_ids:ID[],model:Model} | 202 pending Profile | 400 UNSUPPORTED_CAPABILITY;409 CONSENT_REVOKED/ARTIFACT_UNAVAILABLE;503 MODEL_NOT_READY |
| GET /voices | List;status?:ProfileState,language?:Lang,owner_id?:ID | 200 Page<Profile> | common |
| GET /voices/{profile_id} | owner_id?:ID | 200 Profile | common |
| PATCH /voices/{profile_id}/quality-override | JSON {assessment_id:ID,acknowledged:true} | 200 enrolling Profile | 409 STALE_ASSESSMENT/OVERRIDE_NOT_ALLOWED/INVALID_STATE |
| DELETE /voices/{profile_id} | none | 202 Cleanup | common |
| GET /cleanups/{cleanup_id} | none | 200 Cleanup | common |

Assisted=true requires authorization; false rejects authorization. Immutable consent contents; association Profile.consent_id. Validate active owner consent before sample bytes used/persisted; unauthorized streams discarded. WAV audio/wav,MP3 audio/mpeg,M4A audio/mp4 must match actual decodable bytes. Empty/corrupt/unsupported/oversized/out-of-duration400. Browser recordings use accepted formats. Configured count/byte and approved selected-model duration limits apply before accepting samples. Sample refs nonempty/distinct/available/owner-owned/same active consent; response samples input order.

Q12 upload admission: consent_id, model_id, model_version and file are each required exactly once under the existing multipart parsing rules. Map model_id/model_version to existing Model `{model_id,version}` without normalization or inference. Missing/null/empty/blank, duplicate, malformed or wrongly typed scalar parts and unknown/read-only parts return existing 400 INVALID_INPUT; canonical lowercase UUID and nonblank exact version rules apply. Resolve the explicitly selected model through the trusted approved capability boundary. A well-formed unknown, unapproved or unavailable model returns existing 503 MODEL_NOT_READY, including a known model blocked from readiness; this does not replace invalid/corrupt/unsupported audio or configured/model-bound violations with a new code. Existing audio/limit 400 codes, active-consent 409 and all common authorization/readiness errors remain. No hidden/default/fixture model is selected.

Q12 enrollment flow: select a model from the approved catalog before recording/upload; display its recording_guidance and effective sample-duration bounds, then record/upload with explicit model reference and active owner consent before persistence; create the profile from authorized uploaded samples. Admission uses that selected Capability's sample_min_seconds/sample_max_seconds with applicable stricter configuration limits, not filename metadata or an invented model duration. The upload model is admission context only: no public Artifact field or permanent sample/model binding is added. Profile admission and conditioning independently revalidate every sample against the profile's selected Model and live authorization, safety and readiness gates, including reuse under another model. Public Artifact/Profile schemas remain unchanged. Capability.formats describes generation output; it does not narrow accepted WAV/MP3/M4A sample input. Q11 selected-stream/original-byte rules below apply throughout.

ProfileState: pending→quality_checking→enrolling→enrolled; warning path quality_checking→awaiting_user_override→enrolling. Hard/execution failure→failed with actionable Failure; any nonrevoked state→revoked. Quality has all six check findings once in declared order. Override only current overrideable warning after informed acknowledgement; matching repeat returns current Profile without duplicate enrollment. Only model-needed materials persist; no training promise. Capability returns recording guidance. Null quality/failure before available.

Q11 stream-selection amendment: decode permitted actual audio bytes, not filename/container duration metadata. Select the container-designated default audio stream; if several defaults or none exist, select the lowest-index decodable audio stream. At least one decodable audio stream is required; multiple streams are not an additional rejection condition. Requirements Q11's “one decodable audio stream” and Provenance Check's “one-stream validation” mean one selected stream under the explicit rule in the approved proposal's deterministic measurement policy, not a single-stream-container restriction. Support channels within the selected stream. Use the same selection for metadata, assessment, playback and conditioning; record its index privately. Duration counts decoded sample frames at the selected stream rate. Preserve the stored original; no peak normalization, denoising, trimming or compression is authorized by this amendment. Nonfinite decoded values are corrupt/invalid audio under existing admission rules.

Q11 assessment amendment: pin the effective policy configuration revision, evaluator artifact identity and calibration reference privately with each assessment. Configuration changes do not rewrite historical findings or duplicate enrollment. Unfinished assessments under an obsolete policy require reassessment under the new revision before override acceptance; prior assessment IDs then return the existing 409 STALE_ASSESSMENT. Re-recording uses new authorized artifacts/assessment and cannot revive a stale acknowledgement. Keep the exact existing PATCH body, current-assessment requirement and semantic-repeat behavior. Live consent/resource safety applies regardless of pinned policy. Public Finding and Quality fields and six-finding order remain unchanged. Missing policy/calibration/evaluator readiness prevents dependent enrollment as specified below; execution failure cannot become an overrideable warning or fabricated pass. Necessary private measurement/provenance metadata follows existing deletion/retention fences; no sample bytes, transcripts, embeddings, filenames or private listening annotations in logs.

Deletion/revocation synchronously fences synthesis/retrieval before202; asynchronously purges profile metadata,original samples,derived/model materials,reconstructive caches and associated generated audio within cleanup deadline. Active jobs cannot publish. Repeated delete with retained tombstone same Cleanup; after tombstone removed404. Cleanup failure visible without restoring access/extending deadline. Audit metadata separate retention; retry tombstones retain no private content.

### Jobs/history (HTTP)

| Method/path | Input | Success | Specific failures |
| --- | --- | --- | --- |
| POST /jobs | JSON Generation;required Idempotency-Key header | 202 Acceptance | 400 IDEMPOTENCY_KEY_REQUIRED/UNSUPPORTED_CAPABILITY/LIMIT_EXCEEDED;409 IDEMPOTENCY_CONFLICT/PROFILE_NOT_READY/CONSENT_REVOKED;429 QUOTA_EXHAUSTED/CONCURRENCY_EXHAUSTED;503 MODEL_NOT_READY/BUDGET_STOPPED |
| GET /jobs | List;status?:JobState,profile_id?:ID,owner_id?:ID | 200 Page<Job> | common |
| GET /jobs/{job_id} | owner_id?:ID | 200 Job | common |
| POST /jobs/{job_id}/cancel | none | 200 cancelled Job | 409 INVALID_STATE for completed/failed |
| POST /jobs/{job_id}/regenerations | JSON {script?:Text,style?:Text,controls?:Controls,chunk_ids?:ID[]};required Idempotency-Key | 202 Acceptance new child | submission errors plus409 SOURCE_UNAVAILABLE/INVALID_STATE;400 INVALID_CHUNK |
| GET /jobs/{job_id}/chunks | List;owner_id?:ID | 200 Page<Chunk> | 409 MAPPING_UNAVAILABLE/INVALID_STATE |

Preserve exact Unicode script/punctuation/line breaks; character limits count Unicode scalar values. hi/en/style match approved Capability; neutral mandatory, mixed-language conditional. Omitted controls use pinned approved defaults; supplied Controls both fields required on safe min/max/step grid. Unsupported control/style/language400. Job.controls null only when neither control supported; such model cannot satisfy enabled P0 gate.

Acceptance durably snapshots effective script/profile/model/version/parameters and reserves policy before dispatch. Profile enrolled,consent active,model approved/enabled required. JobState: queued→preparing→running→post_processing→completed; any unfinished state may fail/cancel. No backwards moves. Completion/cancellation one durable winner: cancelled winner denies output publication; completed winner cancel409. Repeated cancellation returns cancelled Job. Timeout→failed JOB_TIMEOUT. Bounded attempts remain one job/deadline; no duplicate final artifacts/accounting. Unused quantity/concurrency protection is released on terminal outcome; measured incurred costs remain. If terminal cost is unknown, Job.measured_cost stays null and its estimated monetary hold remains until authorised Q13 reconciliation; unknown cost is never manufactured as zero.

Snapshots immutable; operational status/output/timestamps/failure/cost may change. Before completion output/duration/completed_at null,mapping_available=false; failure nonnull only failed. Measured cost null until measured, not fabricated zero. History retention cannot override revocation/purge; purged history404. A later legitimate usage.recorded fact may update only retained operational measured_cost; after history purge it is acknowledged under the retained accounting reference without recreating Job content or changing public GET404. See the Q13 accounting-only exception below.

Regeneration requires completed available authorized source, creates new child preserving original. Inherit profile/language/model and omitted script/style/controls; supplied whole values replace. Empty body whole regeneration. Supplied chunk_ids nonempty/distinct/source-owned; section capability required; script replacement disallowed with chunk_ids. Process chunks in original index order. Section result preserves unchanged source audio and supplies joined_preview_artifact_id for explicit join review; whole result joined preview null. Original remains intact subject to deletion/retention.

Chunks half-open Unicode scalar text offsets and half-open audio seconds in assembled WAV; indices start0. Text coverage complete/ordered/nonoverlapping, never midword; punctuation/newlines pause cues. Actual join has no clicks/dropouts/repeated words/unintended gaps and stable loudness/sample rate/identity under approved protocol. Mapping only once complete; not-ready409 rather than misleading empty result.

#### Durable idempotency (Q6)

Mandatory nonblank opaque header bounded by configured bytes, never body field. Scope authenticated owner plus create_job/regenerate_job operation. Fingerprint parsed effective input, pinned model/defaults and regeneration source ID. Object order/chunk selection order irrelevant; exact script significant; equivalent Decimal values equal. Replay omissions resolve original pinned defaults despite later configuration changes. Identical concurrent/restarted submissions return original202 Acceptance (queued/original time), not current status; clients poll. Changed input409. Admission,key binding,reservation one durable outcome; preacceptance rejection binds no key. Minimal key/fingerprint/job-reference/acceptance-time record lasts account lifetime including after deletion, without script/audio. Replay after purge returns original Acceptance, never execution/charge; GET purged job404. Authentication still required; replay restores no content. New key is new request subject to current policy. Q13's separate content-free accounting ledger survives content purge and replay without adding another usage fact; it is not permission to retain script/audio in the retry record.

### Artifacts (HTTP)

| Method/path | Input | Success | Specific failures |
| --- | --- | --- | --- |
| GET /artifacts/{artifact_id}/preview-url | owner_id?:ID | 200 Link | 409 ARTIFACT_UNAVAILABLE/CONSENT_REVOKED |
| GET /artifacts/{artifact_id}/download-url | format?:wav-or-mp3,owner_id?:ID | 200 Link | 400 UNSUPPORTED_FORMAT;409 ARTIFACT_UNAVAILABLE/CONSENT_REVOKED |
| GET /artifacts/{artifact_id}/content | signature:Text,expires_at:Time,disposition:inline-or-attachment,format:wav-or-mp3-or-m4a;Bearer credentials | 200 binary corresponding audio MIME;Content-Disposition matching disposition | 401 INVALID_LINK;409 ARTIFACT_UNAVAILABLE/CONSENT_REVOKED |
| DELETE /artifacts/{artifact_id} | none | 202 Cleanup | common |

Link binds artifact,requesting principal,disposition,format,expiry. Each access rechecks live bearer identity,owner authorization or explicit live scoped administrator grant,active consent/profile/artifact,signature/expiry. URL alone insufficient; different principal403,bad/expired signature401. No unauthenticated object redirect/storage keys exposed. Generated preview/download WAV default; MP3 conditional on approved encoder/license. Samples original format and reject format query. Unsupported format400,no fallback. Range unsupported400 INVALID_INPUT. Output duration positive,≤3000 and all stricter limits; overrun fails OUTPUT_LIMIT_EXCEEDED without publishing partial output. Delete immediately denies access and returns Cleanup; retained permitted job history cannot retrieve deleted output. Sample deletion revokes associated profile. Downloaded local Windows copies outside server purge per Q1.

### Models/policy/audit (HTTP)

| Method/path | Input | Success | Specific failures |
| --- | --- | --- | --- |
| GET /models | List | 200 Page<Capability>,enabled approved only | empty valid before gate |
| GET /quotas/me | none | 200 Usage | common |
| GET /admin/quotas/user/{user_id}/status | none | 200 Usage | common |
| GET /admin/configuration | none | 200 Configuration | common |
| PUT /admin/configuration | JSON Configuration | 200 Configuration | 400 INVALID_CONFIGURATION;409 CONFIGURATION_CONFLICT |
| PUT /admin/quotas/user/{user_id} | JSON Quota | 200 Quota | 400 INVALID_INPUT |
| PUT /admin/models/{model_id}/versions/{version}/approval | JSON ApprovalInput | 200 Approval | 400 INVALID_CONFIGURATION;409 MODEL_GATE_UNSATISFIED |
| GET /admin/audit/events | List;type?:Text,actor_id?:ID,owner_id?:ID,resource_id?:ID | 200 Page<Audit> | common |
| GET /admin/audit/user/{user_id}/timeline | List;type?:Text | 200 Page<Audit> | common |
| GET /admin/audit/job/{job_id}/history | List;type?:Text | 200 Page<Audit> | common |

All /admin require Administrator or403. ApprovalInput={license_evidence_urls:Text[],evaluation_evidence_url:Text,commercial_use_approved:true,capability:Capability,enabled:boolean}. Approval adds model:Model,approved_by:ID,approved_at:Time. Evidence references nonempty HTTPS URLs/operator-local artifacts. Capability model matches path,version exact nonblank percent-encoded string. Requires human-reviewed source/weights/output-use commercial evidence and approved feasibility/protocol results, not unprivileged boolean. Enabling requires hi/en,neutral,mapping,safe basic controls;section/MP3 conditional. Disabled model fences further inference/publication (MODEL_DISABLED failure). Before G1 generation503 MODEL_NOT_READY.

PUT replaces whole resource. Configuration revision must equal current,success increments once;stale409. User Quota replaces default,still stricter system/model/budget bounds. New policy applies admission/ongoing hard safety,does not rewrite history. Audit immutable metadata,eventual/nonblocking,no private content. Unknown exact audit filter empty;known parent no events empty;unknown parent404. Role never implies private-data grant.

### Operator configuration interface

`VOICE_NARRATION_CONFIG` absolute path UTF-8 JSON Configuration; admin PUT same shape publishes durable effective document. Separate bootstrap `VOICE_NARRATION_ADMIN_EMAIL` plus `VOICE_NARRATION_ADMIN_CREDENTIAL_SECRET_REF` provisions verified Administrator outside public registration. Secret values never returned,only references. Missing required configuration disables dependent operation503 CONFIGURATION_REQUIRED with operator diagnostic. No generation with missing model/limits/cost evidence.

| Configuration field | Shape/constraints |
| --- | --- |
| revision,public_base_url,mode | Nat;absolute HTTPS URL (local loopback HTTP exception);mock-or-local-or-cloud |
| auth | {access_token_seconds:Pos,verification_token_seconds:Pos,signed_link_seconds:Pos,password_min_characters:Pos,password_max_characters:Pos};max≥min |
| service_urls | {auth:Text,consent:Text,voices:Text,jobs:Text,artifacts:Text,policy:Text,ai:Text,audit:Text};absolute transport-compliant URLs;Worker no inbound HTTP |
| transport | {environment:local-or-deployed,service_identity_secret_refs:{auth:Text,consent:Text,voices:Text,jobs:Text,artifacts:Text,policy:Text,ai:Text,worker:Text,audit:Text}} |
| storage | {primary_bucket:Text,credential_secret_ref:Text,local_copy_directory:Text-or-null};primary private cloud storage |
| limits | {upload_max_bytes:Pos,samples_per_profile:Pos,samples_total_max_bytes:Pos,script_max_characters:Pos,output_max_seconds:Decimal,job_timeout_seconds:Pos,inference_timeout_seconds:Pos,max_attempts:Pos,retry_delay_seconds:Pos,idempotency_key_max_bytes:Pos,message_max_bytes:Pos,message_rate_per_second:Pos,inflight_messages:Pos,page_default:Pos,page_max:Pos};output>0 and≤3000;page_default≤page_max |
| default_user_quota,system_concurrent_jobs | Quota;Pos;quota audio_seconds>0 |
| budget | {monthly_target_usd:USD,forecast_alert_usd:USD,stop_usd:USD,kill_switch:boolean};target default20.000000;stop>0 |
| retention | {generated_audio_days:Pos,profile_days:Pos,sample_days:Pos,consent_days:Pos,audit_days:Pos,cleanup_window_seconds:Pos};generated default30;cleanup default86400;others explicitly configured |
| enrollment_quality | Required closed object defined below; no defaults |

#### Enrollment quality configuration (Q11 amendment)

This same required subsection applies to Configuration GET, whole-resource PUT and VOICE_NARRATION_CONFIG. All nested fields are required, nonnull and closed; no coercion, implicit defaults or runtime clamping. The following `Decimal` threshold fields are an explicit exception to the shared Decimal string primitive: finite JSON numbers with at most six fractional decimal places; booleans are not numeric. Pos/Nat retain their existing integer meanings. These fields introduce no alternate representation elsewhere.

| enrollment_quality field | Exact shape / constraints |
| --- | --- |
| policy_id | Text exactly `enrollment-acoustics-v1`; immutable algorithm identifier, not script/plugin path |
| calibration_ref | Nonblank Text identifying immutable reviewed calibration evidence bound to every policy field and evaluator hashes; no private audio URL |
| vad | {implementation:Text,artifact_ref:Text,sample_rate_hz:Pos,frame_ms:Pos,mode:Nat}; implementation exactly `webrtc-gmm`; artifact_ref immutable reviewed registry identity, not arbitrary executable/download URL; sample_rate_hz exactly16000; frame_ms exactly20; mode in0..3 |
| clipping | {peak_abs:Decimal,max_fraction:Decimal}; 0<peak_abs<=1; 0<=max_fraction<=1 |
| silence | {frame_rms_dbfs:Decimal,max_fraction:Decimal}; frame_rms_dbfs<0; 0<=max_fraction<=1 |
| noise | {min_snr_db:Decimal,min_speech_seconds:Decimal,min_nonspeech_seconds:Decimal}; finite min_snr_db; both seconds>0 |
| level | {min_speech_rms_dbfs:Decimal,max_speech_rms_dbfs:Decimal}; min<max<=0 |
| speech_presence | {min_fraction:Decimal,min_seconds:Decimal}; 0<=min_fraction<=1; min_seconds>0 |

Out-of-range, unknown, missing, null or wrongly typed subsection fields in configuration submission return existing 400 INVALID_CONFIGURATION. Preserve Administrator authorization, whole-resource replacement, revision equality/CAS, single revision increment and durable publication. GET returns the same effective Configuration shape. An existing document missing enrollment_quality disables only dependent enrollment with existing 503 CONFIGURATION_REQUIRED; it does not retrospectively break unrelated delivered operations. Existing document migration remains separately reviewed executable work.

Unknown/unapproved or mismatched calibration evidence, unavailable evaluator readiness or changed policy/settings/evaluator hashes cannot enable dependent enrollment. Use existing 503 CONFIGURATION_REQUIRED for missing/applicability-invalid configuration or calibration and 503 DEPENDENCY_UNAVAILABLE for evaluator/runtime dependency unavailability, as appropriate; no new code or auto-pass/fallback is introduced. Editing policy limits invalidates calibration applicability until reviewed recalibration. Pin the applicable immutable reviewed evaluator registry identity/hashes and calibration reference. Accepted human calibration must bind all effective policy fields and evaluator hashes before user enrollment enablement; exact evaluator distribution/platform/supply-chain evidence belongs to Enrollment Evaluator Prerequisites and actual calibration execution/acceptance belongs to Enrollment Acoustic Calibration Validation. Neither is claimed complete here. The approved proposal's Calibration and verification before enablement points 1–6 remain the complete acceptance source; no reduced gate or invented result is substituted.

Initial settings VAD16000/20/mode1, clipping0.999/0.001, silence-50/0.60, noise15/0.30/0.30, level-35/-10 and speech0.20/1.00 are approved calibration candidates, not production defaults or measured outcomes. No fabricated artifact_ref/calibration_ref is supplied. Duration remains bounded by the approved model Capability and existing stricter limits; no model duration default is added. Q11's approved deterministic measurement, aggregation, warning and unknown-value policy remains owned by Enrollment RED/GREEN, as specified in requirements.md and the approved proposal; this amendment does not add endpoints, public findings, hard acoustic rejections or executable algorithms.

All fields required except stated defaults;no hidden token/link/rate/upload/retry/model defaults. Secret-resolution failure disables dependency. Deployed encrypted transport;HTTP only local loopback. Day86400 seconds;retention from creation/event occurrence. Artifact.expires_at=created_at plus sample_days or generated_audio_days as appropriate (joined preview uses generated policy);shortened policy updates recompute expiry and fence already-expired resources. Profile/consent expiry triggers revocation;sample expiry revokes linked profile;generated expiry deletes audio only. Retention never delays requested purge or means indefinite consent/audit storage.

Effective script/output/sample bounds minima of configuration,approved model,available quota. For sample admission, the explicit upload Model supplies Capability.sample_min_seconds/sample_max_seconds with applicable stricter configuration limits; profile admission and conditioning recheck the profile's selected Model independently (Q12), with no invented duration/default. Admission reserves maximum effective output duration; completion replaces successful quantity reservation at original Acceptance.created_at with measured duration and releases the remainder. UTC epoch quantity projections, request counts and cross-period unfinished concurrency follow the Q13 Usage meanings above. Timeout spans preparation through postprocessing;max_attempts includes initial;retry cannot extend deadline. Budget uses current-UTC-month first-recognised known cost plus all outstanding estimated monetary holds, including earlier-month/unknown-terminal holds;kill switch or reservation crossing stop_usd503 BUDGET_STOPPED before further work. Forecast=current-month recognised measured spend×actual UTC-month duration/elapsed month duration (at month start, measured spend);crossing alert emits operator metadata. Estimates are not measured spend in this formula. $20 target not guarantee/per-user allowance. Approved model evidence supplies tariffs/estimates;missing dependency503 rather than free execution.

#### Q13 content-free accounting retention

Policy retains only minimum account-scoped, access-controlled usage/request/accounting facts for the account lifetime: owner/job/reservation and original actor/request/command/message identifiers needed to verify accounting authority; original admission/request/measurement/settlement times or equivalent exact aggregate counts; reserved/consumed audio quantities; active/terminal and settlement/deduplication state; estimated holds and known compute/storage amounts. Jobs may retain a minimum accounting-fact receipt/deduplication reference after history purge, without restoring that history.

These lifetime facts retain no script, audio, embedding, waveform, filename, profile/consent identity or text, model material, credential, token, request body, URL or private listening annotation. They do not extend private-content or audit retention, change deletion deadlines, restore purged retrieval or add account deletion. Content purge and idempotent replay neither erase nor recreate counting facts. Later larger-window reprojection uses complete original facts rather than resets or invented zeros. Unavailable required facts cause protection to fail closed with the existing dependency/configuration semantics. Physical exact aggregation/indexing is an Implementation Plan choice, not an additional API field or retention horizon.

### Stable internal HTTP interfaces

Nine owners: Auth identity/grants;Consent authorization;Voices profile/quality;Jobs durable orchestration;Artifact binaries;Policy reservations/usage;AI approved models/conditioning;Worker asynchronous execution;Audit immutable metadata. No direct cross-owner persistence. Gateway infrastructure not tenth domain service. Worker reports callbacks;owners publish facts. Normalized interfaces stable across mock/local/cloud adapters.

Service identity authenticated with configured least privilege;deployed transport encrypted. Required X-Deadline:Time future and bounded by configured/job deadline. For authorised Q13 accounting-only late reconciliation, a fresh future request deadline remains subject to the existing configured bound for non-execution commands; the already-expired execution deadline is not its upper bound. This exception never extends a job/inference deadline or authorises further execution. Context={owner_id:ID,actor_id:ID,request_id:ID} must originate from authorized work,never arbitrary user ownership assertion. Revalidate consent/current authorization before inference and publication;event delay cannot weaken immediate fence.

| Target method/path | Required input JSON except stated | Success | Specific failures |
| --- | --- | --- | --- |
| Auth POST /auth/verify-token | {token:Text} | 200 Account | 401 UNAUTHENTICATED |
| Consent POST /consent/validate | {context:Context,consent_id:ID} | 200 active Consent | 409 CONSENT_REVOKED |
| Voices POST /voices/validate | {context:Context,profile_id:ID,purpose:enrollment-or-generation} | 200 active Profile;generation requires enrolled,enrollment permits pending/quality_checking/enrolling | 409 PROFILE_NOT_READY/CONSENT_REVOKED |
| Voices POST /voices/{profile_id}/enrollment-result | {context:Context,command_id:ID,expected_status:ProfileState,status:ProfileState,quality:Quality-or-null,failure:Failure-or-null} | 200 Profile | 409 INVALID_STATE/RESULT_CONFLICT |
| Jobs POST /jobs/{job_id}/work-item | {context:Context,command_id:ID} | 200 {job:Job,deadline_at:Time,reservation_id:ID} | 409 INVALID_STATE/CONSENT_REVOKED |
| Jobs POST /jobs/{job_id}/status | {context:Context,command_id:ID,expected_status:JobState,status:preparing-or-running-or-post_processing} | 200 Job | 409 INVALID_STATE/RESULT_CONFLICT |
| Jobs POST /jobs/{job_id}/complete | {context:Context,command_id:ID,output_artifact_id:ID,joined_preview_artifact_id:ID-or-null,duration_seconds:Decimal,chunks:Chunk[],cost:Cost} | 200 completed Job | 409 INVALID_STATE/RESULT_CONFLICT;400 OUTPUT_LIMIT_EXCEEDED |
| Jobs POST /jobs/{job_id}/fail | {context:Context,command_id:ID,failure:Failure,cost:Cost-or-null} | 200 failed Job | 409 INVALID_STATE/RESULT_CONFLICT |
| Artifact POST /artifacts/store | multipart context:Context JSON,command_id:ID,profile_id:ID,job_id:ID,kind:generated-or-joined_preview,file:binary WAV | 201 Artifact | 400 INVALID_AUDIO/OUTPUT_LIMIT_EXCEEDED;409 CONSENT_REVOKED/RESULT_CONFLICT |
| Artifact POST /artifacts/metadata | {context:Context,artifact_id:ID} | 200 Artifact | 409 ARTIFACT_UNAVAILABLE |
| Artifact POST /artifacts/batch-delete | {context:Context,command_id:ID,artifact_ids:ID[]} | 202 Cleanup | 409 RESULT_CONFLICT |
| Policy POST /quotas/reserve | {context:Context,command_id:ID,job_id:ID,acceptance_created_at:Time,max_audio_seconds:Decimal,estimated_cost_usd:USD} | 201 {reservation_id:ID} | 429 QUOTA_EXHAUSTED/CONCURRENCY_EXHAUSTED;503 BUDGET_STOPPED |
| Policy POST /quotas/commit-usage | {context:Context,command_id:ID,reservation_id:ID,job_id:ID,audio_seconds:Decimal,cost:Cost} | 200 Usage | 409 RESULT_CONFLICT/INVALID_STATE |
| Policy POST /quotas/release-reservation | {context:Context,command_id:ID,reservation_id:ID,job_id:ID,cost:Cost-or-null} | 200 Usage | 409 RESULT_CONFLICT/INVALID_STATE |
| AI POST /ai/enroll | {context:Context,command_id:ID,profile_id:ID,model:Model,sample_artifact_ids:ID[]} | 200 {quality:Quality,materials:Capability.enrollment_materials} | 409 CONSENT_REVOKED;503 MODEL_NOT_READY |
| AI POST /ai/infer | {context:Context,command_id:ID,job_id:ID,profile_id:ID,model:Model,text:Text,language:Lang,style:Text,controls:Controls-or-null} | 200 binary audio/wav;X-Duration-Seconds:Decimal,X-Sample-Rate-Hz:Pos | 400 UNSUPPORTED_CAPABILITY;409 CONSENT_REVOKED;503 MODEL_NOT_READY/BUDGET_STOPPED |
| AI POST /ai/models/validate-capability | {context:Context,model:Model,generation:Generation} | 200 Capability | 400 UNSUPPORTED_CAPABILITY;503 MODEL_NOT_READY |
| AI POST /ai/models/cost-estimate | {context:Context,model:Model,max_audio_seconds:Decimal} | 200 {estimated_cost_usd:USD} | 503 MODEL_NOT_READY/DEPENDENCY_UNAVAILABLE |
| AI POST /ai/speaker/{profile_id}/purge | {context:Context,command_id:ID} | 202 Cleanup | 409 RESULT_CONFLICT |

Internal common401 invalid service identity,403 unauthorized service/context,400 parsing,404 unknown resource,503 DEPENDENCY_UNAVAILABLE/DEADLINE_EXCEEDED. Commands/callbacks idempotent by target/operation/command_id:matching semantic payload returns original result,changed409 RESULT_CONFLICT. Public state transitions constrain callbacks except the narrowly authorised Q13 accounting-only reconciliation below. Reservations bind original owner/job, one durable quantity outcome and one known-cost settlement; matching repeats never double charge or release resources twice. Completion publishes after durable terminal winner/settlement. Revoked stale execution/publication callback409 and temporary outputs purged; only the Q13 accounting-only exception can settle retained incurred-cost exposure after revocation. Already-purged cleanup succeeds original Cleanup. AI obtains authorized sample bytes via Artifact boundary;conditioning only after enrolling authorization/override,only model-required material. Conditioning independently revalidates samples against the profile's selected Model and live safety/readiness, rather than treating the upload admission model as permanent binding (Q12). Worker stores final output through Artifact;AI/Worker have no public API. Service access to Artifact content uses authenticated service identity and authorized Context in place of public Bearer,requires active matching consent/profile/job and permits only AI sample reads or Worker source-audio reads;it never exposes a public service credential. Internal binary responses obey the same duration/format bounds. Complete callback requires nonempty complete mapping and available matching owner/profile/job artifacts;invalid ranges or associations400 INVALID_INPUT. Artifact store may create inaccessible staged binary;only the durable completed winner makes it publicly available.

#### Q13 reservation and terminal accounting commands

All four changed rows retain closed input objects and existing parsing/errors. command_id and acceptance_created_at are required where declared: missing/null/blank/wrong-type/malformed values use existing 400 INVALID_INPUT. In Jobs fail and Policy release, cost remains a required field; explicit null means measurement unavailable, omission is invalid. Completion and commit-usage still require known nonnull Cost and successful duration/output/terminal-winner validation.

Only the trusted Jobs owner supplies acceptance_created_at: the stable server-authored fact is exactly the immutable Acceptance.created_at used if admission succeeds. Preserve it through retries and carry it in Policy reserve rather than substitute Policy's receipt clock, infer time from opaque IDs or share owner databases. Public callers cannot supply this read-only timestamp in Generation; no public response/configuration field is added. A reservation is tied to its original owner/job and acceptance fact. Matching semantic reserve across command IDs returns the same reservation; changed timestamp/bound/estimate for that bound job returns existing409 RESULT_CONFLICT. Preacceptance rejection and one-durable-admission-outcome rules remain.

A reservation has one durable quantity terminal winner: successful commit or unsuccessful release. Commit after a released outcome and release after a committed outcome return409 INVALID_STATE; neither can reverse that winner or publish output. Within the committed outcome, a fresh command repeating identical known Cost and measured audio has no additional effect; changed known Cost or measured duration returns409 RESULT_CONFLICT.

A terminal failure/cancellation/timeout can release unfinished concurrency and unused quantity reservation even when actual cost is unknown. Keep its estimated monetary hold and Job.measured_cost null until trusted measurement; a stopped job is not kept indefinitely active solely to obtain Cost. A later known Cost reconciles the released-unknown reservation through Policy release with a fresh command_id, removing that hold and recognising one cost without releasing quantities/concurrency again. Within a released outcome, a fresh command carrying the identical already-known final Cost is a no-charge repeat; different known Cost conflicts. A fresh null release after that released outcome already has known Cost returns200 Usage with no effect: retain the known settlement, do not recreate its hold or release resources twice. This rule does not permit release after successful commit. Same-command payload changes remain conflicts, including known-to-null changes.

For a reused Policy command_id, the original semantic payload and original content-free accounting response are required; changed payload409 RESULT_CONFLICT. Reusing a null release's command_id with known Cost is a conflict, not reconciliation. A same-command replay of the original null release after later reconciliation returns its original recorded Usage snapshot but cannot downgrade the actual known state or restore a hold. A fresh command's no-effect semantic repeat returns the Usage snapshot observed for that new command, and its own replays return that recorded snapshot. Current protection always uses current durable owner facts, not a historical replay response. Recognition month and forecast-event deduplication stay bound to the first durable known settlement, never replay time.

These response-replay rules do not authorise an account-lifetime cache of private full Job responses. Ordinary Jobs callbacks, including fail, recheck live identity/context/content fences before returning private data: retained revoked work retains its409 fence and purged Job404 remains even for an otherwise matching old command. Any private response material follows that Job's content retention/purge. Only defined Policy accounting responses and minimal accounting fact references may survive under Q13; late known cost goes to Policy release, not Jobs fail. No replay can restore purged history, expose a script or extend private access.

The late-cost route is Policy release returning Usage, not Jobs fail returning a recreated full Job. The sole terminal/revoked/purged exception requires a configured accounting-authorised service identity, the original authorised owner/work reference, matching retained reservation/job and valid metering evidence. It permits bookkeeping only. It cannot infer, publish, read voice content, restore grants/content, resume execution or bypass consent for another purpose. No arbitrary public actor/ownership assertion is trusted. Malformed IDs400, unknown retained accounting references404 and foreign/unauthorised context403 remain; a purged private Job does not turn a known matching accounting reference into unknown. Unavailable protection/accounting fails closed under existing503 semantics.

Known-cost usage.recorded facts may update only retained operational Job.measured_cost. After purge, legitimate original-work facts are durably acknowledged/deduplicated without recreating history, so Job GET stays404 and public idempotency replay returns only its original Acceptance. A genuinely unknown/unrelated fact retains normal rejection. Raw measurement/reconciliation collaborator mechanics belong to the Implementation Plan and may supply cost evidence, not final Job/Usage decisions or fabricated zero measurements.

### Work commands/domain facts (Message or stream)

Durable broker,not browser WebSocket. Credentials at connection and delivery;least privilege/encrypted deployment. Closed envelope={message_id:ID,type:Text,schema_version:1,owner_id:ID,actor_id:ID-or-null,resource_id:ID,occurred_at:Time,sequence:Pos,request_id:ID,payload:object}. Sequence per resource,not global. No scripts/audio/consent text/secrets in facts. Payload fields exhaustive.

| Type / producer | Payload | Consumers |
| --- | --- | --- |
| voice_profile.enroll / Voices | {profile_id:ID,model:Model} | Worker validates active profile/consent |
| narration.generate / Jobs | {job_id:ID,reservation_id:ID,deadline_at:Time} | Worker retrieves current work-item |
| consent.recorded / Consent | {consent_id:ID} | Audit |
| consent.revoked / Consent | {consent_id:ID,cleanup_id:ID} | Voices/Jobs/Artifact/AI linked purge/cancel;Audit |
| voice_profile.enrolled / Voices | {profile_id:ID} | Audit |
| voice_profile.quality_warning / Voices | {profile_id:ID,assessment_id:ID} | Audit;UI polls Profile |
| voice_profile.enrollment_failed / Voices | {profile_id:ID,code:Text} | Audit |
| voice_profile.revoked / Voices | {profile_id:ID,cleanup_id:ID} | Jobs/Artifact/AI cancel/purge;Audit |
| narration_job.submitted, narration_job.started / Jobs | {job_id:ID} | Audit |
| narration_job.completed / Jobs | {job_id:ID,artifact_id:ID} | Audit |
| narration_job.failed / Jobs | {job_id:ID,code:Text} | Audit |
| narration_job.cancelled / Jobs | {job_id:ID} | Audit |
| artifact.stored / Artifact | {artifact_id:ID} | Audit |
| artifact.deleted / Artifact | {artifact_id:ID,cleanup_id:ID} | Jobs/Voices invalidate references;Audit |
| quota.exceeded / Policy | {job_id:ID,code:Text} | Audit |
| budget.exceeded / Policy | {job_id:ID} | Audit |
| budget.forecast_alert / Policy | {forecast_usd:USD,target_usd:USD} | operator alert consumer;Audit |
| usage.recorded / Policy | {job_id:ID,cost:Cost} | Jobs retained measured-cost update or legitimate original-work ACK after purge, without resurrection;Audit |
| access_grant.changed / Auth | {grant_id:ID,revoked:boolean} | Audit |
| configuration.changed / Policy | {revision:Nat} | services refresh policy;Audit |
| model.approval_changed / AI | {model:Model,enabled:boolean} | Voices/Jobs/Worker;Audit |
| auth.account_registered, auth.email_verified / Auth | {user_id:ID} | Audit |

At-least-once;producer durably binds state+message before acknowledgement;consumer durably deduplicates message_id before ACK. Execution commands are valid only for unfinished current authorised work;duplicates reuse result. Q13 permits only the accounting-only late-cost command and known usage.recorded fact exception described above; it never revives work or weakens synthesis/publication fences. Out-of-order facts reconcile current owner state and never restore access. Invalid bytes/schema/type/payload→terminal INVALID_MESSAGE;unauthorized producer→FORBIDDEN;unknown resource→NOT_FOUND (already-purged cleanup succeeds; known original-work Q13 accounting facts may be acknowledged after private-history purge without recreation);incompatible transition→INVALID_STATE. Terminal quarantine/operator signal without private payload. Dependency failure transient DEPENDENCY_UNAVAILABLE,configured bounded retries/deadline;exhaustion RETRY_EXHAUSTED marks affected job/profile/cleanup failed,never indefinitely active. Configured byte/rate/inflight bounds,backpressure stops admission,producers retain durable unsent work. Disconnect reconnects under retry policy;unacked redelivers. No application ping/close codes (not socket/RPC);broker keepalive mechanics left implementation planning. Audit consumes facts,eventual/nonblocking,no public ingestion. No account-deletion capability/message introduced.

## Contract-Wide Rules

- Parsing: UTF-8 application/json except explicit multipart/binary. Malformed bytes/JSON/percent encoding,duplicate keys/parts/scalar params,wrong types/content types,unknown/read-only fields/query/parts,body on none→400 INVALID_INPUT. No coercion. Over limit400 LIMIT_EXCEEDED.
- Absent/null/blank: required missing/null/empty/whitespace-only400. Optional may omit,never null. Literal null only declared. Empty arrays invalid for sample/grant/evidence/capability languages/styles/formats/materials/guidance;valid for pages,regenerated_chunk_ids and nonpublished mapping metadata. Findings exactly six. Arrays distinct unless ordered measurement collection. Text whitespace preserved except normalized email;blank detection does not rewrite scripts. False/zero valid where range allows.
- Numeric: exact decimal arithmetic;measure conversions half-even to six places;USD exactly six,total=sum displayed compute+storage. Seconds/Hz/bytes explicit;Range min≤default≤max,step>0,grid `(value-min)/step` integer. Positive audio/limit durations;offset/meter zero valid. Estimates distinct from measurement. Only enrollment_quality threshold Decimal inputs use the explicitly defined finite JSON-number exception above; all other Decimal wire fields remain strings.
- Collections/matching: Page rules;exact case-sensitive enum/ID/version/filter except email. Unknown filter400,no partial search. Samples input order,chunks source order,findings declared order;other capability/grant arrays unspecified. Bulk arrays bounded configured message/sample/script limits.
- Identity/access: malformed UUID400,unknown404,existing foreign403 generic body/no private values. Lists owner-only;owner_id allowed for Administrator only with live matching grant,otherwise403. Role never private access. Revoked retained409 CONSENT_REVOKED,purged404. Cleanup read owner-only. Retrieval rechecks owner authorization or explicit live scoped administrator authorization. The Q13 accounting-only exception concerns matching retained bookkeeping references, never private retrieval, grants or resumed execution.
- Mutation: POST create/actions,PUT whole replacement,PATCH quality action only. IDs/owner/consent contents/creation times/job snapshots immutable. Delete202 distinct cleanup completion.
- Errors: JSON `{error:{code:Text,message:Text,details:{field:Text,constraint:Text}[],request_id:ID,timestamp:Time}}`;details=[] permitted. Status/code normative,prose informative,no private echo. All rows inherit400 INVALID_INPUT/LIMIT_EXCEEDED,401 UNAUTHENTICATED,403 FORBIDDEN,404 NOT_FOUND,409 INVALID_STATE,429 RATE_LIMITED,503 CONFIGURATION_REQUIRED/DEPENDENCY_UNAVAILABLE. Specific row codes refine mapping. Unexpected runtime503 INTERNAL_UNAVAILABLE. 429 Retry-After positive integer until policy opportunity(window reset/active deadline);503 only when known. Authentication before private lookup;syntax may fail earlier without lookup.
- Transport: encrypted deployed transit/rest,private storage,managed secrets,least privilege per FR-046;HTTP only loopback local. No provider keys/storage paths exposed. Authorization uncertainty fails closed503;fences independent of events.
- Versions: /api/v1,/internal/v1 and message schema_version1 retained;unknown version rejected,no silent reinterpretation. Q13 intentionally revises the listed internal required inputs/null semantics under this reviewed amendment; old omitted fields are not silently defaulted. Later incompatible change requires reviewed contract process.

## Decisions Resolved

| Decision | Resolution | Source |
| --- | --- | --- |
| Enrollment/routes/callbacks | Consent→authorized artifact→async profile;artifact links;/quotas/me;internal callbacks | Q5 |
| Retry scope/comparison/replay/expiry | Mandatory header;effective input;durable original acceptance;account-lifetime minimal record | Q6 |
| Failure mapping | Common 400/401/403/404/409/429/503 body/codes | Q7 |
| Schemas/limits/lists/money | Closed types,configured/model bounds,cursor/exact filters,six-place half-even USD | Q8;delegation |
| Jobs/regeneration/deletion/retrieval | Durable winner,new child/chunk joins,202 cleanup,live fence | Q9;FR-022–028 |
| Accounts/grants/transport | User registration,separate admin,configured lifetimes,scoped expiring grants,encrypted deployment | Q10 |
| Model/style/controls/materials | Evidence gate,neutral/mapping/basic controls,model-minimal artifacts | FR-013/021/026/041;R-EXP/R-LIC;Plan |
| Quota/budget/retention configuration | Named Configuration,atomic reservations,approved defaults,operator bounds | Q1–4/Q8;FR-044;R-RET/R-GEN |
| Internal consumers | Nine owners,normalized HTTP/messages,current authorization,duplicate-safe settlement | Plan External Contract Requirements;nine-service decision;delegation |
| Enrollment quality configuration and validation | Exact closed enrollment_quality fields; finite JSON-number threshold exception; existing configuration authorization/CAS/errors/publication | requirements.md Q11;approved proposal Exact proposed Configuration contract delta;Plan milestone 8 |
| Enrollment readiness/calibration binding | Only dependent enrollment unavailable with existing configuration/dependency codes until applicable accepted settings/evaluator-bound calibration and evaluator readiness; no hidden defaults | requirements.md Q11;approved proposal configuration/warning/calibration sections;Plan milestone 8 |
| Audio stream selection | Default stream, otherwise lowest-index decodable stream; same selection throughout; private index/original preserved | requirements.md Q11;approved proposal measurement policy;Plan milestone 8 |
| Assessment provenance/reassessment | Private revision/evaluator/calibration binding; reassess obsolete unfinished policy before override; stale old IDs; history and semantic repeat preserved | requirements.md Q11;approved proposal warning section;Plan milestone 8 |
| Upload model selection and failure mapping | Required multipart model_id/model_version map to Model; invalid parts 400 INVALID_INPUT; well-formed unknown/unapproved/unavailable model 503 MODEL_NOT_READY; existing audio/limit/consent errors retained | requirements.md Q12/FR-010;Enrollment-Interface-Completion-Proposal.md C;Plan milestone 12 |
| Guidance, duration and sample reuse | Select model/guidance before recording/upload; enforce selected-model/configuration bounds with active owner consent before acceptance; independently recheck profile-selected model at admission/conditioning; no permanent binding, new response field or output-format input exclusion | requirements.md Q12/AC-ENR-001;approved proposal C;Plan milestone 12 |
| Pagination source and catalog order | Existing limits.page_default/page_max source, no hidden defaults; trusted enabled/approved catalog order uses persisted Approval time/model identity; consumer preserves authenticated snapshots; no new Capability timestamp or public callable contract | requirements.md Q12/FR-012;approved proposal A/B;Plan milestone 12 |
| Quantity periods and canonical admission fact | Original Acceptance.created_at and request receipt project selected epoch interval; active concurrency spans intervals; trusted Jobs carries acceptance_created_at to Policy | requirements.md Q13 quantity rules; Q10 drafting delegation; Plan milestone 16 |
| Money view and budget month | Outstanding holds plus known costs first durably recognised by Policy in current UTC month; original source measured_at preserved; unchanged forecast | requirements.md Q13 budget rules; approved proposal section 2 |
| Unknown cost and command identity | Required nullable fail/release cost, required IDs on all three Policy mutations, one fresh-ID null-to-known reconciliation and no duplicate settlement | requirements.md Q13 terminal-cost rules; approved proposal section 3 |
| Terminal/purge accounting authority | Narrow original-work metering exception, fresh configured-bounded deadline, retained-only Job cost update or legitimate fact ACK without resurrection | requirements.md Q13 terminal-cost rules; Plan milestone 16 |
| Content-free metadata lifetime | Only approved minimum accounting/request/dedup facts for account lifetime; no private content, no new audit/voice retention, exact larger-window reprojection | requirements.md Q13 metadata rules; approved proposal section 4 |

## Compatibility Notes

The complete approved Q12 baseline is carried forward except the enumerated Q13 changes and necessary references. Public schema field names/types, Configuration shape, endpoint catalogue, common status/error codes, numeric precision, $20 target, model/calibration/consent gates and all Q11/Q12 enrollment behavior remain. Usage values now have explicit quantity-window versus budget-month meaning; clients must not label its monthly money fields as quota-window charges.

Internal input compatibility intentionally changes: reserve/commit/release now require command_id, reserve additionally carries trusted acceptance_created_at, and fail/release permit explicit unknown-cost null while remaining required fields. Missing new required fields and unknown/read-only fields remain400; there is no default/legacy reinterpretation. Producers/consumers must be brought into line through their reviewed executable milestones. No source migration or rollout is executed by this document. The canonical admission timestamp is an internal representation of the already approved immutable Acceptance.created_at fact, not a new user choice or public field.

Implemented/executed-work impact, inspected 2026-10-29 UTC: current voice_narration/jobs/application.py contains noncontract input names (script_body/model_id/parameters/body idempotency_key), a 60-second in-memory idempotency cache, pending/processing/complete states, a script-length duration heuristic, float/zero-cost fields and a 200 replay path (notably lines 17,27–55,71,91–101). Its existence is recorded; it is not adopted as contract authority or claimed passing implementation. Policy currently has __init__.py and retention persistence, not a Policy application at this inspection. External tests/test_job_orchestration.py and 016/017 prototype plans are preserved inputs; their fixture, schema, policy and approval-history claims are not accepted as approved requirements, valid RED or verified completion in this workflow. Mutable source is an as-of observation; future implementation planning must reinspect it.

Completed milestones 1–15 and their evidence remain intact. Completed enrollment/persistence/Auth checks do not establish Q13 generation accounting. The approved delivered cohort remains 97 tests; this is not an assertion that every current external test file is approved/passing. Existing Job RED/GREEN own the new reviewed verification/delivery after this contract's approval, including actual source/prototype divergence. No extra completed-alignment milestone or source fix is asserted here.

Historical Q12 impact remains as recorded in completed Plan milestone 12/RED012/OTHER014/GREEN015: selected-model upload, explicit pagination/catalog seams and playback wiring were separately reviewed and verified. Earlier Q11 findings and original approval history remain historical; they are not current claims that delivered enrollment modules are absent.

## Amendments

The Q11/Q12 rows below are historical records, including their then-pending milestones and then-current impact observations. They do not change current stage numbers or imply that those stages are still pending. The Q13 row is the current amendment under review.

| Change | Reason and evidence | Impact | Executed milestones encoding the old decision |
| --- | --- | --- | --- |
| Q11 enrollment_quality configuration/readiness, stream selection and private provenance/reassessment delta | Approved requirements Q11 and proposal (2026-10-25); revised Plan milestone 8 explicitly authorizes amendment of the 2026-10-24 contract before pending enrollment work | Required operator subsection and enrollment-only readiness gate; deterministic stream and stale-assessment behavior; unaffected baseline carried forward. Amendment approved 2026-10-25; see Contract Review Status | None found: delivered Policy retention subsection, Auth subset and generic Consent saves do not encode amended decisions; completed 001–008 history remains unchanged |
| Q12 explicit selected-model upload and guidance/reuse/readiness cross-references; existing pagination source/catalog-order clarification | Approved requirements Q12, proposal A–C and revised Plan milestone 12; inspected current upload and Voices fixture inputs in tests/test_voice_enrollment.py | Intentional required-input revision; response shapes, endpoints, existing errors, formats and Q11 rules retained; no production retrofit. Approved 2026-10-26; see Contract Review Status | Completed 010 upload helper/flows and 011 listing/Voices fixture encode incomplete inputs/order guarantees; pending milestone 13 owns new reviewed test/interface changes; their historical records remain intact |
| Q13 quantity/budget periods, unknown terminal cost, command identities/reconciliation and minimum accounting metadata | Approved requirements Q13 and accounting proposal; approved Plan milestone 16 starts from verified approved Q12 bytes | Internal required-input change and explicit Usage/cost/retention semantics; no public/configuration field or readiness gate change. Awaiting human review | No approved completed generation-accounting milestone in this workflow; completed 1–15 evidence unchanged. Current external Jobs/test/016/017 inputs require review under pending Job RED/GREEN, not inferred approval |

## Contract Completeness Check

Documentation-only self-check against the complete written contract, approved Q13 requirements/proposal and Plan milestone 16; not human approval or runtime evidence. Exactly one row per api-design question.

| Question | Evidence |
| --- | --- |
| 1. Input parsing | Shared closed schemas and common malformed/type/unknown rejection remain. Four internal rows explicitly list all changed inputs; canonical command IDs and trusted acceptance_created_at are required; existing400 mapping applies. |
| 2. Absent/null/empty/blank | Existing rules remain. Only Jobs fail/Policy release cost is explicitly Cost-or-null, still required; omission invalid. Complete/commit cost nonnull. Unknown means unmeasured, never zero. |
| 3. Read-only/unknown fields | Public Generation remains unchanged/closed; clients cannot supply acceptance_created_at or an accounting month. Only trusted Jobs supplies the required internal fact; no new public/config field. |
| 4. Numeric semantics | Original exact six-place half-even USD/Decimal rules unchanged. Quantity epoch formula, original admission attribution, quota reprojection, monthly first recognition, all outstanding holds and exact existing forecast are explicit. Original measurement time and aggregate observation time are distinguished. |
| 5. Collections | All baseline page/sample/finding/chunk orders, empties and bounds remain. Q13 adds no collection/sort interface; ledger physical representation is not prescribed. |
| 6. Matching/filtering | Existing exact canonical ID/enum/version/filter matching remains; reserve binds original owner/job/admission fact; same-ID payload comparison and fresh-ID semantic repeats/conflicts are explicit. No partial lookup or period-selector field added. |
| 7. Errors | Existing normative body/status codes remain. Invalid changed inputs400; unauthorised service/context401/403; unknown bookkeeping reference404; state/payload/known-cost conflicts409; missing protection503. No new error code or fake-cost success. |
| 8. Identity/existence | Original-work owner/reservation/job and accounting-authorised service must match. Purged private history stays404; a known retained accounting reference permits only defined bookkeeping, not private reads or inference. Unknown unrelated facts retain rejection. |
| 9. Mutation semantics | Public snapshots/state rules unchanged. Commit/release have one quantity winner; opposite terminal action409, identical repeats no-charge, conflicting known settlement409. Fresh null after known release is200/no effect; same-ID payload changes409. Original Policy accounting responses are scoped apart from private Jobs responses, which retain live fences/purge. Retained Job cost may update; purged Job never recreated. |
| 10. Internal consistency | Checked Q13 Usage, jobs/cancel/timeout, bounds/forecast/retention, four changed rows, terminal winner/null replay, private response purge, deadline/context exception and usage.recorded against Q13/Plan scope. Only Policy bookkeeping replays survive; no shared-owner transaction, private Job lifetime cache or new execution authority. |
| 11. Authority | Plan remains scope/milestone authority. Milestone16 delivers only this contract; human approval is pending. Existing Job RED/GREEN own tests/behavior; unreviewed prototypes and commit titles are not approval or passing evidence. |

Revision self-check: compared against the retained SHA256-identified Q12 bytes; only Q13 scope/baseline/delta/traceability, accounting meanings, affected lifecycle/protection/retention/internal rows/common references, usage fact consumption, decisions/compatibility/amendment/check/review metadata changed. Unrelated carried sections and every public schema/operation row are checked as raw bytes. No new public/configuration field, tariff, validation threshold, model duration, time default, training approval or enablement is introduced. Exactly eleven completeness rows, one current Contract Review Status and no template comments. No test, package, Docker, service, database, model or calibration operation was executed for this documentation work.

Actual static verification: approved Q12 baseline hash matched d1ccccaee8073f75f9987a137d85319afb28271dd882d1f40d28b4de437060b4; exact baseline copy retained as above. All 79 protected source/test/configuration/authority files matched the pre-edit manifest before this write. All 56 HTTP operations are retained; exactly four internal input rows changed and all 37 public operation rows are byte-identical. Raw-byte equality verified for Out of Scope, all shared public schemas, Accounts, complete Enrollment, Artifacts and operator configuration/Q11 rules; prior Q11/Q12 amendment rows remain exact. The verification manifest records the byte counts/hashes. These are documentation/provenance checks only, not runtime or contract approval.

## Contract Review Status

- Status: Approved by avinash2196 on 2026-10-28 (America/Chicago), recorded 2026-10-29T01:53:20Z — Q13 Job Accounting Contract Amendment (Plan milestone 16).
- Approval history: original contract approved by avinash2196 on 2026-10-24; Q11 amendment approved 2026-10-25T21:30:20Z; complete Q12 amendment approved 2026-10-26T17:39:41Z. These are baseline history, not approval of Q13.
- The main conversation recorded this exact contract's approval and marked milestone 16 complete at the user's word. Dependent Job Implementation Plans may now be prepared; each executable milestone retains its own human-review gate. No installation, calibration, model enablement or provisioning is approved here.
