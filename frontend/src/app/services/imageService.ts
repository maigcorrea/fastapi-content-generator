import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ImageResponse {
  id: string;
  file_name: string;
  user_id: string;
  created_at: string;
  is_deleted: boolean;
}

export const uploadImage = async (file: File, token: string): Promise<ImageResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(`${API_BASE}/images/upload`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`, // 🔹 ahora pasamos el token aquí también
    },
  });

  return res.data;
};

export const listMyImages = async (token: string): Promise<ImageResponse[]> => {
  const res = await axios.get(`${API_BASE}/images/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data;
};

export const getSignedImageUrl = async (imageId: string, token: string): Promise<string> => {
  const res = await axios.get(`${API_BASE}/images/image-url/${imageId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.data.url;
};

export const deleteImage = async (imageId: string, token: string): Promise<void> => {
  await axios.delete(`${API_BASE}/images/${imageId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const listDeletedImages = async (token: string): Promise<ImageResponse[]> => {
  const res = await axios.get(`${API_BASE}/images/trash`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};

export const restoreImage = async (imageId: string, token: string): Promise<void> => {
  await axios.post(`${API_BASE}/images/restore/${imageId}`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  });
};