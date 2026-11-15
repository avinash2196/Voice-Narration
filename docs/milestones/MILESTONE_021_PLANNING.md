# Milestone 021 Planning
## Enrollment Acoustic Calibration Validation (OTHER)

**Date Created:** 2026-10-30  
**Status:** 🔴 BLOCKED — Awaiting User Inputs  
**Expected Timeline:** 6-8 weeks from user input collection

---

## Executive Summary

Milestone 021 is the human gate that validates the acoustic evaluator built in M015 (Enrollment GREEN). It's **NOT about building anything new** — it's about validating that the deterministic acoustic quality checks already work correctly on held-out data.

**Key Points:**
- ✅ No code changes required
- ✅ No new features to implement
- ✅ Uses the frozen evaluator from M015
- ❌ **Requires user-supplied data and reviewers to proceed**
- ✅ Enables real user enrollment when complete

---

## What M021 Does

### Purpose
Prove that the deterministic acoustic evaluator (voice_narration/enrollment/evaluation.py, frozen from M015) correctly implements the Q11 requirements:

| Requirement | What It Validates |
|-------------|------------------|
| **Q11 Criteria** | Six acoustic checks work correctly |
| **Per-Language** | Hindi and English evaluated separately |
| **Speech Detection** | WebRTC VAD accuracy on held-out samples |
| **SNR Estimation** | Noise-ratio estimates accurate ±3dB |
| **Quality Warnings** | Alerts for clipping, silence, noise all working |
| **False Positive Rate** | No excessive false alarms |

### Timeline if All Inputs Provided
```
Phase 1 (Week 1): Setup & inventory freezing
Phase 2 (Weeks 2-3): Independent reviewer evaluation
Phase 3 (Week 3-4): Adjudication & consensus
Phase 4 (Week 4-5): Evaluator validation runs
Phase 5 (Week 5-6): Analysis & report writing
Total: 6 weeks
```

---

## Current Status: What's Completed ✅

| Item | Status | Evidence |
|------|--------|----------|
| Acoustic evaluator built | ✅ DONE (M015) | voice_narration/enrollment/evaluation.py |
| Evaluator frozen/hashed | ✅ READY | git history preserved |
| Test infrastructure ready | ✅ READY | pytest + test suite |
| Q11 requirements approved | ✅ DONE (2026-10-25) | requirements.md approved |
| Evaluation protocol approved | ✅ DONE (2026-10-24) | evaluation-protocol.md v1 approved |
| Chatterbox model selected for investigation | ✅ DONE (2026-10-24) | approved.md recorded |

**What's Blocking Us:**
❌ Private validation dataset (you must supply)  
❌ Hindi reviewer appointment (you must recruit)  
❌ English reviewer appointment (you must recruit)  
❌ Consent/authorization documentation (you must prepare)

---

## What You (avinash2196) Need to Supply

### 1. **Private Validation Dataset** 📁

**Location:** Separate folder outside the repo (e.g., `/data/calibration-validation/`)

**Hindi Samples:**
- 10-15 clean, consented speech samples
- **Must be different from M015 enrollment training samples**
- Various speakers, noise conditions, clarity levels
- Can include:
  - Clean lab recordings
  - Noisy background (café, office, traffic)
  - Quiet whisper/faint speech
  - One or two clipped samples (for edge cases)

**English Samples:**
- 10-15 clean, consented speech samples  
- **Must be different from M015 enrollment training samples**
- Variety of speakers and conditions
- Similar distribution: clean, noisy, faint, clipped

**What NOT to include:**
- ❌ Samples used during M015 training
- ❌ Samples from the same speakers/dataset source
- ❌ Private data without explicit consent
- ❌ Any audio placed in the git repository (stays private)

**Format:**
```
/calibration-validation/
├── manifest.md          # Inventory & consent reference
├── hindi/
│   ├── sample_01.wav
│   ├── sample_02.wav
│   └── ...             (10-15 files)
├── english/
│   ├── sample_01.wav
│   ├── sample_02.wav
│   └── ...             (10-15 files)
└── reference/          # Clean speech controls (optional)
    ├── hindi_clean.wav
    └── english_clean.wav
```

