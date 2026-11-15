import React from 'react';
import { useTTS } from '@/hooks/useTTS';

export function TextToSpeechInput() {
  const { generationText, dispatch } = useTTS();

  const charCount = generationText.length;

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    dispatch({ type: 'SET_TEXT', payload: e.target.value });
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
        className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        data-testid="text-input"
      />

      <div className="flex justify-between items-center mt-2">
        <span className="text-sm text-gray-500" data-testid="char-count">
          {charCount} characters
        </span>

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
    </div>
  );
}
