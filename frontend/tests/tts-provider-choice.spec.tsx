// ============================================================================
// OAM-6 RED: TTS page provider, voice and language per generation, and no text cap
// (chatterbox-original-app; requirements COA-1, COA-3, COA-4, COA-5, COA-7, COA-13, COA-17).
//
// The inference service (port 8003) and the voice service (port 8002) are mocked with msw.
// The page never talks to Chatterbox; no test fakes or calls Chatterbox (COA-16).
// A catch-all handler answers every other request, so no request leaves the test process.
// ============================================================================

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';
import { rest } from 'msw';

import { server } from './mocks/setup';
import { TextToSpeech } from '../src/pages/TextToSpeech';
import { TTSProvider } from '../src/context/TTSContext';
import { AuthContext } from '../src/context/AuthContext';

const INFERENCE = 'http://localhost:8003';
const VOICES = 'http://localhost:8002';

// Inference Provider List as the approved contract defines it (API-Contract.md, Inference Provider List).
const BACKENDS = [
  {
    name: 'azure',
    provider_class: 'AzureSpeechProvider',
    description: 'Azure Cognitive Services Speech (requires AZURE_SPEECH_KEY + AZURE_SPEECH_REGION)',
  },
  {
    name: 'chatterbox',
    provider_class: 'ChatterboxClient',
    description: 'Chatterbox voice cloning (deployed Cloud Run service)',
  },
  {
    name: 'google',
    provider_class: 'GoogleTextToSpeechProvider',
    description: 'Google Cloud Text-to-Speech (requires GOOGLE_APPLICATION_CREDENTIALS)',
  },
  {
    name: 'mock',
    provider_class: 'MockInferenceProvider',
    description: 'Deterministic mock for testing (no external deps)',
  },
];

// Approved Voice List as the approved contract defines it: preloaded Google voices carry
// "provider": "google"; recorded and uploaded voices carry no provider field.
const GOOGLE_VOICE = {
  id: 'en-US-Neural2-A',
  name: 'Google Neural2-A (US English)',
  provider: 'google',
  language: 'en-US',
  gender: 'Female',
  approvalScore: 100,
  status: 'approved',
};
const GOOGLE_HINDI_VOICE = {
  id: 'hi-IN-Neural2-A',
  name: 'Google Neural2-A (Hindi)',
  provider: 'google',
  language: 'hi-IN',
  gender: 'Female',
  approvalScore: 100,
  status: 'approved',
};
const RECORDED_VOICE = {
  id: 'voice-1a2b3c4d',
  name: 'My Chrome recording',
  format: 'WAV',
  duration: 45,
  fileSize: 48213,
  uploadedAt: '2026-11-13T10:00:00.000000',
  status: 'approved',
  approvalScore: 95,
};
const UPLOADED_VOICE = {
  id: 'voice-5e6f7a8b',
  name: 'Uploaded WAV voice',
  format: 'WAV',
  duration: 45,
  fileSize: 96044,
  uploadedAt: '2026-11-13T10:05:00.000000',
  status: 'approved',
  approvalScore: 95,
};
const APPROVED_VOICES = [GOOGLE_VOICE, GOOGLE_HINDI_VOICE, RECORDED_VOICE, UPLOADED_VOICE];

// The nine Chatterbox failure messages of the approved contract (Chatterbox Failure Causes,
// OAF-1 to OAF-9), with <N> = 1200 and <status> = 403 and 500.
const CHATTERBOX_FAILURE_MESSAGES = [
  'Chatterbox voice cloning is not configured. Please retry, or choose another provider.',
  'The Chatterbox time limit setting CHATTERBOX_TIMEOUT_SECONDS is invalid; it must be a positive whole number of seconds. Please retry, or choose another provider.',
  'The voice sample for the selected voice could not be read. Please retry, or choose another provider.',
  'Could not obtain an identity token for Chatterbox. Please retry, or choose another provider.',
  'Chatterbox did not respond within 1200 seconds. Please retry, or choose another provider.',
  'Could not connect to Chatterbox. Please retry, or choose another provider.',
  'Access to Chatterbox was denied (HTTP 403). Please retry, or choose another provider.',
  'Chatterbox returned an error (HTTP 500). Please retry, or choose another provider.',
  'Chatterbox returned a response that is not audio. Please retry, or choose another provider.',
];

