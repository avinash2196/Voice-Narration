# Implementation Plan — Model Feasibility & Licensing Assessment

## Milestone

Model Feasibility & Licensing Assessment, milestone 3 of initial-build.

## Milestone Type

OTHER. Plan.md explicitly assigns documentation, assessment and a validation protocol to this milestone, with no production behavior changes. R-EVAL-001 and Gate G1 are its owned concerns. Unsupported P0 capability cannot be resolved by changing production behavior here; return to planning if that becomes necessary.

## Authoritative References

Paths are repository-relative. Inspected 2026-10-24.

| Reference | Authority / approval |
| --- | --- |
| docs/.ai/initial-build/requirements.md | Approved by avinash2196 on 2026-10-19, with recorded 2026-10-24 scope and contract clarifications. Hindi-first/English, consent, controls, limits, commercial gate and human evaluation govern. |
| docs/.ai/initial-build/Plan.md | Approved revised Plan on 2026-10-24. Current Execution Status: CONTRACT Complete; Developer & Test Harness Complete; this OTHER Pending. Its Model Feasibility scope and FOUNDATION execution evidence govern. Earlier historical current-state paragraphs describe the original baseline, not today's checkout. |
| docs/.ai/initial-build/contract/API-Contract.md | Contract Review Status approved by avinash2196 on 2026-10-24. Capability, Range, model approval, exact script preservation, mapping, controls and conditional section regeneration are authoritative. |
| docs/.ai/initial-build/001_Implementation_Plan_Foundation.md | Human Review records executed and verified 2026-10-24 from user approval; decisions carried forward below. |
| voice_narration_PDD_requirements.md | Proposed product baseline; non-conflicting P0 retained through approved scope clarification. Sections 5, 8 and 9 supply assessment inventory and proposed quality targets, not approved numerical thresholds. |
| requirements-dev.txt; tools/readiness.py; .gitignore | Inspected delivered prerequisite definitions, executable readiness command and local-artifact exclusions; factual context, not additional requirements. |
| Installed plugin commands/create-implementation-plan.md; agents/planner.md | Process instructions. |
| Installed plugin skills/implementation-planning/SKILL.md; skills/prompt-driven-development/SKILL.md; skills/prompt-driven-development/templates/Implementation-Plan.md | Process instructions/template, including validation-protocol OTHER, exact steps, human approval and truthful evidence rules. |
| Installed plugin skills/llm-engineering/SKILL.md; skills/testing/SKILL.md | Evaluation provenance, human-reviewed thresholds, repeated observations and isolation guidance. |
| Primary online sources linked in the proposed candidates/license documents | Research evidence checked 2026-10-24; publisher claims and license text, not measured quality or legal sign-off. |

Plugin root: C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.15.0. No docs/requirements.md exists. No new requirement, contract, milestone or criterion identifier is defined here; corpus case names below identify proposed test data only.

## Carried-Forward Decisions

Preserve 001's CPython 3.13.17 development runtime, isolated project .venv, FastAPI/Uvicorn and browser-native frontend, pytest/HTTPX/Playwright, PostgreSQL 18.6/Psycopg, temporary filesystem artifact roots, NumPy/PyAV, Compose 5.6.0, dependency-only image and actual Linux CI. Preserve its unique temporary database/container/port/path isolation and two passes without intermediate cleanup. No package, image, setting or runner changes are proposed. Model-specific dependencies and a compatible isolated worker runtime belong to Approved Model Test Prerequisites after selection; a candidate's upstream requirements do not amend 001.

Keep nine services, no assumed local CUDA, no paid provisioning, consent before private audio use, model-minimal enrollment material and the existing approval boundary. General readiness does not establish synthesis, model compatibility, corpus acceptance or deployed security.

## Preconditions / Predecessor Evidence

Plan.md's current Execution Status records both predecessors Complete. Its FOUNDATION execution evidence records exact comparison of nine delivered files, Windows two-pass readiness, cleanup and successful real Linux workflow [40132442843](https://github.com/avinash2196/Voice-Narration/actions/runs/40132442843), commit 0fe8c317ffba011ec1e880d7d6d5af93b6b40d5a. Recorded stdout includes both prerequisite passes and explicitly says no application tests executed. This is verified predecessor evidence, not a new run performed by this planner.

No approved unexecuted 002 exists. Human review of this concrete Implementation Plan precedes creating the four deliverables. Their creation precedes a separate human protocol/selection decision; approval of this Implementation Plan does not select or license a model.

## Current Repository State

Read-only inspection before this file was created: model-eval directory absent; approved contract has no selected model; no application tests or inference adapter exists. FOUNDATION files and .venv exist. `git status --short` showed only pre-existing modifications to 001_Implementation_Plan_Foundation.md and Plan.md; preserve both. `Test-Path docs/requirements.md` and `Test-Path docs/.ai/initial-build/model-eval` both returned False. No new runtime failure was observed or inferred. No empty pytest suite is a passing baseline.

The assessment baseline is therefore no approved model, no evaluation artifacts, no corpus/consented audio or listening results, and no measured model costs, memory, latency or cold start. These are unknown measurements, not zero values. Docker was stopped after the recorded successful predecessor run; availability now is not inferred from a stopped runtime.

## Files in Scope

### Files to Create

Only these four documentation artifacts during approved execution:

- docs/.ai/initial-build/model-eval/candidates.md
- docs/.ai/initial-build/model-eval/license-matrix.md
- docs/.ai/initial-build/model-eval/evaluation-protocol.md
- docs/.ai/initial-build/model-eval/approved.md

### Files to Modify

None during document creation. A later main-conversation record of the actual human selection/protocol decision belongs in approved.md as specified by its exact recording steps below; never fabricate the decision. PDD's own verified-execution update in Plan.md is excluded from this scope restriction. This planning task creates only 002, not the proposed deliverables.

