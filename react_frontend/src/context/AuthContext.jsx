import { createContext, useContext, useEffect, useState } from "react";
import { fetchMe, loginUser, registerUser } from "../api/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("wm_token");
    if (!token) {
      setLoading(false);
      return;
    }

    fetchMe()
      .then((me) => setUser(me))
      .catch(() => {
        localStorage.removeItem("wm_token");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const applyAuth = (payload) => {
    localStorage.setItem("wm_token", payload.access_token);
    setUser(payload.user);
  };

  const login = async (username, password) => {
    const payload = await loginUser(username, password);
    applyAuth(payload);
    return payload.user;
  };

  const register = async (username, password) => {
    const payload = await registerUser(username, password);
    applyAuth(payload);
    return payload.user;
  };

  const logout = () => {
    localStorage.removeItem("wm_token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return value;
}
