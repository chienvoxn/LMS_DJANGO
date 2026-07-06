import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api/client';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken') || null);
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken') || null);
  const [loading, setLoading] = useState(true);

  // Load user from storage on mount
  useEffect(() => {
    loadUserFromStorage();
  }, []);

  const loadUserFromStorage = async () => {
    const storedToken = localStorage.getItem('accessToken');
    if (storedToken) {
      try {
        const response = await authAPI.me();
        setUser(response.data);
        setAccessToken(storedToken);
      } catch (error) {
        // Token invalid, clear storage
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        setAccessToken(null);
        setRefreshToken(null);
      }
    }
    setLoading(false);
  };

  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password });
      const { access, refresh } = response.data;
      
      // Store tokens
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      setAccessToken(access);
      setRefreshToken(refresh);
      
      // Fetch user info
      const userResponse = await authAPI.me();
      const userData = userResponse.data;
      setUser(userData);
      
      return { success: true, user: userData };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed. Please check your credentials.',
      };
    }
  };

  const register = async (payload) => {
    try {
      const response = await authAPI.register(payload);
      const { tokens } = response.data;
      
      let userData = null;
      if (tokens) {
        // Auto-login after registration
        localStorage.setItem('accessToken', tokens.access);
        localStorage.setItem('refreshToken', tokens.refresh);
        setAccessToken(tokens.access);
        setRefreshToken(tokens.refresh);
        
        // Fetch user info
        const userResponse = await authAPI.me();
        userData = userResponse.data;
        setUser(userData);
      }
      
      return { success: true, data: response.data, user: userData };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data || 'Registration failed. Please try again.',
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setUser(null);
    setAccessToken(null);
    setRefreshToken(null);
  };

  const value = {
    user,
    accessToken,
    refreshToken,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user && !!accessToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

