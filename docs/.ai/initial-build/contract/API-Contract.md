# API Contract — initial-build

## Contract Scope

Defines public HTTP and stable internal service/message behavior only. [Plan.md](../Plan.md) remains authoritative for scope, milestones and ownership. Concrete schemas/configuration names exercise the user delegation recorded after Q10 in [requirements.md](../requirements.md), and return for human review.

## Baseline

None — new contract. Previous content was an unapproved draft, not published behavior. Requirements approved 2026-10-19; retained P0 and Q5–Q10 recorded 2026-10-24; revised Plan approved 2026-10-24. Plan Current State establishes no implementation. Nine-service deployment shape is approved; remaining architecture details are not.

## Changes in This Work Item

Not applicable — new contract. Revision provenance: replaces the unapproved draft's inline enrollment, job-based downloads, optional/body idempotency keys, retry expiry, offset pagination and arbitrary fixed limits. Adds schemas, async cleanup/enrollment, live authorized artifact access, regeneration/mapping, model/policy configuration and stable service consumers. No approved contract amended.

## Out of Scope

Requirements Explicit Exclusions apply. Advanced emotion/per-line pronunciation and P1 history search/rename excluded from this delivery. No model, evaluation threshold, stack or paid environment selected. Model values follow approved feasibility; failure to support P0 stops that gate.

## Requirement Traceability

| Capability | Source |
| --- | --- |
| Accounts/private grants | R-ACCT-001–003;Q10 |
| Consent/sample/enrollment/quality | R-CONS-001/002;FR-010–013;Q5 |
| Revocation/cleanup/retention | R-REV-001;R-DEL-001;R-RET-001/002;Q9 |
| Text/style/controls/chunks | FR-020/021/025–028;R-EXP-001 |
| Jobs/history/retries/cancellation | FR-022/023/045;Q6/Q9 |
| Preview/export/regeneration | FR-024/028;Q9 |
| Quota/cost/configuration | R-GEN-001;FR-044;NFR-008;Q8 |
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

`A-or-B` denotes the named JSON string enum alternatives, except `-or-null` permits literal JSON null. `Page<T>={items:T[],next_cursor:Text-or-null}`; `List` query=`cursor?:Text,limit?:Pos`. Configured default/max page size. Opaque authenticated cursor binds principal/filters/stable snapshot fixed on first page; altered/incompatible cursor400 INVALID_CURSOR. All pages descending created_at then resource ID (Audit occurred_at/event_id;models approval timestamp then model_id/version from Approval); Chunk pages ascending index. Empty `{items:[],next_cursor:null}`. No offset/arbitrary sort. Model approval timestamp is the persisted approval time,not an additional Capability input.

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
| POST /artifacts/upload | multipart/form-data consent_id:ID,file:binary | 201 sample Artifact | 400 INVALID_AUDIO/LIMIT_EXCEEDED;409 CONSENT_REVOKED;503 MODEL_NOT_READY |
| POST /voices | JSON {name:Text,language:Lang,consent_id:ID,sample_artifact_ids:ID[],model:Model} | 202 pending Profile | 400 UNSUPPORTED_CAPABILITY;409 CONSENT_REVOKED/ARTIFACT_UNAVAILABLE;503 MODEL_NOT_READY |
| GET /voices | List;status?:ProfileState,language?:Lang,owner_id?:ID | 200 Page<Profile> | common |
| GET /voices/{profile_id} | owner_id?:ID | 200 Profile | common |
| PATCH /voices/{profile_id}/quality-override | JSON {assessment_id:ID,acknowledged:true} | 200 enrolling Profile | 409 STALE_ASSESSMENT/OVERRIDE_NOT_ALLOWED/INVALID_STATE |
| DELETE /voices/{profile_id} | none | 202 Cleanup | common |
| GET /cleanups/{cleanup_id} | none | 200 Cleanup | common |

Assisted=true requires authorization; false rejects authorization. Immutable consent contents; association Profile.consent_id. Validate active owner consent before sample bytes used/persisted; unauthorized streams discarded. WAV audio/wav,MP3 audio/mpeg,M4A audio/mp4 must match actual decodable bytes. Empty/corrupt/unsupported/oversized/out-of-duration400. Browser recordings use accepted formats. Configured count/byte and approved model duration limits apply. Sample refs nonempty/distinct/available/owner-owned/same active consent; response samples input order.

