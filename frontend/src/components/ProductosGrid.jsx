import React, { useEffect, useState } from "react";
import Card from "./ProductoCard.jsx";

export default function ProductosGrid() {
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
    <div className="flex flex-wrap justify-center gap-6 mt-6 mb-20">
      {productos.length > 0 ? (
        productos.map((producto) => (
          <Card key={producto.id} producto={producto} />
        ))
      ) : (
        <p className="text-gray-500">Cargando productos...</p>
      )}
    </div>
  );
}
