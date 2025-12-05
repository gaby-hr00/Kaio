import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import Header from "../components/header";
import Footer from "../components/footer";
import ProductosGrid from "../components/ProductosGrid";

export default function Home() {
  const { user, logout } = useAuth();

  const [productos, setProductos] = useState([]);

  useEffect(() => {
    const cargarProductos = async () => {
      try {
        const res = await fetch("http://localhost:4000/productos");
        const data = await res.json();
        setProductos(data);
      } catch (error) {
        console.error("Error cargando productos:", error);
      }
    };

    cargarProductos();
  }, []);

  return (
    <div>
      <Header />

       <h1 className="text-2xl font-semibold mt-6 px-4">
        Bienvenido {user?.nombre_completo}
      </h1>

      <button
        className="bg-red-500 text-white px-4 py-2 rounded mx-4 mt-4"
        onClick={logout}
      >
        Cerrar sesión
      </button> 

      {/* Pasamos los productos */}
      <ProductosGrid productos={productos} />

      
      <Footer />
      
    </div>
  );
}