**Manifest template** (create as `/calibration-validation/manifest.md`):
```markdown
# Calibration Validation Manifest

## Dataset Authorization
- **Owner:** avinash2196
- **Private Location:** [your absolute path]
- **Consent Status:** ✅ All samples consented
- **Date Authorized:** [YYYY-MM-DD]
- **Purpose:** M021 acoustic evaluator validation only

## Hindi Samples (n=12)
- **Source:** [describe source — different dataset than M015 training]
- **Speakers:** 3 different speakers (varied demographics)
- **Conditions:**
  - 4 clean lab recordings
  - 3 with background noise (café/office)
  - 2 faint/quiet samples
  - 2 with clipping or distortion
  - 1 with silence/padding
- **Consent File:** [path to consent document]

## English Samples (n=14)
- **Source:** [describe source — different dataset than M015 training]
- **Speakers:** 4 different speakers
- **Conditions:**
  - 5 clean recordings
  - 4 with background noise
  - 2 faint samples
  - 2 with clipping
  - 1 with echo/reverb
- **Consent File:** [path to consent document]

## Reviewer Appointments
- **Hindi Reviewer:** [Name] — Fluent speaker, [qualifications]
  - Email: [contact]
  - Availability: [dates]
  - Consent to participate: ✅ Yes
  
- **English Reviewer:** [Name] — Native speaker, [qualifications]
  - Email: [contact]
  - Availability: [dates]
  - Consent to participate: ✅ Yes

- **Adjudicator (if needed):** [Name] — Bilingual [dates available]

## Notes
[Any additional context about the validation set]
```

### 2. **Reviewer Recruitment** 👥

**Hindi Reviewer Requirements:**
- Native or fluent Hindi speaker
- Phonetics/linguistics experience preferred (but not required)
- Comfortable listening to 20-30 audio samples
- Can provide independent written annotations
- Available for 2-3 weeks (annotation phase)
- Explicit consent to participate

**English Reviewer Requirements:**
- Native or fluent English speaker
- Audio quality assessment experience helpful
- Comfortable with technical feedback
- Available for 2-3 weeks (annotation phase)
- Explicit consent to participate

**How to Find Reviewers:**
1. **Option A:** Bilingual colleagues or friends
2. **Option B:** Linguistics/audio engineering communities
3. **Option C:** Contract a professional linguistic consultant
4. **Option D:** University linguistics department

**What You Tell Them:**
> "I'm developing a voice-cloning product. I need you to listen to 12-15 voice samples and rate them on speech quality, noise level, clarity, and suitability for training a speech model. Each sample is 5-30 seconds. The task takes about 4-5 hours total (spread over 2-3 weeks). All data is private and confidential."

### 3. **Consent Documentation** 📋

For each sample in your validation dataset, ensure you have:

**Per-Sample Consent:**
- Speaker explicitly consented to use this recording for calibration purposes
- No privacy violations (not public figures, celebrities, etc.)
- Legal right to use the audio (you created it, or you have explicit permission)

**Template Consent Form:**
```
CONSENT FOR CALIBRATION EVALUATION

I, _________________ (name), hereby consent to provide voice recordings 
for use in validating an acoustic quality evaluator for a speech synthesis system.

Recording Details:
- Language: [Hindi / English]
- Date Recorded: [YYYY-MM-DD]
- Sample IDs: [list]
- Duration: [e.g., 5-30 seconds each]

I understand:
✓ Samples will be evaluated by qualified reviewers
✓ Data will be kept private and not shared publicly
✓ Samples may not be reused without my consent
✓ I can withdraw consent at any time

Signed: _________________ Date: _________
```

**Store consent proofs in:**
```
/calibration-validation/consent/
├── sample_hindi_01_consent.pdf
├── sample_hindi_02_consent.pdf
└── ...
```

### 4. **Pre-Validation Checklist** ✅

Before you contact reviewers, complete this checklist:

```markdown
# M021 Pre-Validation Checklist

## Data Preparation
- [ ] Private validation dataset collected (10-15 Hindi, 10-15 English)
- [ ] All samples verified as separate from M015 training set
- [ ] Sample directory structure created
- [ ] manifest.md written with complete inventory
- [ ] All consent documentation collected & stored privately

## Reviewer Recruitment
- [ ] Hindi reviewer identified & contacted
- [ ] Hindi reviewer confirms availability
- [ ] Hindi reviewer consent to participate signed
- [ ] English reviewer identified & contacted
- [ ] English reviewer confirms availability
- [ ] English reviewer consent to participate signed
- [ ] Adjudicator identified (if needed for tie-breaking)

## Setup Documentation
- [ ] Evaluation criteria explained to reviewers
- [ ] Rating scale defined (1-5 scale provided)
- [ ] Sample annotation template prepared
- [ ] Ground truth scale documented
- [ ] Evaluation environment documented (headphones, room, etc.)

## Freezing Evaluator
- [ ] Evaluate commit hash recorded: [git hash]
- [ ] Evaluator file hash recorded: [SHA-256]
- [ ] Detector model hash recorded: [if applicable]
- [ ] Decoder version recorded: [version]
- [ ] All settings frozen (VAD mode, thresholds, etc.)
```

