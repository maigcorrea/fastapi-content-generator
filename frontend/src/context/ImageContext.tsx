"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { listMyImages, ImageResponse } from "@/app/services/imageService";
import { AuthContext } from "./AuthContext";

interface ImageContextType {
  images: ImageResponse[];
  addImage: (image: ImageResponse) => void;
  refreshImages: () => void;
}

const ImageContext = createContext<ImageContextType | null>(null);

export const ImageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    //Lo que haciamos anteriormente en ImageList para cargar las imágenes
  const [images, setImages] = useState<ImageResponse[]>([]); // Estado para almacenar las imágenes
  const { token } = useContext(AuthContext);

  // Carga inicial de imágenes (Hasta aquí era lo que hacíamos en ImageList)
  const refreshImages = async () => {
    try {
      const imgs = await listMyImages(token);
      setImages(imgs);
    } catch (error) {
      console.error("Error cargando imágenes", error);
    }
  };

  // Ahora agregar imagen subida (instantáneo) -> Nuevo
  const addImage = (image: ImageResponse) => {
    setImages((prev) => [image, ...prev]);
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