### Files to Delete

None.

## Proposed Changes

1. candidates.md: compare two concrete bilingual Hindi-capable pipelines, Chatterbox Multilingual V3 and XTTS-v2; distinguish documented capability, design hypothesis, measured evidence and blockers. Record cost/memory/cold-start assessment without invented numbers.
2. license-matrix.md: separate software, each model asset family, tokenizer/vocoder/conditioning/watermark assets, dependencies, private inputs and output permissions. Record commercial restrictions and unresolved closure explicitly. No model is cleared by an umbrella code license.
3. evaluation-protocol.md: propose version 1, exact public text corpus, private-input placement/responsibility, human listening rubric, repeated test cases, measurable proposed thresholds and prospective resource/cost procedure. This is the exact validation protocol under OTHER; it is not an inference harness or authorization to run inference now.
4. approved.md: initially record no selection, no protocol approval and no model enablement. Specify exact human-decision recording steps and distinct evidence required before later production activation.

No classes, APIs, executable signatures, dependencies or product settings change. Range/capability observations below are proposed evaluation decisions for review, not populated contract values.

## Proposed Code / Tests

The following four blocks contain complete proposed initial final document contents. Their factual unknowns are deliberate assessment findings, not instructions to invent missing evidence. Human decisions and future measurements use the explicit protocol steps, rather than placeholder code or an implied approval.

### docs/.ai/initial-build/model-eval/candidates.md

```markdown
# Model candidates

Research date: 2026-10-24. No model selected. No weights downloaded and no inference performed. This comparison supports human selection for later reviewed prerequisites, not production enablement. Quality, throughput, peak RAM/VRAM, cold start and operating cost are not measured for either pipeline.

## Compared pipelines

| Concern | Chatterbox Multilingual V3 | XTTS-v2 |
| --- | --- | --- |
| Identity and upstream | ResembleAI/chatterbox, explicitly V3 multilingual T3, with bundled S3Gen, voice encoder, multilingual tokenizer and Perth watermarking. [Model card](https://huggingface.co/ResembleAI/chatterbox), [loader](https://raw.githubusercontent.com/resemble-ai/chatterbox/master/src/chatterbox/mtl_tts.py). | coqui/XTTS-v2 with Coqui TTS inference code, autoregressive text/audio stage, speaker conditioning, tokenizer and HiFiGAN decoder. [Model card](https://huggingface.co/coqui/XTTS-v2), [implementation](https://raw.githubusercontent.com/coqui-ai/TTS/dev/TTS/tts/models/xtts.py). |
| Languages / enrollment | Official card lists Hindi and English; reference-audio conditioning. No additional voice conversion, translation or transliteration proposed. | Official card lists Hindi and English and cross-language reference-audio cloning. No separate conversion or translation proposed. |
| Version boundary | Current source accepts t3_model=v3, but default remains v2. V3 must be explicit in later reviewed prerequisites. Model family name alone is insufficient provenance. | XTTS-v2 family only; exact immutable code revision and checkpoint hashes not selected. |
| Hindi and mixed text | Devanagari Hindi evaluation required; language list is not pronunciation evidence. Mixed-language quality remains unverified and conditional. | Same. English capability does not establish Hindi quality or mixed-language continuity. |
| Neutral style / controls | Neutral baseline must be evaluated. Source exposes exaggeration and guidance, not a direct pause-strength/pace pair. Those controls must not be relabeled as proven pause/pace controls. | Source includes speed adjustment; no documented direct pause-strength control established by this assessment. Speed parameter availability is not an identity-safe range. |
| Pause / pace route | Hypothesis for later review: boundary-aware synthesis plus controlled pause placement and pitch-preserving tempo processing could satisfy the adapter's two controls. Requires measured identity/word integrity; no native support claim or implementation authorization. | Same pause-processing hypothesis; compare native speed with processing only in later authorized evaluation. No safe range established. |
| Mapping / joins | Exact source-text offsets and generated chunk intervals require application/adapter work and listening verification. Upstream generation alone does not provide approved mapping. | Same. |
| Section regeneration | Independent conditioned segment generation makes a later splice workflow plausible, not proved. Original preservation, unchanged neighboring chunks and explicit join preview must be tested; capability remains unverified. | Same. |
| Reusable profile | Reference audio/derived conditioning may be needed. Retain only proven necessary material; purge reconstructive caches on revocation. No per-user training assumed. | Reference audio/conditioning latents may be needed; same retention constraint. |
| Software / weights / outputs | MIT code and MIT model-card label are promising, subject to per-asset/third-party closure in license-matrix.md. Output commercial use has not received Administrator approval. | MPL-2.0 code does not override CPML-1.0.0 model/output restriction to noncommercial use. Monetized deployment blocked absent a separate demonstrated license. |
| Dependencies / portability | Upstream pyproject reports package 0.1.7 and model-specific Torch/audio/Transformers/Perth dependencies. These are observed metadata, not selected installation versions or proof of current support/compatibility. | Upstream requirements include Torch/audio, text normalization, language tooling and Coqui packages. No installation version selected; upstream availability is not support or CPython 3.13 compatibility evidence. |
| Current disposition | Plausible candidate for human selection for later feasibility work, conditional on license closure and P0 controls/quality. No approval recommended as an accomplished fact. | Useful bilingual technical comparator; public license blocks commercial model/output use. Not a commercially cleared fallback. |

Source preservation: record immutable code/model revision, each file's published digest and applicable license at the later selected-model prerequisite review; compare acquired bytes there. Moving main/master URLs in this research snapshot are not reproducible executable pins. No support policy or dependency resolution was established for either pipeline. Do not install a candidate into the approved general .venv.

## Resource and cost feasibility

Memory, CPU/GPU compatibility, end-to-end cold start, synthesis real-time factor and per-run USD: not measured. Parameter count or checkpoint file size cannot establish peak VRAM. CPU loader branches do not establish acceptable CPU latency; Windows CUDA is not assumed. No claim that either pipeline fits L4, meets 300 seconds or fits $20/month.

Evaluate the complete nine-service system, database, private storage, downloads, artifacts, observability, retry/failure overhead and worker idle/start time. Use current [Cloud Run pricing](https://cloud.google.com/run/pricing) and [GPU service documentation](https://docs.cloud.google.com/run/docs/configuring/services/gpu) only as conditional platform inputs; account region, quota, service/job limits and billing mode require the later Cloud Run readiness milestone. No environment or tariff selected here.

Prospective calculation: run compute USD = sum of each billed resource quantity times its dated regional rate, including startup, unsuccessful attempts and billed idle time; storage USD = byte-time and operation charges; cost per output minute = total attributable run USD divided by output seconds/60. Monthly forecast = measured per-run costs times explicitly supplied run counts + all nine services' fixed/idle costs + storage/egress/other platform costs. Never divide an unknown cost as though it were zero; do not infer $20 is per user. Avoid assumed free tiers or traffic. evaluation-protocol.md defines measurement and missing-input rules.

Cold start is measured from admission into a fresh worker's startup through readiness to synthesize, with download/container/model-load phases separately reported; also report queue wait and time to first audio. The 300-second tolerance remains subject to feasibility. Output has an absolute 3000-second ceiling subordinate to stricter configured quota/resource/budget limits; no 3000-second synthesis is authorized by this assessment.

## Selection recommendation and blockers

Present Chatterbox Multilingual V3 as the first plausible commercial bilingual route for human consideration; retain XTTS-v2 as the restrictive-license comparator. Do not select automatically. Current blockers to production enablement: immutable asset/license closure, Administrator approval, measured Hindi/English identity and pronunciation, supported safe pause/pace, mapping/continuity, compatible authorized compute, cold start and total cost evidence. Conditional section regeneration must be assessed rather than silently promised or removed. If no candidate can satisfy P0, return for a human decision on a separately reviewed alternative; do not weaken P0 or treat a noncommercial license as commercial permission.
```

