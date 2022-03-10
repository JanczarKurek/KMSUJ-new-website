# Monolithic dockerfile for kmsuj website
# Should later be changed so that nginx is separated

from nginx

ENV WEBSITE_DIR="/website"

# Install additional packages
RUN apt update; \
    apt install -y python3 python3-pip;

ADD . $WEBSITE_DIR
ADD nginx.conf /etc/nginx/nginx.conf
RUN mkdir /etc/nginx/logs; \
    mkdir /static

# Setup python
RUN  pip3 install -r $WEBSITE_DIR/requirements.txt

EXPOSE 80/tcp

ENV DJANGO_LOGGING_ROOT="/var/log"

VOLUME /var/log /static /db

ENTRYPOINT ["/bin/bash", "/website/entrypoint.sh"]
