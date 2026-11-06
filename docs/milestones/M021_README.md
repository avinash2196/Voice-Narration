# M021 Milestone Planning — Complete Documentation Package
## Acoustic Calibration Validation (OTHER)

**Date Created:** 2026-10-30  
**Status:** 🔴 BLOCKED — Awaiting User Inputs  
**Timeline:** 6-7 weeks from data submission  

---

## 📚 Complete Document Set

You now have **4 complementary planning documents** + the existing **PDD Implementation Plan framework**:

### For Quick Understanding (Start Here)
📄 **M021_QUICK_START.md** (13 KB, ~15 min read)
- TL;DR (30 seconds)
- 5-minute overview
- Priority action items (1-4)
- Timeline & success metrics
- FAQ & next steps

**Use this for:** Getting the basics quickly, deciding whether to start now

### For Step-by-Step Execution
✅ **M021_ACTION_ITEMS.md** (17 KB, ~45 min read)
- Phase 1: Data Collection (detailed checklist)
- Phase 2: Reviewer Recruitment (detailed)
- Phase 3: Pre-Validation Checklist
- Timeline per phase
- Common pitfalls to avoid
- FAQ

**Use this for:** Following the exact steps to collect data and recruit reviewers

### For Complete Understanding
📋 **MILESTONE_021_PLANNING.md** (18 KB, ~60 min read)
- Executive summary
- What M021 is & why it matters
- Current status (what's done, what's blocked)
- Complete validation protocol (5 phases)
- Success criteria & go/no-go thresholds
- Failure conditions & remedies
- All references to Q11 policy & evaluation protocol
- Known dependencies & waiting states
- FAQ with detailed answers

**Use this for:** Understanding everything in depth, all policy references

### For Integration & Reference
🎯 **M021_COMPLETE_PACKAGE.md** (14 KB, ~10 min skim)
- Summary of all documents
- How these documents fit together
- Reading paths (quick/full/check-progress)
- Your immediate action items
- Document quick reference table
- Success definition
- Next conversation steps

**Use this for:** Navigation between documents, understanding relationships

### PDD Authority (Production Standard)
🔧 **docs/.ai/initial-build/021_Implementation_Plan_Enrollment_Acoustic_Calibration_Validation.md**
- Official PDD Implementation Plan format
- Milestone authorization & references
- Current state & work scope
- Validation protocol (5 phases with exact specs)
- Acceptance criteria (objective, measurable)
- Responsibilities (user & validation team)
- Timeline & dependencies
- Success & outcome definitions
- Execution readiness checklist

**Use this for:** Authority reference, PDD compliance, formal acceptance criteria

---

## 🚀 How to Get Started (Right Now)

### Step 1: Read (Pick One Path)
```
Path A (15 min): M021_QUICK_START.md
                 → TL;DR + action items + FAQ
                 
Path B (2 hours): M021_QUICK_START.md
               → MILESTONE_021_PLANNING.md  
               → M021_ACTION_ITEMS.md
               
Path C (1 hour): M021_COMPLETE_PACKAGE.md
              → Skip to "Your Action Plan" section
```

### Step 2: Decide
```
Option 1: Start M021 prep now (2-4 weeks)
          ✅ Fastest path to validation
          ✅ Enrollment enablement sooner
          
Option 2: Parallel work (M021 + M022 + M023)
          ✅ Multiple milestones progress
          ✅ Finish around same time
          
Option 3: Wait and start later
          ✅ Proceed with M022/M023 first
          ⏳ No deadline on M021
```

### Step 3: Take Action (If Starting Now)
```
Week 1-2:
- [ ] Create /calibration-validation/ folder (outside repo)
- [ ] Start collecting Hindi voice samples (10-15)
- [ ] Start collecting English voice samples (10-15)
- [ ] Email potential reviewers (3-5 people per language)

Week 2-3:
- [ ] Get confirmations from reviewers
- [ ] Collect consent from all speakers
- [ ] Write manifest.md

Week 3:
- [ ] Complete pre-validation checklist
- [ ] Submit: manifest + confirmation
```

### Step 4: We Handle the Rest
```
Weeks 4-9: Validation team runs 5-phase evaluation
           (You can continue other work in parallel)
           
Week 10:   You review MILESTONE_021_CALIBRATION_REPORT.md
           and approve or request corrections
```

---

## 📊 What You'll Get (After 6-7 Weeks)

### If Calibration Passes ✅
```
Speech Presence Accuracy (Hindi):    98% ✅
SNR Estimate Accuracy (Hindi):       1.2 dB ✅
Quality Assessment (Hindi):          100% ✅

Speech Presence Accuracy (English):  96% ✅
SNR Estimate Accuracy (English):     2.1 dB ✅
Quality Assessment (English):        100% ✅

→ Enrollment enablement APPROVED
→ Users can upload voice samples
→ Proceed to M022 (Model Prerequisites)
```

### If Calibration Doesn't Pass ❌
```
[Specific metrics and failures documented]

→ Return to Q11 policy review
→ Identify root cause
→ Options: Retrain detector, adjust thresholds, defer

[No silent threshold adjustment — policy review required]
```

---

## 🎯 Key Facts to Remember

