# M021 Action Items Checklist
## Acoustic Calibration Validation — What YOU Need to Do

**Status:** 🔴 BLOCKED — Awaiting Your Inputs  
**Last Updated:** 2026-10-30  
**Owner:** avinash2196  

---

## 📋 Phase 1: Data Collection (Est. 2-4 weeks)

### Create Private Validation Dataset Directory
```
Priority: 🔴 HIGH — Must complete first
Timeline: Week 1
Effort: 30 min
```

**Action:**
- [ ] Create directory: `/path/to/calibration-validation/` (outside repo)
  - Example: `D:\AudioData\M021_Calibration\` or `/home/user/m021-data/`
  - Do NOT put this in Voice-Narration repo folder
  
**Why:** Keeps private audio out of git

---

### Collect Hindi Validation Samples
```
Priority: 🔴 HIGH — Critical for progress
Timeline: Weeks 1-2
Effort: 4-6 hours
Target: 10-15 samples
```

**Requirements:**
- [ ] **Different source** than M015 enrollment training data
  - If M015 trained on dataset A, use dataset B/C
  - Different speakers preferred
  - Different recording conditions OK (actually preferred)

- [ ] **10-15 total samples** covering:
  - [ ] 4-5 clean, quiet recordings (reference)
  - [ ] 4-5 with background noise (café, office, street)
  - [ ] 2-3 faint/quiet samples (low volume)
  - [ ] 2-3 with clipping or distortion (edge cases)
  - [ ] 1-2 with silence padding (beginning/end)

- [ ] **Consented:** Each speaker gave explicit permission to:
  - Record their voice
  - Use it for model evaluation
  - Keep it private (not public)

- [ ] **Language:** Hindi (Devanagari script or recorded Hindi speech)

- [ ] **Duration:** 5-60 seconds each (natural speech length)

- [ ] **Format:** WAV or MP3 (what's used in M015)

**Where to Find Samples:**
1. Record yourself (easiest if you speak Hindi)
2. Ask Hindi-speaking friends/colleagues
3. YouTube/podcast clips (ensure consent/licensing)
4. Linguistic research databases (with permission)
5. Professional recording services (if budget available)

**Storage:**
```
/calibration-validation/
├── hindi/
│   ├── sample_001_clean.wav
│   ├── sample_002_clean.wav
│   ├── sample_003_noise_cafe.wav
│   ├── sample_004_quiet.wav
│   ├── sample_005_clipped.wav
│   └── ... (10-15 total)
```

**Evidence You'll Need:**
- [ ] Confirm: "All 12 Hindi samples are from different source than M015 training"
- [ ] List speaker names (for diversity check)
- [ ] Note recording conditions for each

---

### Collect English Validation Samples
```
Priority: 🔴 HIGH — Critical for progress
Timeline: Weeks 1-2
Effort: 4-6 hours
Target: 10-15 samples
```

**Requirements:**
- [ ] **Different source** than M015 enrollment training data
- [ ] **10-15 total samples** covering similar variety as Hindi
- [ ] **Consented** from each speaker
- [ ] **English language** (any dialect acceptable)
- [ ] **Duration:** 5-60 seconds each
- [ ] **Format:** WAV or MP3

**Storage:**
```
/calibration-validation/
├── english/
│   ├── sample_001_clean.wav
│   ├── sample_002_clean.wav
│   ├── sample_003_background.wav
│   └── ... (10-15 total)
```

---

### Write Manifest
```
Priority: 🔴 HIGH — Summarizes your dataset
Timeline: Week 2
Effort: 30 min
```

**File:** `/calibration-validation/manifest.md`

**Template:**
```markdown
# Calibration Validation Manifest

## 1. Dataset Overview
- **Owner:** avinash2196
- **Private Location:** /path/to/calibration-validation/
- **Date Prepared:** 2026-XX-XX
- **Status:** ✅ Ready for evaluation

## 2. Hindi Samples (n=12)
### Source Information
- **Description:** Different recordings from [describe source]
- **Speakers:** Names or IDs (for diversity check)
- **Recording Method:** [e.g., phone microphone, studio, etc.]
- **Separately sourced from M015:** ✅ Yes

### Sample Breakdown
| Sample | Speaker | Duration | Condition | Notes |
|--------|---------|----------|-----------|-------|
| 001 | Speaker A | 15s | Clean, quiet | Reference |
| 002 | Speaker B | 20s | Clean, quiet | Reference |
| 003 | Speaker C | 18s | Café noise | Background |
| ... | | | | |

### Consent Status
- **All samples consented:** ✅ Yes
- **Consent proofs location:** /calibration-validation/consent/