// Text longer than the removed 5000-character cap (COA-17): 6600 characters.
const LONG_TEXT = 'Chatterbox long text. '.repeat(300);

// A short, valid PCM WAV file: 16-bit mono, 24000 Hz, four silent frames.
function wavFile(): ArrayBuffer {
  const frames = 4;
  const dataSize = frames * 2;
  const buffer = new ArrayBuffer(44 + dataSize);
  const view = new DataView(buffer);
  const ascii = (offset: number, text: string) => {
    for (let i = 0; i < text.length; i += 1) view.setUint8(offset + i, text.charCodeAt(i));
  };
  ascii(0, 'RIFF');
  view.setUint32(4, 36 + dataSize, true);
  ascii(8, 'WAVE');
  ascii(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, 24000, true);
  view.setUint32(28, 48000, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  ascii(36, 'data');
  view.setUint32(40, dataSize, true);
  return buffer;
}
const CLONED_WAV_FILE = wavFile();
const CLONED_WAV = new Uint8Array(CLONED_WAV_FILE);

// Reads a jsdom Blob, which has no arrayBuffer() method in this test environment.
function blobBytes(blob: Blob): Promise<Uint8Array> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(new Uint8Array(reader.result as ArrayBuffer));
    reader.onerror = () => reject(reader.error);
    reader.readAsArrayBuffer(blob);
  });
}

type InferAnswer = { status: number; body: Record<string, unknown> };
type InferRequest = { jobId: string; body: Record<string, unknown> };

let inferRequests: InferRequest[] = [];
let downloadRequests: string[] = [];
let unexpectedRequests: string[] = [];
let inferAnswer: InferAnswer = { status: 200, body: {} };
let inferGate: Promise<void> | null = null;

function completeAnswer(): InferAnswer {
  return { status: 200, body: { status: 'complete', duration_seconds: 4 / 24000 } };
}

beforeEach(() => {
  inferRequests = [];
  downloadRequests = [];
  unexpectedRequests = [];
  inferAnswer = completeAnswer();
  inferGate = null;
  server.use(
    rest.get(`${INFERENCE}/inference/backends`, (req, res, ctx) =>
      res(ctx.status(200), ctx.json({ backends: BACKENDS }))
    ),
    rest.get(`${VOICES}/voices/approved`, (req, res, ctx) =>
      res(ctx.status(200), ctx.json({ data: APPROVED_VOICES }))
    ),
    rest.get(`${INFERENCE}/inference/generations`, (req, res, ctx) =>
      res(ctx.status(200), ctx.json({ items: [], total: 0, skip: 0, limit: 100 }))
    ),
    rest.post(`${INFERENCE}/inference/jobs/:jobId/infer`, async (req, res, ctx) => {
      const jobId = String(req.params.jobId);
      const body = (await req.json()) as Record<string, unknown>;
      inferRequests.push({ jobId, body });
      if (inferGate) {
        await inferGate;
      }
      const answerBody = inferAnswer.status === 200 ? { job_id: jobId, ...inferAnswer.body } : inferAnswer.body;
      return res(ctx.status(inferAnswer.status), ctx.json(answerBody));
    }),
    rest.get(`${INFERENCE}/inference/jobs/:jobId/download`, (req, res, ctx) => {
      downloadRequests.push(String(req.params.jobId));
      return res(ctx.status(200), ctx.set('Content-Type', 'audio/wav'), ctx.body(CLONED_WAV_FILE));
    }),
    rest.all('*', (req, res, ctx) => {
      unexpectedRequests.push(`${req.method} ${req.url.href}`);
      return res(ctx.status(501), ctx.json({ error: 'unexpected request in test' }));
    })
  );
});

