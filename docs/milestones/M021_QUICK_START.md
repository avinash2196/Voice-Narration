# M021 Quick Start Guide
## Acoustic Calibration Validation — What You Need to Know

**Status:** 🔴 BLOCKED on your inputs  
**Timeline:** 6 weeks after you submit data + reviewers  
**Effort from you:** 8-10 hours of prep work  

---

## TL;DR: The 30-Second Version

**What is M021?**
- Proof that the acoustic quality checker (built in M015) actually works
- Uses real voice samples + human reviewers to validate accuracy
- No code changes—just validation
- **Required** before users can upload voice samples

**What do you need to do?**
1. Collect 10-15 Hindi voice samples (different source than training)
2. Collect 10-15 English voice samples (different source than training)
3. Find a Hindi-fluent person to listen + rate samples
4. Find an English-fluent person to listen + rate samples
5. Get consent from everyone who provided voice samples
6. Send me the list (manifest.md) when ready

**Timeline:**
- **Your prep:** 2-4 weeks (to collect data + find reviewers)
- **Validation:** 6 weeks (reviewing, comparing, reporting)
- **Total:** 8-10 weeks to completion

**Cost:** Free (reviewers can be friends/colleagues)

---

## The 5-Minute Version

### What's Happening

```
M020 (Mock Inference) is DONE ✅
    ↓
M021 (Calibration Validation) is BLOCKED 🔴 ← You are here
    ↓
[Need your data + reviewers to proceed]
    ↓
M022 (Model Prerequisites) — can start now (independent)
M023 (Real-Model Inference) — can start now (independent)
```

### Why M021 Matters

The acoustic evaluator from M015 makes quality decisions:
- ✅ "This sample is good"
- ⚠️ "This sample has background noise (warning)"
- ❌ "This sample has clipping (rejected)"

**We need to prove it's right.** How?
1. Get real samples (Hindi + English)
2. Have humans listen and rate them
3. Run the evaluator on same samples
4. Compare: Does the evaluator match human judgment?
5. If metrics meet targets → Validation passed → Users enabled

---

## Your Action Items (In Priority Order)

### 🔴 Priority 1: Collect Audio Data (2-4 weeks)

**What:** 20-30 voice samples (10-15 Hindi, 10-15 English)

**Where to get:**
- Record yourself (easiest)
- Ask friends/colleagues who speak Hindi/English
- YouTube clips (if you get consent from speaker)
- Professional recording services

**Requirements:**
- ✅ Different speakers/source than M015 training data
- ✅ Mix of clean & noisy recordings
- ✅ All speakers gave explicit permission
- ✅ 5-60 seconds each
- ✅ Keep private (NOT in git repo)

**Storage:**
```
D:\AudioData\M021_Calibration\
├── hindi/
│   ├── sample_01.wav
│   ├── sample_02.wav
│   └── ...
└── english/
    ├── sample_01.wav
    ├── sample_02.wav
    └── ...
```

**Action Steps:**
1. Create folder for validation data (outside repo)
2. Start collecting samples (record, download, ask people)
3. Organize by language
4. For each speaker, get written/email consent

---

### 🔴 Priority 2: Recruit Reviewers (1-2 weeks)

**Who you need:**
1. **Hindi reviewer** — Fluent Hindi speaker
2. **English reviewer** — Native English speaker
3. Both should understand audio quality

**How to find:**
- Ask at work (any Hindi/English speakers?)
- Ask friends/family
- Post on LinkedIn
- Contact universities (linguistics dept)
- Fiverr/Upwork (if budget available, $50-200 each)

**What you tell them:**
> "Help me validate a voice-quality checker. Listen to 15 samples (5-30 sec each), rate on a 1-5 scale. Takes 4-5 hours over 2-3 weeks. All confidential. Want to help?"

**Action Steps:**
1. List 2-3 Hindi speakers you could ask
2. List 2-3 English speakers you could ask
3. Email them the template above
4. Get confirmations of interest
5. Record their contact info + availability

---

### 🟠 Priority 3: Get Consent (1 week)

**For each voice sample:**
- Get the speaker's permission to use it
- Email consent is fine: "I give you permission to use my voice for model evaluation"

**Document it:**
```
/AudioData/M021_Calibration/consent/
├── hindi_01_consent.txt
├── english_01_consent.txt
└── ...
```

---

### 🟠 Priority 4: Write Manifest (2-4 hours)

**File:** `/AudioData/M021_Calibration/manifest.md`

