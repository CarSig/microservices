# --- Stage 1: Build the Vite app ---
FROM node:25.2.1 AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source files
COPY . .

# Build optimized production output
RUN npm run build



# --- Stage 2: Serve the static frontend ---
FROM node:25.2.1

WORKDIR /app

# Install static file server
RUN npm install -g serve

# Copy production build from step 1
COPY --from=build /app/dist ./dist

EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]