afterEach(() => {
  expect(unexpectedRequests).toEqual([]);
});

function AuthenticatedPage() {
  const [authState] = React.useState({
    user: null,
    token: 'mock-test-token',
    refreshToken: 'mock-refresh-token',
    isAuthenticated: true,
    isLoading: false,
    error: null,
  });

  return (
    <AuthContext.Provider value={{ ...authState, dispatch: () => {} }}>
      <TTSProvider>
        <TextToSpeech />
      </TTSProvider>
    </AuthContext.Provider>
  );
}

// Renders the TTS page and waits until its provider list and voice list have loaded.
async function renderPage() {
  render(<AuthenticatedPage />);
  await waitFor(() => {
    expect(screen.getByTestId('provider-radio-google')).toBeInTheDocument();
    expect(screen.getByTestId('provider-radio-chatterbox')).toBeInTheDocument();
  });
  await waitFor(() => {
    expect(screen.getByTestId('voice-select')).toHaveValue(GOOGLE_VOICE.id);
  });
}

function offeredProviders(): string[] {
  return screen.getAllByRole('radio').map((radio) => (radio as HTMLInputElement).value);
}

function offeredVoiceIds(): string[] {
  return within(screen.getByTestId('voice-select'))
    .getAllByRole('option')
    .map((option) => (option as HTMLOptionElement).value)
    .filter((value) => value !== '');
}

function languageOptions(): Array<[string, string]> {
  return within(screen.getByTestId('language-select'))
    .getAllByRole('option')
    .map((option) => [(option as HTMLOptionElement).value, option.textContent ?? '']);
}

type User = ReturnType<typeof userEvent.setup>;

// Waits until Chatterbox is chosen and the voice list shows exactly the recorded and uploaded voices.
async function waitForChatterboxVoices() {
  await waitFor(() => {
    expect(screen.getByTestId('provider-radio-chatterbox')).toBeChecked();
    expect(offeredVoiceIds()).toEqual([RECORDED_VOICE.id, UPLOADED_VOICE.id]);
  });
}

async function chooseChatterbox(user: User) {
  await user.click(screen.getByTestId('provider-radio-chatterbox'));
  await waitForChatterboxVoices();
}

async function chooseVoice(user: User, voiceId: string) {
  await user.selectOptions(screen.getByTestId('voice-select'), voiceId);
  await waitFor(() => {
    expect(screen.getByTestId('voice-select')).toHaveValue(voiceId);
  });
}

async function chooseLanguage(user: User, language: string) {
  await waitFor(() => {
    expect(screen.getByTestId('language-select')).toBeInTheDocument();
  });
  await user.selectOptions(screen.getByTestId('language-select'), language);
  await waitFor(() => {
    expect(screen.getByTestId('language-select')).toHaveValue(language);
  });
}

function enterText(text: string) {
  fireEvent.change(screen.getByTestId('text-input'), { target: { value: text } });
}

async function generate(user: User) {
  await waitFor(() => {
    expect(screen.getByTestId('generate-button')).not.toBeDisabled();
  });
  await user.click(screen.getByTestId('generate-button'));
  await waitFor(() => {
    expect(inferRequests).toHaveLength(1);
  });
}

describe('OAM-6: provider chosen per generation (COA-1)', () => {
  it('OAM-6.1: offers exactly Google and Chatterbox from the provider list, Google first selected', async () => {
    await renderPage();

    expect(offeredProviders().sort()).toEqual(['chatterbox', 'google']);
    expect(screen.getByTestId('provider-radio-google')).toBeChecked();
    expect(screen.getByTestId('provider-radio-chatterbox')).not.toBeChecked();
    expect(screen.getByText('Google Cloud Text-to-Speech')).toBeInTheDocument();
    expect(screen.getByText('Chatterbox voice cloning')).toBeInTheDocument();
  });

  it('OAM-6.2: a Google generation request names provider google', async () => {
    const user = userEvent.setup();
    await renderPage();

    enterText('Hello from Google narration.');
    await generate(user);

    expect(inferRequests[0].body).toMatchObject({
      script: 'Hello from Google narration.',
      voice_id: GOOGLE_VOICE.id,
      provider: 'google',
    });
    await waitFor(() => {
      expect(downloadRequests).toEqual([inferRequests[0].jobId]);
    });
  });
});

