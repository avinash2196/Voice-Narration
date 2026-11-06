# Implementation Plan — Milestone 023
## Real-Model Inference Integration – RED (Test-First)

**Milestone Type:** RED  
**Predecessor:** Approved Model Test Prerequisites (M022)  
**Requirements:** R-EXP-001, FR-027, FR-025, FR-026, R-LIC-001  
**Expected Outcome:** 1 RED test PASSED + 7 GREEN test stubs, 101+ regression baseline preserved

---

## Overview

Milestone 023 is a RED (test-first) milestone that establishes expected failures before M024 (GREEN) production implementation. M023 creates tests that verify:

1. ✅ Real model inference with selected TTS provider (from M022)
2. ✅ Pause/pace controls work within safe ranges (R-EXP-001, FR-027)
3. ✅ Linguistic chunking without word-splitting (FR-025, FR-026)
4. ✅ Join without clicks/dropouts/repeats (FR-025, FR-026)
5. ✅ Model-specific licensing verification (R-LIC-001)
6. ✅ Hindi pronunciation quality (language fidelity)
7. ✅ Identity preservation (voice consistency)

### Key Constraint
- **Test-First Only:** M023 creates test structure with RED test passing (module verification) and 7 GREEN stubs for M024 implementation
- **Use Real Model:** Tests use the actual model selected in M022 (Pyttsx3, gTTS, Azure TTS, etc.)
- **Deterministic Expected Failures:** RED test verifies missing production module before code written

---

## M023 RED Test Specification

### Test File: tests/test_real_model_inference.py

**Structure:**
- 1 RED test (module verification)
- 7 GREEN test stubs (for M024 production implementation)
- Fixtures for real model provider
- Test data (evaluation corpus from M022)

### RED Test (Expected to PASS)

**Purpose:** Verify voice_narration.inference.production module exists and can be imported

```python
class TestRealModelInferenceRED:
    """RED: Module exists and is importable."""
    
    def test_production_inference_module_missing(self):
        """Verify production inference module exists."""
        try:
            from voice_narration.inference.production import ProductionInferenceProvider
            from voice_narration.inference.production import (
                pause_strength_to_duration,
                safe_pace_range,
                chunk_linguistically,
                join_audio_chunks,
            )
            
            assert callable(ProductionInferenceProvider)
            assert callable(pause_strength_to_duration)
            assert callable(safe_pace_range)
            assert callable(chunk_linguistically)
            assert callable(join_audio_chunks)
        except ImportError as e:
            pytest.fail(f"Production inference module missing: {e}")
```

**Expected Result:** ✅ PASSED (when M024 creates voice_narration/inference/production.py)

---

### GREEN Test Stubs (7 tests for M024 implementation)

#### Test Group 1: Pause & Pace Controls (R-EXP-001, FR-027)

**Test 1.1: Pause Strength Mapping**
```python
class TestPauseAndPaceControls:
    
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_pause_strength_to_duration(self, real_model_provider):
        """Map pause_strength [0.0-1.0] to duration in milliseconds."""
        # pause_strength 0.0 → ~200ms
        # pause_strength 0.5 → ~500ms
        # pause_strength 1.0 → ~1000ms
        pass
```

**Test 1.2: Speech Pace Control**
```python
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_speech_pace_within_safe_range(self, real_model_provider):
        """Verify pace [0.5-2.0] produces safe, intelligible output."""
        # Test speeds:
        # - 0.5x (slow, clear)
        # - 1.0x (normal)
        # - 1.5x (fast, still clear)
        # - 2.0x (max, barely intelligible)
        pass
```

#### Test Group 2: Chunking & Joining (FR-025, FR-026)

**Test 2.1: Linguistic Chunking**
```python
class TestLinguisticChunking:
    
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_chunk_linguistically_no_word_split(self, real_model_provider):
        """Verify chunks respect word boundaries, no mid-word splitting."""
        # Input: "Hello world. How are you?"
        # Expected chunks: ["Hello world.", "How are you?"]
        # NOT: ["Hello wor", "ld. How are", " you?"]
        pass
```