### docs/.ai/initial-build/model-eval/license-matrix.md

```markdown
# License and provenance assessment

Research date: 2026-10-24. No commercial-use sign-off. This is a source-backed component inventory and explicit closure record, not a complete resolved-runtime SBOM. Neither candidate has an approved immutable distribution. Missing evidence blocks activation; it is never inferred from a repository badge. No private voice, weights or license acceptance was submitted during research.

| Pipeline / component | Evidence and terms | Commercial/output decision and obligations |
| --- | --- | --- |
| Chatterbox application code | [Resemble MIT text](https://raw.githubusercontent.com/resemble-ai/chatterbox/master/LICENSE). | Software commercial use permitted by MIT subject to notices/disclaimer. Does not independently clear every checkpoint or third-party file. |
| Chatterbox multilingual T3 V3 checkpoint | [Official model card](https://huggingface.co/ResembleAI/chatterbox) identifies MIT; [file inventory](https://huggingface.co/ResembleAI/chatterbox/tree/main) includes t3_mtl23ls_v3.safetensors. | Promising model-level permission evidence; exact revision/digest and per-file applicability not frozen. No Administrator approval. |
| Chatterbox speaker encoder / conditioning | Same model inventory: ve.pt; optional conds.pt. [Loader](https://raw.githubusercontent.com/resemble-ai/chatterbox/master/src/chatterbox/mtl_tts.py). | Checkpoint applicability must be recorded separately. Do not use bundled default voice conditioning as consent for cloning its source speaker. Consented own reference is required. |
| Chatterbox S3Gen / acoustic decoder / vocoder | Model inventory includes s3gen.pt and newer variants. Current multilingual loader uses s3gen.pt. [S3Gen source](https://raw.githubusercontent.com/resemble-ai/chatterbox/master/src/chatterbox/models/s3gen/s3gen.py) contains Apache-2.0 attribution to CosyVoice. | Preserve applicable Apache notices in addition to MIT. V3 T3 does not imply s3gen_v3.pt compatibility. Weight-specific provenance and coverage remain to be closed before acquisition. |
| Chatterbox text tokenizer / language assets | Model inventory and loader identify grapheme_mtl_merged_expanded_v1.json and Cangjie5_TC.json. | Record exact bytes and applicable terms; do not assume tokenizer data inherits the code license automatically. No extra Hindi transliterator selected. |
| Chatterbox speech tokenizer | [Wrapper](https://raw.githubusercontent.com/resemble-ai/chatterbox/master/src/chatterbox/models/s3tokenizer/s3tokenizer.py) imports S3TokenizerV2; [upstream license](https://raw.githubusercontent.com/xingchensong/S3Tokenizer/main/LICENSE) is Apache-2.0. | Source license identified. Audit constructor/download paths and any separately fetched tokenizer checkpoints before freezing distribution; unknown external assets block clearance. |
| Chatterbox Perth watermark | [Perth repository](https://github.com/resemble-ai/Perth), [MIT license](https://raw.githubusercontent.com/resemble-ai/Perth/master/LICENSE). | Preserve notices and output watermark. Audit installed implementation and any separate watermark assets; their complete provenance not established. No watermark removal is proposed. |
| Chatterbox generated output | Model-card MIT designation plus upstream code terms; no output-specific commercial grant independently established in inspected text. | Do not claim ownership, unrestricted output rights or monetized-video clearance solely from MIT code. Human Administrator must approve cited model/output terms and any identified additional restrictions. Voice consent and script rights remain separate. |
| XTTS application code | [Coqui TTS MPL-2.0](https://raw.githubusercontent.com/coqui-ai/TTS/dev/LICENSE.txt). | Software use and redistribution subject to MPL terms/source and notice obligations; no grant overriding model/output terms. |
| XTTS base TTS / speaker conditioning / decoder weights | [Official card](https://huggingface.co/coqui/XTTS-v2), [checkpoint license CPML-1.0.0](https://huggingface.co/coqui/XTTS-v2/raw/main/LICENSE.txt). Includes checkpoint-integrated text/audio, speaker and HiFiGAN components; no separately licensed replacement selected. | CPML restricts model and output to noncommercial use and requires downstream terms/URL. Commercial/monetized route blocked absent actual additional permission; do not assume a purchase option or licensor availability. |
| XTTS tokenizer/config/reference assets | Same model repository and checkpoint license; [loader](https://raw.githubusercontent.com/coqui-ai/TTS/dev/TTS/tts/models/xtts.py). | Every acquired vocab/config/normalization/speaker asset needs exact inventory and coverage. No bundled reference voice is consent evidence. |
| XTTS outputs | CPML text explicitly covers generated outputs, separately from MPL code. | Public checkpoint terms do not permit the intended commercial route. Evaluation exceptions do not clear production. |
| Both pipelines: consented reference audio / transcript / conditioning | requirements.md R-CONS-001/002; R-REV-001; R-DEL-001; approved protocol. | Owner's prior explicit authorization and script rights required; derived conditioning remains private/reconstructive. Retention/purge obligations apply regardless of software license. |
| Both: WAV, MP3 and native audio libraries | [FFmpeg legal guidance](https://ffmpeg.org/legal.html); approved FOUNDATION establishes PyAV codec availability only. | WAV is baseline output. MP3 remains conditional on exact encoder/library build and license review. Codec availability is not export clearance; record native library notices/build options before shipping. |

## Dependency closure

These upstream manifests are evidence of real dependency breadth, not approved pins: [Chatterbox pyproject](https://raw.githubusercontent.com/resemble-ai/chatterbox/master/pyproject.toml), [Coqui requirements](https://raw.githubusercontent.com/coqui-ai/TTS/dev/requirements.txt). Chatterbox's observed 0.1.7 manifest includes NumPy, librosa, s3tokenizer, Torch, torchaudio, Transformers, diffusers, Perth from a moving Git ref, conformer, safetensors, spacy-pkuseg, pykakasi, Gradio, pyloudnorm and OmegaConf. Coqui additionally declares Cython, SciPy, soundfile, scikit-learn, numba, inflect, tqdm, anyascii, PyYAML, fsspec, aiohttp, packaging, mutagen, Flask, pysbd, umap-learn, pandas, matplotlib, trainer, coqpit, jieba, pypinyin, hangul_romanize, gruut language extras, jamo, nltk, g2pkk, bangla, bnnumerizer, bnunicodenormalizer, einops, encodec, Unidecode, num2words and spaCy extras.

Core primary texts include [PyTorch license](https://github.com/pytorch/pytorch/blob/main/LICENSE) and [Transformers license](https://github.com/huggingface/transformers/blob/main/LICENSE). They do not cover unrelated dependencies. Exact resolved versions, direct/transitive license texts, bundled native libraries, redistributed notices, language dictionaries and implicit asset downloads have not been resolved or approved. Do not label the dependency closure complete. No library from these lists is added to requirements-dev.txt.

Before the selected-model prerequisite plan may authorize acquisition, its reviewer must see a row for every direct/transitive package and every asset, with exact source revision/file/published digest, license text URL and revision, commercial-use condition, output condition or explicit absence of a separately stated output term, attribution/source-disclosure obligation, implicit-download location, reviewer disposition and unresolved issue. Inventory the actual selected branch/variant; do not mix V2/V3 or default voices. After authorized acquisition, compare bytes/digests and installed metadata to that reviewed inventory; unexpected downloads, unidentified terms or revision drift stop execution for review. This later resolved inventory is a prerequisite to shipping, not a fabricated result of this documentation assessment.

## Current gate result

Chatterbox: potentially viable, conditional; complete asset/output/dependency closure and human approval outstanding. XTTS-v2: public model/output license incompatible with commercial use; no override obtained. No model enabled. If coverage cannot be established, human selection for investigation can remain conditional, but commercial sign-off must remain withheld. Missing terms cannot be converted into a permissive license by an AI reviewer.
```

