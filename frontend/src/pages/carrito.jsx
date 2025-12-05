import { useEffect } from "react";
import { useCarritoStore } from "../storage/carrito_storage";
import Header from "../components/header";
import Footer from "../components/footer";
import { Trash2 } from "lucide-react";

export default function Carrito({ user }) {
  const { carrito, cargarCarrito } = useCarritoStore();

  useEffect(() => {
    if (user?.id) cargarCarrito(user.id);
  }, [user]);

  return (
    <div className="min-h-screen">
      <Header />

      <h1 className="text-center text-2xl font-bold mt-10 text-[#ff3c8a]">
        Tu Carrito
      </h1>

      <div className="max-w-4xl mx-auto mt-12 mb-28 px-4">
        {carrito.length > 0 ? (
          <div className="space-y-6">
            {carrito.map((item) => (
              <div
                key={item.producto.id}
                className="flex items-center gap-6 bg-white border border-gray-200 rounded-2xl p-4 shadow-sm"
              >
                {/* IMAGEN */}
                <img
                  src={
                    item.producto.imagen
                      ? `http://localhost:4000/uploads/productos/${item.producto.imagen}`
                      : "/placeholder.png"
                  }
                  alt={item.producto.nombre}
                  className="w-24 h-24 object-contain rounded-xl"
                />

                {/* INFO */}
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {item.producto.nombre}
                  </h3>

                  <p className="text-sm text-gray-600 mt-1">
                    {item.producto.descripcion?.substring(0, 80)}...
                  </p>

                  <p className="text-[#ff3c8a] font-bold text-xl mt-2">
                    ${item.producto.precio_unidad}
                  </p>

                  <p className="text-gray-600 text-sm mt-1">
                    Cantidad: {item.cantidad}
                  </p>
                </div>

                {/* ELIMINAR */}
                <button
                  onClick={() => eliminarProducto(item.producto.id)}
                  className="p-2 rounded-full hover:bg-gray-100 transition"
                >
                  <Trash2 size={22} className="text-red-500" />
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center text-gray-500 text-lg mt-20">
            Tu carrito está vacío 🛒
          </p>
        )}

        {/* BOTÓN VACÍAR CARRITO */}
        {carrito.length > 0 && (
          <div className="flex justify-center mt-12">
            <button
              onClick={vaciarCarrito}
              className="px-10 py-3 rounded-full font-semibold text-white shadow"
              style={{ backgroundColor: "#ff3c8a" }}
            >
              Vaciar carrito
            </button>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
