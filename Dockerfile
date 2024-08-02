FROM odoo:latest 
 
# Установка дополнительных пакетов, если необходимо 
RUN apt-get update && apt-get install -y \ 
    python3-pip \ 
    && pip3 install -r requirements.txt