#!/usr/bin/python3

""" do some stuffs

Autors: A. Jeandet

        A. Tavant

"""



import requests
import os
import socket
import time

CARBON_SERVER = 'graphite'
CARBON_PORT = 2003

url_root = "https://hephaistos.lpp.polytechnique.fr/redmine/"

#url_root = "https://129.104.27.7/redmine/"

url = url_root + 'issues.json?limit=1&status_id=2'

status_id_dict = {"new":1,

                  "In_progress":2,

                  "resolved":3,

                  "feedback":4,

                  "closed":5,

                  "rejected":6,

                  "total":"*"}

status_data = {}

for k,v in status_id_dict.items():

    url = url_root + f'issues.json?limit=1&status_id={v}'

    data = requests.get(url).json()

    total_count = data["total_count"]

    status_data[k] = total_count



INTERVAL = float(os.environ.get('COLLECTD_INTERVAL',60))

HOSTNAME = os.environ.get('COLLECTD_HOSTNAME','localhost')


sock = socket.socket()
sock.connect((CARBON_SERVER, CARBON_PORT))
for k,v in status_data.items():
    message = 'redmine.issues.{status} {value} {time}\n'.format(status=k, value=v, time=int(time.time()))
    sock.sendall(message.encode())
    #print('PUTVAL "redmine/issues/count-{status}" interval={interval} N:{value}'.format( status=k, interval=INTERVAL, value=v))

sock.close()
