"use client";
import React, { useEffect, useState, useContext } from "react";
import { listMyImages, ImageResponse } from "@/app/services/imageService";
// import { SignedImage } from "./SignedImage"; Esto ya no hace falta porque ahora usamos el contexto de imágenes, donde ya obtenemos las URLs firmadas de la lista de imágenes. Ahora sólo las pintamos
import { useImageContext } from "@/context/ImageContext";
import { img } from "framer-motion/client";

export const ImageList: React.FC = () => {
  const { images, deleteImage } = useImageContext();
  const [loading, setLoading] = useState<string | null>(null);


  if (images.length === 0) return <p>No tienes imágenes</p>;

  return (
    <div className="grid grid-cols-3 gap-4">
      {images.map((img) => (
        <div key={img.id} className="border p-2 rounded">
          {/* <SignedImage imageId={img.id} alt={`Imagen ${img.id}`} /> */}
          {img.signedUrl ? (
            <img src={img.signedUrl} 
            alt={`Imagen ${img.file_name}`}
            className="rounded shadow" />
          ) : (
            <div className="bg-gray-100 h-32 w-full animate-pulse rounded"></div>
          )}
           <button
            onClick={() => {
              if (confirm("¿Seguro que quieres eliminar esta imagen?")) {
                setLoading(img.id);
                deleteImage(img.id);
                setLoading(null);
              }
            }}
            className="mt-2 px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700"
          >
            Eliminar
          </button>
          {loading === img.id && <p>Eliminando...</p>}
        </div>
      ))}
    </div>
  );
};