### docs/.ai/initial-build/model-eval/evaluation-protocol.md

```markdown
# Evaluation protocol

Protocol version: 1, proposed for human review. No corpus/audio/model execution approved by this document's existence. Numerical choices below are proposals to make R-EVAL-001 measurable; approving document creation does not silently approve these choices. Measured results: not measured. This milestone defines the protocol; later approved prerequisites and inference milestones execute model-dependent cases.

## Inputs and handling

The human reviewer supplies protocol/threshold approval and a model selection decision. Before later execution the consenting speaker supplies explicit purpose/versioned authorization and their own clean reference recording/transcript through an authorized private channel; an operator supplies separately authorized compute and any credentials/rates, and identifies three listeners: the voice owner plus two Hindi-fluent listeners with English comprehension. Do not request uploads in a public repository or place private voice data in Git. Assisted recordings require the voice owner's prior authorization. Missing consent, compute, listener or approval means Waiting, never an assumed pass.

Proposed private run root: an operator-selected absolute directory outside this repository, recorded privately in the run manifest. The operator places consent metadata in consent.json, reference audio in reference.wav, its exact transcript in reference.txt, nonvoice script text in scripts.json, raw generated audio under audio/, and private results in results.json. No private files are created by this assessment. Restrict access to the authorized participants; retain and purge according to the approved separate retention policies, with revocation immediately stopping use. A public evidence summary contains only opaque corpus/run identifiers, hashes where appropriate, nonprivate model/configuration metadata and aggregate scores, never private paths, speaker identity, audio or scripts supplied by users.

The later prerequisite plan must define/validate exact executable manifest schemas and paths before use. This protocol is manual validation steps, not a claim that a harness or schema implementation already exists. No extra model, judge, ASR or speaker-embedding checkpoint is selected for scoring.

## Fixed text corpus, version 1

These original test texts are proposed public inputs. Preserve exact Unicode text, punctuation and line breaks in the job snapshot. A Hindi-fluent reviewer approves intended pronunciation before using the corpus. The corpus includes ten Hindi-led cases and two English cases; mixed-language support is evaluated separately from mandatory hi/en. Text is not a claim that each model supports every control.

| Case | Exact text (the symbol ↵ denotes one line break when preparing the input) | Purpose |
| --- | --- | --- |
| Hindi poem | सुबह की पहली किरण आई,↵आँगन में मुस्कान जगाई।↵धीरे बोलो, ध्यान से सुनो;↵हर ध्वनि में कहानी पाई। | Poetry, comma/semicolon, line breaks. |
| Hindi prose | बरसात के बाद सड़क साफ़ थी। बच्चे पुस्तकालय की ओर चले। वहाँ उन्होंने एक नई कहानी पढ़ी और उसके बारे में बात की। | Neutral connected prose. |
| Hindi numbers | आज 24 अक्टूबर 2026 है। बैठक सुबह 10:30 बजे शुरू होगी। टिकट की कीमत 125 रुपये है। | Dates, time, numerals; approve spoken forms. |
| Hindi conjuncts | विद्यार्थी ने स्वतंत्रता, श्रद्धा, दृष्टि और क्षितिज शब्द स्पष्ट पढ़े। प्रत्येक प्रश्न का उत्तर ध्यानपूर्वक दिया गया। | Conjuncts, aspiration and articulation. |
| Hindi vocabulary | ज़िंदगी की ख़ूबसूरती सिर्फ़ मंज़िल में नहीं, सफ़र में भी है। फ़ैसला करते समय सबकी राय सुनिए। | Nukta/Urdu-derived vocabulary. |
| Hindi names | अनन्या और ऋषभ वाराणसी से आए। उन्होंने प्रयागराज, श्रीनगर और भोपाल की यात्राओं की कहानी सुनाई। | Proper nouns and pronunciation. |
| Hindi questions | तुम आ गए? अच्छा, पहले बैठो। नहीं, अभी मत पढ़ो! एक क्षण रुककर फिर शुरू करो। | Questions, punctuation, pause placement. |
| Hindi mixed | आज हमारी online meeting है। कृपया microphone जाँच लें, फिर हिंदी में अपनी कहानी सुनाएँ। | Conditional code switching; do not substitute Hindi-only success. |
| Hindi silence | एक शांत सुबह थी।↵↵फिर दूर से किसी के चलने की आवाज़ आई। | Repeated line break contextual cues; no unconditional silence assumption. |
| Hindi continuity | नदी के किनारे एक पुराना पेड़ था। उसके नीचे बैठकर मीरा हर दिन अपनी पुस्तक पढ़ती थी। एक दिन उसे पन्नों के बीच एक पत्र मिला। उसने पत्र पढ़ा, मुस्कुराई और अपनी कहानी लिखनी शुरू की। | Chunk seams, stable identity and section replacement. |
| English prose | After the rain, the children walked to the library. They opened a book, read the first page, and talked about the story. | Mandatory English intelligibility and identity. |
| English pauses | Are you ready? Please wait, listen carefully, and begin. Speak calmly; leave enough time for the listener to follow. | English pace/pause and punctuation. |

For 30-second, 2-minute and 5-minute performance observations, the operator and Hindi reviewer prepare longer coherent continuations of Hindi continuity, and record exact UTF-8 bytes/hash and observed output duration in a new immutable private corpus version before running. These are target duration bands, not forced truncation or predicted durations. Freeze actual text and approved limits before execution; do not loop a sentence to pretend it is coherent long-form quality. The 3000-second maximum is not a requirement to synthesize that duration in this assessment. Cases exceeding stricter quota/resource/budget limits are Waiting on an authorized feasible test configuration, not silently executed.

## Recording and repetitions

For every later run record model/code/checkpoint/decoder/tokenizer/watermark immutable identifiers and hashes, dependency lock/image digest, device/driver and CPU/GPU RAM, corpus version/hash, consent authorization reference, actual reference preprocessing, complete effective inference/chunk/join/control settings, seed, attempt, timestamps, output duration, failures and cost inputs. Originals and any processing outputs have separate hashes. Never keep the easiest repeat or discard failed attempts.

Proposal: three independent generations per case with seeds 7, 19 and 43 where the backend honors seeded generation. Record unsupported seed control and use three independent runs anyway; byte equality is not expected. Compare every repeat, including failures. Listener presentation uses opaque case labels and a pre-recorded randomized order, hides candidate and settings, includes the authorized natural reference and an exact repeat to inspect rating consistency. Preserve raw per-listener scores privately and aggregate each language separately; Hindi is primary, English failure is not averaged away.

## Rubric and proposed acceptance decisions

Human ratings are integers 1–5: 1 unusable/unrecognizable; 2 major defects/weak identity; 3 understandable or recognizable with clear defects; 4 clear/natural/recognizable with minor defects; 5 consistently clear/natural/strongly recognizable. Score identity against the authorized reference; pronunciation/intelligibility against the exact script; continuity across all joins; neutral expressiveness/pause appropriateness against intended phrasing. The voice owner scores identity; all three listeners score remaining dimensions. Each rates independently before discussion.

Proposal for review: retain the baseline mean >=4/5 for Hindi pronunciation/intelligibility and owner-rated identity, separately require >=4/5 for English, and require >=4/5 continuity and neutral phrasing for each language. Compute means over all prescribed cases/repeats and preserve per-case scores. Any omitted/extra word changing meaning, truncated word, unintended mid-word pause, audible click/dropout/repeat, wrong speaker or listener score <=2 requires triage and blocks acceptance until the human reviewer accepts a documented remedy and its rerun evidence. No averaging away a critical defect. These are proposed thresholds; no threshold is operative before explicit human approval.

Calibration: listeners first rate the natural reference and a pilot generation with the same rubric in a later authorized environment. Present raw score distributions, defect examples, inter-listener disagreement and candidate feasibility to the human reviewer; record approved thresholds or requested revisions before acceptance evaluation. Thresholds cannot be lowered after seeing failing acceptance results without protocol revision/re-approval and a complete rerun. No numerical latency percentile or memory target invented here; report all observations and let the reviewer assess against feasible resources.

## Exact prospective cases and met/not-met rules

1. Consent/provenance: operator checks prior active consent, authorization scope, all immutable input/model identifiers, corpus and recorded effective settings before loading private samples. Met only if every item exists and access is authorized; otherwise Waiting and no use. This is a protocol check, not proof of implemented product authorization.
2. Hindi/English: generate every fixed case three times in neutral style with one consented profile; listeners compare each complete output with its exact text and reference. Met only when the separately approved per-language rules above pass with all results recorded. Mixed case may be classified unsupported only when the approved capability is conditional/false; mandatory Hindi and English cannot be omitted.
3. Identity reuse: reuse the same profile for at least the first three distinct Hindi scripts and English prose without reenrollment. Met only when owner identity ratings pass and no model-required material is reacquired without authorization. Report required reference/conditioning retention; do not promise voice training.
4. Continuity/mapping: compare original text scalar offsets, each complete chunk, cumulative sample ranges and final output; listen to every join plus one second of context on either side. Met only if no word is split/lost/repeated, mapping covers the exact text and audio as specified by the contract, sample rate/loudness/identity remain stable, and all approved listening rules pass. Record defects and boundary timestamps; waveform metrics alone cannot pass listening acceptance.
5. Pause/pace: the later reviewed adapter plan names the actual supported mechanism before trials. Proposed trial pace multipliers are 0.9, 1.0 and 1.1 relative to neutral; proposed pause multipliers are 0.8, 1.0 and 1.2 relative to the adapter's contextual neutral pauses. These are evaluation settings, not a contract Range or approval to manipulate pitch. Use Hindi questions/poem and English pauses, three repeats each, varying one control at a time. Manually annotate word onset/offset and pause boundaries. Met only when median spoken words per second excluding annotated silence changes monotonically with pace, median boundary pause duration changes monotonically with pause strength, word integrity and approved identity/quality rules pass at every proposed exposed setting, and the mechanism is supported by the assessed pipeline. Report actual effect sizes; no untested interpolation/range/step is approved. If these points are unsuitable or unsupported, stop for revised human-reviewed trials; do not hide either P0 control or infer support from exaggeration/guidance controls.
6. Section regeneration: on Hindi continuity, change only the middle sentence, generate a child version and join preview, compare unchanged source chunks and originals by hashes, and listen to both replacement boundaries. Met only if originals are preserved, unchanged portions are unchanged, the requested replacement is present, mapping is accurate and the preview passes quality/identity rules. If the complete pipeline cannot support sections, record conditional capability false with rationale and human review; whole regeneration remains required and is tested separately. Do not treat independent TTS calls as proof of splice quality.
7. Resource/performance: only after separately approved prerequisites provide runnable commands and authorized compute, collect one uncached startup, three fresh-worker cached-weight startups, and three warm generations in each approved duration band. Report individual times and medians, model load versus downloads, queue wait, time to first audio, wall time, real-time factor=wall inference seconds/output seconds, peak host/GPU memory and failures. Do not claim meaningful p95 from this small sample. Met for the 300-second feasibility comparison only if every observed end-to-end fresh-worker startup is <=300 seconds on the disclosed setup; a miss is a feasibility finding requiring human decision, not permission to change the tolerance. L4 fit stays unverified without actual approved L4 evidence.
8. Cost: operator supplies dated regional tariff/billing mode and actual billed compute/storage/transfer quantities, including startups, failures, retries and idle resources. Compute costs as specified in candidates.md, report measured versus estimated charges separately and retain attributable billing evidence privately. For the monthly target the operator supplies expected runs, cold starts and retention/storage/egress assumptions for all nine services; calculate the full monthly forecast. Met only if quantities/rates/assumptions are complete, measured costs are not replaced by zero/estimates, and the disclosed scenario is <=$20/month; above-target or absent workload is respectively Not met or Not measured/Waiting. No unapproved benchmark spend, always-on GPU or provisioning. Final Cloud Run readiness remains its own milestone.

The assessment milestone executes documentation review and human decisions only. Cases requiring inference, corpus acquisition or compute are prospective instructions for their later approved milestones. No successful synthesis, listening acceptance, license clearance, supported control range, GPU fit or production gate completion can be recorded from this protocol alone.
```

