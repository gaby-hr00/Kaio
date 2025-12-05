import { create } from "zustand";
import { carritoApi } from "../api/carritoApi";

export const useCarritoStore = create((set) => ({
  carrito: [],

  cargarCarrito: async (usuarioId) => {
    if (!usuarioId) return;
    const carritoDB = await carritoApi.listar(usuarioId);
    set({ carrito: carritoDB });
  },

  agregarProducto: async (usuarioId, producto) => {
    if (!usuarioId) return alert("Debes iniciar sesión para agregar productos");
    const response = await carritoApi.agregar(usuarioId, producto.id, 1);

    set((state) => {
      const existe = state.carrito.find(item => item.producto.id === producto.id);
      if (existe) {
        return { carrito: state.carrito.map(item => item.producto.id === producto.id ? { ...item, cantidad: response.cantidad } : item) };
      } else {
        return { carrito: [...state.carrito, response] };
      }
    });
  },

  vaciarCarrito: async (usuarioId) => {
    if (!usuarioId) return;
    await carritoApi.vaciar(usuarioId);
    set({ carrito: [] });
  }
}));
