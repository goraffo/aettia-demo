#!/bin/bash
set -e

# Crear secrets.toml si estamos en Railway (usando variables de entorno)
if [ -n "$GOOGLE_CLIENT_ID" ]; then
  mkdir -p .streamlit
  cat > .streamlit/secrets.toml <<EOF
[auth]
redirect_uri = "${AUTH_REDIRECT_URI}"
cookie_secret = "${AUTH_COOKIE_SECRET}"

[auth.google]
client_id = "${GOOGLE_CLIENT_ID}"
client_secret = "${GOOGLE_CLIENT_SECRET}"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
EOF
fi

envsubst '${PORT}' < /etc/nginx/templates/aettia.conf.template > /etc/nginx/conf.d/aettia.conf

streamlit run app.py --server.port=8501 --server.address=127.0.0.1 --server.headless=true &
nginx -g 'daemon off;' &

wait -n
exit $?