## 3. English Samples (n=14)
### Source Information
- **Description:** [source description]
- **Speakers:** Names or IDs
- **Recording Method:** [method]
- **Separately sourced from M015:** ✅ Yes

### Sample Breakdown
| Sample | Speaker | Duration | Condition | Notes |
|--------|---------|----------|-----------|-------|
| 001 | Speaker X | 12s | Clean | Reference |
| 002 | Speaker Y | 25s | Clean | Reference |
| ... | | | | |

### Consent Status
- **All samples consented:** ✅ Yes
- **Consent proofs location:** /calibration-validation/consent/

## 4. Reference Samples (Optional)
- **Hindi clean reference:** /reference/hindi_clean.wav
- **English clean reference:** /reference/english_clean.wav

## 5. Reviewer Appointments
### Hindi Reviewer
- **Name:** [First Last]
- **Language:** Hindi (native/fluent)
- **Qualifications:** [e.g., linguistics background, audio experience]
- **Contact:** [email or phone]
- **Availability:** [date range]
- **Consent to participate:** ✅ Yes

### English Reviewer
- **Name:** [First Last]
- **Language:** English (native/fluent)
- **Qualifications:** [audio experience, etc.]
- **Contact:** [email or phone]
- **Availability:** [date range]
- **Consent to participate:** ✅ Yes

### Adjudicator (if needed)
- **Name:** [Name] — Bilingual Hindi/English
- **Contact:** [email]
- **Availability:** [dates]

## 6. Data Isolation Confirmation
I confirm that:
- ✅ Hindi samples are from a different source than M015 training data
- ✅ English samples are from a different source than M015 training data
- ✅ All speakers explicitly consented to voice evaluation use
- ✅ All data is kept private (not in public git repository)
- ✅ All data access restricted to authorized reviewers only

## 7. Additional Notes
[Any other context about your validation dataset]

---
**Prepared by:** avinash2196  
**Date:** 2026-XX-XX  
**Ready for validation:** ✅ Yes
```

**To Complete This:**
- [ ] Fill in all `[brackets]` with your actual information
- [ ] Count your samples and verify counts match
- [ ] Confirm different source from M015
- [ ] List reviewer names (even if still recruiting)

---

### Collect & Organize Consent Proofs
```
Priority: 🟠 MEDIUM — Legal requirement
Timeline: Week 2
Effort: 1-2 hours
```

**What You Need:**
For each audio sample, evidence that the speaker consented.

**Options:**
1. **Signed consent form** (best)
   ```
   I, [Speaker Name], consent to provide this voice recording 
   for calibration of a speech model. I understand it will be 
   kept private and used only for quality evaluation.
   
   Signed: _________________ Date: _________
   ```

2. **Email confirmation** (acceptable)
   ```
   Email from speaker: "I give you permission to use my voice 
   recordings for your model evaluation project"
   ```

3. **Recorded verbal consent** (acceptable)
   ```
   Voice memo: "I consent to have this recording evaluated 
   for the voice model calibration study"
   ```

**Storage:**
```
/calibration-validation/consent/
├── hindi_001_consent.pdf  (or .txt, .jpg, etc.)
├── hindi_002_consent.pdf
├── english_001_consent.pdf
└── ...
```

**Action:**
- [ ] Collect consent from each speaker whose sample you have
- [ ] Store in `/calibration-validation/consent/`
- [ ] List consent proofs in manifest.md
- [ ] Verify: "All 26 samples have consent proof"

---

## 👥 Phase 2: Reviewer Recruitment (Est. 2-3 weeks)

### Find & Recruit Hindi Reviewer
```
Priority: 🔴 HIGH — Critical blocker
Timeline: Week 2-3
Effort: 2-4 hours
```

**What to Look For:**
- Native or fluent Hindi speaker
- Willing to listen to 15 samples (2-3 hours total)
- Understands audio/speech quality (linguistics, audio eng., etc.)
- Comfortable giving written feedback
- Available for 2-3 weeks (annotation phase)
- Can maintain confidentiality

**Where to Find:**
1. **Colleagues:** Anyone in your company who speaks Hindi
2. **Friends/Family:** Hindi-speaking friends
3. **Universities:** Linguistics or Audio Engineering departments
4. **LinkedIn:** Search "Hindi linguistics" or "speech scientist"
5. **Fiverr/Upwork:** Contract a professional (costs $50-200)
6. **Communities:** Indian tech forums, language communities

**How to Recruit:**
```
Email Template:

Subject: Help Needed: Audio Evaluation for Voice Model Project

Hi [Name],

