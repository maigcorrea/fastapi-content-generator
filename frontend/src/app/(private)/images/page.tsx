"use client";
import React, { useState } from "react";
import { ImageList } from "@/components/ImageList";
import { TrashList } from "@/components/TrashList";
import { ImageUpload } from "@/components/ImageUpload";

const ImagesPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"images" | "trash">("images");

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Gestión de Imágenes</h1>

      {/* Tabs */}
      <div className="flex gap-4 mb-6">
        <button
          className={`px-4 py-2 rounded ${
            activeTab === "images"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
          onClick={() => setActiveTab("images")}
        >
          Mis imágenes
        </button>
        <button
          className={`px-4 py-2 rounded ${
            activeTab === "trash"
              ? "bg-blue-600 text-white"
              : "bg-gray-200 text-gray-700"
          }`}
          onClick={() => setActiveTab("trash")}
        >
          Papelera
        </button>
      </div>

      {/* Contenido dinámico */}
      {activeTab === "images" && (
        <div>
          {/* <ImageUpload /> */}
          <div className="mt-6">
            <ImageList />
          </div>
        </div>
      )}

      {activeTab === "trash" && (
        <div>
          <TrashList />
        </div>
      )}
    </div>
  );
};

export default ImagesPage;
