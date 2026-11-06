import React, { useState, FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { AuthLayout } from '@/layouts/AuthLayout';
import { validateEmail } from '@/utils/validation';
import { createAuthClient } from '@/services/api/authClient';
import type { FormError } from '@/types/common';

export function Login() {
  const { dispatch, isLoading } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [formErrors, setFormErrors] = useState<FormError[]>([]);
  const [displayError, setDisplayError] = useState<string | null>(null);

  const validateForm = (): boolean => {
    const errors: FormError[] = [];

    if (!formData.email.trim()) {
      errors.push({ field: 'email', message: 'Email is required' });
    } else if (!validateEmail(formData.email)) {
      errors.push({ field: 'email', message: 'Invalid email format' });
    }

    if (!formData.password) {
      errors.push({ field: 'password', message: 'Password is required' });
    }

    setFormErrors(errors);
    return errors.length === 0;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!validateForm()) {
      setFormData((prev) => ({ ...prev, password: '' }));
      return;
    }

    dispatch({ type: 'SET_LOADING', payload: true });
    setDisplayError(null);

    try {
      const authClient = createAuthClient();
      const response = await authClient.login({
        email: formData.email,
        password: formData.password,
      });

      dispatch({
        type: 'LOGIN',
        payload: {
          user: response.user,
          token: response.token,
          refreshToken: response.refreshToken,
        },
      });

      // Redirect to voice management after successful login
      navigate('/voices');
    } catch (error: any) {
      const errorMessage = error?.message || 'Login failed. Please try again.';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      setDisplayError(errorMessage);
      setFormData((prev) => ({ ...prev, password: '' }));
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setFormErrors((prev) => prev.filter((err) => err.field !== name));
  };

  const getFieldError = (field: string): string | undefined => {
    return formErrors.find((err) => err.field === field)?.message;
  };

  return (
    <AuthLayout title="Login">
      <form onSubmit={handleSubmit} className="space-y-4">
        {displayError && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-700 text-sm">{displayError}</p>
          </div>
        )}

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleInputChange}
            disabled={isLoading}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100 ${
              getFieldError('email') ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="you@example.com"
          />
          {getFieldError('email') && (
            <p className="mt-1 text-sm text-red-600">{getFieldError('email')}</p>
          )}
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleInputChange}
            disabled={isLoading}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100 ${
              getFieldError('password') ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="••••••••"
          />
          {getFieldError('password') && (
            <p className="mt-1 text-sm text-red-600">{getFieldError('password')}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-medium rounded-md transition-colors"
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </button>

        <div className="text-center mt-6">
          <p className="text-gray-600 text-sm">
            Don't have an account?{' '}
            <Link to="/auth/signup" className="text-indigo-600 hover:text-indigo-700 font-medium">
              Sign up
            </Link>
          </p>
        </div>
      </form>
    </AuthLayout>
  );
}

export default Login;
