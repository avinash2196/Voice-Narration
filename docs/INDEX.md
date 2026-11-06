# 📚 Voice-Narration Documentation Index

Complete documentation organized by category.

---

## 🚀 **Quick Start**

**Start here if you're new:**

1. **`deployment/SERVICES_QUICK_REFERENCE.md`** - 2-minute overview of all 7 services
2. **`deployment/HOW_TO_RUN_ALL_SERVICES.md`** - Complete setup & running guide
3. **`deployment/M024_DEPLOYMENT_TESTING_GUIDE.md`** - Step-by-step deployment

---

## 📁 **Folder Structure**

### **`/deployment`** - Running & Deploying Services
Contains everything needed to start and run the Voice-Narration platform.

| File | Purpose |
|------|---------|
| `SERVICES_QUICK_REFERENCE.md` | Quick start (2 min) |
| `HOW_TO_RUN_ALL_SERVICES.md` | Complete setup guide |
| `M024_DEPLOYMENT_TESTING_GUIDE.md` | Google TTS setup & testing |

**What's inside:**
- Docker Compose commands
- Manual service startup (7 terminals)
- Port mappings (8001-8006, 5432)
- Environment variable setup
- Service verification tests
- Troubleshooting

---

### **`/milestones`** - Milestone Documentation
Tracks progress across all 24 completed milestones.

#### Milestone Summaries (Status & Implementation)
| File | Milestone | Status |
|------|-----------|--------|
| `EXECUTION_STATUS_SUMMARY.md` | Overview | ✅ |
| `M022_FINAL_STATUS.md` | M022: Multi-Provider TTS | ✅ |
| `M022_IMPLEMENTATION_SUMMARY.md` | M022 Implementation | ✅ |
| `M023_EXECUTION_SUMMARY.md` | M023: RED Tests | ✅ |
| `M024_EXECUTION_SUMMARY.md` | M024: GREEN Code | ✅ |

#### Detailed Milestone Evidence
| File | Milestone | Status |
|------|-----------|--------|
| `MILESTONE_012_EXECUTION_EVIDENCE.md` | M012 | ✅ |
| `MILESTONE_012_REVIEW.md` | M012 Review | ✅ |
| `MILESTONE_016_EXECUTION_EVIDENCE.md` | M016: Voices Service | ✅ |
| `MILESTONE_017_EXECUTION_EVIDENCE.md` | M017: Jobs Service | ✅ |
| `MILESTONE_018_EXECUTION_EVIDENCE.md` | M018: Consent Service | ✅ |
| `MILESTONE_019_EXECUTION_EVIDENCE.md` | M019 | ✅ |
| `MILESTONE_021_PLANNING.md` | M021: Calibration Plan | 🔴 |

#### M021 Calibration (Data Collection Phase)
| File | Purpose |
|------|---------|
| `M021_QUICK_START.md` | Quick overview |
| `M021_README.md` | Full details |
| `M021_ACTION_ITEMS.md` | Step-by-step checklist |
| `M021_COMPLETE_PACKAGE.md` | Complete reference |

---

### **`/planning`** - Project Planning & Requirements
High-level planning, requirements, and project status.

| File | Purpose |
|------|---------|
| `PROJECT_STATUS_DASHBOARD.md` | Current status across all areas |
| `voice_narration_PDD_requirements.md` | Complete requirements (PDD) |
| `M022_M023_REAL_MODEL_PLAN.md` | Real model implementation plan |

---

### **`/testing`** - Test Results & Quality Assurance
Test execution logs, results, and quality assurance documentation.

| File | Purpose |
|------|---------|
| `REVIEW_SUMMARY.md` | Code review summary |
| `SESSION_SUMMARY_M023.txt` | M023 test session summary |
| `step1_before.txt` | Step 1: Initial state |
| `step1_red_baseline.txt` | Step 1: RED baseline tests |
| `step2_red1.txt` | Step 2: RED test creation |
| `step2_red_run1.txt` | Step 2: RED test execution |
| `step3_quick_summary.txt` | Step 3: Progress summary |
| `step3_red2.txt` | Step 3: RED refinements |
| `step3_regression_baseline.txt` | Step 3: Regression baseline |
| `step4_after.txt` | Step 4: Final state |