**Content:**
```
# Calibration Manifest

Owner: avinash2196
Data Location: [path]
Date: 2026-XX-XX

Hindi Samples: 12 (different source from M015)
English Samples: 14 (different source from M015)

Hindi Reviewer: [Name], fluent speaker
English Reviewer: [Name], native speaker

All samples consented: ✅ Yes
All data separate from training: ✅ Yes
Ready for validation: ✅ Yes
```

See `MILESTONE_021_PLANNING.md` for full template.

---

## Timeline: What Happens When

### Week 1-2: You Collect Data
- Decide where to get samples
- Start recording/downloading
- Ask for consent

### Week 2-3: You Find Reviewers
- Contact potential reviewers
- Get confirmations
- Record details

### Week 3: You Submit
- Write manifest.md
- Send confirmation: "M021 ready to start"
- Message: "Here's my data, here's my reviewers, let's go"

### Weeks 4-9: Calibration Team Works (Me)
- Reviewers listen to 20-30 samples (2-3 hours each)
- I compare evaluator results vs. reviewer ratings
- Generate metrics (accuracy, false positives, etc.)
- Write MILESTONE_021_CALIBRATION_REPORT.md

### Week 10: You Review & Accept
- Read the calibration report
- Check metrics pass targets
- Sign off: "Calibration accepted"
- Enrollment is now enabled for real users

---

## Success Looks Like This

**When Everything Works:**
```
Speech Presence Accuracy (Hindi):  98% ✅ (target ≥95%)
SNR Accuracy (Hindi):              1.2 dB ✅ (target ≤3 dB)
Quality Assessment (Hindi):        97% ✅ (target ≥95%)

Speech Presence Accuracy (English): 96% ✅ (target ≥95%)
SNR Accuracy (English):            2.1 dB ✅ (target ≤3 dB)
Quality Assessment (English):      94% ✅ (target ≥95%)

Overall Result: ✅ PASSED

→ Enrollment enablement approved
→ Users can now upload voice samples
→ Proceed to M022 (Model Prerequisites)
```

---

## What If Criteria Not Met?

If SNR accuracy is only 4.5 dB instead of ≤3 dB:

**Options:**
1. **Investigate:** Why is SNR estimate off? (detector issue, bad training data, etc.)
2. **Fix:** Retrain detector, adjust thresholds (requires policy approval)
3. **Defer:** Wait for fix, rerun validation
4. **Document:** Record why criteria not met, what remedy needed

**No Option:** Don't just lower the threshold. That defeats the purpose.

---

## 10-Minute Checklist

Copy this and fill it out:

```
M021 Preparation Checklist
Date: ____________

DATA COLLECTION
□ Created private data folder (outside repo)
□ Collected 10-15 Hindi samples
□ Collected 10-15 English samples
□ All samples from different source than M015
□ Got consent for each sample
□ Stored in organized folder (hindi/ + english/)

REVIEWER RECRUITMENT
□ Identified 2-3 Hindi-fluent people
□ Identified 2-3 English-fluent people
□ Contacted them with recruitment message
□ Got confirmations of interest
□ Recorded names + contact info

CONSENT
□ Have consent proof for all speakers
□ Organized in consent/ subfolder
□ Documented in manifest

DOCUMENTATION
□ Written manifest.md with:
  □ Dataset inventory (counts, sources)
  □ Reviewer names + qualifications
  □ Consent proof locations
  □ Confirmation: "Different from M015 training"

SUBMISSION READY
□ All items above complete
□ Ready to send: manifest + confirmation
□ Can provide: access to data (if needed)

Date ready to submit: ____________
Contact: ____________
```

---

## Three Paths Forward

### Option A: Start Now (Recommended)
**Timeline:** 2-4 weeks to collect data + find reviewers

**Do this:**
1. Start recording/collecting samples today
2. Email potential reviewers this week
3. Get confirmations over next 1-2 weeks
4. Write manifest when ready
5. Submit around early-mid November

**Advantage:** Fastest path to validation

---

### Option B: Wait & Do Later
**Timeline:** Can start anytime (no deadline)

**Advantage:** Other milestones (M022, M023) proceed independently

**Disadvantage:** Enrollment stays disabled until validation complete

---

### Option C: Parallel Progress
**Recommendation:** Do BOTH
- ✅ Start M021 data collection now (2-4 weeks)
- ✅ While data collecting, start M022 (Model Prerequisites)
- ✅ When M021 ready, validation runs (6 weeks)
- ✅ Meanwhile M022 + M023 progress independently
- ✅ All three finish around same time

