#!/bin/bash
set -e
envsubst '${PORT}' < /etc/nginx/templates/aettia.conf.template > /etc/nginx/conf.d/aettia.conf

streamlit run app.py --server.port=8501 --server.address=127.0.0.1 --server.headless=true &
nginx -g 'daemon off;' &

wait -n
exit $?