ProfileState: pending→quality_checking→enrolling→enrolled; warning path quality_checking→awaiting_user_override→enrolling. Hard/execution failure→failed with actionable Failure; any nonrevoked state→revoked. Quality has all six check findings once in declared order. Override only current overrideable warning after informed acknowledgement; matching repeat returns current Profile without duplicate enrollment. Only model-needed materials persist; no training promise. Capability returns recording guidance. Null quality/failure before available.

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

Acceptance durably snapshots effective script/profile/model/version/parameters and reserves policy before dispatch. Profile enrolled,consent active,model approved/enabled required. JobState: queued→preparing→running→post_processing→completed; any unfinished state may fail/cancel. No backwards moves. Completion/cancellation one durable winner: cancelled winner denies output publication; completed winner cancel409. Repeated cancellation returns cancelled Job. Timeout→failed JOB_TIMEOUT. Bounded attempts remain one job/deadline; no duplicate final artifacts/accounting. Unused reservation released; measured incurred costs remain.

Snapshots immutable; operational status/output/timestamps/failure/cost may change. Before completion output/duration/completed_at null,mapping_available=false; failure nonnull only failed. Measured cost null until measured, not fabricated zero. History retention cannot override revocation/purge; purged history404.

Regeneration requires completed available authorized source, creates new child preserving original. Inherit profile/language/model and omitted script/style/controls; supplied whole values replace. Empty body whole regeneration. Supplied chunk_ids nonempty/distinct/source-owned; section capability required; script replacement disallowed with chunk_ids. Process chunks in original index order. Section result preserves unchanged source audio and supplies joined_preview_artifact_id for explicit join review; whole result joined preview null. Original remains intact subject to deletion/retention.

Chunks half-open Unicode scalar text offsets and half-open audio seconds in assembled WAV; indices start0. Text coverage complete/ordered/nonoverlapping, never midword; punctuation/newlines pause cues. Actual join has no clicks/dropouts/repeated words/unintended gaps and stable loudness/sample rate/identity under approved protocol. Mapping only once complete; not-ready409 rather than misleading empty result.

#### Durable idempotency (Q6)

Mandatory nonblank opaque header bounded by configured bytes, never body field. Scope authenticated owner plus create_job/regenerate_job operation. Fingerprint parsed effective input, pinned model/defaults and regeneration source ID. Object order/chunk selection order irrelevant; exact script significant; equivalent Decimal values equal. Replay omissions resolve original pinned defaults despite later configuration changes. Identical concurrent/restarted submissions return original202 Acceptance (queued/original time), not current status; clients poll. Changed input409. Admission,key binding,reservation one durable outcome; preacceptance rejection binds no key. Minimal key/fingerprint/job-reference/acceptance-time record lasts account lifetime including after deletion, without script/audio. Replay after purge returns original Acceptance, never execution/charge; GET purged job404. Authentication still required; replay restores no content. New key is new request subject to current policy.

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

All fields required except stated defaults;no hidden token/link/rate/upload/retry/model defaults. Secret-resolution failure disables dependency. Deployed encrypted transport;HTTP only local loopback. Day86400 seconds;retention from creation/event occurrence. Artifact.expires_at=created_at plus sample_days or generated_audio_days as appropriate (joined preview uses generated policy);shortened policy updates recompute expiry and fence already-expired resources. Profile/consent expiry triggers revocation;sample expiry revokes linked profile;generated expiry deletes audio only. Retention never delays requested purge or means indefinite consent/audit storage.

Effective script/output/sample bounds minima of configuration,approved model,available quota. Admission reserves maximum effective output duration;completion replaces reservation with measured duration/releases remainder. Quota windows UTC epoch-aligned window_seconds. Request count counts authenticated requests;accepted generation/reservation counted once,replay no duplicate generation. Concurrency all unfinished accepted jobs. Timeout spans preparation through postprocessing;max_attempts includes initial;retry cannot extend deadline. Budget UTC month,measured+reserved estimated cost;kill switch or reservation crossing stop_usd503 BUDGET_STOPPED before further work. Forecast=month-to-date measured spend×month duration/elapsed duration (at start measured);crossing alert emits operator metadata. $20 target not guarantee/per-user allowance. Approved model evidence supplies tariffs/estimates;missing dependency503 rather than free execution.

### Stable internal HTTP interfaces