**Test 2.2: Punctuation & Line Breaks as Pause Cues**
```python
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_punctuation_line_breaks_as_cues(self, real_model_provider):
        """Treat periods, commas, line breaks as pause cues, not content."""
        # "Hello. World" → 2 chunks with pause between
        # "Line 1\nLine 2" → 2 chunks with pause between
        pass
```

**Test 2.3: Join Without Artifacts**
```python
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_join_without_clicks_dropouts_repeats(self, real_model_provider):
        """Join chunks without audible clicks, dropouts, or word repeats."""
        # Join audio samples smoothly
        # Verify: no clicks/pops at boundaries
        # Verify: no dropped audio
        # Verify: no word repetition
        pass
```

**Test 2.4: Stable Loudness & Sample Rate**
```python
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_stable_loudness_sample_rate(self, real_model_provider):
        """Verify joined audio maintains stable loudness & sample rate."""
        # All chunks same sample rate (e.g., 48 kHz)
        # Loudness normalized (no sudden jumps between chunks)
        pass
```

#### Test Group 3: Text-to-Audio Mapping (FR-026)

**Test 3.1: Exact Text-to-Audio Chunk Mapping**
```python
class TestTextToAudioMapping:
    
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_exact_text_audio_chunk_mapping(self, real_model_provider):
        """Map each text chunk to exact corresponding audio chunk."""
        # Text chunks: ["Hello", "world"]
        # Audio chunks: [audio_for_hello, audio_for_world]
        # Mapping: text[i] ↔ audio[i]
        pass
```

#### Test Group 4: Model Licensing & Language Quality (R-LIC-001, FR-025)

**Test 4.1: Licensing Verification Gate**
```python
class TestModelLicensingAndQuality:
    
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_licensing_approval_gate(self, real_model_provider):
        """Verify model is approved model (from M022) and licensed for use."""
        # Check model name matches M022 selection
        # Verify approval flag set (R-LIC-001)
        pass
```

**Test 4.2: Hindi Pronunciation Quality**
```python
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_hindi_pronunciation_quality(self, real_model_provider):
        """Verify model produces recognizable Hindi pronunciation."""
        # Test phrases:
        # - "नमस्ते" (Namasté)
        # - "धन्यवाद" (Dhanyavaad)
        # - "कृपया" (Kripaya)
        # Expected: Native speaker recognizes correctly
        pass
```

**Test 4.3: Identity Preservation**
```python
    @pytest.mark.skip(reason="GREEN: M024 production implementation")
    @pytest.mark.asyncio
    async def test_identity_preservation_across_chunks(self, real_model_provider):
        """Verify voice identity consistent across all chunks."""
        # Same voice ID → same speaker across entire narration
        # No sudden voice changes or artifacts
        pass
```

---

## Production Code Interface (For M024)

### Module: voice_narration/inference/production.py

M024 must implement:

```python
from voice_narration.inference import InferenceProvider

class ProductionInferenceProvider(InferenceProvider):
    """Production inference provider using real TTS model from M022."""
    
    async def generate(
        self,
        script: str,
        voice_id: str,
        pause_strength: float = 0.5,  # [0.0-1.0]
        pace: float = 1.0,  # [0.5-2.0]
        **kwargs
    ) -> dict:
        """Generate audio using real model."""
        # Must:
        # 1. Use model from M022
        # 2. Support pause_strength & pace controls
        # 3. Chunk linguistically (no word splitting)
        # 4. Join without artifacts
        # 5. Preserve identity & language fidelity
        pass

def pause_strength_to_duration(pause_strength: float) -> int:
    """Convert pause_strength [0.0-1.0] to duration [200-1000] ms."""
    pass

def safe_pace_range() -> tuple:
    """Return safe pace range [min, max] for selected model."""
    # Most models support [0.5-2.0]
    pass

def chunk_linguistically(text: str) -> list:
    """Split text into chunks respecting word boundaries."""
    # Split on: periods, commas, line breaks
    # Don't split: mid-word, mid-sentence
    pass

def join_audio_chunks(chunks: list) -> bytes:
    """Join audio chunks with pause, no artifacts."""
    # Add pause between chunks
    # Normalize loudness
    # Verify same sample rate
    pass
```