---

## Files to Review

1. **MILESTONE_021_PLANNING.md** — Full details
   - Complete overview
   - Validation process (5 phases)
   - Success criteria
   - Known dependencies

2. **M021_ACTION_ITEMS.md** — Step-by-step
   - Phase 1: Data Collection (detailed)
   - Phase 2: Reviewer Recruitment (detailed)
   - Pre-validation checklist
   - Timeline breakdown

3. **This file (M021_QUICK_START.md)** — Quick reference
   - 30-second summary
   - Action items
   - Timeline
   - FAQ (below)

---

## FAQ

**Q: Can I use YouTube clips?**  
A: Only with speaker's explicit permission. Public upload ≠ consent for ML use.

**Q: Must reviewers be professional?**  
A: No. Any fluent speaker with basic audio knowledge works. Friends are fine.

**Q: Can I use samples from M015 training?**  
A: NO. Must be separate/held-out (different speakers/source).

**Q: Do I need consent forms?**  
A: Yes. Email consent from speakers is fine: "I give permission to use my voice for this evaluation."

**Q: What if I can't find reviewers?**  
A: Contract professionals (Upwork, Fiverr). Costs $50-200 per person.

**Q: How much data do I need?**  
A: Minimum 10-15 per language. More is fine (50+), but minimal diminishing returns.

**Q: What if calibration fails?**  
A: Identify root cause (detector issue, wrong thresholds, etc.), fix it, rerun validation. No shortcuts.

**Q: Can M022/M023 start before M021?**  
A: Yes! They're independent. M021 validates enrollment. M022/M023 develop models. No hard dependency.

**Q: How long until I get results?**  
A: 6 weeks from data submission. 8-10 weeks total if including your prep time.

**Q: Is there a cost?**  
A: No (if reviewers are friends). If contract reviewers: $100-400 total.

**Q: What happens if I don't do M021?**  
A: Enrollment stays disabled. Users can't upload voice samples. Gates downstream enrollment/model testing.

---

## Your Next Steps (Right Now)

### Step 1: Read the Planning Docs
- [ ] Read MILESTONE_021_PLANNING.md (15 min)
- [ ] Skim M021_ACTION_ITEMS.md (5 min)
- [ ] Complete the checklist above (5 min)

### Step 2: Make a Decision
- [ ] Will you start M021 prep now?
- [ ] Or wait to coordinate with M022/M023?
- [ ] Or defer for later?

### Step 3: If Starting Now
- [ ] Open folder for audio data (outside repo)
- [ ] List 3-5 potential Hindi speakers
- [ ] List 3-5 potential English speakers
- [ ] Send yourself calendar reminder: "Start M021 data collection this week"

### Step 4: Check In
Once you have data + reviewers ready, send:
```
Subject: M021 Calibration — Ready to Start

Message:
- Data location: [path]
- Hindi reviewer: [name] ([contact])
- English reviewer: [name] ([contact])
- Manifest: [attached or here]
- All samples consented: ✅ Yes
- Data separate from training: ✅ Yes
- Ready to proceed: ✅ Yes
```

---

## One More Thing

**M021 is a Gate, Not a Blocker:**

```
M021 Enablement (Human acoustic validation)
   ↓
   Only affects: Real user enrollment
   
M022 Model Prerequisites (separate)
M023 Real-Model Inference (separate)
   ↓
   Can proceed independently
   
Job Orchestration, Mock Inference
   ↓
   Already complete (M016-M020)
```

**Translation:** You don't need M021 to proceed with anything else. But if you want users to upload voice samples, M021 must pass.

---

## Summary Table

| Item | Timeline | Effort | Status | Next Step |
|------|----------|--------|--------|-----------|
| Audio data collection | 2-4 weeks | 4-6 hrs | 🔴 TODO | Start recording |
| Reviewer recruitment | 1-2 weeks | 2 hrs | 🔴 TODO | Email people |
| Consent docs | 1 week | 1 hr | 🔴 TODO | Get approvals |
| Manifest writing | 1 day | 30 min | 🔴 TODO | Fill template |
| **Submit inputs** | — | — | 🔴 TODO | Send confirmation |
| **Validation runs** | 6 weeks | 0 | ⏳ WAITING | I handle this |
| **Review report** | 1 day | 30 min | ⏳ WAITING | You sign off |

---

**Questions?** Review MILESTONE_021_PLANNING.md or M021_ACTION_ITEMS.md for details.

**Ready to start?** Get going on data collection. You've got this! 🚀

