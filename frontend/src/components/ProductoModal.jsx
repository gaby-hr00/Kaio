import { X } from "lucide-react";
import { useCarritoStore } from "../storage/carrito_storage";

export default function ProductoModal({ producto, onClose }) {
  const { agregarProducto } = useCarritoStore();
  const { user } = useAuth(); // ✅ obtener usuario

  const handleAgregar = () => {
    if (!user) return alert("Debes iniciar sesión");
    agregarProducto(user.id, producto); // pasar user.id al store
    onClose();
  };

  return (
    // OVERLAY que cierra al hacer click
    <div
      className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50"
      onClick={onClose}
    >
      {/* MODAL — evita que el click dentro cierre */}
      <div
        className="bg-white rounded-3xl shadow-lg w-[850px] p-6 relative flex gap-6"
        onClick={(e) => e.stopPropagation()}
      >
        {/* BOTÓN DE CERRAR */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-full transition"
        >
          <X size={24} />
        </button>

        {/* IMAGEN IZQUIERDA */}
        <div className="w-1/2 flex items-center justify-center">
          <img
            src={
              producto.imagen
                ? `http://localhost:4000/uploads/productos/${producto.imagen}`
                : "/placeholder.png"
            }
            alt={producto.nombre}
            className="w-full max-h-[420px] object-contain rounded-xl"
          />
        </div>

        {/* INFO DERECHA */}
        <div className="w-1/2 flex flex-col justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{producto.nombre}</h2>

            <p className="text-gray-600 mt-3 leading-relaxed">
              {producto.descripcion}
            </p>

            <p className="text-[28px] font-bold text-[#ff3c8a] mt-6">
              ${producto.precio_unidad}
            </p>
          </div>

          {/* BOTÓN AGREGAR AL CARRITO */}
          <button
            onClick={handleAgregar}
            className="mt-8 w-full py-3 rounded-full font-semibold text-white"
            style={{ backgroundColor: "#ff3c8a" }}
          >
            Agregar al carrito
          </button>

        </div>
      </div>
    </div>
  );
}
