# Milestone 021 Planning — Complete Package Summary
## Acoustic Calibration Validation (OTHER)

**Date Prepared:** 2026-10-30  
**Status:** 🔴 BLOCKED — Awaiting User Inputs  
**Owner:** avinash2196  

---

## What Was Just Created

Three comprehensive planning documents to help you prepare for M021:

### 📄 Document 1: MILESTONE_021_PLANNING.md (18 KB)
**Purpose:** Complete, detailed specification  
**Contents:**
- Executive summary (what, why, who needs it)
- Detailed validation protocol (5 phases)
- Acceptance criteria & success definitions
- Failure conditions & remedies
- User input requirements (data, personnel, documentation)
- Timeline breakdown (6-week validation process)
- Dependencies & waiting states
- All references to Q11 & evaluation protocol

**Read this if:** You want to understand everything in detail

**Key Sections:**
- What M021 Does (Purpose & Timeline)
- Current Status (What's Completed vs. Blocked)
- What You Must Supply
- Validation Protocol Specification (5 Phases)
- Success Criteria (Go/No-Go Thresholds)
- Deliverables (What Gets Created)

---

### ✅ Document 2: M021_ACTION_ITEMS.md (18 KB)
**Purpose:** Step-by-step checklist and action plan  
**Contents:**
- Phase 1: Data Collection checklist
  - Create validation directory
  - Collect Hindi samples (10-15)
  - Collect English samples (10-15)
  - Write manifest.md
  - Collect & organize consent proofs
- Phase 2: Reviewer Recruitment checklist
  - Find & recruit Hindi reviewer
  - Find & recruit English reviewer
  - Formalize agreements
- Phase 3: Pre-Validation Checklist
  - Data readiness verification
  - Reviewer readiness verification
  - Evaluator freezing
  - Final sign-off

**Read this if:** You want step-by-step instructions with checkboxes

**Key Sections:**
- What to collect (detailed breakdown)
- Who to recruit (qualifications & where to find)
- When to do it (timelines per phase)
- What goes where (file organization)
- FAQ (common questions answered)

---

### 🚀 Document 3: M021_QUICK_START.md (13 KB)
**Purpose:** Quick reference and fast overview  
**Contents:**
- TL;DR (30-second version)
- 5-minute overview
- Action items (priority order)
- Timeline (what happens when)
- Success metrics table
- 10-minute checklist
- FAQ
- Next steps

**Read this if:** You want the highlights without all the details

**Key Sections:**
- What is M021? (quick answer)
- Your action items (priority 1-4)
- Timeline: Weeks 1-10
- Three paths forward (now, later, or parallel)
- Files to review (which doc to read for what)

---

## How to Use These Documents

### Reading Path #1: "Just Tell Me What to Do" (1 hour)
1. **Read:** M021_QUICK_START.md (15 min)
2. **Skim:** M021_ACTION_ITEMS.md sections 1-3 (20 min)
3. **Action:** Complete 10-minute checklist (15 min)
4. **Result:** Ready to start data collection

---

### Reading Path #2: "I Want Full Understanding" (2 hours)
1. **Read:** M021_QUICK_START.md (15 min)
2. **Read:** MILESTONE_021_PLANNING.md (45 min)
3. **Study:** M021_ACTION_ITEMS.md (30 min)
4. **Review:** All checklists & success criteria (20 min)
5. **Result:** Deep understanding of what's needed & why

---

### Reading Path #3: "Just Checking Progress" (10 min)
1. **Read:** M021_QUICK_START.md TL;DR section (3 min)
2. **Scan:** Status & timeline sections (5 min)
3. **Result:** Know where you stand

---

## Your Immediate Action Items

### 🔴 This Week
- [ ] Read M021_QUICK_START.md
- [ ] Decide: Will you start M021 prep now or wait?
- [ ] If yes: Create data collection folder (outside repo)
- [ ] If yes: Start recruiting reviewers (email potential people)

### 🟠 Next 2-3 Weeks
- [ ] Collect 10-15 Hindi voice samples (different source from M015)
- [ ] Collect 10-15 English voice samples (different source from M015)
- [ ] Get explicit consent from all speakers
- [ ] Finalize reviewer recruitment
- [ ] Write manifest.md summarizing everything

### 🟡 By End of November
- [ ] Complete pre-validation checklist
- [ ] Submit: Path to data + reviewer info + manifest
- [ ] Send confirmation: "M021 inputs ready for validation"

---

## Document Quick Reference

| Question | Document | Section | Read Time |
|----------|----------|---------|-----------|
| What is M021? | QUICK_START | TL;DR | 2 min |
| Why do we need it? | PLANNING | Purpose | 5 min |
| What do I need to collect? | ACTION_ITEMS | Phase 1 | 20 min |
| Who do I need to recruit? | ACTION_ITEMS | Phase 2 | 15 min |
| What's the timeline? | QUICK_START | Timeline | 5 min |
| How do I know it passed? | QUICK_START | Success Looks Like | 3 min |
| What if it fails? | PLANNING | Failure Conditions | 5 min |
| Can other milestones proceed? | PLANNING | Dependencies | 5 min |
| Step-by-step instructions? | ACTION_ITEMS | Full doc | 45 min |
| I need to submit data—what do I send? | ACTION_ITEMS | Phase 3 | 10 min |
| Complete understanding | PLANNING | Full doc | 60 min |

---

## Key Facts to Remember

✅ **What's Already Done:**
- Evaluator built & frozen (M015)
- Infrastructure ready (M002)
- Q11 approved (2026-10-25)
- Evaluation protocol approved (2026-10-24)

❌ **What You Must Provide:**
- Private validation dataset (Hindi + English, 10-15 each)
- Hindi-fluent reviewer
- English-fluent reviewer
- Consent documentation

⏰ **Timeline:**
- Your prep: 2-4 weeks
- Validation: 6 weeks
- Total: 8-10 weeks to completion

📊 **Success Requires All Per-Language Criteria Met:**
- Speech presence accuracy ≥95%
- SNR estimate accuracy ≤±3dB
- Quality assessment agreement ≥95%
- Warning detection rate ≥90%

⚠️ **Important Constraints:**
- Data must be different source than M015 training
- No code changes (validation-only milestone)
- No threshold tuning after seeing results
- Separate validation for Hindi & English

🚀 **Other Milestones Are Independent:**
- M022 (Model Prerequisites) can proceed in parallel
- M023 (Real-Model Inference) can proceed in parallel
- Only enrollment enablement gates on M021

---

## Three Ways to Proceed

### Option A: Start Now ⚡ (Recommended)
**Effort:** 8-10 hours over 2-4 weeks  
**Timeline:** Complete by early December  
**Advantage:** Fastest path to enrollment enablement  

**Action:**
1. Start data collection this week
2. Recruit reviewers next week
3. Submit manifest week 3
4. Validation starts week 4

---

### Option B: Parallel Work 🚀 (Also Recommended)
**Effort:** Same as Option A, but overlapped with M022/M023  
**Timeline:** All three complete around same time  
**Advantage:** Multiple milestones progress simultaneously  

**Action:**
1. Start M021 data collection now
2. Simultaneously start M022 planning/prerequisites
3. Simultaneously start M023 test planning
4. When M021 data ready, validation starts (while M022/M023 continue)

---

### Option C: Defer for Now ⏳ (Also Fine)
**Effort:** 0 now, 8-10 hours later  
**Timeline:** Complete whenever you're ready  
**Advantage:** Time to focus on other work first  

**Action:**
1. Do nothing now
2. Start M021 when ready (no deadline)
3. Other milestones proceed independently

---

## Quality Gates (Must Pass to Proceed)

M021 uses **measurable, objective criteria**. All must pass:

```
✅ Hindi validation set:
   - Speech present accuracy ≥ 95%
   - SNR estimate error ≤ 3 dB (mean absolute error)
   - Quality assessment agreement ≥ 95%
   - Warning detection rate ≥ 90%

✅ English validation set:
   - Speech present accuracy ≥ 95%
   - SNR estimate error ≤ 3 dB (mean absolute error)
   - Quality assessment agreement ≥ 95%
   - Warning detection rate ≥ 90%

✅ Both languages must pass independently
✅ Both metrics and evidence must be documented
✅ Human acceptance must be recorded
```

**Pass:** → Enrollment enablement approved  
**Fail:** → Return to Q11 policy review (identify root cause, fix)

---

## What Gets Created (Deliverables)

### From Validation Team (Me)
When M021 completes, you get:

1. **MILESTONE_021_CALIBRATION_REPORT.md** (10-15 KB)
   - Executive summary
   - Per-language metrics table
   - Sample inventory (reference only)
   - Reviewer qualifications
   - Detailed results & analysis
   - Human acceptance signature
   - Timestamp

2. **Calibration Evidence Summary**
   - Evaluator version & hash (frozen)
   - Detector model version
   - Sample manifest reference
   - Reviewer names & qualifications
   - Adjudication notes (if disagreements)

### NOT Created (Kept Private)
- ❌ Audio files (deleted after evaluation)
- ❌ Individual reviewer annotations (only consensus)
- ❌ Personal data beyond qualifications
- ❌ Any raw sample copies

---

## Dependency Map

```
Enrollment Enablement (User-facing enrollment)
    ↓
M021 (Calibration Validation) ← You must supply data + reviewers
    ↓
Q11 requirements verified ✅
    ↓
Real users can upload voice samples

---

Model Production (Inference)
    ↓
M022 (Model Prerequisites) ← Independent from M021
M023 (Real-Model Inference RED)
    ↓
No dependency on M021 (separate gate)

---

Job Orchestration (Backend)
    ↓
M016-M020 Complete ✅ (already done)
    ↓
No dependency on M021

---

Conclusion: M021 only blocks enrollment enablement.
All other work can proceed independently.
```

---

## Success Definition

M021 is **COMPLETE and SUCCESSFUL** when:

✅ All per-language accuracy criteria met (95%+ speech, 95%+ quality, etc.)  
✅ MILESTONE_021_CALIBRATION_REPORT.md produced & reviewed  
✅ avinash2196 approves: "Calibration accepted for enrollment enablement"  
✅ Timestamp recorded in git history  
✅ Enrollment endpoints enabled for real users  

---

## Next: The Conversation

When you're ready to proceed, the next steps are:

1. **You:** "I've collected data + found reviewers. Here's the manifest."
2. **Validation Team:** Receives manifest, verifies completeness
3. **Validation Team:** Schedules annotation phases, recruits starts
4. **Timeline:** 6 weeks of validation work
5. **Outcome:** MILESTONE_021_CALIBRATION_REPORT.md with metrics
6. **You:** Review metrics, accept calibration
7. **System:** Enrollment enabled for real users

---

## FAQ Quick Links

| Question | Document | Section |
|----------|----------|---------|
| How much data? | ACTION_ITEMS | "Collect Hindi Validation Samples" |
| Which language first? | ACTION_ITEMS | Both simultaneously |
| Can I use YouTube? | QUICK_START | FAQ section |
| Are reviewers paid? | QUICK_START | FAQ section |
| Must use M015 training data? | ACTION_ITEMS | "Collect..." (NO) |
| What if calibration fails? | PLANNING | "Failure Conditions" |
| Can other work proceed? | PLANNING | "Dependencies" |
| Timeline if I start now? | QUICK_START | "Timeline" section |

---

## How These Docs Fit Together

```
M021_QUICK_START.md
├─ 30-second summary (you are here)
├─ 5-minute overview
├─ Priority action items
├─ 10-minute checklist
└─ "Read the other docs for details"

    ↓

M021_ACTION_ITEMS.md
├─ Phase 1: Data Collection (detailed)
├─ Phase 2: Reviewer Recruitment (detailed)
├─ Phase 3: Pre-Validation Checklist
└─ "Go to PLANNING for policy/criteria details"

    ↓

MILESTONE_021_PLANNING.md
├─ Complete specification
├─ All Q11 criteria mapped
├─ Success/failure conditions
├─ Full acceptance thresholds
└─ "Reference for everything"
```

---

## Your Action Plan (Start Here)

### Right Now (5 minutes)
- [ ] Open M021_QUICK_START.md
- [ ] Read TL;DR + 5-minute sections
- [ ] Decide: Start now or later?

### If Starting Now (2-4 weeks)
- [ ] Follow Phase 1 in M021_ACTION_ITEMS.md
- [ ] Collect data (Hindi + English samples)
- [ ] Recruit reviewers
- [ ] Get consent docs
- [ ] Write manifest.md
- [ ] Submit confirmation

### Then (6 weeks)
- [ ] Validation team does annotation, comparison, reporting
- [ ] You wait (sit back, other work proceeds)

### Finally (1 week)
- [ ] Review MILESTONE_021_CALIBRATION_REPORT.md
- [ ] Approve: "Calibration accepted"
- [ ] Proceed: M022 and beyond

---

## Commits Just Made

These documents were added to git:

```
212ced4 Add M021 Quick Start Guide
c4cec2b Plan Milestone 021: Acoustic Calibration Validation
[+ existing milestone planning commits]
```

**How to access:**
```bash
cd Voice-Narration
git log --oneline | head -5  # See commits

cat M021_QUICK_START.md      # Read quick start
cat M021_ACTION_ITEMS.md     # Read action items
cat MILESTONE_021_PLANNING.md # Read full planning
```

---

## Support & Questions

**If you have questions about:**
- **What to collect** → See M021_ACTION_ITEMS.md Phase 1
- **Who to recruit** → See M021_ACTION_ITEMS.md Phase 2
- **Why we need M021** → See MILESTONE_021_PLANNING.md "Purpose"
- **Timeline** → See M021_QUICK_START.md "Timeline"
- **Success criteria** → See MILESTONE_021_PLANNING.md "Acceptance Criteria"
- **Failure scenarios** → See MILESTONE_021_PLANNING.md "Failure Conditions"

---

## TL;DR of the TL;DR

**M021 validates the acoustic quality checker works correctly.**

**You need to supply:**
- 10-15 Hindi voice samples (different source than training)
- 10-15 English voice samples (different source than training)
- Hindi-fluent reviewer
- English-fluent reviewer
- Consent documentation

**Timeline:**
- Your prep: 2-4 weeks
- Validation: 6 weeks  
- Total: 8-10 weeks

**Outcome:**
- ✅ Pass → Users can upload voice samples
- ❌ Fail → Return to policy review (no shortcuts)

**Other work:** Proceeds independently (no hard blocking)

---

## Ready to Go?

**Three documents in your repo:**
1. ✅ M021_QUICK_START.md — Read first (this is the summary)
2. ✅ M021_ACTION_ITEMS.md — Follow when starting
3. ✅ MILESTONE_021_PLANNING.md — Reference for everything

**Next action:** 
1. Read M021_QUICK_START.md (15 min)
2. Decide: start now or wait?
3. If yes: create data folder, start recruiting reviewers
4. If no: move to M022/M023 and come back when ready

Good luck! 🚀