### docs/.ai/initial-build/model-eval/approved.md

```markdown
# Human model and protocol decision record

No human model selection recorded. No evaluation-protocol approval recorded. No software/weights/output commercial approval recorded. No production enablement authorized. No benchmark/listening results measured. This initial record intentionally waits for actual human decisions; its filename is not approval.

Review inputs: candidates.md, license-matrix.md and evaluation-protocol.md version 1. Chatterbox Multilingual V3 is a plausible investigation route, with asset/output/dependency closure, P0 pause/pace and runtime feasibility still unresolved. XTTS-v2 public model/output terms restrict commercial use. Neither is a cleared production alternative.

## Exact decision-recording steps

1. The main conversation presents all three completed documents and their unknowns to the human reviewer. Ask for a specific candidate selection for later reviewed feasibility/prerequisite work, or rejection, and explicit approval or revision of protocol version 1 including numerical trials/thresholds. Selecting a candidate does not resolve its unknowns or waive any P0 requirement.
2. Only after the human responds, append their exact decision, reviewer identity, UTC timestamp and scope to this file. Record model family/variant and the three reviewed document revisions; separately record selection-for-investigation, protocol approval, commercial-use approval and production enablement as distinct decisions. Use the actual approved thresholds or explicit requested revisions; never infer them from approval to create documents.
3. If selection or protocol is missing/rejected, record Waiting or the actual rejection and keep this milestone incomplete. Present one focused next decision using the observed blocker; do not select a fallback, alter requirements or start later milestone work.
4. Before recording commercial-use approval, supply the exact immutable software/checkpoint/tokenizer/decoder/conditioning/watermark/dependency inventory and applicable license/output-use evidence from license-matrix.md, and obtain explicit Administrator approval. Unresolved terms keep commercial approval withheld. Before production enablement, also require actual approved protocol results and all applicable later implementation/security gates; a human preference does not substitute for those results.
5. After the required assessment review and actual model selection/protocol approval are recorded, verify the four documents and predecessor preservation checks, then record only this OTHER milestone's evidence through the PDD workflow. No later milestone starts automatically. Approved Model Test Prerequisites still needs its own concrete human-reviewed Implementation Plan before dependencies/assets/compute are acquired.

Assessment completion is not production/model-quality acceptance. Actual listening, memory/latency/cost/cold-start measurements remain for later authorized execution, with Not measured until that occurs. If no plausible permissible P0 pipeline can be selected, keep the assessment Waiting and return to planning with a focused proposal rather than marking it complete.
```

