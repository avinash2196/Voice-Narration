import { useState, FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { createAuthClient } from '../../services/api/authClient';
import { AuthLayout } from '../../layouts/AuthLayout';

interface SignupFormData {
  email: string;
  password: string;
  confirmPassword: string;
  agreedToTerms: boolean;
}

interface FormErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
  agreedToTerms?: string;
  general?: string;
}

export function Signup() {
  const navigate = useNavigate();
  const { dispatch } = useAuth();
  const [formData, setFormData] = useState<SignupFormData>({
    email: '',
    password: '',
    confirmPassword: '',
    agreedToTerms: false,
  });
  const [formErrors, setFormErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  const validateEmail = (email: string): boolean => {
    return email.includes('@') && email.length > 3 && email.indexOf('@') !== 0;
  };

  const validatePassword = (password: string): boolean => {
    return (
      password.length >= 8 &&
      /[A-Z]/.test(password) &&
      /\d/.test(password)
    );
  };

  const validateForm = (): boolean => {
    const errors: FormErrors = {};

    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }

    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (!validatePassword(formData.password)) {
      errors.password = 'Password must be at least 8 characters with 1 uppercase letter and 1 number';
    }

    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.agreedToTerms) {
      errors.agreedToTerms = 'You must agree to the terms and conditions';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setFormErrors({});

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    try {
      const client = createAuthClient();
      const response = await client.signup({
        email: formData.email,
        password: formData.password,
        confirmPassword: formData.confirmPassword,
        agreedToTerms: formData.agreedToTerms,
      });

      if (response.token) {
        dispatch({
          type: 'LOGIN',
          payload: {
            user: response.user,
            token: response.token,
            refreshToken: response.refreshToken,
          },
        });
        navigate('/voices');
      }
    } catch (error: any) {
      const errorMessage = error?.message || 'Signup failed. Please try again.';
      setFormErrors({ general: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    if (formErrors[name as keyof FormErrors]) {
      setFormErrors(prev => {
        const updated = { ...prev };
        delete updated[name as keyof FormErrors];
        return updated;
      });
    }
  };

  return (
    <AuthLayout title="Create Account">
      <div className="w-full space-y-4">
        <p className="text-gray-600 text-center text-sm">
          Already have an account?{' '}
          <Link to="/auth/login" className="text-blue-600 hover:text-blue-700 font-medium">
            Sign in
          </Link>
        </p>

        {formErrors.general && (
          <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {formErrors.general}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="you@example.com"
              disabled={isLoading}
              className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                formErrors.email ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {formErrors.email && <p className="text-red-600 text-sm mt-1">{formErrors.email}</p>}
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
              placeholder="••••••••"
              disabled={isLoading}
              className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                formErrors.password ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {formErrors.password && <p className="text-red-600 text-sm mt-1">{formErrors.password}</p>}
            <p className="text-xs text-gray-500 mt-1">Min 8 chars, 1 uppercase, 1 number</p>
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleInputChange}
              placeholder="••••••••"
              disabled={isLoading}
              className={`w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                formErrors.confirmPassword ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {formErrors.confirmPassword && (
              <p className="text-red-600 text-sm mt-1">{formErrors.confirmPassword}</p>
            )}
          </div>

          <div className="flex items-start space-x-2">
            <input
              id="agreedToTerms"
              name="agreedToTerms"
              type="checkbox"
              checked={formData.agreedToTerms}
              onChange={handleInputChange}
              disabled={isLoading}
              className="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
            />
            <label htmlFor="agreedToTerms" className="text-sm text-gray-700">
              I agree to the{' '}
              <a href="#" onClick={e => e.preventDefault()} className="text-blue-600 hover:text-blue-700 font-medium">
                Terms and Conditions
              </a>
            </label>
          </div>
          {formErrors.agreedToTerms && (
            <p className="text-red-600 text-sm">{formErrors.agreedToTerms}</p>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors mt-6"
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <p className="text-center text-xs text-gray-600 mt-4">
          By signing up, you agree to our Terms and Privacy Policy
        </p>
      </div>
    </AuthLayout>
  );
}

export default Signup;
