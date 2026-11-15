# 001_Implementation_Plan_FOUNDATION.md

**Work Item:** frontend-voice-cloning-mvp  
**Milestone:** M0 - FOUNDATION  
**Phase:** IMPLEMENTATION PLANNING  
**Duration:** Weeks 1-2  
**Effort:** 40 hours  
**Created:** 2026-10-31  
**Status:** AWAITING USER APPROVAL

---

## Executive Summary

M0-FOUNDATION establishes the complete React project scaffolding, build tooling, CI/CD skeleton, and development environment. This phase produces a working dev server (`npm run dev`), test runner (`npm run test`), and Docker environment—but no feature implementation yet.

**Key Deliverable:** A production-ready project structure where M1-RED (auth tests) can begin immediately after M0 completion.

**Success Criteria:** Developer runs `npm run dev`, `npm run test`, and `npm run build` without errors; Docker image builds and runs.

---

## Project Structure

### Folder Layout

```
Voice-Narration/
├── src/
│   ├── components/
│   │   ├── common/              # Shared components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   └── ui/                  # UI primitives (TailwindCSS-based)
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       ├── Card.tsx
│   │       ├── Modal.tsx
│   │       ├── Spinner.tsx
│   │       └── Toast.tsx
│   ├── pages/
│   │   ├── Auth/
│   │   │   ├── Signup.tsx        # (M1-GREEN)
│   │   │   └── Login.tsx         # (M1-GREEN)
│   │   ├── Voice/
│   │   │   ├── Upload.tsx        # (M2-GREEN)
│   │   │   └── Manage.tsx        # (M2-GREEN)
│   │   ├── Generate/
│   │   │   ├── TTS.tsx           # (M3-GREEN)
│   │   │   └── History.tsx       # (M3-GREEN)
│   │   ├── Settings.tsx          # (M3-GREEN)
│   │   └── NotFound.tsx
│   ├── services/
│   │   ├── api/
│   │   │   ├── authClient.ts     # (M1-GREEN)
│   │   │   ├── voiceClient.ts    # (M2-GREEN)
│   │   │   ├── inferenceClient.ts # (M3-GREEN)
│   │   │   ├── jobsClient.ts     # (M3-GREEN)
│   │   │   ├── evaluationClient.ts # (M2-GREEN)
│   │   │   └── httpClient.ts     # Base HTTP client (M0)
│   │   └── storage/
│   │       └── localStorage.ts   # Local storage utilities (M0)
│   ├── context/
│   │   ├── AuthContext.tsx       # (M1-GREEN)
│   │   ├── VoiceContext.tsx      # (M2-GREEN)
│   │   └── GenerationContext.tsx # (M3-GREEN)
│   ├── hooks/
│   │   ├── useAuth.ts            # (M1-GREEN)
│   │   ├── useVoice.ts           # (M2-GREEN)
│   │   ├── useVoiceQuality.ts    # (M2-GREEN)
│   │   ├── useGenerationJob.ts   # (M3-GREEN)
│   │   ├── useRateLimit.ts       # (M3-GREEN)
│   │   └── useFetch.ts           # Generic fetch hook (M0)
│   ├── types/
│   │   ├── auth.ts               # Auth types (M1-GREEN)
│   │   ├── voice.ts              # Voice types (M2-GREEN)
│   │   ├── generation.ts         # TTS types (M3-GREEN)
│   │   ├── common.ts             # Shared types (M0)
│   │   └── api.ts                # API response types (M0)
│   ├── utils/
│   │   ├── validation.ts         # Form validation (M0)
│   │   ├── jwt.ts                # JWT decode (M1-GREEN)
│   │   ├── audio.ts              # Audio utilities (M2-GREEN)
│   │   ├── formatters.ts         # Date/time formatting (M0)
│   │   └── constants.ts          # App constants (M0)
│   ├── middleware/
│   │   ├── tokenInterceptor.ts   # (M1-GREEN)
│   │   └── errorHandler.ts       # (M0)
│   ├── App.tsx                   # Root app component (M0)
│   ├── main.tsx                  # Vite entry point (M0)
│   └── index.css                 # TailwindCSS imports (M0)
├── tests/
│   ├── auth.spec.tsx             # (M1-RED)
│   ├── voice.spec.tsx            # (M2-RED)
│   ├── tts.spec.tsx              # (M3-RED)
│   ├── mocks/
│   │   ├── auth-handlers.ts      # (M1-RED)
│   │   ├── voices-handlers.ts    # (M2-RED)
│   │   ├── jobs-handlers.ts      # (M3-RED)
│   │   ├── inference-handlers.ts # (M3-RED)
│   │   ├── ai-evaluation-handlers.ts # (M2-RED)
│   │   └── setup.ts              # MSW setup (M0)
│   ├── fixtures/
│   │   ├── users.ts              # (M1-RED)
│   │   ├── voices.ts             # (M2-RED)
│   │   └── generations.ts        # (M3-RED)
│   └── vitest.config.ts          # Vitest configuration (M0)
├── public/
│   ├── index.html                # (M0)
│   └── favicon.ico               # (M0)
├── .github/
│   └── workflows/
│       ├── lint.yml              # ESLint + Prettier CI (M0)
│       ├── test.yml              # Run tests on PR (M0)
│       └── build.yml             # Build verification (M0)
├── docker/
│   ├── Dockerfile                # Production Docker image (M0)
│   └── Dockerfile.dev            # Dev Docker image (M0)
├── .env.example                  # Environment template (M0)
├── .env.development              # Dev environment (M0)
├── .env.staging                  # Staging environment (M0)
├── .env.production               # Production environment (M0)
├── .eslintrc.json                # ESLint config (M0)
├── .prettierrc.json              # Prettier config (M0)
├── vite.config.ts                # Vite config (M0)
├── vitest.config.ts              # Vitest config (M0)
├── tsconfig.json                 # TypeScript config (M0)
├── tailwind.config.js            # TailwindCSS config (M0)
├── postcss.config.js             # PostCSS config (M0)
├── package.json                  # Dependencies (M0)
├── pnpm-lock.yaml                # Lockfile (M0)
├── Dockerfile                    # Docker (M0)
├── docker-compose.yml            # Docker Compose for local dev (M0)
├── README.md                     # Setup instructions (M0)
└── .gitignore                    # Git ignore (M0)
```

