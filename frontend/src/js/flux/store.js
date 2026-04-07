import { useEffect, useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;



export function useStoreState() {
  const [session, setSession] = useState(getStoredSession);
  
function getStoredSession() {
  return {
    token: localStorage.getItem("token") || "",
    role: localStorage.getItem("role") || "",
    username: localStorage.getItem("username") || "",
  };
}

  useEffect(() => {
    if (session.token) {
      localStorage.setItem("token", session.token);
    } else {
      localStorage.removeItem("token");
    }

    if (session.role) {
      localStorage.setItem("role", session.role);
    } else {
      localStorage.removeItem("role");
    }

    if (session.username) {
      localStorage.setItem("username", session.username);
    } else {
      localStorage.removeItem("username");
    }
  }, [session]);

  const store = {
    data: {
      isAuthenticated: Boolean(session.token),
      session,
    },
    actions: {
      login: async function login(role, credentials) {
        const response = await fetch(`${API_URL}/${role}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(credentials),
        });

        const data = await response.json();

        if (!response.ok) {
          return { ok: false, message: data.msg || "Login failed." };
        }

        setSession({
          token: data.access_token,
          role,
          username: credentials.username,
        });

        return { ok: true, data };
      },
      register: async function register(role, payload) {
        const endpoint =
          role === "teacher" ? `${API_URL}/teachers` : `${API_URL}/students`;

        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
          return { ok: false, message: data.msg || "Registration failed." };
        }

        return { ok: true, data };
      },
      logout: function logout() {
        setSession({ token: "", role: "", username: "" });
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        localStorage.removeItem("username");
      },
    },
  };

  return store;
}