✅ **What's Already Done:**
- Acoustic evaluator built & frozen (M015)
- Q11 policy approved (2026-10-25)
- Evaluation protocol v1 approved (2026-10-24)
- Infrastructure ready (M002)

❌ **What You Must Provide:**
- Private validation dataset (Hindi + English, 10-15 each)
- Hindi-fluent reviewer
- English-fluent reviewer
- Consent documentation

⏰ **Timeline:**
- Your prep: 2-4 weeks
- Validation: 6 weeks
- Total: 8-10 weeks

🚫 **Important Constraints:**
- Data must be different source than M015 training
- No code changes (validation-only)
- No threshold tuning after seeing results
- Both languages must pass independently

🔗 **Independent Milestones:**
- M022 (Model Prerequisites) — can proceed in parallel
- M023 (Real-Model Inference) — can proceed in parallel
- Job orchestration (done) — no impact

---

## 📖 Reading Guide by Use Case

| Question | Document | Section | Time |
|----------|----------|---------|------|
| "What is M021?" | QUICK_START | TL;DR | 2 min |
| "Should I start now?" | QUICK_START | Timeline | 5 min |
| "How do I collect data?" | ACTION_ITEMS | Phase 1 | 20 min |
| "Who should I recruit?" | ACTION_ITEMS | Phase 2 | 15 min |
| "What's the exact criteria?" | PLANNING | Acceptance Criteria | 5 min |
| "What if it fails?" | PLANNING | Failure Conditions | 5 min |
| "Complete understanding" | PLANNING | Full doc | 60 min |
| "How do these fit together?" | COMPLETE_PACKAGE | Full doc | 10 min |
| "Official authority" | Implementation Plan | Full doc | 45 min |
| "Just tell me the steps" | ACTION_ITEMS | Checklist | 30 min |

---

## 🗂️ File Locations

```
Voice-Narration/
├── M021_README.md (this file)
├── M021_QUICK_START.md
├── M021_ACTION_ITEMS.md
├── MILESTONE_021_PLANNING.md
├── M021_COMPLETE_PACKAGE.md
└── docs/
    └── .ai/
        └── initial-build/
            └── 021_Implementation_Plan_Enrollment_Acoustic_Calibration_Validation.md
```

---

## ✅ Your Checklist

### Before Reading Anything
- [ ] You've read this README (5 min)

### Pick Your Path
- [ ] Path A: QUICK_START only (15 min total)
- [ ] Path B: QUICK_START + PLANNING + ACTION_ITEMS (2 hours total)
- [ ] Path C: COMPLETE_PACKAGE summary (1 hour total)

### Make a Decision
- [ ] Yes, starting M021 prep now
- [ ] No, deferring to later
- [ ] Yes, but parallel with M022/M023

### If Starting Now
- [ ] Read M021_ACTION_ITEMS.md Phase 1 carefully
- [ ] Create /calibration-validation/ folder
- [ ] Email 3-5 potential Hindi reviewers
- [ ] Email 3-5 potential English reviewers
- [ ] Start collecting samples

### When Ready to Submit
- [ ] All Hindi samples collected (10-15)
- [ ] All English samples collected (10-15)
- [ ] Consent from all speakers collected
- [ ] Reviewers confirmed & ready
- [ ] manifest.md written
- [ ] Pre-validation checklist completed
- [ ] Send confirmation: "M021 inputs ready"

---

## 🤔 Common Questions

**Q: How long will this take?**  
A: 2-4 weeks to collect data + recruit reviewers. Then 6-7 weeks validation. Total: 8-10 weeks.

**Q: Do I need to pay reviewers?**  
A: No (if friends/colleagues). Optional if hiring professionals ($100-200 total).

**Q: Can other milestones proceed?**  
A: Yes! M022, M023, and job orchestration all proceed independently.

**Q: What if I can't find reviewers?**  
A: M021 stays blocked until you do. This is a gate — no workarounds.

**Q: Can I use data from M015 training?**  
A: No. Must be separate/held-out source.

**Q: What happens if calibration fails?**  
A: Return to Q11 policy review. Identify root cause, fix, rerun. No shortcuts.

---

## 🎓 Next Steps (Right Now)

1. **Skim this README** (5 min) ← You are here
2. **Choose your reading path** (decide now)
3. **Read the chosen docs** (15 min to 2 hours depending on path)
4. **Decide:** Start M021 or wait?
5. **If yes:** Follow M021_ACTION_ITEMS.md Phase 1

---

## 📞 Document Support

- **Quick questions?** → M021_QUICK_START.md FAQ section
- **Detailed questions?** → MILESTONE_021_PLANNING.md FAQ section
- **Step-by-step help?** → M021_ACTION_ITEMS.md (follow checklist)
- **Official policy?** → Implementation Plan document

---

## Summary

**M021 validates that the acoustic quality checker works correctly.**

**You provide:** Data + reviewers + consent documentation  
**We provide:** Validation, metrics, calibration report  
**Outcome:** Enrollment enabled or policy review  

**Status:** Ready to begin when you provide inputs  
**Timeline:** 6-7 weeks from data submission  
**Effort:** 8-10 hours from you (mostly upfront)  

---

**Ready to go? Start with M021_QUICK_START.md → 15 minutes → action items**

Good luck! 🚀
