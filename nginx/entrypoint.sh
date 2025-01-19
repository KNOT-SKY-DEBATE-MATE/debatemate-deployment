#!/bin/bash

if [ -z "$NGINX_SERVER_NAME" ] || [ -z "$CERTBOT_EMAIL" ]; then
  echo "Error: NGINX_SERVER_NAME and CERTBOT_EMAIL must be set."
  exit 1
fi

if [ ! -f "/etc/letsencrypt/live/$NGINX_SERVER_NAME/fullchain.pem" ]; then
  certbot certonly --nginx \
    --non-interactive \
    --agree-tos \
    --email "$CERTBOT_EMAIL" \
    -d "$NGINX_SERVER_NAME" \
    ${CERTBOT_STAGING:+--staging}
fi

envsubst '${NGINX_SERVER_NAME}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
nginx -g "daemon off;"
