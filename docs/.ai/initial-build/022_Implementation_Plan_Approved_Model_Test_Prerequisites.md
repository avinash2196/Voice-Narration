# Implementation Plan — Milestone 022
## Approved Model Test Prerequisites (FOUNDATION)

**Milestone Type:** FOUNDATION (Prerequisite Establishment)  
**Predecessor:** Enrollment Acoustic Calibration Validation (M021)  
**Requirement:** R-LIC-001 (Model license/approval), R-EXP-001 (Expressive controls)  
**Expected Outcome:** Model-specific test prerequisites verified + Repeatable commands recorded

---

## Overview

Milestone 022 establishes the executable prerequisites needed to run Real-Model Inference Integration RED (M023) and subsequent RED/GREEN/integration milestones. This FOUNDATION milestone does NOT create production code or tests. Instead, it:

1. ✅ Confirms model selection (user decision)
2. ✅ Verifies test assets availability (permitted samples, evaluation corpus)
3. ✅ Confirms compute environment readiness (local, cloud, GPU/CPU)
4. ✅ Records exact repeatable commands for environment setup
5. ✅ Validates all prerequisites in actual deployment environment

### Key Constraints
- **No production code** — This is prerequisites-only
- **No placeholder symbols** — Real model assets must be present
- **No implicit provisioning** — All resources explicitly recorded (with costs, if any)
- **Model selection must be done** — Cannot proceed without approved model choice
- **Exact repeatable commands** — Every setup step must be documented and verified

---

## Prerequisites for M022 to Start

### User Input Required (BLOCKING)

| Item | Required For | Status |
|------|-------------|--------|
| **Model Selection** | Determine which model to use (Pyttsx3, gTTS, Azure TTS, ElevenLabs, etc.) | ⏳ WAITING |
| **Model License/Approval** | Proof that model use is permitted (open source, licensed, API terms accepted) | ⏳ WAITING |
| **Evaluation Corpus** | Consented examples for testing real model quality (separate from enrollment/calibration) | ⏳ WAITING |
| **Compute Environment** | Where will testing run? (Local machine, cloud VM, container, GPU cluster?) | ⏳ WAITING |
| **Cost Budget** | If cloud/paid services, what's the test budget? | ⏳ WAITING |
| **Runtime Authorization** | Admin approval to use selected model in production (R-LIC-001) | ⏳ WAITING |

---

## Milestone 022 Execution Flow

### Phase 1: Model Selection Confirmation (Week 1)

**Input from avinash2196:**
```
Selected Model: [Model Name]
Provider: [Open source / Commercial / API]
Version: [Exact version number]
License: [License type, URL to license terms]
Language Support: [Languages supported]

Hindi Support: [Yes/No, any caveats?]
English Support: [Yes/No, any caveats?]

Installation Method: [pip, conda, git clone, API credentials, etc.]
Compute Requirements: [CPU only, GPU recommended, GPU required, RAM estimate, etc.]
```

**Verification Steps:**
1. ✅ License terms reviewed and accepted
2. ✅ Language support verified for Hindi + English
3. ✅ Version is stable/released (not alpha/beta unless explicitly approved)
4. ✅ Model can generate deterministic output (repeatability for testing)
5. ✅ Commercial use restrictions documented (if any)

**Output:** Model selection approved & recorded in git

### Phase 2: Test Assets & Corpus (Week 1-2)

**Input from avinash2196:**
```
Evaluation Corpus Location: [path/to/corpus/]
Sample Count: [n Hindi, n English samples]
Sample Format: [text scripts for synthesis]
Quality Range: [short/long, varied content, etc.]
Consent Status: [All samples consented for testing?]

Test Assertions:
  - Acceptable audio duration range
  - Required output formats (WAV, MP3, etc.)
  - Quality baseline (SNR, clipping, artifacts)
  - Language fidelity (pronunciation, accent)
```

**Verification Steps:**
1. ✅ Evaluation corpus exists & is accessible
2. ✅ All samples have explicit consent for testing
3. ✅ Corpus separate from enrollment training/calibration data
4. ✅ Sample count sufficient (≥5 per language minimum)
5. ✅ Test assertions defined and measurable

**Output:** Corpus location & test assertions documented

### Phase 3: Compute Environment Verification (Week 2)