---

## Fixtures Required

### real_model_provider Fixture

```python
@pytest.fixture
async def real_model_provider(model_config):
    """Real inference provider initialized with M022 model."""
    from voice_narration.inference.production import ProductionInferenceProvider
    
    provider = ProductionInferenceProvider(
        model_name=model_config["model_name"],
        model_version=model_config["model_version"],
        language_support=["hi", "en"],
    )
    yield provider
    await provider.close()
```

### model_config Fixture

```python
@pytest.fixture
def model_config():
    """Model configuration from M022 prerequisites."""
    # Loaded from M022 setup (environment variable or config file)
    return {
        "model_name": "[from M022]",  # e.g., "gTTS", "Azure TTS", "Pyttsx3"
        "model_version": "[from M022]",  # e.g., "1.2.3"
        "evaluation_corpus_path": "[from M022]",
        "approved": True,  # From R-LIC-001
    }
```

### evaluation_corpus Fixture

```python
@pytest.fixture
def evaluation_corpus():
    """Evaluation test data from M022."""
    return {
        "hindi_samples": [
            {"text": "नमस्ते", "id": "hi-001"},
            {"text": "धन्यवाद", "id": "hi-002"},
            # ... more samples
        ],
        "english_samples": [
            {"text": "Hello world.", "id": "en-001"},
            {"text": "How are you?", "id": "en-002"},
            # ... more samples
        ]
    }
```

---

## Test Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | 1 RED test verifies module exists | ✅ Will PASS when M024 creates module |
| 2 | 7 GREEN test stubs created | ✅ Will be created in M023 |
| 3 | Test file: tests/test_real_model_inference.py | ✅ Will be created |
| 4 | Fixtures defined (real_model_provider, model_config) | ✅ Will be created |
| 5 | RED test runnable without M024 code | ✅ Tests module import |
| 6 | GREEN tests marked @pytest.mark.skip | ✅ Will be marked for M024 |
| 7 | Evaluation corpus integrated | ✅ From M022 |
| 8 | All 7 GREEN tests ready for M024 | ✅ Structure prepared |

---

## Expected Test Results (After M023 Creation)

**Before M024 execution:**
```
pytest tests/test_real_model_inference.py -v
```

**Expected:**
```
✅ TestRealModelInferenceRED::test_production_inference_module_missing — FAILED
   (ImportError: No module named 'voice_narration.inference.production')
   → RED test expects failure until M024 creates module
```

**After M024 creates module:**
```
✅ TestRealModelInferenceRED::test_production_inference_module_missing — PASSED
⏳ TestPauseAndPaceControls::test_pause_strength_to_duration — SKIPPED
⏳ TestPauseAndPaceControls::test_speech_pace_within_safe_range — SKIPPED
⏳ TestLinguisticChunking::test_chunk_linguistically_no_word_split — SKIPPED
⏳ TestLinguisticChunking::test_punctuation_line_breaks_as_cues — SKIPPED
⏳ TestLinguisticChunking::test_join_without_clicks_dropouts_repeats — SKIPPED
⏳ TestLinguisticChunking::test_stable_loudness_sample_rate — SKIPPED
⏳ TestTextToAudioMapping::test_exact_text_audio_chunk_mapping — SKIPPED
⏳ TestModelLicensingAndQuality::test_licensing_approval_gate — SKIPPED
⏳ TestModelLicensingAndQuality::test_hindi_pronunciation_quality — SKIPPED
⏳ TestModelLicensingAndQuality::test_identity_preservation_across_chunks — SKIPPED

1 PASSED, 10 SKIPPED
```

---

## Regression Baseline

**Expected regression test results after M023:**
```
101+ PASSED (M019 baseline)
14+ SKIPPED (M017/M018/M023 GREEN stubs)
7 FAILED (pre-existing, unchanged)
```

**No new failures expected from M023 (RED only, no production code changes).**

---

## Success Criteria

✅ **M023 RED is successful when:**

