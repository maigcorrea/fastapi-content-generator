# Usar una imagen oficial de Node
FROM node:18

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración e instalar dependencias
COPY package*.json ./
RUN npm install

# Copiar el resto del código
COPY . .

# Exponer el puerto de Vite (o React)
EXPOSE 5173

# Ejecutar el servidor de desarrollo
CMD ["npm", "run", "dev", "--", "--host"]