describe('OAM-6: recorded and uploaded voices for Chatterbox (COA-3)', () => {
  it('OAM-6.3: with Chatterbox chosen, lists only recorded and uploaded voices and sends the one chosen', async () => {
    const user = userEvent.setup();
    await renderPage();

    await chooseChatterbox(user);
    expect(screen.getByTestId('voice-select')).toHaveValue(RECORDED_VOICE.id);
    expect(screen.getByRole('option', { name: /My Chrome recording/ })).toBeInTheDocument();
    expect(screen.getByRole('option', { name: /Uploaded WAV voice/ })).toBeInTheDocument();

    await chooseVoice(user, UPLOADED_VOICE.id);
    enterText('Speak in my uploaded voice.');
    await generate(user);

    expect(inferRequests[0].body).toEqual({
      script: 'Speak in my uploaded voice.',
      voice_id: UPLOADED_VOICE.id,
      provider: 'chatterbox',
      language: 'en',
    });
  });
});

describe('OAM-6: English or Hindi for Chatterbox (COA-5)', () => {
  it.each([
    ['English', 'en'],
    ['Hindi', 'hi'],
  ])('OAM-6.4: with Chatterbox chosen, %s can be chosen and is sent', async (_name, language) => {
    const user = userEvent.setup();
    await renderPage();

    await user.click(screen.getByTestId('provider-radio-chatterbox'));
    await waitFor(() => {
      expect(languageOptions()).toEqual([
        ['en', 'English'],
        ['hi', 'Hindi'],
      ]);
    });
    expect(screen.getByTestId('language-select')).toHaveValue('en');

    await waitForChatterboxVoices();
    await chooseLanguage(user, language);
    enterText('Namaste and hello.');
    await generate(user);

    expect(inferRequests[0].body).toEqual({
      script: 'Namaste and hello.',
      voice_id: RECORDED_VOICE.id,
      provider: 'chatterbox',
      language,
    });
  });
});

describe('OAM-6: Chatterbox failure messages shown (COA-7)', () => {
  it.each(CHATTERBOX_FAILURE_MESSAGES)('OAM-6.5: shows the failure message "%s"', async (message) => {
    const user = userEvent.setup();
    inferAnswer = { status: 503, body: { error: message } };
    await renderPage();

    await chooseChatterbox(user);
    enterText('This clone will fail.');
    await generate(user);

    expect(inferRequests[0].body).toMatchObject({ provider: 'chatterbox', voice_id: RECORDED_VOICE.id });
    await waitFor(() => {
      expect(within(screen.getByTestId('error-display')).getByText(message)).toBeInTheDocument();
    });
    expect(screen.queryByTestId('audio-player-container')).not.toBeInTheDocument();
    expect(downloadRequests).toEqual([]);
  });
});

describe('OAM-6: cloned speech plays on the page (COA-4)', () => {
  it('OAM-6.6: loads the audio of a finished Chatterbox generation into the player', async () => {
    const createObjectURL = vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:cloned-speech');
    try {
      const user = userEvent.setup();
      await renderPage();

      await chooseChatterbox(user);
      enterText('Hello in my own voice.');
      await generate(user);

      expect(inferRequests[0].body).toMatchObject({ provider: 'chatterbox', voice_id: RECORDED_VOICE.id });
      await waitFor(() => {
        expect(downloadRequests).toEqual([inferRequests[0].jobId]);
      });
      await waitFor(() => {
        const player = screen.getByTestId('audio-player-container');
        expect((within(player).getByTestId('audio-element') as HTMLAudioElement).src).toBe('blob:cloned-speech');
      });
      expect(createObjectURL).toHaveBeenCalledTimes(1);
      const loaded = createObjectURL.mock.calls[0][0] as Blob;
      expect(loaded.type).toBe('audio/wav');
      expect(await blobBytes(loaded)).toEqual(CLONED_WAV);
    } finally {
      createObjectURL.mockRestore();
    }
  });
});