---

## The Validation Process (Phases)

Once you've supplied the inputs above, here's what happens:

### Phase 1: Setup & Inventory (Week 1)
1. **Receive your inputs** (dataset, reviewers, consent)
2. **Freeze evaluator version:**
   ```bash
   git log -1 voice_narration/enrollment/evaluation.py
   sha256sum voice_narration/enrollment/evaluation.py
   ```
3. **Verify data completeness** (counts, sources, consent)

### Phase 2: Reviewer Annotation (Weeks 2-3)
Each reviewer independently listens to 20-30 samples and rates:

**Rating Scale (1-5):**
- 5 = Excellent, clear, natural speech
- 4 = Good, minor issues
- 3 = Understandable, clear issues
- 2 = Major defects, hard to understand
- 1 = Unusable, unrecognizable

**Per-Sample Criteria:**
- Speech presence: "Is speech clearly audible?" (Y/N)
- SNR estimate: "Estimate signal-to-noise ratio" (dB)
- Noise type: "Background, wind, room, echo, other?" (choose)
- Clipping: "Is there audible clipping/distortion?" (Y/N/Maybe)
- Silence: "How much silence?" (none/some/lots)
- Overall quality: (1-5 rating above)
- Recommendation: (Suitable / Warning / Unsuitable)

### Phase 3: Adjudication (Week 3-4)
If reviewers disagree on a sample:
- Adjudicator listens and breaks tie
- Record the consensus rating
- Move forward with majority/consensus result

### Phase 4: Evaluator Validation (Week 4-5)
Run the frozen evaluator on same 20-30 samples:

```python
from voice_narration.enrollment.evaluation import EvaluatorV1

evaluator = EvaluatorV1(policy_version="Q11_v1")

for sample in validation_samples:
    result = evaluator.assess(sample)
    # result contains:
    # - speech_present (bool)
    # - estimated_snr (float, dB)
    # - noise_type (str)
    # - quality_assessment (str: Suitable/Warning/Unsuitable)
    # - warnings (list)
```

### Phase 5: Comparison & Report (Weeks 5-6)
Compare evaluator results vs. ground truth (reviewer consensus):

**Metrics to Calculate:**
- Speech presence accuracy: % correct (target: ≥95%)
- SNR accuracy: mean error in dB (target: ±3 dB)
- Noise type accuracy: % correct (target: ≥85%)
- Quality assessment agreement: % correct (target: ≥95%)
- Warning detection rate: % of warnings caught (target: ≥90%)

**Separate Hindi & English results**

---

## Success Criteria (Go/No-Go Decision)

M021 is **SUCCESSFUL** when:

✅ All per-language metrics meet targets:
- Speech presence accuracy ≥ 95% (Hindi & English separately)
- SNR mean absolute error ≤ 3 dB (Hindi & English separately)
- Quality assessment agreement ≥ 95%
- Warning detection rate ≥ 90%

✅ Complete immutable evidence recorded:
- MILESTONE_021_CALIBRATION_REPORT.md with all metrics
- Evaluator version & hashes frozen
- Reviewer names & qualifications documented
- No production code changed

✅ Human acceptance obtained:
- avinash2196 reviews report
- avinash2196 signs: "Calibration accepted for enrollment enablement"
- Timestamp recorded

---

## If Criteria NOT Met

If results don't meet targets (e.g., SNR accuracy only 87%, not 95%):

**Options (in order):**
1. **Identify root cause** (Was evaluator too strict? Too lenient? Detector needs retraining?)
2. **Return to policy review** (Does the Q11 policy need adjustment?)
3. **Consider corrective actions:**
   - Retrain detector on more/different data
   - Adjust numeric thresholds (requires policy approval)
   - Defer enrollment enablement until resolved

**No "fudging":** We don't adjust thresholds after seeing results. Either we fix the root cause or we wait.

---

## What Happens Next

### If M021 Passes ✅
→ **Proceed to M022** (Approved Model Test Prerequisites)
→ Enrollment enablement approved
→ Job orchestration continues independently

### If M021 Fails ❌
→ **Return to Q11 policy review**
→ Understand why criteria not met
→ Options: Retrain detector, adjust thresholds (policy decision), or defer

### If User Inputs Missing ⏳
→ **M021 stays BLOCKED**
→ Can still work on M022, M023 (Job + Mock Inference continue)
→ Return to M021 when ready

---

## Dependencies & What's Already Ready

