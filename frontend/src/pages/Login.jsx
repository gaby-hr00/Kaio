import React, { useState } from "react";
import { motion } from "framer-motion";
import PasswordInput from "../components/PasswordInput";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Home from "./Home.jsx";

const API = import.meta.env.VITE_API_URL || "http://localhost:4000";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ correo: "", contrasena: "" });
  const [loading, setLoading] = useState(false);
  const [note, setNote] = useState(null);

  const handleChange = (e) => {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
    setNote(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.correo || !form.contrasena) {
      setNote({ type: "error", text: "Completa correo y contraseña." });
      return;
    }

    setLoading(true);

    // ---- LLAMADA AL CONTEXTO DE AUTENTICACIÓN ----
    const result = await login({ correo: form.correo, contrasena: form.contrasena });

    setLoading(false);

    // ---- ERROR ----
    if (!result.ok) {
      setNote({ type: "error", text: result.error || "Credenciales inválidas" });
      return;
    }

    // ---- LOGIN EXITOSO ----
    setNote({ type: "success", text: "Inicio de sesión exitoso." });

    // 👉 GUARDAR TOKEN EN LOCAL STORAGE
    if (result.token) {
      localStorage.setItem("token", result.token);
    }

    // 👉 REDIRECCIONAR
    setTimeout(() => navigate("/Home"), 600);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-md bg-white rounded-2xl shadow-lg p-8"
      >
        <h2 className="text-2xl font-bold mb-4">Iniciar sesión</h2>

        {note && (
          <div
            className={`mb-3 p-3 rounded ${
              note.type === "error"
                ? "bg-red-100 text-red-700"
                : "bg-green-100 text-green-700"
            }`}
          >
            {note.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="text-sm font-medium">Correo</label>
            <input
              name="correo"
              type="email"
              value={form.correo}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded mt-1"
            />
          </div>

          <div>
            <label className="text-sm font-medium">Contraseña</label>
            <PasswordInput
              name="contrasena"
              value={form.contrasena}
              onChange={(e) =>
                setForm((s) => ({ ...s, contrasena: e.target.value }))
              }
              placeholder="Tu contraseña"
            />
          </div>

          <button
            disabled={loading}
            className={`w-full py-2 rounded-lg text-white font-semibold mt-2 ${
              loading ? "bg-pink-300" : "bg-pink-600 hover:bg-pink-700"
            }`}
          >
            {loading ? "Ingresando..." : "Entrar"}
          </button>

          <p className="text-center text-sm text-gray-600 mt-2">
            ¿No tienes cuenta?{" "}
            <Link to="/register" className="text-pink-600 font-medium">
              Crear cuenta
            </Link>
          </p>
        </form>
      </motion.div>
    </div>
  );
}
