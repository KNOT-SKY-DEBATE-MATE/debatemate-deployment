FROM nginx:latest
RUN apt-get update && apt-get install -y --no-install-recommends certbot python3-certbot-nginx && apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /etc/nginx
COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