---

### **`/guides`** - User Guides & References
User-facing documentation and quick reference guides.

| File | Purpose |
|------|---------|
| `README.md` | Project overview (copy from root) |

---

### **`/initial-build`** - M022/M023 Implementation Plans
Detailed implementation plans for multi-provider TTS infrastructure.

*Auto-generated implementation documentation*

---

### **`/architecture`** - Architecture & Design
System architecture, design decisions, and technical specifications.

*Technical architecture documentation*

---

### **`/contract`** - API Contracts
API request/response specifications and contracts.

*API contract definitions*

---

### **`/model-eval`** - Model Evaluation
Model evaluation, performance metrics, and quality assessments.

*Model evaluation documentation*

---

### **`.ai/`** - AI Planning (Hidden)
Planning documents used by AI agents for implementation.

*Generated implementation plans and specifications*

---

## 📊 **Navigation by Use Case**

### **"I want to run the services"**
→ Start with: **`deployment/SERVICES_QUICK_REFERENCE.md`**

### **"I want detailed setup instructions"**
→ Read: **`deployment/HOW_TO_RUN_ALL_SERVICES.md`**

### **"I want to use Google TTS"**
→ Follow: **`deployment/M024_DEPLOYMENT_TESTING_GUIDE.md`**

### **"I want to understand the architecture"**
→ Check: **`milestones/M024_EXECUTION_SUMMARY.md`** + **`architecture/`**

### **"I want to see test results"**
→ Review: **`testing/`** folder

### **"I want to understand requirements"**
→ Read: **`planning/voice_narration_PDD_requirements.md`**

### **"I want milestone status"**
→ See: **`milestones/EXECUTION_STATUS_SUMMARY.md`**

### **"I need to collect M021 calibration data"**
→ Follow: **`milestones/M021_QUICK_START.md`** or **`milestones/M021_ACTION_ITEMS.md`**

---

## 🎯 **Service Documentation**

Each service has documentation in the respective source folder:

- **Auth Service** (8001) → `voice_narration/auth/`
- **Voices Service** (8002) → `voice_narration/voices/`
- **Jobs Service** (8003) → `voice_narration/jobs/`
- **Consent Service** (8004) → `voice_narration/consent/`
- **Inference Service** (8005) → `voice_narration/inference/`
- **AI Evaluation** (8006) → `voice_narration/ai/`

---

## 📝 **File Types**

- **`.md`** - Markdown documentation
- **`.txt`** - Plain text logs and output
- **`.py`** - Python source code

---

## ✅ **Status Summary**

| Category | Files | Status |
|----------|-------|--------|
| Deployment | 3 | ✅ Ready |
| Milestones | 20+ | ✅ Complete (except M021) |
| Planning | 3 | ✅ Ready |
| Testing | 10 | ✅ Complete |
| Guides | 1 | ✅ Ready |
| **TOTAL** | **40+** | **✅ Organized** |

---

## 🚀 **Getting Started Checklist**

- [ ] Read `deployment/SERVICES_QUICK_REFERENCE.md` (2 min)
- [ ] Run `docker-compose -f compose.harness.yaml up -d`
- [ ] Verify all services running
- [ ] Run tests: `pytest tests/test_linguistic_chunking_and_controls.py -v`
- [ ] Read `deployment/M024_DEPLOYMENT_TESTING_GUIDE.md` for TTS setup
- [ ] Add Google TTS credentials to `.env`
- [ ] Generate real audio

---

## 📞 **Quick Links**

**For running services:** → `deployment/`  
**For understanding progress:** → `milestones/`  
**For requirements:** → `planning/`  
**For test results:** → `testing/`  
**For architecture:** → `architecture/`  

---

**Last Updated:** 2026-10-31  
**Total Milestones:** 24/24 Complete ✅  
**Services:** 7 Ready to Run ✅  
**Tests Passing:** 39/39 ✅