Nine owners: Auth identity/grants;Consent authorization;Voices profile/quality;Jobs durable orchestration;Artifact binaries;Policy reservations/usage;AI approved models/conditioning;Worker asynchronous execution;Audit immutable metadata. No direct cross-owner persistence. Gateway infrastructure not tenth domain service. Worker reports callbacks;owners publish facts. Normalized interfaces stable across mock/local/cloud adapters.

Service identity authenticated with configured least privilege;deployed transport encrypted. Required X-Deadline:Time future and bounded by configured/job deadline. Context={owner_id:ID,actor_id:ID,request_id:ID} must originate from authorized work,never arbitrary user ownership assertion. Revalidate consent/current authorization before inference and publication;event delay cannot weaken immediate fence.

| Target method/path | Required input JSON except stated | Success | Specific failures |
| --- | --- | --- | --- |
| Auth POST /auth/verify-token | {token:Text} | 200 Account | 401 UNAUTHENTICATED |
| Consent POST /consent/validate | {context:Context,consent_id:ID} | 200 active Consent | 409 CONSENT_REVOKED |
| Voices POST /voices/validate | {context:Context,profile_id:ID,purpose:enrollment-or-generation} | 200 active Profile;generation requires enrolled,enrollment permits pending/quality_checking/enrolling | 409 PROFILE_NOT_READY/CONSENT_REVOKED |
| Voices POST /voices/{profile_id}/enrollment-result | {context:Context,command_id:ID,expected_status:ProfileState,status:ProfileState,quality:Quality-or-null,failure:Failure-or-null} | 200 Profile | 409 INVALID_STATE/RESULT_CONFLICT |
| Jobs POST /jobs/{job_id}/work-item | {context:Context,command_id:ID} | 200 {job:Job,deadline_at:Time,reservation_id:ID} | 409 INVALID_STATE/CONSENT_REVOKED |
| Jobs POST /jobs/{job_id}/status | {context:Context,command_id:ID,expected_status:JobState,status:preparing-or-running-or-post_processing} | 200 Job | 409 INVALID_STATE/RESULT_CONFLICT |
| Jobs POST /jobs/{job_id}/complete | {context:Context,command_id:ID,output_artifact_id:ID,joined_preview_artifact_id:ID-or-null,duration_seconds:Decimal,chunks:Chunk[],cost:Cost} | 200 completed Job | 409 INVALID_STATE/RESULT_CONFLICT;400 OUTPUT_LIMIT_EXCEEDED |
| Jobs POST /jobs/{job_id}/fail | {context:Context,command_id:ID,failure:Failure,cost:Cost} | 200 failed Job | 409 INVALID_STATE/RESULT_CONFLICT |
| Artifact POST /artifacts/store | multipart context:Context JSON,command_id:ID,profile_id:ID,job_id:ID,kind:generated-or-joined_preview,file:binary WAV | 201 Artifact | 400 INVALID_AUDIO/OUTPUT_LIMIT_EXCEEDED;409 CONSENT_REVOKED/RESULT_CONFLICT |
| Artifact POST /artifacts/metadata | {context:Context,artifact_id:ID} | 200 Artifact | 409 ARTIFACT_UNAVAILABLE |
| Artifact POST /artifacts/batch-delete | {context:Context,command_id:ID,artifact_ids:ID[]} | 202 Cleanup | 409 RESULT_CONFLICT |
| Policy POST /quotas/reserve | {context:Context,job_id:ID,max_audio_seconds:Decimal,estimated_cost_usd:USD} | 201 {reservation_id:ID} | 429 QUOTA_EXHAUSTED/CONCURRENCY_EXHAUSTED;503 BUDGET_STOPPED |
| Policy POST /quotas/commit-usage | {context:Context,reservation_id:ID,job_id:ID,audio_seconds:Decimal,cost:Cost} | 200 Usage | 409 RESULT_CONFLICT/INVALID_STATE |
| Policy POST /quotas/release-reservation | {context:Context,reservation_id:ID,job_id:ID,cost:Cost} | 200 Usage | 409 RESULT_CONFLICT/INVALID_STATE |
| AI POST /ai/enroll | {context:Context,command_id:ID,profile_id:ID,model:Model,sample_artifact_ids:ID[]} | 200 {quality:Quality,materials:Capability.enrollment_materials} | 409 CONSENT_REVOKED;503 MODEL_NOT_READY |
| AI POST /ai/infer | {context:Context,command_id:ID,job_id:ID,profile_id:ID,model:Model,text:Text,language:Lang,style:Text,controls:Controls-or-null} | 200 binary audio/wav;X-Duration-Seconds:Decimal,X-Sample-Rate-Hz:Pos | 400 UNSUPPORTED_CAPABILITY;409 CONSENT_REVOKED;503 MODEL_NOT_READY/BUDGET_STOPPED |
| AI POST /ai/models/validate-capability | {context:Context,model:Model,generation:Generation} | 200 Capability | 400 UNSUPPORTED_CAPABILITY;503 MODEL_NOT_READY |
| AI POST /ai/models/cost-estimate | {context:Context,model:Model,max_audio_seconds:Decimal} | 200 {estimated_cost_usd:USD} | 503 MODEL_NOT_READY/DEPENDENCY_UNAVAILABLE |
| AI POST /ai/speaker/{profile_id}/purge | {context:Context,command_id:ID} | 202 Cleanup | 409 RESULT_CONFLICT |

