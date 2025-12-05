import React, { useState } from "react";
import { motion } from "framer-motion";
import PasswordInput from "../components/PasswordInput";
import { useNavigate, Link } from "react-router-dom";

const API = import.meta.env.VITE_API_URL || "http://localhost:4000";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    nombre_completo: "",
    correo: "",
    fecha_nacimiento: "",
    tipo_identificacion: "",
    identificacion: "",
    contrasena: "",
    confirm_contrasena: "",
    celular: "",
    direccion: "",
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [note, setNote] = useState(null);

  const handleChange = (e) => {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
    setErrors((prev) => ({ ...prev, [e.target.name]: null }));
    setNote(null);
  };

  const validate = () => {
    const err = {};
    if (!form.correo) err.correo = "Correo obligatorio";
    else if (!/^\S+@\S+\.\S+$/.test(form.correo)) err.correo = "Correo inválido";
    if (!form.nombre_completo) err.nombre_completo = "Nombre obligatorio";
    if (!form.identificacion) err.identificacion = "Identificación obligatoria";
    if (!form.contrasena || form.contrasena.length < 6) err.contrasena = "Mínimo 6 caracteres";
    if (form.contrasena !== form.confirm_contrasena) err.confirm_contrasena = "Las contraseñas no coinciden";
    if (!form.celular) err.celular = "Celular obligatorio";
    if (!form.direccion) err.direccion = "Dirección obligatoria";
    return err;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const v = validate();
    if (Object.keys(v).length > 0) {
      setErrors(v);
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            nombre_completo: form.nombre_completo,
            correo: form.correo,
            contrasena: form.contrasena,
            fecha_nacimiento: form.fecha_nacimiento || null,
            tipo_identificacion: form.tipo_identificacion || null,
            identificacion: form.identificacion || null,
            celular: form.celular || null
            }),

      });
      const data = await res.json();
      if (!res.ok) {
        setNote({ type: "error", text: data.detail || "Error al registrar" });
      } else {
        setNote({ type: "success", text: "Registro exitoso." });
        setTimeout(() => navigate("/login"), 1000);
      }
    } catch (err) {
      setNote({ type: "error", text: "No hay conexión con el servidor." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
        className="w-full max-w-lg bg-white rounded-2xl shadow-lg p-8"
      >
        <h2 className="text-2xl font-bold mb-4">Crear cuenta</h2>

        {note && (
          <div
            className={`mb-4 p-3 rounded ${
              note.type === "error" ? "bg-red-100 text-red-700" : "bg-green-100 text-green-700"
            }`}
          >
            {note.text}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="text-sm font-medium">*Correo</label>
            <input
              name="correo"
              type="email"
              value={form.correo}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded mt-1 bg-gray-200"
            />
            {errors.correo && <p className="text-xs text-red-600 mt-1">{errors.correo}</p>}
          </div>

          <div>
            <label className="text-sm font-medium">*Nombre completo</label>
            <input
              name="nombre_completo"
              value={form.nombre_completo}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded mt-1 bg-gray-200"
            />
            {errors.nombre_completo && <p className="text-xs text-red-600 mt-1 bg-gray-200">{errors.nombre_completo}</p>}
          </div>

          
            <div>
              <label className="text-sm font-medium">*Tipo documento</label>
              <select name="tipo_identificacion" value={form.tipo_identificacion} onChange={handleChange} className="w-full border px-3 py-2 rounded mt-1 bg-gray-200">
                <option value="">Seleccione</option>
                <option value="CC">Cédula</option>
                <option value="CE">Cédula extranjera</option>
                <option value="TI">Tarjeta identidad</option>
                <option value="PP">Pasaporte</option>
                <option value="NIT">NIT</option>
                <option value="RUT">RUT</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">*Identificación</label>
              <input name="identificacion" value={form.identificacion} onChange={handleChange} className="w-full border px-3 py-2 rounded mt-1 bg-gray-200" />
              {errors.identificacion && <p className="text-xs text-red-600 mt-1">{errors.identificacion}</p>}
            </div>
          

          <div>
            <label className="text-sm font-medium">*Fecha de nacimiento</label>
            <input name="fecha_nacimiento" type="date" value={form.fecha_nacimiento} onChange={handleChange} className="w-full border px-3 py-2 rounded mt-1 bg-gray-200" />
          </div>

          <div>
            <label className="text-sm font-medium">*Contraseña</label>
            <PasswordInput name="contrasena" value={form.contrasena} onChange={(e) => setForm((s) => ({ ...s, contrasena: e.target.value }))} placeholder="Mínimo 6 caracteres" />
            {errors.contrasena && <p className="text-xs text-red-600 mt-1">{errors.contrasena}</p>}
          </div>

          <div>
            <label className="text-sm font-medium">*Confirmar contraseña</label>
            <PasswordInput name="confirm_contrasena" value={form.confirm_contrasena} onChange={(e) => setForm((s) => ({ ...s, confirm_contrasena: e.target.value }))} placeholder="Repite la contraseña" />
            {errors.confirm_contrasena && <p className="text-xs text-red-600 mt-1">{errors.confirm_contrasena}</p>}
          </div>

          <div>
            <label className="text-sm font-medium">*Celular</label>
            <input name="celular" value={form.celular} onChange={handleChange} className="w-full border px-3 py-2 rounded mt-1" />
            {errors.celular && <p className="text-xs text-red-600 mt-1">{errors.celular}</p>}
          </div>

          <div>
            <label className="text-sm font-medium">*Dirección</label>
            <input name="direccion" value={form.direccion} onChange={handleChange} className="w-full border px-3 py-2 rounded mt-1" />
            {errors.direccion && <p className="text-xs text-red-600 mt-1">{errors.direccion}</p>}
          </div>

          <button
            disabled={loading}
            className={`w-full py-2 rounded-lg text-white font-semibold mt-2 ${
              loading ? "bg-pink-300 cursor-not-allowed" : "bg-pink-600 hover:bg-pink-700"
            }`}
          >
            {loading ? "Registrando..." : "Crear cuenta"}
          </button>

          <p className="text-center text-sm text-gray-600 mt-2">
            ¿Ya tienes cuenta? <Link to="/login" className="text-pink-600 font-medium">Inicia sesión</Link>
          </p>
        </form>
      </motion.div>
    </div>
  );
}