## Execution Steps

1. Confirm this Implementation Plan's Human Review records actual approval, predecessors remain Complete, and this milestone remains Pending. Read the current documents; preserve unrelated work.
2. Create only the four exact content blocks above. Do not acquire weights, accept hosted terms, create private inputs, install packages, create a benchmark harness or perform inference.
3. Perform documentation/provenance review: follow each primary link; verify claims still match the specific component. Unknown/changed terms stay unresolved and are presented to the reviewer, not silently rewritten as cleared. A change to the proposed content beyond actual decision recording returns for review.
4. Present candidate, unresolved licenses/capabilities and proposed protocol/thresholds for actual human selection and protocol review. Follow approved.md's exact steps; keep Waiting until those decisions exist. Human approval cannot be predicted.
5. Verify document content/scope and preserve FOUNDATION checks below. Record actual observations separately from prospective model cases. Only after all completion criteria pass may the main workflow update Plan.md for this milestone; no inference milestone is executed here.

## Acceptance / Completion Criteria

- Four reviewed artifacts exist, compare at least two realistic Hindi-capable pipelines and cover English, neutral style, reusable identity, pronunciation, joins/mapping, pause/pace, conditional section regeneration and original preservation. No unsupported P0 capability is assumed away.
- Software/asset/output/dependency evidence and unresolved restrictions are explicit. No false license closure, checkpoint hash, version support, benchmark or cost claim. Commercial activation remains blocked on actual complete inventory/approval.
- A versioned, consent-aware measurable protocol exists with exact text cases, supplied-input responsibilities/private placement, proposed thresholds awaiting specific review, later execution steps and met/not-met rules. Missing measurements remain Not measured, never passed.
- Actual human candidate selection for later reviewed work and explicit protocol/threshold approval are recorded; otherwise this OTHER remains Waiting/incomplete. Approval of this Implementation Plan alone is not those decisions. Production enablement/commercial sign-off remain distinct and may remain withheld pending later evidence.
- Only the four documentation files change during execution, apart from actual human-decision recording there and this milestone's PDD execution bookkeeping. No executable behavior or prerequisite is changed; no private audio in Git.
- Applicable preserved FOUNDATION verification succeeds as specified below, and no failed check is dismissed or weakened. No application regression suite exists at this baseline.

