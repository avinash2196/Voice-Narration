# Implementation Plan — Milestone 021
## Enrollment Acoustic Calibration Validation (OTHER)

**Milestone Type:** OTHER (Human Validation)  
**Predecessor:** Mock Inference Adapter GREEN (M020)  
**Requirements:** Q11 Calibration validation  
**Expected Outcome:** Immutable calibration evidence + Human acceptance recorded

---

## Overview

Milestone 021 is a human-driven validation milestone. It validates the deterministic acoustic behavior delivered by Enrollment GREEN (M015) through a separate, carefully controlled calibration protocol. This validation proves that the delivered acoustic evaluator works correctly for the enrolled voices, independent of:
- Deterministic implementation correctness (already proven by M015 tests)
- Production model synthesis quality (separate gate at M023+)
- Human training/collection outcomes (not in scope)

### Key Constraints
- **No production code changes** — This milestone only validates existing behavior
- **Immutable calibration evidence** — All test conditions, settings, and evaluator hashes are frozen and recorded
- **Human expertise required** — Qualified reviewers (Hindi/English speakers) needed
- **Private consented data** — Uses user-supplied Hindi/English validation set with permission
- **Separate held-out evaluation** — Different samples from enrollment training to avoid overfitting claims
- **No calibration tuning** — If criteria not met, returns to policy review rather than covert parameter adjustment

---

## Validation Protocol Specification

### 1. Calibration Objectives

Validate that the deterministic acoustic evaluator (delivered in M015) correctly implements Q11 requirements:

**Q11 Criteria to Validate:**
1. ✅ Independent analytic assessment (no model synthesis involved)
2. ✅ Per-language speech/control assessments (separate Hindi/English)
3. ✅ Suitable-clip warning accuracy and understandability
4. ✅ Estimated SNR acceptance criteria correctness
5. ✅ Recoverable, actionable feedback for users
6. ✅ Silent/noise rejection working correctly
7. ✅ Silence detection and handling
8. ✅ Speech presence detection

### 2. Input Requirements (User-Supplied)

The user (avinash2196) must supply:
- **Private Hindi/English validation dataset** (consented, held-out from enrollment)
- **Clean speech controls** (reference recordings)
- **Noise controls** (synthetic/natural noise samples)
- **Reviewer appointments** (Hindi-capable + English-capable evaluators, minimum 1 person per language)
- **Manifest/authorization** (proof of consent and data authorization)

