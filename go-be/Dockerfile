# Build stage
FROM golang:1.23-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache git

# Copy dependency files if present
COPY go.mod* go.sum* ./
RUN if [ -f go.mod ]; then go mod download; fi

# Copy application code
COPY . .

# Build statically linked binary
RUN if [ -f main.go ]; then \
      CGO_ENABLED=0 GOOS=linux go build -o /app/server .; \
    else \
      mkdir -p /app && echo "echo 'go-be binary placeholder'" > /app/server && chmod +x /app/server; \
    fi

# Production runtime stage
FROM alpine:3.20

WORKDIR /app

COPY --from=builder /app/server /app/server

EXPOSE 8080

CMD ["/app/server"]