## Verification

### Commands and Exact Review Steps

From repository root, after approved document creation:

```powershell
git diff --check
git status --short
Get-ChildItem docs/.ai/initial-build/model-eval -File | Select-Object Name,Length
Get-Content docs/.ai/initial-build/model-eval/candidates.md
Get-Content docs/.ai/initial-build/model-eval/license-matrix.md
Get-Content docs/.ai/initial-build/model-eval/evaluation-protocol.md
Get-Content docs/.ai/initial-build/model-eval/approved.md
```

Review met only when the four exact proposed initial contents match their blocks and any appended human decision matches actual authorization, every primary claim has the stated source, every unknown is explicit and every required decision is present before completion. Inspect status against the starting modifications; no extra file is permitted. Read the complete artifacts, not only keyword counts. For the corpus manually confirm ten Hindi-led/two English cases, exact line-break convention, private consent boundary, three repeats and separate language scores; trace each P0 concern to its case above. Confirm no actual measurement is claimed and no model/dependency/configuration was installed. Missing human approval is Waiting, not a passing review.

Preserved checks are 001's prerequisite checks, not invented application tests. Because only documentation changes, preserve the recorded successful Windows two-pass and real Linux CI baseline without reinstalling/rebuilding/repeating expensive readiness solely to recreate identical evidence. Verify the nine foundation files remain unchanged with:

```powershell
git diff --exit-code HEAD -- requirements-dev.txt pytest.ini compose.harness.yaml containers/harness.Dockerfile .dockerignore .gitignore tools/readiness.py docs/developer-setup.md .github/workflows/harness.yml
```

