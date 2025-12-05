import React, { useState } from "react";
import Login from "./Login";
import Register from "./Register";

export default function AuthContainer() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="w-full h-screen flex items-center justify-center bg-[#f6f5f7] font-[Poppins]">
      <div className="relative w-[768px] max-w-full min-h-[480px] rounded-xl bg-white shadow-[0_14px_28px_rgba(0,0,0,0.25),0_10px_10px_rgba(0,0,0,0.22)] overflow-hidden">

        {/* PANEL ANIMADO */}
        <div
          className={`
            absolute top-0 h-full w-1/2 text-white flex flex-col justify-center items-center p-10
            transition-all duration-700 ease-in-out
            ${isLogin
              ? "left-1/2 bg-gradient-to-r from-[#ff4b2b] to-[#ff416c]"
              : "left-0 bg-gradient-to-r from-[#be4bdb] to-[#ff416c]"
            }
          `}
        >
          {isLogin ? (
            <>
              <h1 className="text-4xl font-bold mb-2">¡Bienvenido!</h1>
              <p className="mb-6 opacity-90">Inicia sesión con tu cuenta</p>
              <button
                onClick={() => setIsLogin(false)}
                className="px-10 py-3 rounded-full border border-white hover:bg-white hover:text-[#ff416c] transition"
              >
                Registrar
              </button>
            </>
          ) : (
            <>
              <h1 className="text-4xl font-bold mb-2">Hola!!!</h1>
              <p className="mb-6 opacity-90">Crea tu cuenta</p>
              <button
                onClick={() => setIsLogin(true)}
                className="px-10 py-3 rounded-full border border-white hover:bg-white hover:text-[#be4bdb] transition"
              >
                Iniciar Sesión
              </button>
            </>
          )}
        </div>

        {/* FORMULARIOS */}
        <div
          className={`
            absolute top-0 h-full w-1/2 flex items-center justify-center p-10
            transition-all duration-700 ease-in-out
            ${isLogin ? "left-0" : "left-1/2"}
          `}
        >
          {isLogin ? <Login /> : <Register />}
        </div>
      </div>
    </div>
  );
}
