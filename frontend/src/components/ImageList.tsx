"use client";
import React, { useEffect, useState, useContext } from "react";
import { listMyImages, ImageResponse } from "@/app/services/imageService";
import { SignedImage } from "./SignedImage";
import { AuthContext } from "@/context/AuthContext";

export const ImageList: React.FC = () => {
  const [images, setImages] = useState<ImageResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const { token } = useContext(AuthContext);

  const fetchImages = async () => {
    setLoading(true);
    try {
      const data = await listMyImages(token);
      setImages(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages();
  }, []);

  if (loading) return <p>Cargando imágenes...</p>;
  if (images.length === 0) return <p>No tienes imágenes</p>;

  return (
    <div className="grid grid-cols-3 gap-4">
      {images.map((img) => (
        <div key={img.id} className="border p-2 rounded">
          <SignedImage imageId={img.id} alt={`Imagen ${img.id}`} />
        </div>
      ))}
    </div>
  );
};
