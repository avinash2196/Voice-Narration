import React from 'react';
import { useTTS } from '@/hooks/useTTS';
import { ChatterboxLanguage } from '@/types/tts';

const LANGUAGES: Array<{ code: ChatterboxLanguage; label: string }> = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'Hindi' },
];

export function LanguageSelector() {
  const { selectedLanguage, dispatch } = useTTS();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const language = LANGUAGES.find((option) => option.code === e.target.value);
    if (language) {
      dispatch({ type: 'SELECT_LANGUAGE', payload: language.code });
    }
  };

  return (
    <div className="w-full" data-testid="language-selector-container">
      <label htmlFor="language-select-field" className="block text-sm font-medium text-gray-700 mb-2">
        Language
      </label>

      <select
        id="language-select-field"
        value={selectedLanguage}
        onChange={handleChange}
        className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        data-testid="language-select"
      >
        {LANGUAGES.map((language) => (
          <option key={language.code} value={language.code}>
            {language.label}
          </option>
        ))}
      </select>
    </div>
  );
}
