# Voice Cloning Frontend - M0 FOUNDATION

This is the React frontend for the Voice Cloning application, built with:
- **React 18** + **TypeScript**
- **Vite** (fast dev server)
- **TailwindCSS** (styling)
- **Vitest** + **MSW** (testing)
- **ESLint** + **Prettier** (code quality)
- **Docker** (containerization)

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pnpm install

# Start dev server (runs on http://localhost:5173)
pnpm dev

# Run tests
pnpm test

# Run linter
pnpm lint

# Format code
pnpm format

# Type check
pnpm type-check

# Build for production
pnpm build

# Preview production build
pnpm preview
```

### Docker Development

```bash
# Build dev image
docker build -f docker/Dockerfile.dev -t voice-cloning-frontend:dev .

# Run dev container
docker run -p 5173:5173 voice-cloning-frontend:dev

# Build production image
docker build -t voice-cloning-frontend:latest .

# Run production container
docker run -p 80:80 voice-cloning-frontend:latest
```

## 📁 Project Structure

```
src/
├── components/      # React components
│   ├── common/     # Shared components (Header, Footer, etc.)
│   └── ui/         # UI primitives (Button, Input, etc.)
├── pages/          # Page components (will be added in M1-M3)
├── services/       # API clients and utilities
│   ├── api/       # HTTP client
│   └── storage/   # Local storage helpers
├── context/        # React Context (will be added in M1-M3)
├── hooks/          # Custom React hooks (will be added in M1-M3)
├── types/          # TypeScript type definitions
├── utils/          # Utility functions
├── middleware/     # Request/response middleware
├── App.tsx         # Root app component
└── main.tsx        # Entry point
```

## 🔧 Configuration

- **Vite**: `vite.config.ts`
- **TypeScript**: `tsconfig.json`
- **ESLint**: `.eslintrc.json`
- **Prettier**: `.prettierrc.json`
- **TailwindCSS**: `tailwind.config.js`
- **Vitest**: `vitest.config.ts`

## 📝 Environment Variables

Copy `.env.example` to `.env.development` or `.env.production` and update as needed:

```bash
VITE_AUTH_API_URL=http://localhost:8001
VITE_VOICES_API_URL=http://localhost:8002
VITE_JOBS_API_URL=http://localhost:8003
VITE_INFERENCE_API_URL=http://localhost:8005
VITE_EVALUATION_API_URL=http://localhost:8006
```

## 🧪 Testing

Tests are written using **Vitest** and **MSW** (Mock Service Worker):

```bash
# Run tests in watch mode
pnpm test

# Run tests with UI
pnpm test:ui

# Generate coverage report
pnpm test:coverage
```

## 🚀 Deployment

### Build

```bash
pnpm build
```

Output is in `dist/` folder.

### Docker

```bash
docker build -t voice-cloning-frontend:latest .
docker run -p 80:80 voice-cloning-frontend:latest
```

## 📚 Next Steps (Milestones)

- **M1-RED** (Week 3): Auth tests (45+ test cases)
- **M1-GREEN** (Week 4): Auth implementation
- **M2-RED** (Week 5): Voice management tests
- **M2-GREEN** (Week 6): Voice upload/record implementation
- **M3-RED** (Week 7): TTS generation tests
- **M3-GREEN** (Week 8): TTS implementation
- **M4-REFACTOR** (Optional): Performance & accessibility improvements

## 📄 License

MIT
