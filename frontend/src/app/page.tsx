'use client';
import Navbar from "@/components/NavBar";
import ProtectRoutes from "@/components/ProtectRoutes";
import Image from "next/image";

export default function Home() { 
  return (
    <>
      {/* <ProtectRoutes adminOnly> // Protege las rutas, solo permite acceso a admins */}
      <Navbar></Navbar>
        <h1>FRONTEND</h1>
      {/* </ProtectRoutes> */}
    </>
  );
}