# Enrollment catalog listing seam — correction proposal

## Problem and scope

GREEN planning found an incomplete dependency interface in approved RED plan 010. `tests/test_voice_enrollment.py` requests authenticated `GET /models` before a request supplies a model identity. The fixture passes only `capability(model)`, and its implementation rejects every argument except the exact synthetic model. The approved contract already requires listing enabled/approved capabilities. No enumeration source is passed to the Voices factory.

The recommended correction adds an explicit `list_capabilities()` collaborator. It changes neither public behavior nor product requirements. No production implementation, source test, approved Plan or approved Implementation Plan is changed by this proposal. Completed RED evidence remains historical evidence of intended missing modules, not proof that these later test bodies have executed.

Sources inspected: approved `contract/API-Contract.md` Models interface; `010_Implementation_Plan_Voice_Enrollment_RED.md` Interface choices and complete test block; current `tests/test_voice_enrollment.py` TestCatalog, make_voices and test_guidance_formats_playback_admission_and_originals; Plan.md completed milestone 10 and pending milestone 11.

## Exact proposed test delta

The following is the complete proposed diff to the existing test. It is for review only, not application authority.

```diff
--- a/tests/test_voice_enrollment.py
+++ b/tests/test_voice_enrollment.py
@@ -53,6 +53,11 @@
         if not self.model_ready or model != MODEL:
             fail("MODEL_NOT_READY")
         return deepcopy(self.cap)
+
+    def list_capabilities(self):
+        # Synthetic enabled/approved catalog records for this isolated test only.
+        # This does not grant production model or calibration approval.
+        return [deepcopy(self.cap)] if self.model_ready else []
 
     def snapshot(self):
         return {"revision": self.revision, "enrollment_quality": deepcopy(self.policy)}
@@ -112,7 +117,9 @@
         return voices_factory(repository=repository, authenticate=auth.state.verify_token,
                               validate_consent=consents.state.validate_owner_consent,
                               artifacts=artifacts.state.enrollment_samples, enrollment=adapter,
-                              capability=catalog.capability, policy_snapshot=catalog.snapshot,
+                              capability=catalog.capability,
+                              list_capabilities=catalog.list_capabilities,
+                              policy_snapshot=catalog.snapshot,
                               calibration=catalog.calibration, clock=lambda: now[0])
 
     voices = make_voices(voices_repo)
```

The corresponding proposed internal Voices factory contract gains required keyword-only `list_capabilities`, a zero-argument callable returning the enabled/approved Capability records available through the catalog boundary. Existing `capability(model)` remains the keyed lookup for admission and enrollment. Authentication, pagination and public serialization remain actual Voices behavior governed by the unchanged API contract. Production must obtain catalog records through its authorized catalog boundary; it may not infer model identities by hardcoding fixture constants or inspecting a bound object's private fields. The new callable supplies catalog data, not acoustic findings, enrollment state or permission to bypass model readiness.

No existing assertion is removed or weakened. The current fixture's single model remains deliberately synthetic and nonproduction. A later exact correction plan must also test the collaborator's empty/ready enumeration and defensive-copy behavior without interpreting those fixture checks as product-model evidence.

## Proposed review sequence

1. Human approves this correction direction.
2. A fresh create-plan revision preserves completed milestones/evidence and inserts a narrowly scoped test-wiring correction before the pending Enrollment GREEN. Its type must follow PDD's no-production-behavior-change rules; the proposed OTHER scope changes test collaborator wiring only. This is a Plan revision, not permission to edit a completed RED milestone's history.
3. After Plan approval, prepare an exact Implementation Plan for that correction, including the affected factory-interface documentation and test diff. Do not rewrite the approved 010 artifact as if the original included the new seam; the new artifact records the delta and carries the old evidence forward explicitly.
4. The correction's verification must pass: exact diff/preservation checks, collection of the intended cases, isolated catalog-fixture checks, and the preserved 57-case regression suite. Do not run expected missing-feature failures and label them a passing OTHER result. Do not claim new RED runtime evidence merely from collection or fixture checks. If the workflow instead requires new RED execution, that needs its own correctly typed approved milestone and criteria.
5. Prepare the Enrollment GREEN Implementation Plan against the corrected, reviewed interface. Its actual full suite must pass after implementation; no production code is authorized by this proposal.

No requirement or external contract amendment is proposed: the existing `/models` behavior stays unchanged. No dependency/configuration/runtime/Docker operation, commit, push or publication is proposed. Existing 57 passing cases, six quality tests, other enrollment assertions, service ownership, quality policy and calibration gates are preserved.

## Human Review

Status: Approved by avinash2196 on 2026-10-25 (America/Chicago; recorded 2026-10-26T04:12:59Z), in response to review of this exact narrow correction and review sequence. This authorizes the proposed planning/review flow, not application of the test delta or production implementation.
