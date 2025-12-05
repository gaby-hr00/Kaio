import React from "react";

export default function Overlay({ handleSignIn, handleSignUp }) {
  return (
    <div className="overlay-container">
      <div className="overlay">
        {/* PANEL IZQUIERDO */}
        <div className="overlay-panel overlay-left">
          <h1>¡Bienvenido!</h1>
          <p>Inicia sesión con tu cuenta</p>

          <button className="ghost" onClick={handleSignIn}>
            Inicia sesión
          </button>
        </div>

        {/* PANEL DERECHO */}
        <div className="overlay-panel overlay-right">
          <h1>Hola!!!</h1>
          <p>Crear tu cuenta</p>

          <button className="ghost" onClick={handleSignUp}>
            Registrar
          </button>
        </div>
      </div>
    </div>
  );
}