**Input from avinash2196:**
```
Test Environment:
  - Platform: [Windows, Linux, macOS, Cloud (AWS/Azure/GCP), Container]
  - Python Version: [3.8, 3.9, 3.10, 3.11, 3.12]
  - Available RAM: [GB]
  - GPU Available: [Yes/No - CUDA version, Memory]
  - Internet Requirement: [Local model, API endpoint, hybrid]
  - Installed Dependencies: [List any pre-installed libs]

If Cloud/Paid:
  - Service: [Azure TTS, ElevenLabs, etc.]
  - Account: [Type - personal, business, trial]
  - Budget Limit: [$100/month, $500/month, unlimited trial, etc.]
  - Cost Per Request: [Estimated cost]
```

**Verification Steps:**
1. ✅ Python environment matches project requirements
2. ✅ Model installation succeeds on target platform
3. ✅ Test can generate at least 1 sample (smoke test)
4. ✅ Output is valid audio (correct format, not corrupted)
5. ✅ Cost tracking set up (if applicable)

**Output:** Environment setup verified & commands recorded

### Phase 4: Exact Repeatable Commands (Week 2-3)

**Create setup script:** `setup_m022_model_environment.sh` (or `.ps1` for Windows)

```bash
#!/bin/bash
# Milestone 022: Model Test Prerequisites Setup

# Step 1: Install model
echo "Installing [Model Name] version [X.Y.Z]..."
pip install [model-package]==[version]

# Verify installation
python -c "
import [model_module]
print('[Model Name] version:', [model_module].__version__)
assert [model_module].__version__ == '[X.Y.Z]', 'Version mismatch'
"

# Step 2: Download/configure test assets
echo "Downloading evaluation corpus..."
wget -O corpus.zip https://[location]/corpus/v1.zip
unzip corpus.zip -d ./test_corpus/

# Step 3: Verify model can generate output
echo "Testing model generation..."
python tests/test_model_prerequisites.py

# Step 4: Record environment hash
echo "Recording environment state..."
pip freeze > requirements-m022.txt
git add requirements-m022.txt
git commit -m "M022: Model environment setup - [Model Name] version [X.Y.Z]"

# Step 5: Cost accounting (if applicable)
if [ -f "credentials.env" ]; then
    echo "Cloud credentials loaded from credentials.env"
    echo "Estimated cost per 100k requests: $[X]"
fi

echo "✅ M022 prerequisites setup complete"
```

**Commands must be:**
- ✅ Deterministic (same result every run)
- ✅ Reproducible (work on different machines)
- ✅ Documented (with explanations)
- ✅ Version-pinned (exact package versions)
- ✅ Testable (include verification steps)

**Output:** setup_m022_model_environment.sh + requirements-m022.txt committed

### Phase 5: Smoke Test Execution (Week 3)

**Create:** `tests/test_model_prerequisites.py`

```python
"""
Milestone 022: Model Test Prerequisites Verification

Validates that:
1. Model can be imported
2. Model generates audio
3. Output is valid format
4. Generation is reproducible
5. No errors on simple input
"""

import pytest
from voice_narration.inference.production import ProductionInferenceProvider


@pytest.fixture
def model_config():
    """Model configuration from M022 setup."""
    return {
        "model_name": "[Model Name]",
        "version": "[X.Y.Z]",
        "supported_languages": ["hi", "en"],
        "output_format": "wav",
    }


class TestModelImport:
    """Model can be imported and initialized."""
    
    def test_model_import(self, model_config):
        """Verify model package is installed."""
        try:
            provider = ProductionInferenceProvider(model_config)
            assert provider is not None
        except ImportError as e:
            pytest.fail(f"Model import failed: {e}")


class TestModelGeneration:
    """Model can generate audio output."""
    
    @pytest.mark.asyncio
    async def test_generate_hindi(self, model_config):
        """Test Hindi audio generation."""
        provider = ProductionInferenceProvider(model_config)
        
        output = await provider.generate(
            script="नमस्ते, यह एक परीक्षण है।",  # "Hello, this is a test"
            voice_id="test-voice",
            language="hi"
        )
        
        assert output["output_seconds"] > 0
        assert len(output["audio_bytes"]) > 0
        assert output["format"] == "wav"
    
    @pytest.mark.asyncio
    async def test_generate_english(self, model_config):
        """Test English audio generation."""
        provider = ProductionInferenceProvider(model_config)
        
        output = await provider.generate(
            script="Hello, this is a test.",
            voice_id="test-voice",
            language="en"
        )
        
        assert output["output_seconds"] > 0
        assert len(output["audio_bytes"]) > 0
        assert output["format"] == "wav"


class TestReproducibility:
    """Model output is reproducible (same input → same output)."""
    
    @pytest.mark.asyncio
    async def test_reproducible_generation(self, model_config):
        """Same script generates identical output twice."""
        provider = ProductionInferenceProvider(model_config)
        
        script = "Reproducibility test"
        
        output1 = await provider.generate(script, "voice-1", language="en")
        output2 = await provider.generate(script, "voice-1", language="en")
        
        # For deterministic models, outputs should be identical
        # For stochastic models, at least duration should be similar
        assert abs(output1["output_seconds"] - output2["output_seconds"]) < 0.1
```