### Key Naming Conventions

| Category | Convention | Example |
|----------|-----------|---------|
| Components | PascalCase | `VoiceUploader.tsx`, `TextInput.tsx` |
| Pages | PascalCase | `Login.tsx`, `VoiceManage.tsx` |
| Hooks | camelCase, prefix `use` | `useAuth.ts`, `useVoiceQuality.ts` |
| Services | camelCase, suffix `Client` | `authClient.ts`, `inferenceClient.ts` |
| Types | PascalCase | `AuthState.ts`, `VoiceSample.ts` |
| Utils | camelCase | `validation.ts`, `formatters.ts` |
| Constants | UPPER_SNAKE_CASE | `MAX_FILE_SIZE`, `RATE_LIMIT_PER_HOUR` |
| Tests | `*.spec.tsx` | `auth.spec.tsx`, `voice.spec.tsx` |
| Mocks | `*-handlers.ts` | `auth-handlers.ts`, `voices-handlers.ts` |

---

## Component Registry (M0 Scope)

### Common Components (Shared across all pages)

| Component | File | Props | Purpose |
|-----------|------|-------|---------|
| ErrorBoundary | `src/components/common/ErrorBoundary.tsx` | `{children, fallback?}` | Catch React errors, display fallback UI |
| Header | `src/components/common/Header.tsx` | `{user?, onLogout?}` | Top navigation bar (logo, user info, logout) |
| Sidebar | `src/components/common/Sidebar.tsx` | `{activeRoute?, onNavigate?}` | Left navigation menu |
| Footer | `src/components/common/Footer.tsx` | `{}` | Footer (copyright, links) |

### UI Primitives (TailwindCSS-based components)

