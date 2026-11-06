# Implementation Plan: M1 FOUNDATION — Database & Storage Infrastructure

**Milestone:** M1  
**Type:** FOUNDATION  
**Status:** READY FOR EXECUTION  
**Created:** 2026-11-05

---

## Objective

Establish all prerequisite infrastructure for persistence layers (database, storage directories, migrations, dependencies) so that M2-M5 RED/GREEN milestones can implement and test persistence behavior.

**Success:** PostgreSQL running, schema created, migrations working, storage ready, all dependencies installed.

---

## Tasks

### T1: Install PostgreSQL 14+ on Windows

**Objective:** Get a working PostgreSQL server running locally.

**Steps:**

1. **Download PostgreSQL installer**
   ```powershell
   # Option A: Download from https://www.postgresql.org/download/windows/
   # Choose PostgreSQL 14 or 15 (latest stable)
   
   # Or Option B: Use chocolatey if installed
   choco install postgresql -y --params '/Password:postgres123'
   ```

2. **Run installer (if manual download)**
   - Accept default installation path: `C:\Program Files\PostgreSQL\14`
   - Accept default port: 5432
   - Set superuser password: `postgres123` (or your choice)
   - Keep default options

3. **Verify installation**
   ```powershell
   # Should show PostgreSQL version
   psql --version
   
   # Should connect successfully
   psql -U postgres -h localhost -d postgres -c "SELECT 1"
   # Password: postgres123
   ```

**Expected Output:**
```
PostgreSQL is installed, version 14.x
Server running on port 5432
psql connection successful
```

**Rollback:** `choco uninstall postgresql -y` or use Windows "Add/Remove Programs"

---

### T2: Create Database & User

**Objective:** Set up a dedicated database and user for the application.

**Steps:**

1. **Connect to PostgreSQL as superuser**
   ```powershell
   psql -U postgres -h localhost
   ```

2. **Create database and user** (in psql prompt)
   ```sql
   -- Create user
   CREATE USER voice_narration WITH PASSWORD 'voice123';
   
   -- Create database
   CREATE DATABASE voice_narration OWNER voice_narration;
   
   -- Grant privileges
   GRANT CONNECT ON DATABASE voice_narration TO voice_narration;
   GRANT CREATE ON DATABASE voice_narration TO voice_narration;
   
   -- Exit
   \q
   ```

3. **Verify connection with new user**
   ```powershell
   psql -U voice_narration -h localhost -d voice_narration -c "SELECT 1"
   # Password: voice123
   ```

**Expected Output:**
```
Database voice_narration created
User voice_narration created
Connection with new user successful
```

**Rollback:**
```sql
DROP DATABASE voice_narration;
DROP USER voice_narration;
```

---

### T3: Add Dependencies to `requirements.txt`

**Objective:** Add Python packages needed for persistence.

**Steps:**

1. **Edit `requirements.txt`** (or `pyproject.toml` if using Poetry)
   
   Add these lines:
   ```
   SQLAlchemy==2.0.23
   psycopg2-binary==2.9.9
   alembic==1.13.1
   python-dotenv==1.0.0
   ```

