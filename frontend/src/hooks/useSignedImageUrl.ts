import { useEffect, useState, useContext } from "react";
import { getSignedImageUrl } from "@/app/services/imageService";

// hook para obtener la URL firmada de una imagen
// recibe el ID de la imagen y el token de autenticación
// devuelve la URL y un estado de carga
export const useSignedImageUrl = (imageId: string | null, token: string | null) => {
  const [url, setUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!imageId || !token) return;

    setLoading(true);
    getSignedImageUrl(imageId, token)
      .then((signedUrl) => setUrl(signedUrl))
      .finally(() => setLoading(false));
  }, [imageId, token]);

  return { url, loading };
};