1. **RED test structure verified:**
   - tests/test_real_model_inference.py created with 1 RED test + 7 GREEN stubs
   - RED test currently FAILS (expects missing module)

2. **Test infrastructure complete:**
   - Fixtures for real_model_provider, model_config, evaluation_corpus
   - All 7 GREEN tests defined with docstrings & skip reasons
   - Test file imports real model from M022 config

3. **GREEN stubs ready for M024:**
   - 7 stubs cover all requirements (pause/pace, chunking, joining, licensing, language quality)
   - Each stub includes clear purpose & expected behavior
   - All marked @pytest.mark.skip("GREEN: M024 production implementation")

4. **Regression baseline preserved:**
   - 101+ tests still passing (M019 baseline)
   - No new failures introduced
   - Existing 7 pre-existing failures unchanged

5. **Execution evidence recorded:**
   - MILESTONE_023_EXECUTION_EVIDENCE.md documents RED test structure
   - All test names and purposes listed
   - Expected M024 interface specification included

---

## Deliverables

### 1. tests/test_real_model_inference.py
- 1 RED test (module verification)
- 7 GREEN test stubs (M024 production implementation)
- Fixtures: real_model_provider, model_config, evaluation_corpus
- Full docstrings & skip reasons

### 2. MILESTONE_023_EXECUTION_EVIDENCE.md
- RED test verification (1 PASSED – module import fails)
- Test structure documentation (1 RED + 7 GREEN)
- Fixture definitions
- M024 interface specification
- Regression baseline confirmation

### 3. Updated tests/conftest.py
- model_config fixture (loads from M022)
- evaluation_corpus fixture (from M022)

---

## Non-Code-Change Policy

**M023 produces NO production code:**
- ❌ No voice_narration/inference/production.py (that's M024)
- ❌ No production functions or classes
- ❌ No changes to existing production code
- ❌ No configuration changes

**Only deliverables:**
- ✅ Test file with 1 RED + 7 GREEN stubs
- ✅ Fixtures for M024
- ✅ Execution evidence
- ✅ Interface specification

---

## Execution Sequence

1. **Create tests/test_real_model_inference.py**
   - 1 RED test (module verification)
   - 7 GREEN test stubs (all marked SKIP)
   - Fixtures from M022 config

2. **Run RED test to verify expected failure**
   ```bash
   pytest tests/test_real_model_inference.py::TestRealModelInferenceRED -v
   # Expected: ImportError (production module doesn't exist yet)
   ```

3. **Run full test suite to confirm no regressions**
   ```bash
   pytest tests/ -v
   # Expected: 101+ PASSED, 14+ SKIPPED, 7 FAILED (unchanged)
   ```

4. **Create MILESTONE_023_EXECUTION_EVIDENCE.md**
   - Document RED test (expected failure)
   - List all 7 GREEN tests
   - Interface specification for M024
   - Regression baseline confirmation

5. **Commit M023**
   - Test file + fixtures
   - Execution evidence
   - Comprehensive commit message

---

## Handoff to M024

When M023 is ✅ COMPLETE:

**M024 (Real-Model Inference Integration GREEN) will:**
- Create voice_narration/inference/production.py
- Implement ProductionInferenceProvider class
- Implement pause_strength_to_duration(), safe_pace_range(), chunk_linguistically(), join_audio_chunks()
- Complete 7 GREEN tests with full assertions
- Execute & verify: 1 RED PASSED + 7 GREEN PASSED, 101+ regression

---

## Timeline

**M023 Duration:** 2-3 days (test-only, no production code)

- Day 1: Create test file + fixtures
- Day 1: Verify RED test fails (expected)
- Day 2: Run regression suite
- Day 2: Create execution evidence
- Day 3: Commit M023

---

## Summary

✅ **M023 RED establishes test-first interface for real model inference:**
- Tests pause/pace controls (R-EXP-001, FR-027)
- Tests chunking/joining (FR-025, FR-026)
- Tests licensing verification (R-LIC-001)
- Tests Hindi pronunciation & identity (language fidelity)
- Interface specification ready for M024 production implementation
- Regression baseline preserved

**Status:** Ready to execute M023 after M022 complete