2. **Install packages**
   ```powershell
   cd C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```powershell
   python -c "import sqlalchemy; import psycopg2; import alembic; print('✓ All packages installed')"
   ```

**Expected Output:**
```
✓ All packages installed
```

**Rollback:** `pip uninstall SQLAlchemy psycopg2-binary alembic python-dotenv -y`

---

### T4: Create `.env.production` Configuration File

**Objective:** Store database credentials and paths (not committed to git).

**Steps:**

1. **Create `.env.production` in project root**
   
   Path: `C:\Users\avina\Downloads\avinash-repo\v11\Voice-Narration\.env.production`

2. **Content:**
   ```
   # PostgreSQL Configuration
   DATABASE_URL=postgresql://voice_narration:voice123@localhost:5432/voice_narration
   
   # Storage Configuration
   AUDIO_STORAGE_PATH=./audio_storage
   AUDIO_RETENTION_DAYS=30
   
   # TTS Service Configuration
   INFERENCE_PROVIDER=google
   GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
   
   # Voice Service Configuration
   VOICE_SERVICE_URL=http://localhost:8002
   ```

3. **Verify file created**
   ```powershell
   Get-Content .\.env.production
   ```

**Expected Output:**
```
DATABASE_URL and other env vars visible
```

**Rollback:** `Remove-Item .\.env.production`

---

### T5: Create Storage Directory Structure

**Objective:** Set up disk directories for audio file storage.

**Steps:**

1. **Create directory structure**
   ```powershell
   mkdir audio_storage
   mkdir audio_storage\generations
   mkdir audio_storage\temp
   mkdir audio_storage\archive
   
   # Verify
   Get-ChildItem audio_storage -Recurse
   ```

2. **Set permissions (optional, Windows ACL)**
   ```powershell
   # Allow current user full control
   icacls audio_storage /grant:r "$env:USERNAME`:F" /t /q
   ```

**Expected Output:**
```
audio_storage/
├── generations/
├── temp/
└── archive/
```

**Rollback:** `Remove-Item audio_storage -Recurse`

---

### T6: Initialize Alembic for Migrations

**Objective:** Set up migration tracking so schema changes are version-controlled.

**Steps:**

1. **Initialize Alembic in project**
   ```powershell
   cd voice_narration\inference
   alembic init alembic
   cd ..\..
   ```

2. **Configure `alembic.ini`** (set database URL)
   
   Edit `voice_narration\inference\alembic\alembic.ini`:
   
   Find line:
   ```ini
   sqlalchemy.url = driver://user:password@localhost/dbname
   ```
   
   Replace with:
   ```ini
   sqlalchemy.url = postgresql://voice_narration:voice123@localhost:5432/voice_narration
   ```

3. **Verify Alembic works**
   ```powershell
   cd voice_narration\inference
   alembic current
   # Should show: "No migrations have been applied yet"
   cd ..\..
   ```

**Expected Output:**
```
Alembic initialized
Configuration set
alembic current returns no migrations
```

**Rollback:** `Remove-Item voice_narration\inference\alembic -Recurse`

---

### T7: Create Initial Database Schema (SQLAlchemy Models)

**Objective:** Define database tables for generations and voices.

**Steps:**

1. **Create `voice_narration/inference/models.py`**

   ```python
   from sqlalchemy import Column, String, Float, DateTime, Integer, Text, Boolean, ForeignKey
   from sqlalchemy.ext.declarative import declarative_base
   from datetime import datetime, timedelta
   import uuid
   
   Base = declarative_base()
   
   class Voice(Base):
       __tablename__ = 'voices'
       
       id = Column(String(50), primary_key=True)  # e.g., "en-US-Neural2-A"
       name = Column(String(255), nullable=False)
       language = Column(String(20), nullable=False)  # e.g., "en-US"
       gender = Column(String(20), nullable=False)  # Male, Female, Neutral
       is_active = Column(Boolean, default=True)
       created_at = Column(DateTime, default=datetime.utcnow)
       
   
   class Generation(Base):
       __tablename__ = 'generations'
       
       id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
       job_id = Column(String(100), nullable=False, unique=True, index=True)
       text = Column(Text, nullable=False)
       voice_id = Column(String(50), ForeignKey('voices.id'), nullable=False)
       duration_seconds = Column(Float, nullable=True)  # Calculated from audio
       file_path = Column(String(500), nullable=False)  # Relative path in audio_storage/
       status = Column(String(20), default='completed')  # completed, failed, deleted
       created_at = Column(DateTime, default=datetime.utcnow, index=True)
       expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30), index=True)
       error_message = Column(Text, nullable=True)  # If status=failed
       
       def __repr__(self):
           return f"<Generation {self.id[:8]}... voice={self.voice_id} text_len={len(self.text)}>"
   
   
   class GenerationAudit(Base):
       __tablename__ = 'generation_audit'
       
       id = Column(Integer, primary_key=True, autoincrement=True)
       generation_id = Column(String(36), ForeignKey('generations.id'))
       action = Column(String(50))  # created, downloaded, deleted, expired
       timestamp = Column(DateTime, default=datetime.utcnow)
   ```

2. **Create database session factory** (`voice_narration/inference/db.py`)

   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   import os
   from dotenv import load_dotenv
   
   # Load environment
   env_file = '.env.production'
   if os.path.exists(env_file):
       load_dotenv(env_file)
   
   DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://voice_narration:voice123@localhost:5432/voice_narration')
   
   engine = create_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   
   def get_db():
       """Dependency for FastAPI"""
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   
   def create_all_tables():
       """Create all tables from models"""
       from models import Base
       Base.metadata.create_all(bind=engine)
   ```

3. **Test models**
   ```powershell
   python -c "from voice_narration.inference.models import Base, Generation; print('✓ Models loaded')"
   ```

