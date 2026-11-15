# Plugin Review Documentation

This folder contains institutional knowledge about process gaps, lessons learned, and agent behavior issues discovered during Voice Narration Platform development.

**Purpose**: Prevent recurring mistakes and improve processes for future projects.

---

## Contents

### 1. [01_CRITICAL_FE_BE_Architecture_Gap.md](01_CRITICAL_FE_BE_Architecture_Gap.md)
**Severity**: 🔴 CRITICAL  
**Category**: Architecture & Design Process  

**Finding**: Frontend was built in complete isolation from backend microservice architecture, resulting in:
- No login flow wired to auth system
- No protected routes
- Hardcoded API URLs
- No session restoration
- No Bearer token injection
- Broken app with "not authenticated" error

**Root Cause**: Frontend development started before architecture was understood. No collaborative design phase.

**How Fixed**: M1-GREEN implementation (3 phases: Auth + APIs + Error Handling)

**Process Improvement**: Create architecture review gate before frontend code starts.

---

### 2. [02_Agent_Behavior_Drift_Documentation.md](02_Agent_Behavior_Drift_Documentation.md)
**Severity**: 🟡 MEDIUM  
**Category**: Plugin Workflow / Process  

**Finding**: During milestone execution, agent created 8 separate documentation files (90+ KB) instead of updating Plan.md.

**Root Cause**: 
- Ambiguous instructions ("document the work")
- Agent didn't know Plan.md is single source of truth
- No validation before creating new files

**User Feedback**: "Plugin asks to update the plan, not new summary files"

**Process Improvement**: Add explicit constraint "Update Plan.md only" and validation checklist.

---

### 3. [03_Over_Creation_of_Summary_Files.md](03_Over_Creation_of_Summary_Files.md)
**Severity**: 🟡 MEDIUM  
**Category**: Plugin Workflow / File Creation Pattern  

**Finding**: Despite M1 lesson about behavior drift, agent still creates unnecessary summary files during M2-RED (e.g., M2-RED-TEST-SUMMARY.md, 14.4 KB).

**Pattern**: 
- Test milestone completes (✅ correct)
- Plan.md updates (✅ correct)
- BUT: Creates comprehensive guide file (✗ anti-pattern)
- File duplicates information that belongs in Plan.md
- Violates single-source-of-truth principle

**Root Cause**:
- One lesson insufficient to change behavior pattern
- "Be helpful" default overrides process constraints
- No explicit checklist before file creation
- Misunderstanding of what is "deliverable"

**User Feedback**: "Copilot still creates too many files like summary which are not needed as per our plugin"

**Process Improvement**: Add 5-question validation checklist before creating ANY file outside Plan.md deliverables.

---

## Key Insights

### Architecture First, Code Second
> Never write frontend code without understanding backend architecture.

✅ **Correct Process**:
1. Backend team documents service architecture
2. Frontend team reviews and asks questions
3. Both teams sign off on design (**APPROVAL GATE**)
4. Then backend builds services
5. Then frontend builds UI against real backend

❌ **What Happened**:
1. Frontend scaffolded in parallel with backend
2. No architecture review
3. Frontend built with wrong assumptions
4. Complete rework needed during integration

### Plan.md is Authoritative (And Only File)
> All milestone progress tracked in one file (Plan.md). Only required code deliverables created, no summary files.

✅ **Correct Process**:
1. Define work in Plan.md [Milestone] section
2. Execute milestone code (create only required deliverables)
3. Update Plan.md with results (status, deliverables, effort)
4. Proceed to next milestone
5. Zero extra documentation files

❌ **What Happened (M1)**:
1. Executed milestone code (excellent)
2. Created 8 separate documentation files
3. Plan.md minimally updated
4. Multiple conflicting sources of truth

❌ **What Happened (M2)**:
1. Executed milestone code (excellent)
2. Created M2-RED-TEST-SUMMARY.md (14.4 KB)
3. Plan.md updated correctly
4. BUT: Unnecessary summary file added maintenance burden

### Validation Before File Creation
> Add explicit 5-question checklist before creating any file outside Plan.md deliverables.

**Checklist (MUST answer before creating):**
1. Is this in Plan.md deliverables? → YES: Create ✅ | NO: Q2
2. Is this a test fixture/mock/type (needed by tests)? → YES: Create ✅ | NO: Q3
3. Is this explicitly requested/approved? → YES: Create ✅ | NO: Q4
4. Could this go in Plan.md instead? → YES: Update Plan.md only ✅ | NO: Q5
5. Should I ask user first? → YES: Ask 🔔 | NO: Don't create ✗

