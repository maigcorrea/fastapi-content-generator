"use client";
import React, { useState, useContext } from "react";
import { uploadImage } from "@/app/services/imageService";
import { AuthContext } from "@/context/AuthContext";

export const ImageUpload: React.FC<{ onUploaded: () => void }> = ({ onUploaded }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const { token } = useContext(AuthContext);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      await uploadImage(file, token);
      onUploaded(); // refresca la lista
      setFile(null);
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