I'm developing a voice cloning product and need to validate 
that my quality evaluator works correctly. I'm looking for a 
Hindi-fluent person to listen to 12-15 voice samples (5-30 sec 
each) and rate them on quality/clarity/noise level.

Timeline: About 4-5 hours total over 2-3 weeks
Confidentiality: All data is private; not for publication
Compensation: [Optional: payment, or just "Thanks!"]
What you do: Listen and fill out a rating form per sample

Would you be interested? Let me know!

Thanks,
avinash2196
```

**Action:**
- [ ] Identify 2-3 potential Hindi reviewers (backup plan)
- [ ] Contact them with above template
- [ ] Get confirmation of interest
- [ ] Get their availability dates
- [ ] Get email address for details
- [ ] Record name & qualifications

---

### Find & Recruit English Reviewer
```
Priority: 🔴 HIGH — Critical blocker
Timeline: Week 2-3
Effort: 2-4 hours
```

**What to Look For:**
- Native or fluent English speaker
- Willing to listen to 15 samples (2-3 hours total)
- Audio/speech quality experience
- Available for 2-3 weeks
- Willing to maintain confidentiality

**Where to Find:**
- Same sources as Hindi reviewer
- Easier to find (English speakers more common)

**Action:**
- [ ] Identify 2-3 potential English reviewers
- [ ] Contact them
- [ ] Get confirmation of interest
- [ ] Record name & qualifications
- [ ] Note availability dates

---

### Formalize Reviewer Agreements
```
Priority: 🟠 MEDIUM — Legal/professional
Timeline: Week 3
Effort: 1 hour
```

**For Each Reviewer, Get:**
- [ ] Name & preferred contact method
- [ ] Brief qualifications (e.g., "Native Hindi speaker, linguistics background")
- [ ] Explicit consent to participate
- [ ] Availability (date range for annotation)
- [ ] Confidentiality agreement

**Simple Consent Template:**
```
REVIEWER CONSENT FORM

I, _________________ [Name], agree to participate in the 
calibration evaluation for a voice model project.

I understand:
✓ I will listen to 12-15 voice samples (5-30 seconds each)
✓ I will rate each sample on quality, noise, clarity, etc.
✓ Task takes approximately 4-5 hours total
✓ All data is confidential and private
✓ Results may be used internally for model validation
✓ My identity and feedback will not be published

I am: ☐ Native  ☐ Fluent  [Hindi / English] speaker
My background: _____________ [e.g., linguist, engineer]
Available dates: _____________ [e.g., Nov 1-15]

Signed: _________________ Date: _________
```

**Action:**
- [ ] Prepare consent forms for each reviewer
- [ ] Get signed consent (email OK: "I consent")
- [ ] Store in `/calibration-validation/reviewer-consent/`
- [ ] Update manifest.md with reviewer info

---

## ✅ Phase 3: Pre-Validation Checklist

```
Priority: 🔴 HIGH — Gate before starting evaluation
Timeline: Week 3
Effort: 30 min
```

**Complete This Before Starting Annotation:**

### Data Readiness
- [ ] Hindi samples collected (10-15) and stored
- [ ] English samples collected (10-15) and stored
- [ ] All samples consented
- [ ] manifest.md written with full inventory
- [ ] Consent proofs organized in /consent/ folder
- [ ] Data confirmed separate from M015 training set

### Reviewer Readiness
- [ ] Hindi reviewer recruited, confirmed, consent signed
- [ ] English reviewer recruited, confirmed, consent signed
- [ ] Adjudicator recruited (if needed for tie-breaking)
- [ ] Reviewer contact info recorded
- [ ] Reviewer qualifications documented

### Evaluation Setup
- [ ] Rating scale defined (1-5 scale explained to reviewers)
- [ ] Annotation template prepared (what to fill out per sample)
- [ ] Ground truth scale explained
- [ ] Evaluation environment requirements documented
  - [ ] Quiet room recommended
  - [ ] Good headphones/speakers
  - [ ] Note any background noise during evaluation

### Evaluator Freezing
- [ ] Commit hash of evaluation.py recorded: ________________
- [ ] File hash (SHA-256) recorded: ________________
- [ ] Detector model version recorded: ________________
- [ ] All thresholds/settings noted (no changes during validation)

### Final Sign-Off
```
I confirm that:
✅ All data collected and consented
✅ All reviewers recruited and ready
✅ Evaluation criteria clear
✅ Evaluator frozen (no changes to code)
✅ Ready to start Phase 2 (annotation)