| Component | File | Props | Purpose |
|-----------|------|-------|---------|
| Button | `src/components/ui/Button.tsx` | `{children, variant?, size?, disabled?, onClick?}` | Reusable button |
| Input | `src/components/ui/Input.tsx` | `{type?, placeholder?, value?, onChange?, error?}` | Text input with validation |
| Card | `src/components/ui/Card.tsx` | `{children, title?, className?}` | Container with border/shadow |
| Modal | `src/components/ui/Modal.tsx` | `{isOpen, onClose, children, title?}` | Popup dialog |
| Spinner | `src/components/ui/Spinner.tsx` | `{size?, color?}` | Loading indicator |
| Toast | `src/components/ui/Toast.tsx` | `{message, type?, duration?}` | Notification message |

### Root Component

| Component | File | Props | Purpose |
|-----------|------|-------|---------|
| App | `src/App.tsx` | `{}` | Root component (routes, providers) |

---

## API Service Layer (M0 Scope)

### Base HTTP Client

**File:** `src/services/api/httpClient.ts`

```typescript
export interface HttpClientConfig {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
}

export interface HttpResponse<T> {
  data: T;
  status: number;
  headers: Record<string, string>;
}

export interface HttpError {
  status: number;
  message: string;
  data?: any;
}

export class HttpClient {
  constructor(config: HttpClientConfig) { }
  
  async get<T>(url: string, options?: any): Promise<HttpResponse<T>>;
  async post<T>(url: string, data: any, options?: any): Promise<HttpResponse<T>>;
  async put<T>(url: string, data: any, options?: any): Promise<HttpResponse<T>>;
  async delete<T>(url: string, options?: any): Promise<HttpResponse<T>>;
  
  setAuthToken(token: string): void;
  clearAuthToken(): void;
}
```

**Purpose:** Generic HTTP client for all API calls (axios-like, but smaller).

### API Clients (created in later milestones, scaffolded in M0)

| Client | File | Purpose | Milestone |
|--------|------|---------|-----------|
| authClient | `src/services/api/authClient.ts` | Auth Service (8001) | M1-GREEN |
| voiceClient | `src/services/api/voiceClient.ts` | Voices Service (8002) | M2-GREEN |
| jobsClient | `src/services/api/jobsClient.ts` | Jobs Service (8003) | M3-GREEN |
| inferenceClient | `src/services/api/inferenceClient.ts` | Inference Service (8005) | M3-GREEN |
| evaluationClient | `src/services/api/evaluationClient.ts` | AI Evaluation Service (8006) | M2-GREEN |

Each client will:
- Extend or use HttpClient
- Define typed methods for each API endpoint
- Handle error mapping to user-friendly messages
- Include request/response logging in development

---

## Build & Tooling Setup

### Vite Configuration

