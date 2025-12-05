import { useEffect, useState } from "react";
import Header from "../components/header";
import Footer from "../components/footer";
import ProductoCard from "../components/ProductoCard";
import { useFavoritosStore } from "../storage/favoritos_storage";
import { useAuth } from "../context/AuthContext";

export default function Favoritos() {
  const { favoritos } = useFavoritosStore();
  const [productosFavoritos, setProductosFavoritos] = useState([]);

  useEffect(() => {
    const cargarProductosFavoritos = async () => {
      try {
        const productos = await Promise.all(
          favoritos.map(async (fav) => {
            const res = await fetch(`http://localhost:4000/productos/${fav.producto_id}`);
            return res.json();
          })
        );

        setProductosFavoritos(productos);
      } catch (error) {
        console.error("Error cargando productos favoritos:", error);
      }
    };

    if (favoritos.length > 0) cargarProductosFavoritos();
  }, [favoritos]);

  return (
    <div className="min-h-screen">
      <Header />

      <h1 className="text-center text-2xl font-bold mt-10 text-[#ff3c8a]">
        Tus Favoritos
      </h1>

      {/* GRID DE FAVORITOS */}
      <div className="flex flex-wrap justify-center gap-6 mt-10 mb-20">
        {productosFavoritos.length > 0 ? (
          productosFavoritos.map((producto) => (
            <ProductoCard key={producto.id} producto={producto} />
          ))
        ) : (
          <p className="text-gray-500 text-lg mt-20">
            Aún no tienes productos en favoritos 💗
          </p>
        )}
      </div>

      <Footer />
    </div>
  );
}
