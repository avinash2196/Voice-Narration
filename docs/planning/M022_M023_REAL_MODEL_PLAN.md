# M022 & M023: Real Model Integration Planning

## Quick Status
- **M022** (FOUNDATION): Select TTS model, get credentials, set up compute
- **M023** (RED): Write tests expecting real model to work
- **Then M024** (GREEN): Integrate real inference code

---

## M022: Approved Model Test Prerequisites (FOUNDATION)

### What you need to decide:
1. **Which TTS model?**
   - Azure Speech (SpeechSynthesis API)
   - Google Text-to-Speech
   - ElevenLabs (if budget allows)
   - Other?

2. **Which languages/voices?**
   - Hindi (required by Q11)
   - English (MVP scope)
   - How many voices per language?

3. **Where to run inference?**
   - Local machine (if model < 4GB, GPU available)
   - Cloud (Azure, Google, AWS)
   - Docker container + GPU

### M022 Deliverable:
A `docs/.ai/initial-build/022_Implementation_Plan_Approved_Model_Test_Prerequisites.md` with:
- Selected model + justification
- License terms + links
- API keys/credentials setup (no actual keys in repo)
- Local/cloud environment verification script
- Sample test that loads the model successfully

### Timeline:
- Model selection: 1-2 hours
- Credentials setup: 1-2 hours
- Environment validation: 2-3 hours
- **Total: ~1 day**

---

## M023: Real-Model Inference Integration RED

### What RED must test:
From Plan.md line 457-466:

1. **R-EXP-001; FR-027** — Pause strength & speech pace controls
   - Generate model-supported pause/pace within safe ranges
   - Don't break identity
   - Only expose controls if model supports them

2. **FR-025; FR-026** — Linguistic chunking
   - Split text without breaking words
   - Treat punctuation/line breaks as pause cues
   - Join audio without clicks, dropouts, repeats
   - Keep loudness/sample-rate stable
   - Preserve exact text-to-audio mapping

3. **R-LIC-001** — Licensing validation
   - Prevent production without software/weights/output evidence
   - Use only approved model
   - Demo Hindi pronunciation + quality

### Test stubs already exist:
Tests in `tests/test_real_model_inference.py` (from prior planning):
- `test_pause_strength_within_range`
- `test_speech_pace_support`
- `test_chunk_without_word_splits`
- `test_join_without_artifacts`
- `test_model_license_verification`
- `test_hindi_pronunciation_quality`
- `test_identity_preservation`

### M023 Deliverable:
A `docs/.ai/initial-build/023_Implementation_Plan_Real_Model_Inference_Integration_RED.md` with:
- Test code for above 7 checks
- All marked as `@pytest.mark.xfail` (expected to fail until M024 GREEN)
- Verification that tests collect without errors
- Clear failure reasons (e.g., "MockInferenceProvider doesn't support pause_strength parameter")

### Timeline:
- Write 7 test functions: 2-3 hours
- Verify pytest collects them: 30 min
- Document expected failures: 1 hour
- **Total: ~1 day**

---

## Next After RED:

**M024: Real-Model Inference Integration GREEN**
- Replace MockInferenceProvider with real model
- Implement chunking/joining logic
- Make all 7 tests pass
- Preserve 101-test regression baseline

---

## Questions for you:

1. Which TTS model do you prefer?
2. Do you have Azure/Google/other credentials already?
3. Local inference or cloud-based?
4. How many voices to validate initially?

Once you decide, we can execute M022 today.
