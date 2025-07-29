'use client'
import React from 'react'
import { ImageUpload } from '@/components/ImageUpload'
import { ImageList } from '@/components/ImageList'

const page = () => {
  const refresh = () => window.location.reload();
  return (
    <>
     
        <h1 className="text-xl mb-4 font-bold">Gestión de Imágenes</h1>
        <ImageUpload onUploaded={refresh} />
        <div className="mt-6">
          <ImageList />
        </div>
    
    </>
    
  )
}

export default page