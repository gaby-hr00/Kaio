import { createContext, useContext, useEffect, useState } from "react";
import { useFavoritosStore } from "../storage/favoritos_storage";
import { useCarritoStore } from "../storage/carrito_storage";

const AuthContext = createContext();
const API = import.meta.env.VITE_API_URL || "http://localhost:4000";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [loading, setLoading] = useState(true);

  // Stores
  const cargarFavoritos = useFavoritosStore((state) => state.cargarFavoritos);
  const limpiarFavoritos = useFavoritosStore((state) => state.limpiarFavoritos);
  const cargarCarrito = useCarritoStore((state) => state.cargarCarrito);
  const vaciarCarrito = useCarritoStore((state) => state.vaciarCarrito);

  // Cargar usuario si hay token
  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    fetch(`${API}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => {
        if (!r.ok) throw new Error("Token inválido");
        return r.json();
      })
      .then((data) => {
        setUser(data);
        cargarFavoritos(data.id, token);
        cargarCarrito(data.id);
      })
      .catch(() => {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, [token]);

  // LOGIN
  const login = async ({ correo, contrasena }) => {
    try {
      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, contrasena }),
      });

      const data = await res.json();

      if (!res.ok || !data.access_token) {
        return { ok: false, error: data.detail || "Credenciales inválidas" };
      }

      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);

      // Obtener usuario logueado
      const meRes = await fetch(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });

      const meData = await meRes.json();

      if (meRes.ok) {
        setUser(meData);
        cargarFavoritos(meData.id, data.access_token);
        cargarCarrito(meData.id);
      }

      return { ok: true, token: data.access_token, user: meData };
    } catch (err) {
      return { ok: false, error: "Error de conexión con el servidor." };
    }
  };

  // LOGOUT
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    limpiarFavoritos();
    vaciarCarrito();
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