Expected no output/exit 0, matched to the actual successful predecessor commit/evidence above. If any prerequisite file changes or a new runtime concern is found, stop for review rather than reuse stale evidence. If runtime readiness must then be re-established in the authorized existing environment, the exact preserved command is `.\.venv\Scripts\python.exe tools/readiness.py`, whose single invocation already performs both passes without cleanup; expected both passes and final prerequisite-ready message, exit 0. Do not treat unavailable Docker or a failed probe as a pass, silently change the command or reinstall prerequisites under this documentation scope.

### Expected Evidence

Expected / Predicted — Not Yet Verified: four matching reviewed documentation files, all source/capability/license unknowns truthful, recorded actual human selection/protocol approval and preserved successful prerequisite checks with unchanged executable files. Prospective inference/listening/cost cases are not executed by this milestone and are not completion evidence for model quality. Waiting for a human decision is not completed OTHER evidence.

### Planning-Time Dry Run

No disposable model/inference dry run was performed: no model, consented corpus, approved protocol, selected-model environment, rates or human listeners are supplied/approved, and model acquisition/execution belongs to later milestones. A disposable copy cannot supply these inputs or human approvals. No scratch file, model asset, runtime, private recording or environment was created. Documentation source research and baseline existence/status inspection were performed; lightweight exact-content/scope checks are recorded below. FOUNDATION runtime work was not repeated: executable prerequisite files are outside this plan's changes and actual Windows/Linux success evidence is preserved. No causal runtime explanation or new test pass is claimed.

## Risks

Moving upstream research refs may change before the selected-model prerequisite review; freeze exact assets and verify current supported dependencies there, never by assuming this research snapshot pins a runtime. Chatterbox's MIT model label leaves component/output applicability requiring explicit closure; XTTS's CPML restricts the intended commercial route. Source-declared controls do not establish both required safe basic controls. The post-processing route is a hypothesis and needs later reviewed implementation and evidence; unsupported P0 stops selection/activation rather than silently removing it. Memory/cold-start/cost cannot be certified without actual authorized compute/workload; nine-service overhead may exceed $20. Private sample/conditioning leakage is prevented by authorized external storage and absence from this documentation diff, not by a claimed completed product privacy implementation.

## Pre-authorized Contingencies

None. A different candidate, changed protocol/threshold, additional file/dependency or production behavior returns for review. Truthful actual human-decision recording in approved.md is part of the exact protocol, not permission to invent consent or broaden scope.

## Rollback / Recovery

If this milestone's document creation must be reversed, remove only its four newly created documents after checking no human decision/evidence would be lost; preserve supplied/private inputs outside Git under their policy. Do not reset/clean the repository or touch the predecessor/other documentation. Decisions already recorded are history and require explicit human correction rather than silent erasure.

## Explicitly Out of Scope

Production/model code; tests/configuration/runtime/container changes; model-specific installs, weight/tokenizer/vocoder/watermark acquisition; synthetic inference; public/private audio uploads; consent acceptance on behalf of a speaker; cloud provisioning or benchmark spend; licensed-model purchase; automatic model/protocol/license approval; fixed production control ranges; threshold relaxation; new traffic/uptime/telemetry requirements; approving remaining architecture; executing any subsequent milestone.

## Exact-Code and Authority Review

| Proposed file | Complete initial content / no pseudocode | Matches proposal / introduced dependency or setting |
| --- | --- | --- |
| candidates.md | Complete block; unknown measurements explicitly stated. | Item 1; model names are comparison evidence, not installed dependencies. |
| license-matrix.md | Complete block; unresolved inventory explicitly blocks clearance. | Item 2; upstream manifests are cited provenance, no package/config changes. |
| evaluation-protocol.md | Complete block and exact manual validation steps/input responsibilities/met rules. | Item 3; proposed metrics/trial values trace R-EVAL-001 and baseline calibration, require explicit human approval, no production setting. |
| approved.md | Complete initial block and exact later decision-recording steps. | Item 4; no prefilled approval or model identifier pretending selection. |

No template comments, pseudocode, partial executable fragments or reused authority identifiers are introduced. Distinct corpus names label test inputs, not new requirements. No dependency/version is selected for installation, so this plan does not assert current support for observed candidate manifest versions. The exact manual validation steps are the OTHER protocol; later selected-model runnable commands require their own reviewed prerequisites rather than fabricated commands now.

Planning checks actually run on 2026-10-24: `git diff --check` returned exit 0 (only Git's LF/CRLF informational warnings for pre-existing 001/Plan edits). The exact `git diff --exit-code HEAD --` command above returned no changes for all nine delivered prerequisite files. `git status --short` showed only the two pre-existing 001/Plan modifications plus this new 002. Inspection found four complete markdown deliverable blocks, twelve balanced fence lines, zero template comments, zero trailing-whitespace lines and exactly one Human Review status field. `Test-Path docs/.ai/initial-build/model-eval` remained False. These are documentation/scope checks, not runtime verification, listening, legal clearance or human approval. The four blocks correspond one-to-one to Proposed Changes; cases 2–6 cover required language/identity/continuity/controls/regeneration concerns and cases 7–8 separately preserve the 300-second/$20 feasibility checks and subordinate 3000-second limit. No prerequisite file was changed and no test was run or classified as newly passing.

## Human Review

Status: Executed and verified on 2026-10-24 from avinash2196's recorded approval. Four exact assessment documents were created and reviewed; the main conversation then recorded the user's separate Chatterbox Multilingual V3 investigation selection and protocol v1 approval in model-eval/approved.md. See Plan.md, Model assessment documentation evidence — 2026-10-24, for source/document/preservation checks and actual decision revisions. Commercial clearance, model acquisition, runtime measurements and production enablement remain separate gates; this completion authorizes no subsequent milestone's execution.
