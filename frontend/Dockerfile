# =============================================================================
# STAGE 1: Build the React + TypeScript static assets
# =============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency manifests
COPY package.json package-lock.json ./

# Install dependencies deterministically
RUN npm ci

# Copy application source code
COPY . .

# Build production bundle with TypeScript check + Vite minify
RUN npm run build

# =============================================================================
# STAGE 2: Serve via Nginx reverse proxy
# =============================================================================
FROM nginx:1.27-alpine AS runner

# Remove default Nginx welcome page
RUN rm -rf /usr/share/nginx/html/*

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled artifacts from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Health check to ensure Nginx is serving content
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
