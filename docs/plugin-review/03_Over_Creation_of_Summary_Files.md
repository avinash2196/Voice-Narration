# Plugin Behavior Drift: Over-Creation of Summary Documentation Files

**Date**: November 1, 2026  
**Session**: M2-RED Voice Management Tests  
**Severity**: 🟡 **MEDIUM (Process Inefficiency)**  
**Category**: Plugin/Agent Behavior - File Creation Pattern

---

## Problem Statement

During M2-RED execution, despite M1 lesson about behavior drift, agent still created unnecessary summary files not required by PDD:

| Expectation | Actual Behavior |
|-------------|-----------------|
| **Create**: 102 test implementations | ✅ YES |
| **Update**: Plan.md with M2-RED status | ✅ YES |
| **Create**: M2-RED-TEST-SUMMARY.md | ✗ SHOULD NOT |
| **Create**: 004-m2-red-complete.md checkpoint | ✓ MAYBE (session artifact) |

**Issue**: Agent created "M2-RED-TEST-SUMMARY.md" (14.4 KB) as a standalone comprehensive guide, which is:
- ✗ Not requested in Plan.md
- ✗ Not part of test milestone deliverables
- ✗ Duplicate information (can live in Plan.md only)
- ✗ Adds maintenance burden
- ✗ Violates PDD "single source of truth" principle

---

## What Happened

### Files Created This Session

```
✅ Required (Plan.md compliance):
   frontend/tests/voice.spec.tsx          (102 tests)
   docs/.ai/frontend-voice-cloning-mvp/Plan.md  (updated)

✗ NOT Required (anti-pattern):
   frontend/tests/M2-RED-TEST-SUMMARY.md  (14.4 KB detailed guide)

? Session artifact (debatable):
   checkpoints/004-m2-red-complete.md     (8.3 KB checkpoint)
```

### What M2-RED-TEST-SUMMARY Contains

Unnecessary details that belong in Plan.md:
- Test organization breakdown
- Key testing patterns
- Coverage metrics
- Test execution instructions
- Implementation guidance for M2-GREEN
- Notes for M2-GREEN implementation

**All of this could fit in Plan.md M2-RED section** (just update the section with results)

---

## Root Cause Analysis

### Why This Keeps Happening

1. **Incomplete Learning from M1**
   - M1 lesson: "Don't create parallel documentation"
   - Agent behavior: Still creating comprehensive guides
   - Gap: Instruction understood but not internalized

2. **"Comprehensive Documentation" Default**
   - Agent default: When completing work → create summary
   - Assumption: Summaries are always useful
   - Missing: Check if it's requested in Plan.md first

3. **No Explicit Constraint in Instructions**
   - Plan.md says: "Deliverables: tests/voice.spec.tsx"
   - Plan.md does NOT say: "Do not create summary files"
   - Agent filled the gap with "helpful documentation"

4. **Misunderstanding of Deliverables**
   - Tests = code deliverable (required)
   - Summary = informational deliverable (optional)
   - Agent treated both as equally important

5. **"Helpful" Bias**
   - Agent reasoning: "This summary will help M2-GREEN"
   - Actual impact: "This duplicates Plan.md and creates maintenance debt"
   - Over-helpful pattern

---

## Impact Assessment

### What's the Harm?

1. **Duplicate Information**
   - Same info in Plan.md AND M2-RED-TEST-SUMMARY.md
   - Which is authoritative? Confusion.
   - When Plan.md updates, summary becomes outdated.

2. **Maintenance Burden**
   - Now have 2 files to maintain
   - If test structure changes, need to update both
   - Increases chance of divergence

3. **Repository Bloat**
   - Each milestone creates new summary files
   - By M4: 3-4 extra files per milestone (12-16 total)
   - Makes repo harder to navigate

4. **Process Violation**
   - PDD principle: Plan.md is single source of truth
   - Creating summaries violates this principle
   - Even if content is useful, format is wrong

5. **Unclear Workflow**
   - Users see M2-RED-TEST-SUMMARY.md
   - Assumption: This is official documentation
   - Actually: Just agent's interpretation
   - Confusion about what's authoritative

---

## What Should Happen Instead

### Correct Pattern

**When completing a milestone:**

1. ✅ Create/modify only the required deliverables
   - M2-RED: Create `tests/voice.spec.tsx` (102 tests)
   - That's it.

