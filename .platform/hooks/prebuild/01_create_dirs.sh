#!/bin/bash
if [ ! -d /var/cache/nginx ]; then
  mkdir -p /var/cache/nginx
  chown -R nginx:nginx /var/cache/nginx
  chmod 755 /var/cache/nginx
fi

if [ ! -d /var/sockets ]; then
  mkdir -p /var/sockets
  chown -R webapp:webapp /var/sockets
  chmod 755 /var/sockets
fi
