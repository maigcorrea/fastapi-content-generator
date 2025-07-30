'use client'
import React from 'react'
import { ImageList } from '@/components/ImageList'

const page = () => {
  return (
    <>
     
        <h1 className="text-xl mb-4 font-bold">Historial de Imágenes</h1>
        <div className="mt-6">
          <ImageList />
        </div>
    
    </>
    
  )
}

export default page