Signed: _________________ Date: _________
```

---

## 📝 Summary of Your Deliverables

**Send When Ready:**

1. **Path to `/calibration-validation/manifest.md`**
   - Complete inventory of all samples
   - Reviewer info
   - Consent proof locations

2. **Confirmation Message:**
   ```
   "M021 calibration validation ready to start.
   
   - Hindi samples: 12 (collected and consented)
   - English samples: 14 (collected and consented)
   - Hindi reviewer: [Name] (contact info in manifest)
   - English reviewer: [Name] (contact info in manifest)
   - Data location: [path]
   - Evaluator frozen at commit: [hash]
   
   Ready to proceed with Phase 2 annotation."
   ```

3. **Copies of:**
   - manifest.md
   - Reviewer consent forms (proof they agreed)
   - Data access instructions (if needed)

---

## 🚀 How to Submit Your Inputs

When you have completed all items in **Phases 1 & 2**, send:

```
Subject: M021 Calibration Validation — Inputs Ready

To: [where you're submitting]

Message:
[Include the confirmation message above]

Attachments or Links:
1. Calibration manifest: [path or file]
2. Reviewer consent proofs: [location]
3. Data access instructions: [if needed]

Ready to start: ✅ Yes
Timeline to complete: 6 weeks from today
```

Once submitted:
- I will verify data/reviewer/consent completeness
- Schedule the annotation phases
- Run evaluator validation
- Produce calibration report with metrics
- You review and accept (or request corrections)

---

## 📊 Timeline Summary

| Phase | Weeks | Your Action | Status |
|-------|-------|------------|--------|
| **1. Data Collection** | 1-4 | Collect samples, write manifest, get consent | 🔴 TODO |
| **2. Reviewer Recruitment** | 2-3 | Find & recruit reviewers, get consent | 🔴 TODO |
| **3. Pre-Validation** | 3 | Complete checklist, freeze evaluator | 🔴 TODO |
| **[Submit Inputs]** | — | Send manifest + confirmation | 🔴 TODO |
| **4. Annotation** (Me) | 4-5 | Reviewers listen & rate samples | ⏳ WAITING |
| **5. Adjudication** (Me) | 5-6 | Resolve disagreements | ⏳ WAITING |
| **6. Evaluator Validation** (Me) | 6-7 | Run evaluator on samples | ⏳ WAITING |
| **7. Analysis & Report** (Me) | 7-8 | Calculate metrics, write report | ⏳ WAITING |
| **[Review & Accept]** | 8 | You review calibration report | ⏳ WAITING |

**Total Timeline:** 6-8 weeks from data submission

---

## ⚠️ Common Pitfalls (Avoid These!)

❌ **Don't:**
- Use samples from M015 training data (must be held-out)
- Put audio files in git repository (keep private)
- Forget to get consent (legal requirement)
- Skip the manifest (hard to track what you collected)
- Recruit reviewers after submitting data (do it before)
- Change evaluator settings during validation (must be frozen)
- Average Hindi & English results (validate separately)

✅ **Do:**
- Keep all audio private (outside repo)
- Get explicit consent from each speaker
- Collect from multiple speakers/conditions
- Document everything in manifest
- Freeze evaluator hash before starting
- Recruit reviewers ASAP (longest pole)

---

## 🤔 FAQ

**Q: Can I use clips from public YouTube videos?**  
A: Only if you have explicit consent from the speaker. Public upload ≠ consent to use for ML evaluation.

**Q: Do reviewers need to be professional linguists?**  
A: Helpful, but not required. Any fluent Hindi/English speaker with basic audio quality knowledge works.

**Q: Can I be my own reviewer?**  
A: Not recommended (bias), but you could if absolutely necessary. Better to have independent reviewers.

**Q: What if I can't find reviewers?**  
A: Wait and keep looking, or contract professionals (Upwork, Fiverr). M021 is a gate; we don't proceed without it.

**Q: How much audio data do I need?**  
A: 10-15 samples per language minimum. More is OK (50+), but diminishing returns.

**Q: Can other milestones proceed while I'm collecting data for M021?**  
A: Yes! M022 (Model Prerequisites) and M023 (Real-Model Inference) can proceed independently.

---

## 📞 Next Step

**When you're ready:**
1. ✅ Complete Phases 1 & 2 above
2. ✅ Prepare manifest.md with all required info
3. ✅ Send confirmation: "M021 inputs ready"
4. ⏳ I'll verify and schedule annotation phases

**Questions before starting?**
- Ask in your next message
- Reference this checklist for specifics

---

**Status:** 🔴 BLOCKED — Waiting for your inputs  
**Owner:** avinash2196  
**Due:** No deadline (but sooner = faster validation)  
**Impact:** Enrollment enablement gates on M021 completion

