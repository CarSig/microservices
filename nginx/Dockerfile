FROM nginx:alpine

# 1. Remove default server config
RUN rm /etc/nginx/conf.d/default.conf

# 2. Copy your nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# 3. Copy frontend build (VERY IMPORTANT)
COPY dist/ /usr/share/nginx/html/
