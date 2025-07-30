'use client'
import React from 'react'
import { ImageUpload } from '@/components/ImageUpload'
import { ImageList } from '@/components/ImageList'

const page = () => {
  return (
    <>
     
        <h1 className="text-xl mb-4 font-bold">Gestión de Imágenes</h1>
        <ImageUpload />
    
    
    </>
    
  )
}

export default page