**File:** `vite.config.ts`

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
    },
  },
  build: {
    target: 'es2020',
    outDir: 'dist',
    sourcemap: false,
  },
})
```

**Purpose:** Vite dev server (fast refresh), build config, dev proxy for backend APIs.

### TypeScript Configuration

**File:** `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "strict": true,
    "esModuleInterop": true,
    "jsx": "react-jsx",
    "resolveJsonModule": true,
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@services/*": ["./src/services/*"]
    }
  }
}
```

**Purpose:** TypeScript strict mode, path aliases for imports.

### ESLint Configuration

**File:** `.eslintrc.json`

```json
{
  "env": { "browser": true, "es2020": true },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "rules": {
    "react/react-in-jsx-scope": "off",
    "no-console": ["warn", { "allow": ["error", "warn"] }]
  }
}
```

**Purpose:** Code quality checks (no unused vars, consistent style).

### Prettier Configuration

**File:** `.prettierrc.json`

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

**Purpose:** Code formatting (consistent indentation, quotes, line length).

### Vitest Configuration

**File:** `tests/vitest.config.ts` (or `vitest.config.ts` at root)

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/mocks/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'tests/'],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

**Purpose:** Test runner config (jsdom for DOM testing, MSW setup, coverage).

### TailwindCSS Configuration

**File:** `tailwind.config.js`

```javascript
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Purpose:** TailwindCSS utility classes (responsive design).

### Package.json Scripts

**File:** `package.json`

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src tests --ext .ts,.tsx",
    "format": "prettier --write src tests",
    "type-check": "tsc --noEmit"
  }
}
```

**Purpose:** Standard npm commands for development.

---

## Development Environment

### Environment Variables

**File:** `.env.example`

```
# Backend Services (local development)
VITE_AUTH_API_URL=http://localhost:8001
VITE_VOICES_API_URL=http://localhost:8002
VITE_JOBS_API_URL=http://localhost:8003
VITE_INFERENCE_API_URL=http://localhost:8005
VITE_EVALUATION_API_URL=http://localhost:8006

# Frontend Config
VITE_APP_NAME=Voice Cloning
VITE_APP_VERSION=1.0.0
VITE_LOG_LEVEL=debug

# Feature Flags (for Phase 2)
VITE_FEATURE_BATCH_GENERATION=false
VITE_FEATURE_VOICE_SHARING=false
```

**File:** `.env.development` (created from .env.example)

**File:** `.env.staging` (staging backend URLs)

**File:** `.env.production` (production backend URLs)

**Purpose:** Configuration per environment (dev/staging/prod).

### Local Backend Service Setup

**File:** `docker-compose.yml` (at repo root, created by M0)

```yaml
version: '3.8'
services:
  auth-service:
    image: voice-narration-auth:latest
    ports: ["8001:8001"]
    environment:
      DATABASE_URL: postgresql://...
  
  voices-service:
    image: voice-narration-voices:latest
    ports: ["8002:8002"]
    
  jobs-service:
    image: voice-narration-jobs:latest
    ports: ["8003:8003"]
    
  inference-service:
    image: voice-narration-inference:latest
    ports: ["8005:8005"]
    
  ai-evaluation-service:
    image: voice-narration-ai-evaluation:latest
    ports: ["8006:8006"]
    
  postgres:
    image: postgres:15
    ports: ["5432:5432"]
    environment:
      POSTGRES_PASSWORD: postgres
```

**Purpose:** One-command start for all backend services during frontend development.

### Docker Dev Environment

**File:** `docker/Dockerfile.dev`

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY . .

EXPOSE 5173

CMD ["pnpm", "dev"]
```

**Purpose:** Containerized dev environment (matches CI/CD and production setup).

### CI/CD Pipeline Skeleton

**File:** `.github/workflows/lint.yml`

```yaml
name: Lint
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm install -g pnpm
      - run: pnpm install
      - run: pnpm lint
      - run: pnpm format:check
```

**File:** `.github/workflows/test.yml`

```yaml
name: Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm install -g pnpm
      - run: pnpm install
      - run: pnpm test
      - run: pnpm test:coverage
```

**File:** `.github/workflows/build.yml`

```yaml
name: Build
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm install -g pnpm
      - run: pnpm install
      - run: pnpm build
```

**Purpose:** Automated lint, test, and build verification on every commit.

---

## Implementation Tasks (M0 Breakdown)

### Task M0-001: Project Initialization & Folder Structure

**Deliverables:**
- React + TypeScript project initialized with Vite
- All folders created (src/components/, src/services/, etc.)
- .gitignore configured
- README.md created with setup instructions
- Initial Git commit

**Acceptance Criteria:**
- ✅ `pnpm install` completes without errors
- ✅ Folder structure matches section "Folder Layout" above
- ✅ `npm run dev` starts dev server on http://localhost:5173
- ✅ Git history shows initial commit

**Estimated Effort:** 4 hours

**Dependencies:** None (first task)

---

### Task M0-002: TypeScript & Build Tooling Setup

**Deliverables:**
- `tsconfig.json` configured (strict mode)
- `vite.config.ts` configured (dev server, build settings)
- `tsconfig.app.json` for app code
- `tsconfig.node.json` for Vite config
- Build command verified

**Acceptance Criteria:**
- ✅ `pnpm build` produces `dist/` folder with optimized bundle
- ✅ `pnpm type-check` passes (no TS errors)
- ✅ Source maps disabled in production build
- ✅ Dev server hot-reload works

**Estimated Effort:** 3 hours

**Dependencies:** M0-001

---

### Task M0-003: Linting, Formatting & Code Quality

**Deliverables:**
- ESLint configured (react, typescript plugins)
- Prettier configured
- `.eslintrc.json` and `.prettierrc.json` created
- Pre-commit hooks configured (husky)
- Lint and format scripts added to package.json

**Acceptance Criteria:**
- ✅ `pnpm lint` runs without errors (on empty src/)
- ✅ `pnpm format` formats all files consistently
- ✅ Git pre-commit hook prevents commits with lint errors
- ✅ IDE extensions recommend ESLint/Prettier configs

**Estimated Effort:** 3 hours

**Dependencies:** M0-001, M0-002

---

### Task M0-004: Testing Setup (Vitest + MSW)

**Deliverables:**
- `vitest.config.ts` configured (jsdom, globals)
- MSW (Mock Service Worker) installed and configured
- `tests/mocks/setup.ts` created (MSW setup)
- `tests/mocks/` folder structure created (ready for handlers)
- `tests/fixtures/` folder created (test data factories)
- Example test template created

**Acceptance Criteria:**
- ✅ `pnpm test` runs and discovers tests
- ✅ MSW server starts before tests run
- ✅ Test coverage reporter configured (HTML output)
- ✅ Can run single test: `pnpm test -- auth.spec.tsx`
- ✅ `pnpm test:coverage` generates coverage report in `coverage/`

**Estimated Effort:** 4 hours

**Dependencies:** M0-002, M0-003

---

### Task M0-005: TailwindCSS & UI Framework

**Deliverables:**
- TailwindCSS installed and configured
- `tailwind.config.js` and `postcss.config.js` created
- `src/index.css` created with Tailwind directives
- Base UI component file structure created (Button, Input, Card, Modal, Spinner, Toast)
- Tailwind class utilities example in root App.tsx

**Acceptance Criteria:**
- ✅ TailwindCSS classes work in component files
- ✅ CSS bundle includes only used utilities (purging works)
- ✅ Dev server shows Tailwind-styled content
- ✅ UI components folder has skeleton files (not implemented, just structure)

**Estimated Effort:** 2 hours

**Dependencies:** M0-001, M0-002

---

### Task M0-006: Docker & Environment Setup

**Deliverables:**
- `docker/Dockerfile.dev` created (dev image)
- `docker/Dockerfile` created (production image)
- `docker-compose.yml` created (all 7 backend services)
- `.env.example` created with all variables
- `.env.development`, `.env.staging`, `.env.production` created
- Docker build verified locally

**Acceptance Criteria:**
- ✅ `docker build -f docker/Dockerfile.dev -t voice-cloning-frontend:dev .` succeeds
- ✅ `docker run -p 5173:5173 voice-cloning-frontend:dev` starts dev server
- ✅ `docker-compose up` starts all 7 backend services + postgres
- ✅ `.env` files not committed to git (in .gitignore)

**Estimated Effort:** 3 hours

**Dependencies:** M0-001

---

### Task M0-007: CI/CD Pipeline Skeleton & Base HTTP Client

**Deliverables:**
- `.github/workflows/lint.yml` created (ESLint + Prettier checks)
- `.github/workflows/test.yml` created (run Vitest + coverage)
- `.github/workflows/build.yml` created (verify build)
- `src/services/api/httpClient.ts` created (base HTTP class skeleton)
- `src/types/api.ts` created (API response types)
- Initial GitHub Actions workflow trigger verified

**Acceptance Criteria:**
- ✅ GitHub Actions workflows visible in repo (if public)
- ✅ `pnpm lint`, `pnpm test`, `pnpm build` all pass locally
- ✅ HttpClient class can be imported: `import { HttpClient } from '@services/api/httpClient'`
- ✅ API types file can be imported: `import type { ApiResponse } from '@types/api'`

**Estimated Effort:** 3 hours

**Dependencies:** M0-001 through M0-006

---

## Success Criteria (M0 Complete)

The M0-FOUNDATION milestone is **complete** when:

1. ✅ **Project Structure:** Folder layout matches specification above
2. ✅ **Development Server:** `pnpm dev` starts on http://localhost:5173 with hot-reload
3. ✅ **Build:** `pnpm build` produces optimized `dist/` folder
4. ✅ **Testing:** `pnpm test` discovers and runs tests (empty for now)
5. ✅ **Code Quality:** `pnpm lint` and `pnpm format` work without errors
6. ✅ **TypeScript:** `pnpm type-check` passes (strict mode)
7. ✅ **TailwindCSS:** Utility classes work in components
8. ✅ **Docker:** `docker build` and `docker-compose up` succeed
9. ✅ **CI/CD:** GitHub Actions workflows trigger on push (lint, test, build jobs)
10. ✅ **Environment:** `.env.development` connects to localhost:8001-8006 backend services
11. ✅ **Git:** Initial commit includes all scaffolding (no generated code)
12. ✅ **Documentation:** README.md explains setup steps
13. ✅ **Ready for M1-RED:** Base HTTP client and API types in place, test infrastructure ready

### Definition of Done
- No TypeScript errors
- No console warnings
- All npm scripts execute without errors
- All code passes lint checks
- Git history is clean with meaningful commits
- Every team member can run `pnpm install && pnpm dev` and have working dev environment

---

## Implementation Timeline (M0 is 2 weeks)

```
Week 1:
  Mon: M0-001 (Project Init) + M0-002 (TypeScript) [7h]
  Tue: M0-003 (Linting) + M0-004 (Testing Setup) [8h]
  Wed: M0-005 (TailwindCSS) [2h]
  Thu: M0-006 (Docker) + M0-007 (CI/CD) [6h]
  Fri: Integration testing, documentation [3h]

Week 2:
  Mon-Fri: Buffer for unforeseen issues, polish, team review
```

---

## Approval Status

**Status:** ⏳ **AWAITING USER APPROVAL**

This Implementation Plan for M0-FOUNDATION is comprehensive and ready for execution. It:

- ✅ Specifies exact folder structure and file organization
- ✅ Defines 6 UI component categories + root component
- ✅ Provides all configuration files (Vite, TypeScript, ESLint, Prettier, TailwindCSS)
- ✅ Includes Docker + CI/CD skeleton
- ✅ Breaks M0 into 7 concrete implementation tasks
- ✅ Provides realistic effort estimates (40 hours total)
- ✅ Specifies measurable acceptance criteria per task
- ✅ References only approved Plan.md (no re-planning)

**Please review and confirm approval. Once approved, Implementation phase (code creation) will begin in a separate task.**

---

## Clarification Log

| # | Question | User Answer | Date |
|----|----------|------------|------|
| (None recorded yet) | | | |

---

## Provenance Check

- **Project structure** derived from: Standard React best practices + Plan.md folder references
- **Component registry** based on: Plan.md success criteria (UI components needed by M1, M2, M3)
- **API client structure** derived from: Backend services architecture (7 services on ports 8001-8006)
- **Build tooling** based on: Vite (modern, fast) + TypeScript strict + TailwindCSS (Plan.md tech stack)
- **Testing framework** based on: Plan.md requirement for MSW + Vitest (fast, modern alternative to Jest)
- **Docker setup** based on: docs/deployment/ folder (existing backend Docker experience)
- **CI/CD workflows** derived from: Standard GitHub Actions patterns for Node.js projects
- **Environment variables** based on: Backend service ports from docs/deployment/HOW_TO_RUN_ALL_SERVICES.md
- **File naming conventions** based on: React/TypeScript community standards
- **Effort estimates** based on: Complexity per task + typical scaffolding overhead

---

**End of 001_Implementation_Plan_FOUNDATION.md**

**Next Step:** After approval, Implementation phase creates actual React code per this plan specification.
