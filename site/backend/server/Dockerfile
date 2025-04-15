# backend/Dockerfile
FROM golang:1.23.4 AS builder

# Set the working directory
WORKDIR /app

# Install Air for live reloading
RUN go install github.com/air-verse/air@v1.61.5

# Copy Go modules files and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the application source code
COPY . .

# Build the application (optional, for production)
# RUN go build -o main .

EXPOSE 8080
# Use Air for live reloading in development
CMD ["air", "-c", ".air.toml"]