**Expected Output:**
```
✓ Models loaded
No errors importing SQLAlchemy models
```

**Rollback:** `Remove-Item voice_narration\inference\models.py, voice_narration\inference\db.py`

---

### T8: Create Initial Alembic Migration

**Objective:** Generate migration file that creates all tables.

**Steps:**

1. **Update `alembic/env.py`** to import models
   
   Edit `voice_narration/inference/alembic/env.py`:
   
   Find:
   ```python
   target_metadata = None
   ```
   
   Replace with:
   ```python
   from voice_narration.inference.models import Base
   target_metadata = Base.metadata
   ```

2. **Generate migration**
   ```powershell
   cd voice_narration\inference
   alembic revision --autogenerate -m "Initial schema: voices and generations tables"
   cd ..\..
   ```

3. **Review generated file**
   ```powershell
   Get-ChildItem voice_narration\inference\alembic\versions
   # Should show: 0001_Initial_schema...py
   ```

4. **Apply migration**
   ```powershell
   cd voice_narration\inference
   alembic upgrade head
   cd ..\..
   ```

5. **Verify tables created**
   ```powershell
   psql -U voice_narration -d voice_narration -c "\dt"
   # Should show: generations, voices, generation_audit, alembic_version
   ```

**Expected Output:**
```
Migration file created: 0001_Initial_schema_...py
alembic upgrade head successful
Tables created in PostgreSQL:
- generations
- voices
- generation_audit
- alembic_version
```

**Rollback:**
```powershell
cd voice_narration\inference
alembic downgrade base
cd ..\..
# Remove migration file manually
```

---

### T9: Seed Default Voices

**Objective:** Pre-populate database with 5 Google voices.

**Steps:**

1. **Create seed script** (`voice_narration/inference/seed_voices.py`)

   ```python
   from db import SessionLocal, create_all_tables
   from models import Voice
   
   DEFAULT_VOICES = [
       Voice(
           id='en-US-Neural2-A',
           name='English US Female (A)',
           language='en-US',
           gender='Female'
       ),
       Voice(
           id='en-US-Neural2-C',
           name='English US Female (C)',
           language='en-US',
           gender='Female'
       ),
       Voice(
           id='en-US-Neural2-E',
           name='English US Male (E)',
           language='en-US',
           gender='Male'
       ),
       Voice(
           id='hi-IN-Neural2-A',
           name='Hindi India Female (A)',
           language='hi-IN',
           gender='Female'
       ),
       Voice(
           id='hi-IN-Neural2-B',
           name='Hindi India Male (B)',
           language='hi-IN',
           gender='Male'
       ),
   ]
   
   def seed_voices():
       create_all_tables()
       db = SessionLocal()
       try:
           for voice in DEFAULT_VOICES:
               existing = db.query(Voice).filter_by(id=voice.id).first()
               if not existing:
                   db.add(voice)
                   print(f"Added voice: {voice.id}")
           db.commit()
           print("✓ All voices seeded")
       except Exception as e:
           print(f"✗ Error seeding voices: {e}")
           db.rollback()
       finally:
           db.close()
   
   if __name__ == '__main__':
       seed_voices()
   ```

2. **Run seed script**
   ```powershell
   python voice_narration/inference/seed_voices.py
   ```

3. **Verify voices in database**
   ```powershell
   psql -U voice_narration -d voice_narration -c "SELECT id, name, language FROM voices;"
   # Should show 5 voices
   ```

**Expected Output:**
```
Added voice: en-US-Neural2-A
Added voice: en-US-Neural2-C
Added voice: en-US-Neural2-E
Added voice: hi-IN-Neural2-A
Added voice: hi-IN-Neural2-B
✓ All voices seeded
```

**Rollback:**
```powershell
psql -U voice_narration -d voice_narration -c "DELETE FROM voices;"
```

---

### T10: Test Database Connection from Application

**Objective:** Verify that the TTS service can connect to PostgreSQL.

**Steps:**

1. **Create test script** (`test_db_connection.py`)

   ```python
   import os
   import sys
   from dotenv import load_dotenv
   
   # Load env
   load_dotenv('.env.production')
   
   # Test connection
   from voice_narration.inference.db import SessionLocal, engine
   from voice_narration.inference.models import Voice, Generation
   
   try:
       # Test engine connection
       with engine.connect() as conn:
           result = conn.execute("SELECT 1")
           print("✓ PostgreSQL connection successful")
       
       # Test SessionLocal
       db = SessionLocal()
       voices = db.query(Voice).all()
       print(f"✓ Query successful: found {len(voices)} voices")
       
       # Test model
       gens = db.query(Generation).all()
       print(f"✓ Generations table accessible: {len(gens)} rows")
       
       db.close()
       print("✓ All database tests passed")
       
   except Exception as e:
       print(f"✗ Database error: {e}")
       sys.exit(1)
   ```

