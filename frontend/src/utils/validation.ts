import type { FormError } from '../types/common';

export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePassword = (password: string): FormError[] => {
  const errors: FormError[] = [];

  if (password.length < 8) {
    errors.push({
      field: 'password',
      message: 'Password must be at least 8 characters long',
    });
  }

  if (!/[A-Z]/.test(password)) {
    errors.push({
      field: 'password',
      message: 'Password must contain at least one uppercase letter',
    });
  }

  if (!/[0-9]/.test(password)) {
    errors.push({
      field: 'password',
      message: 'Password must contain at least one number',
    });
  }

  return errors;
};

export const validatePasswordMatch = (
  password: string,
  confirmPassword: string
): FormError[] => {
  const errors: FormError[] = [];

  if (password !== confirmPassword) {
    errors.push({
      field: 'confirmPassword',
      message: 'Passwords do not match',
    });
  }

  return errors;
};

export const validateTextLength = (
  text: string,
  maxLength: number,
  minLength: number = 1
): FormError[] => {
  const errors: FormError[] = [];

  if (text.length < minLength) {
    errors.push({
      field: 'text',
      message: `Text must be at least ${minLength} character(s)`,
    });
  }

  if (text.length > maxLength) {
    errors.push({
      field: 'text',
      message: `Text must not exceed ${maxLength} characters (current: ${text.length})`,
    });
  }

  return errors;
};

export const validateFileSize = (
  fileSize: number,
  maxSizeBytes: number
): FormError[] => {
  const errors: FormError[] = [];

  if (fileSize > maxSizeBytes) {
    const maxSizeMB = maxSizeBytes / (1024 * 1024);
    const actualSizeMB = (fileSize / (1024 * 1024)).toFixed(2);
    errors.push({
      field: 'file',
      message: `File size must not exceed ${maxSizeMB}MB (actual: ${actualSizeMB}MB)`,
    });
  }

  return errors;
};
