FROM redis:latest
WORKDIR /usr/local/etc/redis
COPY redis.conf.template .
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN apt-get update && \
    apt-get install -y gettext && \
    chmod +x /usr/local/bin/entrypoint.sh && \
    mkdir -p /var/log/redis /data && \
    touch /var/log/redis/redis.log && \
    chown redis:redis /var/log/redis/redis.log && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