Internal common401 invalid service identity,403 unauthorized service/context,400 parsing,404 unknown resource,503 DEPENDENCY_UNAVAILABLE/DEADLINE_EXCEEDED. Commands/callbacks idempotent by target/operation/command_id:matching semantic payload returns original result,changed409 RESULT_CONFLICT. Public state transitions constrain callbacks. Reservations keyed job_id,one durable settlement;repeat never double charges. Completion publishes after durable terminal winner/settlement. Revoked stale callback409 and temporary outputs purged. Already-purged cleanup succeeds original Cleanup. AI obtains authorized sample bytes via Artifact boundary;conditioning only after enrolling authorization/override,only model-required material. Worker stores final output through Artifact;AI/Worker have no public API. Service access to Artifact content uses authenticated service identity and authorized Context in place of public Bearer,requires active matching consent/profile/job and permits only AI sample reads or Worker source-audio reads;it never exposes a public service credential. Internal binary responses obey the same duration/format bounds. Complete callback requires nonempty complete mapping and available matching owner/profile/job artifacts;invalid ranges or associations400 INVALID_INPUT. Artifact store may create inaccessible staged binary;only the durable completed winner makes it publicly available.

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
| usage.recorded / Policy | {job_id:ID,cost:Cost} | Jobs measured-cost update;Audit |
| access_grant.changed / Auth | {grant_id:ID,revoked:boolean} | Audit |
| configuration.changed / Policy | {revision:Nat} | services refresh policy;Audit |
| model.approval_changed / AI | {model:Model,enabled:boolean} | Voices/Jobs/Worker;Audit |
| auth.account_registered, auth.email_verified / Auth | {user_id:ID} | Audit |

At-least-once;producer durably binds state+message before acknowledgement;consumer durably deduplicates message_id before ACK. Commands valid only unfinished current authorized work;duplicates reuse result. Out-of-order facts reconcile current owner state and never restore access. Invalid bytes/schema/type/payload→terminal INVALID_MESSAGE;unauthorized producer→FORBIDDEN;unknown resource→NOT_FOUND (already-purged cleanup succeeds);incompatible transition→INVALID_STATE. Terminal quarantine/operator signal without private payload. Dependency failure transient DEPENDENCY_UNAVAILABLE,configured bounded retries/deadline;exhaustion RETRY_EXHAUSTED marks affected job/profile/cleanup failed,never indefinitely active. Configured byte/rate/inflight bounds,backpressure stops admission,producers retain durable unsent work. Disconnect reconnects under retry policy;unacked redelivers. No application ping/close codes (not socket/RPC);broker keepalive mechanics left implementation planning. Audit consumes facts,eventual/nonblocking,no public ingestion. No account-deletion capability/message introduced.

## Contract-Wide Rules