**What Will NOT Be Supplied by AI:**
- Collection, outreach, or consent gathering (user's responsibility)
- Voice samples or speaker recordings (must be supplied with authorization)
- Reviewer training or coordination (user appoints reviewers)
- Calibration parameter tuning (validation-only)

### 3. Validation Sequence

#### Phase 1: Setup & Inventory (Week 1)
1. **Receive user inputs:**
   - Private manifest of validation dataset location
   - Reviewer names and languages
   - Clean/noise control samples
   - Consent documentation

2. **Freeze evaluator version & hash:**
   ```
   git log voice_narration/enrollment/evaluation.py | head -1
   sha256sum voice_narration/enrollment/evaluation.py > evaluator.sha256
   ```
   Record exact commit hash, file hash, detector version, model version.

3. **Verify inventory completeness:**
   - Minimum Hindi examples: 10-15 held-out samples
   - Minimum English examples: 10-15 held-out samples
   - Separate source from enrollment training set
   - Clean speech, natural speech, various noise conditions
   - Explicit reviewer consent to listen and annotate

#### Phase 2: Independent Reviewer Annotation (Weeks 2-3)
Each reviewer independently evaluates **each sample** using Q11 criteria:

**Per-Sample Evaluation Checklist:**
1. **Speech Presence:** Is speech clearly audible?
2. **SNR Estimate:** What is the estimated Signal-to-Noise ratio?
3. **Noise Type:** Background, wind, room, echo, other?
4. **Clipping:** Is there audible clipping/distortion?
5. **Silence:** How much silence (leading/trailing)?
6. **Language Match:** Matches selected language?
7. **Quality Assessment:**
   - ✅ Suitable for enrollment
   - ⚠️ Warning (noise, faint, other concern)
   - ❌ Unsuitable (poor quality, clipping, wrong language)

**Reviewer Instructions:**
- Use standard listening conditions (headphones, quiet room)
- Annotate independently (no cross-reviewer influence)
- Record exact reasoning for any "Warning" or "Unsuitable" judgments
- Save annotations with sample ID, timestamp, reviewer name

#### Phase 3: Adjudication (Week 4)
Two independent reviewers → Consensus via adjudication:
- If both agree → Consensus result
- If disagree → Adjudicator (expert reviewer) breaks tie
- Document all disagreements and resolutions
- Final consensus becomes **ground truth**

#### Phase 4: Evaluator Validation (Week 4-5)
Run the delivery M015 evaluator on **same samples** using frozen settings:

```python
from voice_narration.enrollment.evaluation import EvaluatorV1

evaluator = EvaluatorV1(
    policy_version="Q11_v1",  # Frozen
    detector_model_hash="...",  # Frozen from Phase 1
    decoder_version="...",  # Frozen
)

results = []
for sample in validation_dataset:
    assessment = evaluator.assess(sample)
    results.append({
        "sample_id": sample.id,
        "language": sample.language,
        "evaluator_speech_present": assessment.speech_present,
        "evaluator_snr": assessment.estimated_snr,
        "evaluator_noise_type": assessment.noise_type,
        "evaluator_quality": assessment.quality_assessment,
        "evaluator_warnings": assessment.warnings,
        "evaluator_recommendations": assessment.recommendations,
    })
```

#### Phase 5: Agreement Analysis (Week 5-6)

Compare evaluator outputs vs. ground truth (adjudicated reviewer consensus):

**Metrics (by language):**
1. **Speech Presence Agreement:** (% exact match)
   - Expected: ≥ 95% accuracy
   
2. **SNR Accuracy:**
   - Expected: Estimated SNR within ±3 dB of reviewer estimate
   - Measure: Mean absolute error

3. **Noise Type Classification:**
   - Expected: ≥ 85% exact match where applicable
   
4. **Quality Assessment Agreement:**
   - Suitable vs. Unsuitable: ≥ 95%
   - Warning detection: ≥ 90% sensitivity (catches warnings reviewers flagged)

5. **Acceptable Rejection:**
   - False negative rate (missed warnings): < 5%
   - False positive rate (false warnings): < 15%

6. **Per-Language Breakdown:**
   - Hindi: Separate metrics
   - English: Separate metrics
   - **Both must meet criteria independently**

**Output Example:**
```
=== Calibration Validation Report ===

Hindi Validation Set (n=12 samples):
  Speech Presence Accuracy: 100% (12/12)
  SNR Estimate MAE: 1.2 dB (within ±3 dB)
  Noise Type Accuracy: 91.7% (11/12)
  Quality Assessment: 100% (12/12)
  Warning Sensitivity: 100% (5/5 warnings caught)
  
English Validation Set (n=14 samples):
  Speech Presence Accuracy: 100% (14/14)
  SNR Estimate MAE: 0.8 dB (within ±3 dB)
  Noise Type Accuracy: 85.7% (12/14)
  Quality Assessment: 100% (14/14)
  Warning Sensitivity: 88% (7/8 warnings caught)

Overall: ✅ PASSED (all criteria met)
```

---

## Acceptance Criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Evaluator version frozen & hashed | | `evaluator.sha256` recorded |
| 2 | Private validation dataset manifest | | User supplies authorized location/consent |
| 3 | Minimum Hindi examples (10-15) | | Separate from enrollment training set |
| 4 | Minimum English examples (10-15) | | Separate from enrollment training set |
| 5 | Qualified reviewers appointed | | Names, languages, qualifications recorded |
| 6 | Independent reviewer annotations | | All samples evaluated independently |
| 7 | Adjudication completed | | Disagreements resolved, consensus recorded |
| 8 | Ground truth established | | Final reviewer consensus per sample |
| 9 | Evaluator run on frozen settings | | Same evaluator version as M015 |
| 10 | Agreement metrics calculated | | Per-language results computed |
| 11 | Speech presence accuracy ≥ 95% | | Hindi ✅, English ✅ |
| 12 | SNR accuracy ≤ ±3 dB MAE | | Hindi ✅, English ✅ |
| 13 | Quality assessment ≥ 95% | | Hindi ✅, English ✅ |
| 14 | Warning sensitivity ≥ 90% | | Hindi ✅, English ✅ |
| 15 | Calibration report completed | | MILESTONE_021_CALIBRATION_REPORT.md |
| 16 | Human acceptance recorded | | avinash2196 signature + timestamp |
| 17 | No parameter tuning occurred | | Policy review required if criteria not met |
| 18 | No production code changed | | All files unchanged except evidence |

---

## Success Criteria

✅ **M021 is SUCCESSFUL when:**

1. **All 8 per-language criteria met:**
   - Speech presence accuracy ≥ 95%
   - SNR accuracy ≤ ±3 dB mean absolute error
   - Quality assessment agreement ≥ 95%
   - Warning sensitivity ≥ 90%
   - Separate validation for Hindi and English

2. **Immutable evidence recorded:**
   - MILESTONE_021_CALIBRATION_REPORT.md with all metrics
   - Evaluator version & hashes (frozen)
   - Reviewer names & qualifications
   - Sample inventory & sources
   - All per-language & overall results
   - No private audio or annotations stored (reference manifest only)

3. **Human acceptance obtained:**
   - avinash2196 reviews complete report
   - avinash2196 signs off: "Calibration accepted for enrollment enablement"
   - Timestamp recorded

4. **No code changes made:**
   - All production/test files unchanged
   - Evidence-only deliverable
   - No hidden parameter tuning

---

## Failure Conditions

❌ **M021 returns to Policy Review if:**

1. **Criteria not met (e.g., SNR accuracy only 87%, not 95%):**
   - Report findings to user
   - Return to policy review for root cause
   - Options: Retrain detector, adjust thresholds (policy decision), defer enrollment

2. **Insufficient data:**
   - Fewer than 10 examples per language
   - Reviewer count insufficient (< 1 per language)
   - Incomplete adjudication (> 20% unresolved disagreements)

3. **Missing authorization:**
   - Consent documentation incomplete
   - Private data not properly isolated from enrollment training
   - Reviewer appointment not formalized

4. **Evaluator mismatch:**
   - Wrong evaluator version used (must match M015 frozen state)
   - Evaluator modified during validation
   - Settings changed from frozen baseline

**No "passing" outcome if criteria unmet.** Issues return for policy decisions, not silent override.

---

## Inputs Required from User (avinash2196)

### Timing
**Timeline:** 6 weeks recommended (Phase 1: 1 week, Phase 2-3: 2 weeks, Phase 4-5: 2 weeks, Phase 6: 1 week)

### Data Inputs
1. **Private validation dataset location:**
   ```
   /path/to/validation/hindi/ (10-15 held-out samples)
   /path/to/validation/english/ (10-15 held-out samples)
   ```
   - Separate source from M015 enrollment training data
   - Consented, authorized
   - Documented in manifest

2. **Clean speech reference samples:**
   - 2-3 high-quality clean recordings per language
   - Used for evaluator baseline comparison

3. **Noise control samples:**
   - Background noise (café, traffic, office)
   - White/pink noise
   - Room echo
   - Wind/environmental

### Personnel Inputs
1. **Hindi reviewer:**
   - Native or fluent speaker
   - Phonetics/linguistics experience preferred
   - Available for independent annotation + adjudication
   - Explicit consent to listen and annotate

2. **English reviewer:**
   - Native or fluent speaker
   - Audio quality assessment experience preferred
   - Available for independent annotation + adjudication
   - Explicit consent to listen and annotate

3. **Adjudicator (if needed):**
   - Bilingual (Hindi/English)
   - Breaks ties on disagreements
   - Expert-level acoustic assessment

### Documentation Inputs
1. **Manifest & consent:**
   ```
   Private Manifest Location: [path/manifest.md]
   Validation Dataset Size: [n Hindi samples, n English samples]
   Reviewer: [Name] — Hindi, [qualifications], consent ✅
   Reviewer: [Name] — English, [qualifications], consent ✅
   Consent File: [path/to/consent/proof.pdf]
   Data Authorization: Consented for this calibration only
   ```

2. **Pre-validation checklist:**
   ```
   - [ ] Dataset sourced from different population than M015 training
   - [ ] All samples have explicit user consent
   - [ ] Reviewers trained on Q11 criteria
   - [ ] Evaluation environment documented (headphones, room, etc.)
   - [ ] Evaluator version frozen & hashed
   - [ ] Ground truth scale defined (5-point? binary?)
   ```

---

## Deliverables

### What Will Be Created (Validation-Only, No Code)

1. **MILESTONE_021_CALIBRATION_REPORT.md** (10-15 KB)
   - Executive summary
   - Per-language accuracy metrics (table format)
   - Sample inventory (count, source, consent status)
   - Reviewer qualifications & independence statement
   - Detailed results (speech presence, SNR, noise type, quality, warnings)
   - Agreement analysis (confusion matrices optional)
   - Acceptance threshold validation (all criteria met? Y/N)
   - Human sign-off section with timestamp

2. **Calibration Evidence Reference** (no private data)
   - Evaluator version & file hash
   - Detector model hash
   - Sample manifest reference (no audio)
   - Reviewer names & qualifications
   - Adjudication notes (sample of disagreements resolved)

### What Will NOT Be Created/Stored
- ❌ Private audio recordings
- ❌ Individual reviewer annotations (only consensus)
- ❌ Personal data beyond reviewer names/qualifications
- ❌ Raw sample files
- ❌ Any private content after calibration complete

---

## Known Dependencies & Waiting States

| Item | Provided By | Status | Impact If Missing |
|------|-------------|--------|-------------------|
| Private validation dataset | avinash2196 | ⏳ WAITING | Cannot proceed (must wait) |
| Hindi reviewer appointment | avinash2196 | ⏳ WAITING | Cannot proceed (must wait) |
| English reviewer appointment | avinash2196 | ⏳ WAITING | Cannot proceed (must wait) |
| Consent documentation | avinash2196 | ⏳ WAITING | Cannot proceed (invalid data use) |
| Evaluator M015 frozen | Completed M015 | ✅ READY | None (already frozen in git) |
| Test infrastructure M015 | Completed M015 | ✅ READY | None (already available) |

---

## No-Code-Change Statement

**This milestone produces validation evidence only.** It does NOT:
- ❌ Change any production code
- ❌ Change any test code
- ❌ Modify runtime configuration
- ❌ Add dependencies or tooling
- ❌ Alter enrollment behavior or accuracy
- ❌ "Tune" or adjust parameters based on results

**If calibration criteria not met,** the path forward is policy review and decision, not covert parameter adjustment.

---

## Timeline & Handoff

### Phase Breakdown
- **Phase 1 (Week 1):** User supplies inputs, setup complete
- **Phase 2 (Week 2-3):** Independent reviewer annotation
- **Phase 3 (Week 3-4):** Adjudication & ground truth finalization
- **Phase 4 (Week 4-5):** Evaluator validation runs
- **Phase 5 (Week 5-6):** Agreement analysis & report writing
- **Phase 6 (Final):** User acceptance & sign-off

### Handoff to Next Milestone
If ✅ ACCEPTED:
- Proceed to M022 (Approved Model Test Prerequisites FOUNDATION)
- Enrollment remains ENABLED (not gated by model approval)
- Deterministic evaluator verified & trusted

If ❌ NOT PASSED:
- Return to Q11 policy review
- No model selection until resolved
- User decides: retrain detector, adjust thresholds, or defer enrollment

---

## Success Definition

✅ **M021 is complete when:**
1. All Q11 per-language criteria validated & passed
2. MILESTONE_021_CALIBRATION_REPORT.md written & reviewed
3. avinash2196 explicitly accepts: "Calibration accepted for enrollment enablement"
4. Timestamp recorded
5. No production code changed

**Status:** Ready for user input (inputs required to start Phase 1)

---

## References

- **Q11 Requirement:** docs/.ai/initial-build/requirements.md (Calibration and verification before enablement section)
- **Enrollment GREEN (M015):** Deterministic evaluator implementation to be validated
- **Private Manifest:** User supplies location/authorization path
- **Evaluator Source:** voice_narration/enrollment/evaluation.py (frozen at M015 completion)

---

## Next Steps

1. **User supplies inputs** (private dataset, reviewers, consent):
   ```
   - Private validation dataset location (Hindi + English, held-out)
   - Reviewer appointments (names, qualifications, consent)
   - Consent/authorization documentation
   - Pre-validation checklist completion
   ```

2. **Calibration team executes** (6-week timeline):
   - Phase 1: Setup & inventory
   - Phase 2-3: Reviewer annotation & adjudication
   - Phase 4-5: Evaluator validation & analysis
   - Phase 6: Report & sign-off

3. **avinash2196 reviews & accepts:**
   - Review MILESTONE_021_CALIBRATION_REPORT.md
   - Verify all per-language criteria met
   - Approve: "Calibration accepted for enrollment enablement"
   - Timestamp recorded in git commit

4. **Proceed to M022** (Model prerequisites) when approved