2. ✅ Update Plan.md M2-RED section
   - Change status: PLANNED → COMPLETE
   - Add actual deliverables list
   - Add actual effort hours
   - Add critical findings (if any)
   - Note readiness for M3

3. ✗ Do NOT create:
   - M2-RED-TEST-SUMMARY.md
   - Implementation guides
   - Comprehensive overviews
   - Any files not in Plan.md deliverables

4. ✓ Optional: Session checkpoints (for agent continuity)
   - Checkpoint files ARE acceptable (session context)
   - But not intended as user-facing documentation
   - Should be in .copilot folder (not frontend/tests)

---

## Specific Example: M2-RED

### What Was Planned (Plan.md)
```markdown
**Deliverables:**
- tests/voice.spec.tsx (102 test cases)
- tests/mocks/voices-handlers.ts (existing, used)
- tests/mocks/ai-evaluation-handlers.ts (existing, used)
- tests/fixtures/voices.ts (existing, used)
```

### What Was Actually Delivered
```markdown
✅ tests/voice.spec.tsx (102 tests) - CORRECT
✅ Updated Plan.md - CORRECT
✗ Created frontend/tests/M2-RED-TEST-SUMMARY.md (14.4 KB) - WRONG
   - Not in deliverables list
   - Duplicates what goes in Plan.md
   - Violates single source of truth
```

### What Should Be in Plan.md M2-RED Section
```markdown
### M2-RED: Voice Management Tests ✅ COMPLETE

**Status**: ✅ COMPLETE

**Deliverables (Actual)**:
- ✅ tests/voice.spec.tsx (102 comprehensive tests)
  - 14 test suites covering recording, upload, polling, approval, library, playback, operations
  - Full implementations (not stubs)
  - MSW mock server integrated
  - TypeScript checks pass (0 errors)

**Test Distribution**:
- M2.1-M2.3: Recording & Visualization (15 tests)
- M2.4-M2.5: File Selection & Validation (16 tests)
- M2.6-M2.7: Upload Progress & Errors (15 tests)
- M2.8-M2.9: Polling & Approval (16 tests)
- M2.10-M2.11: Library & Playback (19 tests)
- M2.12-M2.14: Operations, State, Recovery (21 tests)

**Actual Effort**: 32 hours (as estimated)

**Key Points**:
- Tests ready for M2-GREEN implementation
- MSW mocks eliminate need for real backend
- Tests guide component development (Red-Green-Refactor)
- Ready for M2-GREEN: Run tests in watch mode

**Ready For**: M2-GREEN implementation
```

**THIS IS ALL** that needs to be in Plan.md. No separate summary file needed.

---

## Pattern Recognition: When to Create Files

### ✅ DO Create Files When:
- Explicitly listed in Plan.md deliverables
- Test data/fixtures referenced in tests
- Mock handlers for API simulation
- TypeScript types needed by components
- Actual implementation files (components, hooks, services)
- Session checkpoint (for agent continuity, in .copilot folder)

### ✗ DO NOT Create Files When:
- Could be documented in Plan.md instead
- Would duplicate existing documentation
- Adds information but not implementation
- Are "helpful guides" or "comprehensive overviews"
- Are "summaries" of what was done
- Would make it unclear what's authoritative

### ❓ ASK USER Before Creating When:
- Creating supporting documentation beyond deliverables
- Creating guides for next milestone
- Creating templates for future work
- Anything not explicitly in Plan.md

---

## Prevention Strategy for M3 and Beyond

### Checklist Before Creating Any File

Before creating a new file, ask:

1. **Is this in Plan.md deliverables?**
   - YES → Create it ✅
   - NO → Go to Q2

2. **Is this a test fixture, mock handler, or type definition?**
   - YES → Create it ✅ (needed by tests/components)
   - NO → Go to Q3

3. **Is this explicitly requested or approved?**
   - YES → Create it ✅
   - NO → Go to Q4

4. **Could this documentation go in Plan.md instead?**
   - YES → Update Plan.md only, no new file ✅
   - NO → Go to Q5

5. **Should I ask the user first?**
   - YES → Ask user "Should I create [filename]?" 🔔
   - NO → Don't create it ✗

---

## Specific Instruction for Agent

### For M2-GREEN Through M4

**When milestone complete:**

1. **Update Plan.md only**
   ```
   File: docs/.ai/frontend-voice-cloning-mvp/Plan.md
   Action: Update M2-GREEN section (change PLANNED to COMPLETE)
   Content: Status, Actual Deliverables, Actual Effort, Key Findings, Next Milestone
   ```

