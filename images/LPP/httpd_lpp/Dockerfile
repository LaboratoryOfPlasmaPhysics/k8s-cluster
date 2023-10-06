from debian:12

RUN apt update && apt upgrade -y && \
    apt install -y apache2 libapache2-mod-php && \
    a2enmod ssl && \
    mkdir /etc/apache2/mods-docker /etc/apache2/sites-docker && \
    echo "IncludeOptional /etc/apache2/mods-docker/*.conf" >> /etc/apache2/apache2.conf && \
    echo "IncludeOptional /etc/apache2/sites-docker/*.conf" >> /etc/apache2/apache2.conf 


VOLUME /var/www/ /etc/apache2/mods-docker /etc/apache2/sites-docker

CMD ["apache2ctl",  "-D", "FOREGROUND"]
EXPOSE 443 80
STOPSIGNAL SIGTERM
