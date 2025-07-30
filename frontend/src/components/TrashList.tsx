"use client";
import { useImageContext } from "@/context/ImageContext";
import { img } from "framer-motion/client";
import { useState } from "react";

export const TrashList: React.FC = () => {
  const { trash, restoreFromTrash } = useImageContext();
  const [loading, setLoading] = useState<string | null>(null);

  if (trash.length === 0) return <p>No tienes imágenes en la papelera</p>;

  return (
    <>
    <div className="grid grid-cols-3 gap-4">
      {trash.map((img) => (
        <div key={img.id} className="border p-2 rounded relative">
          <img src={img.signedUrl} alt={img.file_name} className="rounded shadow" />
          <button
            className="absolute top-2 right-2 bg-green-600 text-white px-2 py-1 rounded"
            onClick={() => {
                if (confirm("¿Seguro que quieres restaurar esta imagen?")) {
                    setLoading(img.id);
                    restoreFromTrash(img.id);
                    setLoading(null);
              }
            }}
          >
            Restaurar
          </button>
          {loading === img.id && <p>Restaurando...</p>}
        </div>
      ))}
    </div>
    </>
  );
};