2. **Run test**
   ```powershell
   python test_db_connection.py
   ```

**Expected Output:**
```
✓ PostgreSQL connection successful
✓ Query successful: found 5 voices
✓ Generations table accessible: 0 rows
✓ All database tests passed
```

**Rollback:** N/A (read-only test)

---

### T11: Update Environment Configuration for Services

**Objective:** Configure services to use `.env.production` on startup.

**Steps:**

1. **Update `start-inference-service.bat`**
   
   Edit file (or create if needed):
   ```batch
   @echo off
   setlocal enabledelayedexpansion
   
   REM Set database configuration
   set DATABASE_URL=postgresql://voice_narration:voice123@localhost:5432/voice_narration
   
   REM Set TTS provider
   set INFERENCE_PROVIDER=google
   set GOOGLE_APPLICATION_CREDENTIALS=.\service-account-key.json
   
   REM Set audio storage
   set AUDIO_STORAGE_PATH=.\audio_storage
   set AUDIO_RETENTION_DAYS=30
   
   REM Load .env.production if it exists
   if exist .env.production (
       for /f "tokens=* delims== eol=# " %%a in (.env.production) do (
           if not "%%a"=="" set %%a
       )
   )
   
   echo Starting TTS Service (port 8003)...
   echo DATABASE_URL: %DATABASE_URL%
   echo INFERENCE_PROVIDER: %INFERENCE_PROVIDER%
   
   python -m voice_narration.inference
   pause
   ```

2. **Verify batch file**
   ```powershell
   Get-Content .\start-inference-service.bat
   ```

**Expected Output:**
```
Batch file shows database configuration
Environment variables set before Python starts
```

**Rollback:** `Remove-Item .\start-inference-service.bat`

---

### T12: Documentation & Verification Checklist

**Objective:** Document what was done and verify everything works.

**Steps:**

1. **Create `FOUNDATION_CHECKLIST.md`**

   ```markdown
   # M1 FOUNDATION — Verification Checklist
   
   - [ ] PostgreSQL installed (version 14+)
   - [ ] Database `voice_narration` created
   - [ ] User `voice_narration` created with password `voice123`
   - [ ] psql connection test passed
   - [ ] Dependencies installed: SQLAlchemy, psycopg2, alembic, python-dotenv
   - [ ] `.env.production` file created with correct settings
   - [ ] Storage directories created: audio_storage/generations, audio_storage/temp, audio_storage/archive
   - [ ] Alembic initialized
   - [ ] Initial migration created and applied
   - [ ] Tables visible in PostgreSQL (generations, voices, generation_audit)
   - [ ] Seed script ran successfully
   - [ ] 5 voices seeded in database
   - [ ] Database connection test passed
   - [ ] `start-inference-service.bat` updated with DATABASE_URL
   
   ## Final Verification Command
   
   ```powershell
   psql -U voice_narration -d voice_narration -c "SELECT COUNT(*) FROM voices; SELECT COUNT(*) FROM generations;"
   ```
   
   Expected output: `5 voices, 0 generations`
   
   ## Performance Baseline
   
   - Connection time: < 100ms
   - Query time (5 voices): < 50ms
   - Write time (new generation): < 200ms
   ```

2. **Run final verification**
   ```powershell
   # Test PostgreSQL connection
   psql -U voice_narration -d voice_narration -c "SELECT COUNT(*) as voices FROM voices; SELECT COUNT(*) as generations FROM generations;"
   
   # Test Python import
   python -c "from voice_narration.inference.db import SessionLocal; from voice_narration.inference.models import Voice, Generation; print('✓ Ready for M2 tests')"
   ```

**Expected Output:**
```
psql output:
 voices | count
--------+-------
      5 |     0

Python output:
✓ Ready for M2 tests
```

---

## Verification Commands (Quick Reference)

Run these to verify M1 is complete:

