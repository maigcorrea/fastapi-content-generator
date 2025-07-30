"use client";
import React from "react";
import { useContext } from "react";
import { useSignedImageUrl } from "../hooks/useSignedImageUrl";
import { AuthContext } from "@/context/AuthContext";

export const SignedImage: React.FC<{ imageId: string; alt?: string }> = ({ imageId, alt }) => {
  const { token } = useContext(AuthContext);
  // Usamos un hook personalizado para obtener la URL firmada
  // Este hook maneja la lógica de carga y error
  // y devuelve la URL de la imagen y un estado de carga
  const { url, loading } = useSignedImageUrl(imageId, token);

  if (loading) return <p>Cargando imagen...</p>;
  if (!url) return <p>No se pudo obtener la imagen</p>;

  return <img src={url} alt={alt || "imagen"} className="w-40 h-40 object-cover rounded" />;
};
