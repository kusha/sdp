#!/usr/bin/env sh
set -eu

envsubst '${PORT} ${FAILOVER_PORT_1} ${FAILOVER_PORT_2} ${FAILOVER_PORT_3}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

exec "$@"