**Running smoke test:**
```bash
pytest tests/test_model_prerequisites.py -v
# Expected: 4 tests PASSED
```

**Output:** tests/test_model_prerequisites.py + results recorded

### Phase 6: Documentation & Approval (Week 3)

**Create:** `MILESTONE_022_PREREQUISITES_RECORD.md`

```markdown
# Milestone 022 Prerequisites Record

## Model Selection
- **Model Name:** [Model Name]
- **Version:** [X.Y.Z]
- **License:** [License type, URL]
- **Approval Date:** [YYYY-MM-DD]
- **Approved By:** avinash2196

## Test Environment
- **Platform:** [Windows/Linux/macOS/Cloud]
- **Python Version:** [3.X]
- **Installation Method:** [pip/conda/git/API]
- **Status:** ✅ Verified working

## Test Assets
- **Evaluation Corpus:** [path/location]
- **Sample Count:** [n Hindi, n English]
- **Consent Status:** ✅ All samples authorized
- **Test Assertions:** [List of measurable criteria]

## Compute Environment
- **Local/Cloud:** [local/AWS/Azure/GCP]
- **GPU Available:** [Yes/No]
- **Estimated Cost:** [$X per test run or "free/open-source"]
- **Smoke Test Result:** ✅ 4/4 tests PASSED

## Setup Commands
```bash
bash setup_m022_model_environment.sh
```

## Verification Status
- [x] Model installed and importable
- [x] Smoke test passes (Hindi + English generation)
- [x] Reproducibility verified
- [x] Environment documented
- [x] Costs accounted for (if applicable)
- [x] avinash2196 approval obtained

## Next Steps
Ready for M023 (Real-Model Inference Integration RED)
```

**Output:** MILESTONE_022_PREREQUISITES_RECORD.md committed

---

## Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | Model selection recorded | Model name, version, license in git |
| 2 | License terms approved | Admin approval documented |
| 3 | Hindi support verified | Model generates Hindi audio ✅ |
| 4 | English support verified | Model generates English audio ✅ |
| 5 | Evaluation corpus exists | Samples accessible & consented |
| 6 | Test environment documented | Platform, Python version, dependencies listed |
| 7 | Setup script repeatable | Same commands work on different machines |
| 8 | Smoke test passes (Hindi) | test_generate_hindi PASSED |
| 9 | Smoke test passes (English) | test_generate_english PASSED |
| 10 | Reproducibility verified | Same input → consistent output |
| 11 | Output format valid | Generated audio is valid WAV/MP3 |
| 12 | Costs documented (if paid) | Budget, per-request cost recorded |
| 13 | All commands in git | setup_m022_model_environment.sh committed |
| 14 | requirements pinned | requirements-m022.txt with exact versions |
| 15 | Prerequisites record complete | MILESTONE_022_PREREQUISITES_RECORD.md |

---

## Success Criteria

✅ **M022 is SUCCESSFUL when:**

1. **Model selection confirmed & approved:**
   - Model name, version, license all recorded
   - avinash2196 approval for production use obtained
   - License restrictions documented

2. **Test environment fully verified:**
   - Model installation succeeds
   - Smoke test passes (Hindi + English generation)
   - Reproducibility confirmed
   - Output format valid

3. **Repeatable setup documented:**
   - setup_m022_model_environment.sh works end-to-end
   - requirements-m022.txt with exact versions
   - All setup steps in git

4. **Prerequisites record complete:**
   - MILESTONE_022_PREREQUISITES_RECORD.md
   - All acceptance criteria marked ✅
   - Environment ready for M023 RED

**Ready to proceed to M023 (Real-Model Inference Integration RED):**
- ✅ Model selected & approved
- ✅ Test environment verified
- ✅ Setup repeatable
- ✅ Test framework ready

