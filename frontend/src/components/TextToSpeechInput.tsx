import React from 'react';
import { useTTS } from '@/hooks/useTTS';

const MAX_CHARS = 5000;
const WARNING_THRESHOLD = 0.9;

export function TextToSpeechInput() {
  const { generationText, dispatch } = useTTS();

  const charCount = generationText.length;
  const percentage = charCount / MAX_CHARS;
  const isWarning = percentage >= WARNING_THRESHOLD;

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value.slice(0, MAX_CHARS);
    dispatch({ type: 'SET_TEXT', payload: text });
  };

  const handleClear = () => {
    dispatch({ type: 'SET_TEXT', payload: '' });
  };

  return (
    <div className="w-full" data-testid="text-input-container">
      <label htmlFor="text-input-field" className="block text-sm font-medium text-gray-700 mb-2">
        Text to Convert
      </label>

      <textarea
        id="text-input-field"
        value={generationText}
        onChange={handleChange}
        placeholder="Enter text to convert to speech..."
        maxLength={MAX_CHARS}
        className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        data-testid="text-input"
      />

      <div className="flex justify-between items-center mt-2">
        <span
          className={`text-sm ${
            isWarning ? 'text-red-600 font-semibold' : 'text-gray-500'
          }`}
          data-testid="char-count"
        >
          {charCount} / {MAX_CHARS}
        </span>

        {isWarning && (
          <span className="text-sm text-red-600 font-semibold" data-testid="char-warning">
            ⚠️ 90% capacity reached
          </span>
        )}

        {charCount > 0 && (
          <button
            onClick={handleClear}
            className="text-sm px-3 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition"
            data-testid="clear-button"
          >
            Clear
          </button>
        )}
      </div>

      {charCount >= MAX_CHARS && (
        <p className="text-xs text-red-500 mt-1" data-testid="max-chars-warning">
          Maximum character limit reached
        </p>
      )}
    </div>
  );
}