```powershell
# 1. PostgreSQL running
psql -U postgres -c "SELECT 1"

# 2. Database exists
psql -U voice_narration -d voice_narration -c "SELECT current_database()"

# 3. Tables created
psql -U voice_narration -d voice_narration -c "\dt"

# 4. Voices seeded
psql -U voice_narration -d voice_narration -c "SELECT COUNT(*) FROM voices"
# Expected: 5

# 5. Dependencies installed
python -c "import sqlalchemy; import psycopg2; import alembic; print('OK')"

# 6. Storage directories exist
Test-Path .\audio_storage\generations, .\audio_storage\temp, .\audio_storage\archive

# 7. .env.production exists
Test-Path .\.env.production
```

---

## Success Criteria

✅ **M1 FOUNDATION complete when ALL of these are true:**

1. PostgreSQL server running on localhost:5432
2. Database `voice_narration` exists and is accessible
3. User `voice_narration` exists with correct password
4. Three tables created: `voices`, `generations`, `generation_audit`
5. Five Google voices seeded in `voices` table
6. Alembic migrations initialized and working
7. All required Python packages installed
8. `.env.production` configured with database URL
9. Storage directories created: `audio_storage/{generations,temp,archive}`
10. Database connection test passes
11. SQLAlchemy models load without errors
12. TTS service can connect to database on startup

**Evidence:** All 12 verification commands above pass without errors.

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| PostgreSQL won't install | Low | High | Use chocolatey or manual installer, check Windows Defender |
| Connection refused on 5432 | Medium | High | Verify PostgreSQL service running: `Get-Service PostgreSQL*` |
| Wrong password | Low | High | Re-create user with known password, update `.env.production` |
| Alembic migration fails | Low | High | Verify SQLAlchemy and models correct, check alembic.ini DATABASE_URL |
| Disk space insufficient | Low | Medium | Allocate 10+ GB for audio storage |
| Permissions denied on directory | Medium | Medium | Run PowerShell as Administrator, check icacls |

---

## Rollback Procedure

If M1 fails and needs to be rolled back:

```powershell
# 1. Delete storage directories
Remove-Item .\audio_storage -Recurse -Force

# 2. Drop database and user
psql -U postgres -c "DROP DATABASE voice_narration; DROP USER voice_narration;"

# 3. Uninstall Python packages
pip uninstall SQLAlchemy psycopg2-binary alembic python-dotenv -y

# 4. Remove migrations
Remove-Item .\voice_narration\inference\alembic -Recurse -Force

# 5. Remove model files
Remove-Item .\voice_narration\inference\models.py, .\voice_narration\inference\db.py, .\test_db_connection.py

# 6. Remove .env file
Remove-Item .\.env.production

# System is now back to pre-M1 state
```

---

## Next Steps After M1

Once M1 is complete and verified:

1. **Run M2 RED tests** (persistence tests)
   - Tests will verify that `Generation` model can be created and persisted
   - Tests will verify that audio files can be saved to disk
   
2. **Setup monitoring** (optional)
   - Consider: database backups, disk space alerts
   - Consider: PostgreSQL query logging for debugging

3. **Approval for M3 GREEN** (implementation)
   - Approval gate: M2 tests all fail with valid RED evidence
   - Proceed: Implement storage layer (M3)

---

## Time Estimate

- T1-T2 (PostgreSQL setup): 10-15 minutes
- T3-T4 (Dependencies & config): 5 minutes
- T5 (Storage directories): 2 minutes
- T6-T8 (Alembic & migrations): 10-15 minutes
- T9-T10 (Models & seeding): 10 minutes
- T11-T12 (Verification): 10 minutes

**Total: 45-60 minutes**

---

## Execution Log

| Time | Task | Status | Notes |
|------|------|--------|-------|
| — | T1: Install PostgreSQL | Pending | — |
| — | T2: Create DB & user | Pending | — |
| — | T3: Add dependencies | Pending | — |
| — | T4: Create `.env.production` | Pending | — |
| — | T5: Create storage dirs | Pending | — |
| — | T6: Initialize Alembic | Pending | — |
| — | T7: Create models | Pending | — |
| — | T8: Create migration | Pending | — |
| — | T9: Seed voices | Pending | — |
| — | T10: Test connection | Pending | — |
| — | T11: Update .bat files | Pending | — |
| — | T12: Verify all | Pending | — |

---

## Sign-Off

**Created:** 2026-11-05  
**Status:** READY TO EXECUTE  
**Approval:** Awaiting execution authorization

Once you confirm, I will execute M1 tasks step-by-step and update the Execution Log with results.

---

**Work Item:** audio-download-persistence  
**Milestone:** M1 FOUNDATION  
**Implementation Plan Version:** 1.0