---

## Inputs Required from User (avinash2196)

### Blocking Inputs (Must Provide Before Starting)

1. **Model Selection:**
   ```
   Model Name: [Pyttsx3, gTTS, Azure TTS, ElevenLabs, etc.]
   Version: [Exact version number]
   License: [URL or description]
   ```

2. **Runtime Approval (R-LIC-001):**
   ```
   Approved for production use: [Yes/No]
   Approval Date: [YYYY-MM-DD]
   Approval Reason: [Why is this model acceptable?]
   ```

3. **Evaluation Corpus:**
   ```
   Location: [path/to/corpus]
   Hindi Samples: [count]
   English Samples: [count]
   Sample Format: [Plain text scripts]
   Consent Status: [All consented for testing?]
   ```

4. **Compute Environment:**
   ```
   Test Platform: [Windows/Linux/macOS/Cloud]
   GPU Available: [Yes/No, if yes: CUDA version]
   Budget (if cloud): [$X/month or "free"]
   ```

### Optional Inputs

- Test assertions (specific quality targets)
- Reviewer notes on model selection rationale
- Known limitations or caveats

---

## Known Constraints

### Model Selection Constraints
- ✅ Must support Hindi (primary requirement)
- ✅ Must support English (secondary requirement)
- ✅ Must allow testing without real-time API dependency (for reliability)
- ✅ Must be licensable for commercial use (implied by R-LIC-001)
- ✅ Must produce deterministic output (for repeatable tests)

### Test Environment Constraints
- ⚠️ No always-on GPU required (local testing must be possible)
- ⚠️ No expensive provisioning implicit (costs must be approved explicitly)
- ⚠️ Must be reproducible (exact version pins required)
- ⚠️ Must support both local and cloud paths (flexibility)

---

## Non-Code Changes Policy

**M022 produces NO production code changes:**
- ❌ No new production modules created
- ❌ No changes to voice_narration/ core
- ❌ No changes to tests/ (except test_model_prerequisites.py)
- ❌ No configuration changes (must be explicit user inputs)

**Only deliverables are:**
- ✅ Setup scripts (reproducible, not production code)
- ✅ Requirements files (version pins)
- ✅ Documentation (implementation plan, prerequisites record)
- ✅ Test prerequisites (setup verification only)

---

## Timeline

- **Phase 1 (Week 1):** Model selection + license approval
- **Phase 2 (Week 1-2):** Test assets & corpus verification
- **Phase 3 (Week 2):** Compute environment setup & verification
- **Phase 4 (Week 2-3):** Exact repeatable commands documented
- **Phase 5 (Week 3):** Smoke test execution (4/4 PASSED)
- **Phase 6 (Week 3):** Prerequisites record complete + approval

**Total Duration:** 3 weeks (could be faster if inputs provided quickly)

---

## Known Waiting States

| Item | Provided By | Status |
|------|-------------|--------|
| Model Selection | avinash2196 | ⏳ WAITING |
| License/Approval | avinash2196 | ⏳ WAITING |
| Evaluation Corpus | avinash2196 | ⏳ WAITING |
| Compute Environment | avinash2196 | ⏳ WAITING |
| Smoke Test Framework | AI | ✅ READY |
| Setup Script Template | AI | ✅ READY |

---

## Handoff to M023

When M022 is ✅ COMPLETE:
- Model is selected & approved (R-LIC-001 satisfied)
- Environment is verified & repeatable
- Test framework ready (smoke test passing)
- avinash2196 approval recorded

**Then M023 (Real-Model Inference Integration RED) can start:**
- Create production InferenceProvider for selected model
- Run M023 RED tests using real model
- Verify pause/pace controls and chunk handling

---

## Next Steps

1. **avinash2196 provides model selection input:**
   - Model name, version, license
   - Runtime approval (R-LIC-001)
   - Evaluation corpus location
   - Compute environment details

2. **M022 execution (3 weeks):**
   - Phases 1-6 executed sequentially
   - Smoke test passes
   - Prerequisites record completed

3. **avinash2196 approves:**
   - Reviews MILESTONE_022_PREREQUISITES_RECORD.md
   - Confirms all criteria met
   - Approves: "Model prerequisites verified"

4. **Proceed to M023:**
   - Real-Model Inference Integration RED
   - Production InferenceProvider creation
   - Pause/pace + chunk handling tests