| Item | Provider | Status | Available For M021? |
|------|----------|--------|---------------------|
| Acoustic evaluator | M015 completed | ✅ READY | ✅ Yes, frozen |
| Test infrastructure | M002 (FOUNDATION) | ✅ READY | ✅ Yes |
| Q11 requirements approved | Policy decision | ✅ APPROVED (2026-10-25) | ✅ Yes |
| Evaluation protocol approved | Policy decision | ✅ APPROVED (2026-10-24) | ✅ Yes |
| Private validation dataset | **avinash2196** | ❌ WAITING | ❌ Not yet supplied |
| Hindi reviewer | **avinash2196** | ❌ WAITING | ❌ Not yet appointed |
| English reviewer | **avinash2196** | ❌ WAITING | ❌ Not yet appointed |
| Consent documentation | **avinash2196** | ❌ WAITING | ❌ Not yet provided |

---

## How to Start M021

### Step 1: Data Collection (2-4 weeks)
1. Create `/calibration-validation/` directory (outside repo)
2. Collect 10-15 Hindi samples (consented, from different source than M015)
3. Collect 10-15 English samples (consented, from different source than M015)
4. Write manifest.md with complete inventory
5. Gather consent proofs for all samples

### Step 2: Reviewer Recruitment (1-2 weeks)
1. Find Hindi-fluent reviewer (colleague, friend, or professional)
2. Find English-fluent reviewer (colleague, friend, or professional)
3. Explain the task (4-5 hours per reviewer, confidential)
4. Get their agreement & contact info
5. Create reviewer manifest (names, qualifications, contact)

### Step 3: Submit Your Inputs
When ready, provide:
1. Path to `/calibration-validation/manifest.md`
2. Reviewer contact info
3. Confirmation: "Ready to start M021 calibration"

### Step 4: Sit Back
The calibration team (me) will:
1. Verify data/reviewer/consent completeness
2. Run independent annotation phases
3. Collect ground truth
4. Run evaluator validation
5. Produce MILESTONE_021_CALIBRATION_REPORT.md

### Step 5: Review & Accept
You review the report and either:
- ✅ "Calibration accepted" → Proceed to M022
- ⚠️ "Issues need investigation" → Return to policy review

---

## Key Reminders

🔒 **Privacy First:**
- Keep all samples private (outside repo)
- No audio files in git
- Consent required for every sample
- Restrict reviewer access to calibration-only use

🔧 **No Code Changes:**
- M021 is pure validation
- No evaluator tuning
- No threshold adjustments
- If issues found, we fix the root cause via policy review

📊 **Per-Language Validation:**
- Hindi results separate from English
- Both must meet criteria independently
- No averaging away weak language performance

🎯 **Enrollment Enablement:**
- M021 pass = Enrollment can be enabled for real users
- M021 fail = Enrollment stays disabled (waiting for fix)
- Model selection (M022) is independent

---

## Files to Create/Submit

### Required from You:
- [ ] `/calibration-validation/manifest.md` — Dataset inventory
- [ ] `/calibration-validation/consent/` — Consent proofs
- [ ] Reviewer contact information
- [ ] Confirmation message: "M021 inputs ready for validation"

### Will Be Created During M021:
- [ ] MILESTONE_021_CALIBRATION_REPORT.md — Full validation results
- [ ] Calibration evidence summary (frozen evaluator hash, settings, etc.)
- [ ] Per-language metrics table
- [ ] Human acceptance signature & timestamp

---

## Questions?

**What if I don't have reviewers?**
→ We can wait, or you can recruit professional linguistic consultants

**Can I use samples from M015 training?**
→ No, must be held-out (different source/speakers)

**How long does validation take?**
→ 6 weeks total if all inputs ready at start

**Can I proceed with other milestones while waiting for M021?**
→ Yes! M022 (Model Prerequisites) and M023 (Real-Model Inference) can proceed independently

**What if calibration fails?**
→ We identify why, fix the root cause (via policy review), and rerun

**Is there a production fallback if calibration fails?**
→ No. Enrollment stays disabled until calibration passes.

---

## Summary

**M021 = Proof that the acoustic evaluator works**

**Status:** 🔴 BLOCKED on user inputs  
**Timeline:** 6 weeks from data/reviewer submission  
**Outcome:** ✅ Enrollment enabled for real users  
**Impact:** Determines when users can upload voice samples

**Your Action Items:**
1. Collect private Hindi/English validation samples (10-15 each)
2. Recruit Hindi-fluent reviewer
3. Recruit English-fluent reviewer
4. Prepare consent documentation
5. Submit via manifest + contact info

**Next Meeting:** Schedule calibration kickoff once inputs submitted

