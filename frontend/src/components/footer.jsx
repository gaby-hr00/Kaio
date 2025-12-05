import { Twitter, Instagram, Facebook } from 'lucide-react';

export default function Footer() {
    return (
        <div className="bg-[#fbd8de] w-full h-60 ">
            <div className='flex items-center justify-center gap-60'>
                <div className="flex flex-col font-general text-1xl text-center gap-y-4">
                    <p className=''>
                        ¡Siguenos en nuestras redes!
                    </p>
                    <div className="flex gap-5 justify-center">
                        <Twitter size={40} />
                        <Instagram size={40} />
                        <Facebook size={40} />
                    </div>
                    <p>
                        kaio@gmail.com
                    </p>
                </div>

                <div className="flex flex-col text-center gap-y-4">
                    <h3 className="font-bold">
                        SOBRE KAIŌ
                    </h3>
                    <p className="text-1xlm">
                        ¿Quienes somos?<br /> ¿Cómo comprar?<br /> Preguntas frecuentes<br /> Contáctanos
                    </p>
                </div>
            </div>
            <div className="border-t-2 border-black flex items-center justify-center gap-60 pt-3 text-1xl font-bold">
                <p>© 2025 KAIŌ</p>
                <a href="/pdf/TerminosyCondiciones.pdf" target="_blank" rel="noopener noreferrer" className="cursor-pointer hover:underline">Términos y condiciones</a>
            </div>
        </div>
    );
}