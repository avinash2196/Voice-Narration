import { useContext } from 'react';
import { AuthContext, type AuthContextType } from '../context/AuthContext';

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error(
      'useAuth must be used within an AuthProvider. Please wrap your component tree with <AuthProvider> from ../context/AuthContext.'
    );
  }
  return context;
}
