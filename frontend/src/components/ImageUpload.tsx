"use client";
import React, { useState, useContext } from "react";
import { uploadImage } from "@/app/services/imageService";
import { AuthContext } from "@/context/AuthContext";
import { useImageContext } from "@/context/ImageContext";

export const ImageUpload: React.FC = () =>  {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const { token } = useContext(AuthContext);
  const { addImage } = useImageContext();

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const image = await uploadImage(file, token);
      // Después de subir, limpiamos el campo de subida
      setFile(null);
      // Y actualizamos el contexto de imágenes para reflejar la nueva imagen
      addImage(image); // Añade la imagen y obtiene su url firmada

    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded">
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button
        className="ml-2 px-3 py-1 bg-blue-600 text-white rounded"
        disabled={!file || loading}
        onClick={handleUpload}
      >
        {loading ? "Subiendo..." : "Subir imagen"}
      </button>
    </div>
  );
};
