const API_URL = "http://localhost:4000/carritos";

export const carritoApi = {
  agregar: async (usuario_id, producto_id, cantidad = 1) => {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario_id, producto_id, cantidad }),
    });
    return await res.json();
  },

  listar: async (usuario_id) => {
    // ✅ usar ruta correcta según backend
    const res = await fetch(`${API_URL}/${usuario_id}`);
    return await res.json();
  },

  actualizar: async (item_id, cantidad) => {
    const res = await fetch(`${API_URL}/${item_id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cantidad }),
    });
    return await res.json();
  },

  vaciar: async (usuario_id) => {
    await fetch(`${API_URL}/vaciar/${usuario_id}`, {
      method: "DELETE",
    });
  },
};
