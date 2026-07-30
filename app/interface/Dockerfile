# Stage 1: Build React app
FROM node:20-alpine AS builder

WORKDIR /app

COPY app/interface/package.json app/interface/package-lock.json ./
RUN npm ci

COPY app/interface/ ./

# Copy openapi.json (referenced by tests and types)
COPY docs/api/openapi.json /docs/api/openapi.json

RUN npm run build

# Stage 2: Serve with Nginx + proxy to backend
FROM nginx:alpine

# Remove default config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built React app
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost/api/v1/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
