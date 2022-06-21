FROM fedora:36

COPY redmine-stats.py /usr/bin/redmine-stats.py
COPY lpp-services-status.py /usr/bin/lpp-services-status.py
COPY entrypoint.sh /entrypoint.sh

RUN dnf install -y python3-requests.noarch procps-ng bind-utils python3-pip &&\
	dnf clean all &&\
	pip3 install ping3 &&\
	chmod +x /usr/bin/redmine-stats.py /usr/bin/lpp-services-status.py /entrypoint.sh

CMD ["/entrypoint.sh"]
