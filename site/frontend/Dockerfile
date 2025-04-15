# frontend/Dockerfile
FROM node:18 AS builder
WORKDIR /app

# Copy only package files to cache dependencies
COPY package.json package-lock.json ./
RUN npm install --production
RUN npm install axios

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Use a lightweight server for the built files

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
