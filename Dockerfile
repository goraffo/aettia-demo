FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends nginx gettext-base \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /etc/nginx/sites-enabled/default /etc/nginx/conf.d/default.conf

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY nginx/aettia.conf.template /etc/nginx/templates/aettia.conf.template
RUN chmod +x start.sh

CMD ["./start.sh"]