describe('OAM-6: Generate disabled during a Chatterbox generation (COA-13)', () => {
  it('OAM-6.7: keeps the Generate button disabled while the Chatterbox generation is running', async () => {
    let release: () => void = () => {};
    inferGate = new Promise<void>((resolve) => {
      release = resolve;
    });
    try {
      const user = userEvent.setup();
      await renderPage();

      await chooseChatterbox(user);
      enterText('A long clone that takes a while.');
      await generate(user);

      expect(inferRequests[0].body).toMatchObject({ provider: 'chatterbox', voice_id: RECORDED_VOICE.id });
      expect(screen.getByTestId('generate-button')).toBeDisabled();

      release();
      await waitFor(() => {
        expect(screen.getByTestId('audio-player-container')).toBeInTheDocument();
      });
      expect(inferRequests).toHaveLength(1);
    } finally {
      release();
    }
  });
});

describe('OAM-6: no text length limit for any provider (COA-17)', () => {
  function expectLongTextKeptWhole() {
    const textInput = screen.getByTestId('text-input') as HTMLTextAreaElement;
    expect(textInput.value.length).toBe(LONG_TEXT.length);
    expect(textInput).toHaveValue(LONG_TEXT);
    expect(textInput).not.toHaveAttribute('maxlength');
    expect(screen.getByTestId('char-count')).toHaveTextContent(/^6600 characters$/);
    expect(screen.queryByText(/\/ 5000/)).not.toBeInTheDocument();
    expect(screen.queryByTestId('char-warning')).not.toBeInTheDocument();
    expect(screen.queryByText(/90% capacity/i)).not.toBeInTheDocument();
    expect(screen.queryByTestId('max-chars-warning')).not.toBeInTheDocument();
    expect(screen.queryByText(/maximum character limit/i)).not.toBeInTheDocument();
  }

  it('OAM-6.8: sends text over 5000 characters whole to Google and shows the failed-generation error when Google rejects it', async () => {
    const user = userEvent.setup();
    const rejection = 'Inference failed: 400 Either `input.text` or `input.ssml` is longer than the limit of 5000 bytes.';
    inferAnswer = { status: 500, body: { error: rejection } };
    await renderPage();

    expect(LONG_TEXT).toHaveLength(6600);
    enterText(LONG_TEXT);
    expectLongTextKeptWhole();
    await generate(user);

    expect(inferRequests[0].body).toMatchObject({ script: LONG_TEXT, provider: 'google' });
    await waitFor(() => {
      const errorDisplay = screen.getByTestId('error-display');
      expect(within(errorDisplay).getByText('Generation Failed')).toBeInTheDocument();
      expect(within(errorDisplay).getByText(rejection)).toBeInTheDocument();
    });
    expect(downloadRequests).toEqual([]);
  });

  it('OAM-6.9: sends text over 5000 characters whole to Chatterbox', async () => {
    const user = userEvent.setup();
    await renderPage();

    enterText(LONG_TEXT);
    expectLongTextKeptWhole();
    await chooseChatterbox(user);
    expectLongTextKeptWhole();
    await generate(user);

    expect(inferRequests[0].body).toEqual({
      script: LONG_TEXT,
      voice_id: RECORDED_VOICE.id,
      provider: 'chatterbox',
      language: 'en',
    });
    await waitFor(() => {
      expect(downloadRequests).toEqual([inferRequests[0].jobId]);
    });
  });

  it('OAM-6.10: shows no "Max 5000 chars/request" label on the providers it offers', async () => {
    await renderPage();

    expect(screen.getByTestId('provider-option-google')).toBeInTheDocument();
    expect(screen.getByTestId('provider-option-chatterbox')).toBeInTheDocument();
    expect(screen.queryAllByText(/chars\/request/)).toHaveLength(0);
  });
});
