'use client';
import { useState, useEffect } from 'react';
import Navbar from "@/components/NavBar";
import Image from "next/image";
import { motion } from 'framer-motion';
import { Sparkles, Hash, Image as ImageIcon, Share2, Zap, ArrowRight } from 'lucide-react';

export default function Home() {
  const [isVisible, setIsVisible] = useState(false);
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    setIsVisible(true);
    
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const platforms = [
    { name: 'Instagram', icon: '📸' },
    { name: 'TikTok', icon: '🎵' },
    { name: 'X (Twitter)', icon: '𝕏' },
    { name: 'YouTube', icon: '▶️' },
    { name: 'LinkedIn', icon: '💼' },
    { name: 'Pinterest', icon: '📌' },
  ];

  const features = [
    {
      icon: <Zap className="w-8 h-8 text-yellow-400" />,
      title: "Alcance Máximo",
      description: "Aumenta la visibilidad de tus publicaciones con hashtags optimizados para cada plataforma."
    },
    {
      icon: <ImageIcon className="w-8 h-8 text-purple-400" />,
      title: "Análisis Inteligente",
      description: "Nuestra IA analiza el contenido de tus imágenes para sugerir los hashtags más relevantes."
    },
    {
      icon: <Share2 className="w-8 h-8 text-violet-400" />,
      title: "Multiplataforma",
      description: "Optimiza tus publicaciones para cualquier red social con un solo clic."
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-purple-900 to-black text-white">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden opacity-30">
        {[...Array(20)].map((_, i) => (
          <div 
            key={i}
            className="absolute rounded-full bg-purple-500"
            style={{
              width: Math.random() * 10 + 5 + 'px',
              height: Math.random() * 10 + 5 + 'px',
              left: Math.random() * 100 + 'vw',
              top: Math.random() * 100 + 'vh',
              animation: `float ${Math.random() * 5 + 5}s linear infinite`,
              opacity: Math.random() * 0.5 + 0.1
            }}
          />
        ))}
      </div>

      <Navbar />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 pt-20 pb-32">
        <div className="max-w-7xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mb-8"
          >
            <h1 className="text-4xl sm:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-violet-300 to-yellow-300 mb-6">
              Potencia tu Alcance con Hashtags Inteligentes
            </h1>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-10">
              Sube una imagen y deja que nuestra IA genere los hashtags perfectos para maximizar tu visibilidad en cualquier plataforma.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-full font-semibold text-lg hover:from-purple-700 hover:to-violet-700 transition-all transform hover:scale-105 flex items-center gap-2">
                Probar Ahora <ArrowRight className="w-5 h-5" />
              </button>
              <button className="px-8 py-4 bg-transparent border-2 border-purple-500 text-white rounded-full font-semibold text-lg hover:bg-purple-900/30 transition-all">
                Ver Demostración
              </button>
            </div>
          </motion.div>
          
          <motion.div 
            className="mt-20 relative"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 to-transparent rounded-3xl blur-3xl -z-10"></div>
            <div className="bg-gray-900/50 backdrop-blur-sm border border-purple-500/30 rounded-3xl p-8 max-w-4xl mx-auto">
              <div className="flex flex-wrap justify-center gap-4 mb-6">
                {platforms.map((platform, index) => (
                  <div key={index} className="flex items-center gap-2 bg-gray-800/50 px-4 py-2 rounded-full border border-purple-500/20">
                    <span>{platform.icon}</span>
                    <span>{platform.name}</span>
                  </div>
                ))}
              </div>
              <div className="relative">
                <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-yellow-400 rounded-2xl opacity-75 blur"></div>
                <div className="relative bg-gray-900 p-8 rounded-2xl border border-purple-500/30">
                  <div className="flex flex-col items-center justify-center h-64 border-2 border-dashed border-purple-500/30 rounded-xl mb-6">
                    <ImageIcon className="w-12 h-12 text-purple-400 mb-4" />
                    <p className="text-gray-400">Arrastra y suelta tu imagen aquí</p>
                    <p className="text-sm text-gray-500 mt-2">o haz clic para seleccionar</p>
                  </div>
                  <button className="w-full py-3 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg font-semibold hover:from-purple-700 hover:to-violet-700 transition-all">
                    Generar Hashtags
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-purple-900/50 to-black">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl sm:text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-yellow-300">
              Potencia tu Presencia Digital
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Descubre cómo nuestros hashtags inteligentes pueden transformar tu estrategia en redes sociales
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2, duration: 0.6 }}
                className="bg-gray-900/50 backdrop-blur-sm p-8 rounded-2xl border border-purple-500/20 hover:border-purple-500/50 transition-all hover:shadow-lg hover:shadow-purple-500/10"
              >
                <div className="w-16 h-16 bg-purple-900/50 rounded-xl flex items-center justify-center mb-6 mx-auto">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3 text-center">{feature.title}</h3>
                <p className="text-gray-400 text-center">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Hashtags Matter */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-black">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-3xl sm:text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-yellow-300 to-yellow-500">
                ¿Por qué son importantes los hashtags?
              </h2>
              <p className="text-lg text-gray-300 mb-8">
                Los hashtags son la clave para descubrir contenido en las redes sociales. Nuestra tecnología de IA analiza las tendencias actuales y el contenido de tus imágenes para ofrecerte los hashtags más efectivos para cada plataforma.
              </p>
              <ul className="space-y-4">
                {[
                  "Aumentan la visibilidad de tus publicaciones",
                  "Atraen a tu audiencia objetivo",
                  "Mejoran el engagement y las interacciones",
                  "Ayudan a posicionarte como experto en tu nicho"
                ].map((item, index) => (
                  <li key={index} className="flex items-start">
                    <div className="flex-shrink-0 mt-1">
                      <div className="w-6 h-6 rounded-full bg-yellow-400 flex items-center justify-center">
                        <svg className="w-3 h-3 text-black" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    </div>
                    <span className="ml-3 text-gray-300">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="relative"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 to-yellow-400/20 rounded-3xl transform rotate-6 scale-105 -z-10"></div>
              <div className="bg-gray-900/80 backdrop-blur-sm p-8 rounded-3xl border border-purple-500/30">
                <div className="space-y-6">
                  <div className="flex items-center gap-4 p-4 bg-gray-800/50 rounded-xl border border-purple-500/20">
                    <div className="w-12 h-12 rounded-lg bg-purple-900/50 flex items-center justify-center">
                      <ImageIcon className="w-6 h-6 text-purple-400" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-white">Sube tu imagen</h4>
                      <p className="text-sm text-gray-400">Arrastra o selecciona una imagen de tu dispositivo</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 p-4 bg-gray-800/50 rounded-xl border border-purple-500/20">
                    <div className="w-12 h-12 rounded-lg bg-violet-900/50 flex items-center justify-center">
                      <Hash className="w-6 h-6 text-violet-400" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-white">Selecciona la plataforma</h4>
                      <p className="text-sm text-gray-400">Elige la red social para la que necesitas los hashtags</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 p-4 bg-gray-800/50 rounded-xl border border-yellow-500/20">
                    <div className="w-12 h-12 rounded-lg bg-yellow-900/50 flex items-center justify-center">
                      <Sparkles className="w-6 h-6 text-yellow-400" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-white">Obtén hashtags perfectos</h4>
                      <p className="text-sm text-gray-400">Nuestra IA genera los hashtags ideales para tu imagen</p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-black to-purple-900/30">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-yellow-400 rounded-3xl opacity-75 blur"></div>
            <div className="relative bg-gray-900 p-12 rounded-3xl border border-purple-500/30">
              <h2 className="text-3xl sm:text-4xl font-bold mb-6">
                ¿Listo para llevar tu alcance al siguiente nivel?
              </h2>
              <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                Únete a miles de creadores que ya están mejorando su visibilidad con nuestros hashtags generados por IA.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="px-8 py-4 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-full font-semibold text-lg hover:from-purple-700 hover:to-violet-700 transition-all transform hover:scale-105 flex items-center gap-2">
                  Comenzar Ahora <ArrowRight className="w-5 h-5" />
                </button>
                <button className="px-8 py-4 bg-transparent border-2 border-purple-500 text-white rounded-full font-semibold text-lg hover:bg-purple-900/30 transition-all">
                  Ver Demo
                </button>
              </div>
              <div className="mt-8 flex flex-wrap justify-center gap-4">
                {platforms.slice(0, 6).map((platform, index) => (
                  <div key={index} className="flex items-center gap-2 bg-gray-800/50 px-4 py-2 rounded-full border border-purple-500/20">
                    <span>{platform.icon}</span>
                    <span className="text-sm">{platform.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <footer className="py-8 px-4 sm:px-6 lg:px-8 bg-black border-t border-purple-900/50">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <Sparkles className="w-6 h-6 text-yellow-400" />
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-yellow-300">
              HashGen AI
            </span>
          </div>
          <div className="flex gap-6">
            <a href="#" className="text-gray-400 hover:text-white transition-colors">Inicio</a>
            <a href="#features" className="text-gray-400 hover:text-white transition-colors">Características</a>
            <a href="#how-it-works" className="text-gray-400 hover:text-white transition-colors">Cómo Funciona</a>
            <a href="#pricing" className="text-gray-400 hover:text-white transition-colors">Precios</a>
          </div>
          <p className="mt-4 md:mt-0 text-sm text-gray-500">
            © {new Date().getFullYear()} HashGen AI. Todos los derechos reservados.
          </p>
        </div>
      </footer>

      <style jsx global>{`
        @keyframes float {
          0% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
          100% { transform: translateY(0px); }
        }
        
        body {
          overflow-x: hidden;
        }
      `}</style>
    </div>
  );
}
