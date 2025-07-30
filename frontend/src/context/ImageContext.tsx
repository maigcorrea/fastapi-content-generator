"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { listMyImages, ImageResponse, getSignedImageUrl } from "@/app/services/imageService";
import { AuthContext } from "./AuthContext";

interface ImageWithSignedUrl extends ImageResponse {
  signedUrl?: string; // URL firmada generada
}

// Definimos el tipo del contexto de imágenes
// Este contexto manejará las imágenes y sus URLs firmadas
// También incluirá una función para agregar imágenes al estado
// y una función para refrescar la lista de imágenes
// Esto permite que los componentes que usan este contexto puedan acceder a las imágenes y actualizarlas
// sin necesidad de pasar props manualmente entre componentes
// Esto es útil para mantener el estado de las imágenes en un lugar centralizado
// y evitar la necesidad de recargar la página para ver nuevas imágenes subidas
// Además, permite que los componentes que muestran imágenes puedan reaccionar a cambios en el estado de las imágenes
// y actualizarse automáticamente cuando se agregan nuevas imágenes
// Esto mejora la experiencia del usuario al hacer que la aplicación sea más dinámica y reactiva
// También permite que los componentes que muestran imágenes puedan acceder a las URLs firmadas
// sin necesidad de hacer llamadas adicionales al servidor para obtenerlas
// Esto reduce la carga en el servidor y mejora el rendimiento de la aplicación


//FLUJO:
// 1. Se obtiene la lista de imágenes del usuario al cargar el componente (refreshImages)
// 2. Se obtienen las URLs firmadas para cada imagen (refreshImages con fetchSignedUrls)
// 3. Se almacenan las imágenes con sus URLs firmadas en el estado del contexton(refreshImages)
// 4. Cuando se sube una nueva imagen, se obtiene su URL firmada y
//    se agrega al estado del contexto (addImage)
// 5. Los componentes que usan este contexto se actualizan automáticamente
//    cuando se agregan nuevas imágenes o se refresca la lista
// 6. Los componentes que muestran imágenes pueden acceder a las URLs firmadas
//    sin necesidad de hacer llamadas adicionales al servidor

interface ImageContextType {
  images: ImageWithSignedUrl[];
  addImage: (image: ImageResponse) => void;
  refreshImages: () => void;
}

const ImageContext = createContext<ImageContextType | null>(null);

export const ImageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token } = useContext(AuthContext);
  const [images, setImages] = useState<ImageWithSignedUrl[]>([]);

  const fetchSignedUrls = async (images: ImageResponse[]): Promise<ImageWithSignedUrl[]> => {
    return Promise.all(
      images.map(async (img) => {
        const url = await getSignedImageUrl(img.id, token);
        return { ...img, signedUrl: url };
      })
    );
  };

  // Carga inicial de imágenes con URLs firmadas
  const refreshImages = async () => {
    try {
      const imgs = await listMyImages(token); // Cargamos las imágenes del usuario (Esto antes lo hacíamos en ImageList)
      const imgsWithUrls = await fetchSignedUrls(imgs); // Obtenemos las URLs firmadas para cada imagen
      setImages(imgsWithUrls); // Actualizamos el estado con las imágenes y sus URLs firmadas
    } catch (error) {
      console.error("Error cargando imágenes", error);
    }
  };

  // Ahora agregar imagen subida (instantáneo) y obtener su url firmada (El proceso anterior)-> Nuevo
  const addImage = async (image: ImageResponse) => {
    const signedUrl = await getSignedImageUrl(image.id, token); // Obtenemos la URL firmada para la nueva imagen
    setImages((prev) => [{...image, signedUrl}, ...prev]); // Agregamos la nueva imagen al estado con su URL firmada
  };

  useEffect(() => {
    refreshImages();
  }, []);

  return (
    <ImageContext.Provider value={{ images, addImage, refreshImages }}>
      {children}
    </ImageContext.Provider>
  );
};

export const useImageContext = () => {
  const ctx = useContext(ImageContext);
  if (!ctx) throw new Error("useImageContext debe estar dentro de ImageProvider");
  return ctx;
};