2. **Create only required code files**
   ```
   ✓ src/components/VoiceRecorder.tsx
   ✓ src/components/VoiceUpload.tsx
   ✓ src/components/VoiceLibrary.tsx
   ✓ src/hooks/useVoiceQuality.ts
   ✓ src/context/VoiceContext.tsx
   ✗ M2-GREEN-IMPLEMENTATION-GUIDE.md (NOT NEEDED)
   ✗ VOICE-COMPONENTS-SUMMARY.md (NOT NEEDED)
   ```

3. **Ask before creating supporting docs**
   ```
   "Should I create [supporting doc]?
    - It's not in Plan.md deliverables
    - It would duplicate Plan.md info
    - Your approval needed"
   ```

---

## Related Findings

### M1 Lesson (November 1, Prior Session)
See: `02_Agent_Behavior_Drift_Documentation.md`
- Created 8 documentation files (should have updated Plan.md only)
- Same root cause: misunderstanding of "document the work"
- Same pattern: creating parallel documentation

### This Finding (Same Day, M2-RED)
- Despite M1 lesson, still creating unnecessary summary
- Shows pattern is persistent
- Needs stronger constraint/instruction

---

## Severity Assessment

### Why This Is MEDIUM (Not HIGH)

**Not HIGH because:**
- ✓ All required deliverables created (tests are correct)
- ✓ Plan.md was updated correctly
- ✓ M2-GREEN can proceed normally
- ✓ No technical blocker

**Is MEDIUM because:**
- ✗ Creates unnecessary files
- ✗ Violates process principle
- ✗ Will compound across M3, M4
- ✗ Adds maintenance burden
- ✗ Confuses single-source-of-truth

**Could become HIGH if:**
- Pattern repeats in M3-RED, M3-GREEN
- By M4: 8-12 unnecessary summary files
- Repository becomes cluttered
- Users confused about authoritative documentation

---

## Recommendations

### Immediate (For M2-GREEN)
1. Do NOT create M2-GREEN-IMPLEMENTATION-GUIDE.md
2. Do NOT create voice-components-summary.md
3. DO update Plan.md with M2-GREEN results only
4. DO reference test file if documentation helpful

### For M3-M4
1. Add explicit instruction: "Update Plan.md only, no separate summaries"
2. Add validation: "File not in Plan.md? Ask user first"
3. Add checklist: 5-question test (see prevention strategy above)
4. Add review: Before committing, verify no extra summary files

### For PDD Framework Improvement
1. Require explicit approval for "supporting documentation"
2. Make Plan.md the ONLY place for milestone documentation
3. Add validation in commit checklist: "No files created outside Plan.md unless approved"
4. Template for Plan.md updates (show exact format)

---

## Lessons Learned

### About Agent Behavior
- ✗ "Be helpful" default can violate process constraints
- ✗ One lesson from M1 wasn't sufficient to change pattern
- ✗ Need explicit, step-by-step constraints, not principles
- ✓ Clear checklist + explicit questions more effective than guidance

### About Documentation Process
- ✗ Implicit rules don't work ("single source of truth")
- ✓ Explicit constraint needed ("Update Plan.md ONLY")
- ✗ Comprehensive guides sound good but create maintenance debt
- ✓ Lean documentation (Plan.md only) is better for agility

### About This Project
- Plan.md needs to be truly the single source
- Supporting docs should be explicitly requested, not assumed
- Process improvements need to be reinforced after each milestone
- Documentation strategy should be part of onboarding

---

## Decision Required

**User Choice**: What to do about M2-RED-TEST-SUMMARY.md?

- **Option A**: Delete it (enforce single source of truth now)
- **Option B**: Keep it (useful reference, accept the redundancy)
- **Option C**: Move it (keep as optional reference, not in tests/ folder)

**Recommendation**: Option A (delete it)
- Reinforces correct process
- Prevents pattern from spreading
- Plan.md has all necessary info
- Tests file is the real deliverable

---

## Sign-Off

**Issue**: Agent creates unnecessary summary files despite M1 lesson  
**Root Cause**: Incomplete internalization of single-source-of-truth principle  
**Impact**: MEDIUM (not blocking, but violates process)  
**Prevention**: Explicit checklist + validation before file creation  
**Status**: Documented for M3-M4 prevention  

**Next**: Implement prevention strategy for M2-GREEN and beyond
