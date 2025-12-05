import { useNavigate } from "react-router-dom";
import Search from "../components/search";
import { Heart, UserRound, ShoppingCart, HouseHeart } from "lucide-react";

export default function Header() {
  const navigate = useNavigate();

  return (
    <header className="bg-[#fbd8de] p-4 flex items-center gap-6 w-full">
      {/* LOGO */}
      <img
        src="/LOGO.png"
        alt="Logo"
        className="h-15 w-auto cursor-pointer"
        onClick={() => navigate("/")}
      />

      {/* SEARCH CENTRADO */}
      <div className="flex-1 flex justify-center">
        <div className="w-full max-w-4xl">
          <Search />
        </div>
      </div>

      {/* ICONOS A LA DERECHA */}
      <div className="flex items-center gap-6 pr-4">
        {/* ❤️ Home */}
        <button
          className="cursor-pointer hover:text-[#b61d32] transition-colors"
          onClick={() => navigate("/home")}
        >
          <HouseHeart className="w-6 h-6" />
        </button>

        {/* ❤️ FAVORITOS */}
        <button
          className="cursor-pointer hover:text-[#b61d32] transition-colors"
          onClick={() => navigate("/favoritos")}
        >
          <Heart className="w-6 h-6" />
        </button>

        {/* 👤 PERFIL (puedes cambiar ruta luego) */}
        <button
          className="cursor-pointer hover:text-[#b61d32] transition-colors"
          onClick={() => navigate("/perfil")}
        >
          <UserRound className="w-6 h-6" />
        </button>

        {/* 🛒 CARRITO */}
        <button
          className="cursor-pointer hover:text-[#b61d32] transition-colors"
          onClick={() => navigate("/carrito")}
        >
          <ShoppingCart className="w-6 h-6" />
        </button>
      </div>
    </header>
  );
}