---

## Recommendations

### For M2-M4 Milestones

1. **Before Starting**
   - ✅ Review Plan.md [Milestone] section
   - ✅ Understand scope and success criteria
   - ✅ Identify dependencies from previous milestone
   - ✅ Confirm: No summary/guide files planned

2. **During Execution**
   - ✅ Build required features
   - ✅ Test against requirements
   - ❌ Do NOT create parallel documentation
   - ❌ Do NOT create summary files
   - ✅ Apply 5-question validation before any new file

3. **After Completion**
   - ✅ Update Plan.md [Milestone] section:
     - Status (COMPLETE, BLOCKED, etc.)
     - Deliverables (actual vs. planned)
     - Effort (actual vs. estimated)
     - Critical findings
     - Dependencies for next milestone
   - ❌ Do NOT create summary files
   - ❌ Do NOT create implementation guides
   - ❌ Do NOT create comprehensive overviews
   - ✅ Reference supporting docs FROM Plan.md (if needed)

### For Future Projects

1. **Add Architecture Review Gate**
   - Create architecture design document before frontend code
   - Get both backend and frontend team sign-off
   - Document: services, ports, data flow, API contracts

2. **Add Process Constraint (EXPLICIT)**
   - "One Plan file per project"
   - "All milestone progress in Plan.md"
   - "No parallel documentation without explicit approval"
   - **"Do not create summary files, implementation guides, or comprehensive overviews"**

3. **Add Validation Checklist**
   - 5-question test BEFORE creating any file
   - Before starting code: "Is architecture approved?"
   - Before proceeding to next milestone: "Is Plan.md up to date?"

---

## Related Files

- **docs/.ai/frontend-voice-cloning-mvp/Plan.md** - Authoritative milestone tracker (ONLY file)
- **docs/frontend-authentication/** - Auxiliary documentation (clearly linked FROM Plan.md)
- **frontend/tests/voice.spec.tsx** - Required code deliverable (not documentation)

---

## Timeline

- **Oct 24, 2026**: Frontend scaffolding (without architecture review)
- **Oct 31, 2026**: User reported "No auth" error
- **Nov 1, 2026**: Architecture review → identified critical gaps
- **Nov 1, 2026**: M1-GREEN execution (3 phases implemented)
- **Nov 1, 2026 (Early)**: Plugin behavior drift identified (8 doc files) → Finding #2
- **Nov 1, 2026 (M2-RED)**: M2-RED tests completed
- **Nov 1, 2026 (Late)**: User reported: "Copilot still creates too many files" → Finding #3
- **Nov 1, 2026 (End)**: Over-creation pattern identified as 2nd behavior drift issue

---

## Lessons Learned

### Agent Behavior
- ✗ One lesson from M1 insufficient to change persistent patterns
- ✗ "Be helpful" bias overrides process constraints
- ✗ Implicit rules don't prevent unwanted behavior
- ✓ Explicit checklist + validation more effective than guidance
- ✓ Constraints must be clear and actionable

### Process Design
- ✗ Single-source-of-truth as principle doesn't work (needs explicit rule)
- ✗ "Comprehensive documentation" always sounds good but creates debt
- ✓ Lean documentation (Plan.md only) better for agility
- ✓ Ask user before creating any file outside deliverables

### This Project
- Need stronger constraints for remaining milestones
- 5-question checklist must be enforced
- User approval needed for any new files
- Plan.md must remain single source of truth

---

## Next Steps

For M2-GREEN and beyond:
1. ✅ Apply 5-question validation before ANY new file
2. ✅ Update Plan.md only (no summary files)
3. ✅ Keep auxiliary docs separate and clearly linked
4. ✅ Ask user before creating anything not in deliverables
5. ✅ Enforce: Plan.md is the ONLY place for milestone documentation

**Key Change from M1 to M2**: 
- M1: Created 8 doc files (❌ learned from it)
- M2: Created 1 summary file (✓ better, but still violated principle)
- M3+: Create 0 summary files (✓✓ goal state)

---

**Last Updated**: November 1, 2026  
**Status**: 🟢 Active - Prevention strategy for M2-GREEN and beyond (3 drift issues tracked)
