import { Heart } from "lucide-react";
import { useFavoritosStore } from "../storage/favoritos_storage";
import { useAuth } from "../context/AuthContext";
import { useState } from "react";
import ProductoModal from "./ProductoModal";

export default function ProductoCard({ producto }) {
  const { user, token } = useAuth();
  const { favoritos, toggleFavorito } = useFavoritosStore();

  const [showModal, setShowModal] = useState(false);

  const esFavorito = favoritos.some(
    (fav) => fav.producto_id === producto.id
  );

  const handleFavorito = (e) => {
    e.stopPropagation(); // ⬅️ evita que al hacer click abra el modal
    if (!user) {
      alert("Debes iniciar sesión para usar favoritos");
      return;
    }
    toggleFavorito(producto.id, user.id, token);
  };

  return (
    <>
      {/* CARD */}
      <div
        className="w-[290px] bg-white rounded-3xl shadow-sm border border-gray-200 relative pb-6 cursor-pointer"
        onClick={() => setShowModal(true)}
      >
        {/* CORAZÓN */}
        <button onClick={handleFavorito} className="absolute top-3 right-3">
          <Heart
            size={24}
            strokeWidth={1.5}
            color="#ff3c8a"
            fill={esFavorito ? "#ff3c8a" : "none"}
          />
        </button>

        {/* IMAGEN */}
        <div className="flex justify-center pt-10 pb-4">
          <img
            src={
              producto.imagen
                ? `http://localhost:4000/uploads/productos/${producto.imagen}`
                : "/placeholder.png"
            }
            alt={producto.nombre}
            className="h-[190px] object-contain"
          />
        </div>

        {/* NOMBRE */}
        <h3 className="text-center font-semibold text-[16px] text-gray-900 px-4 leading-tight">
          {producto.nombre}
        </h3>

        {/* PRECIO */}
        <p className="text-center font-bold text-[22px] mt-2 text-[#ff3c8a]">
          ${producto.precio_unidad}
        </p>

        {/* BOTÓN */}
        <div className="flex justify-center mt-5">
          <button
            className="px-6 py-2 text-[15px] rounded-full border-[2px] font-medium transition hover:text-white"
            style={{
              borderColor: "#ff3c8a",
              color: "#ff3c8a",
            }}
            onMouseEnter={(e) => (e.target.style.backgroundColor = "#ff3c8a")}
            onMouseLeave={(e) => (e.target.style.backgroundColor = "transparent")}
          >
            Agregar al carrito
          </button>
        </div>
      </div>

      {/* MODAL */}
      {showModal && (
        <ProductoModal producto={producto} onClose={() => setShowModal(false)} />
      )}
    </>
  );
}