- Parsing: UTF-8 application/json except explicit multipart/binary. Malformed bytes/JSON/percent encoding,duplicate keys/parts/scalar params,wrong types/content types,unknown/read-only fields/query/parts,body on none→400 INVALID_INPUT. No coercion. Over limit400 LIMIT_EXCEEDED.
- Absent/null/blank: required missing/null/empty/whitespace-only400. Optional may omit,never null. Literal null only declared. Empty arrays invalid for sample/grant/evidence/capability languages/styles/formats/materials/guidance;valid for pages,regenerated_chunk_ids and nonpublished mapping metadata. Findings exactly six. Arrays distinct unless ordered measurement collection. Text whitespace preserved except normalized email;blank detection does not rewrite scripts. False/zero valid where range allows.
- Numeric: exact decimal arithmetic;measure conversions half-even to six places;USD exactly six,total=sum displayed compute+storage. Seconds/Hz/bytes explicit;Range min≤default≤max,step>0,grid `(value-min)/step` integer. Positive audio/limit durations;offset/meter zero valid. Estimates distinct from measurement.
- Collections/matching: Page rules;exact case-sensitive enum/ID/version/filter except email. Unknown filter400,no partial search. Samples input order,chunks source order,findings declared order;other capability/grant arrays unspecified. Bulk arrays bounded configured message/sample/script limits.
- Identity/access: malformed UUID400,unknown404,existing foreign403 generic body/no private values. Lists owner-only;owner_id allowed for Administrator only with live matching grant,otherwise403. Role never private access. Revoked retained409 CONSENT_REVOKED,purged404. Cleanup read owner-only. Retrieval rechecks owner authorization or explicit live scoped administrator authorization.
- Mutation: POST create/actions,PUT whole replacement,PATCH quality action only. IDs/owner/consent contents/creation times/job snapshots immutable. Delete202 distinct cleanup completion.
- Errors: JSON `{error:{code:Text,message:Text,details:{field:Text,constraint:Text}[],request_id:ID,timestamp:Time}}`;details=[] permitted. Status/code normative,prose informative,no private echo. All rows inherit400 INVALID_INPUT/LIMIT_EXCEEDED,401 UNAUTHENTICATED,403 FORBIDDEN,404 NOT_FOUND,409 INVALID_STATE,429 RATE_LIMITED,503 CONFIGURATION_REQUIRED/DEPENDENCY_UNAVAILABLE. Specific row codes refine mapping. Unexpected runtime503 INTERNAL_UNAVAILABLE. 429 Retry-After positive integer until policy opportunity(window reset/active deadline);503 only when known. Authentication before private lookup;syntax may fail earlier without lookup.
- Transport: encrypted deployed transit/rest,private storage,managed secrets,least privilege per FR-046;HTTP only loopback local. No provider keys/storage paths exposed. Authorization uncertainty fails closed503;fences independent of events.
- Versions: new /api/v1,/internal/v1,message schema_version1;unknown version rejected,no silent reinterpretation. Later incompatible change requires reviewed contract process.

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

## Compatibility Notes

No approved published predecessor to preserve. Unapproved architecture examples need separate alignment/review and do not override this proposal. No architecture/Plan/requirements edits. Model feasibility unproven;disabled behavior/capability shapes do not claim a feasible selected model. No Amendments section because no approved contract amended.

## Contract Completeness Check

Bounded documentation self-check,not approval/runtime/model validation. Exactly one row for each api-design question.

| Question | Evidence |
| --- | --- |
| 1. Input parsing | Shared notation,row inputs,Contract-Wide parsing,message rejection. |
| 2. Absent/null/empty/blank | Required/optional convention,Contract-Wide rules,inheritance/null exceptions. |
| 3. Read-only/unknown | Closed objects,unknown fields/query/parts rejected;message schema terminal. |
| 4. Numeric semantics | Primitives,Range/Cost,quota/forecast formulas,half-even rules. |
| 5. Collections | Page snapshot/cursor/limits/empty;chunk/sample/finding ordering. |
| 6. Matching/filtering | Exact filters/IDs/versions;normalized email;no search. |
| 7. Errors | Common status/body,operation refinements,message terminal/transient signals. |
| 8. Identity/existence | Malformed400/unknown404/foreign403/revoked409/purged404;cleanup/replay. |
| 9. Mutation semantics | Create/actions,whole PUT,quality override,immutable snapshot,durable winner,202 cleanup. |
| 10. Internal consistency | Compared Q5–Q10,retained FR-013/021/026/028 and revised Plan;prior paths/key expiry/constants removed. |
| 11. Authority | Contract Scope retains Plan scope/milestone authority;human review below. |

New labels are transport/schema names,not reused requirement/milestone identifiers;R-/FR-/AC- labels reference sources only. Revision addresses old routes,optional/body keys,key expiry,fixed upload/rate/token/link limits,queued-only cancellation,quota403 and delete204. No template comments remain.

## Contract Review Status

- Status: Approved by avinash2196 on 2026-10-24. Recorded by the main conversation at the user's explicit approval of this completed contract.
- CONTRACT completion is recorded in ../Plan.md. Dependent FOUNDATION implementation planning may proceed; execution still requires approval of its own concrete Implementation Plan. This approval does not approve remaining architecture examples or provision cloud resources.
