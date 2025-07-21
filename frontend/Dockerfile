# Imagen base con Node.js
FROM node:20-alpine

# Directorio de trabajo
WORKDIR /app

# Copiar los archivos del package
COPY package.json package-lock.json* ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código
COPY . .

# Compilar el proyecto (por si quieres usar `next build` en producción más adelante)
# En desarrollo no se necesita compilar

# Exponer puerto
EXPOSE 3000

# Ejecutar servidor de desarrollo
CMD ["npm", "run", "dev"]
