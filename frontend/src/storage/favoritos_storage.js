import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useFavoritosStore = create(
  persist(
    (set, get) => ({
      favoritos: [],

      /** Cargar favoritos del backend según el usuario */
      cargarFavoritos: async (usuario_id, token) => {
        try {
          const res = await fetch(`http://localhost:4000/favoritos?user=${usuario_id}`, {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (!res.ok) return;

          const data = await res.json();
          set({ favoritos: data });
        } catch (error) {
          console.log("Error cargando favoritos:", error);
        }
      },

      /** Alternar favorito en backend + sincronizar store */
      toggleFavorito: async (producto_id, usuario_id, token) => {
        if (!usuario_id) return;

        try {
          const res = await fetch("http://localhost:4000/favoritos/toggle", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              producto_id,
              usuario_id,
            }),
          });

          const data = await res.json();

          if (data.isFavorite) {
            // Se añadió → agregar al store
            set({
              favoritos: [
                ...get().favoritos,
                { usuario_id, producto_id }
              ]
            });
          } else {
            // Se eliminó → quitar del store
            set({
              favoritos: get().favoritos.filter(
                (f) => f.producto_id !== producto_id
              ),
            });
          }
        } catch (err) {
          console.log("Error en toggle favorito:", err);
        }
      },

      
      limpiarFavoritos: () => set({ favoritos: [] }),
    }),

    {
      name: "favoritos-storage",
      partialize: (state) => ({ favoritos: state.favoritos }),
    }
  )
);
