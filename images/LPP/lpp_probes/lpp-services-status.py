#!/usr/bin/python3

import os
import socket
import time
import requests
from  multiprocessing import Pool
import sys, traceback
from ping3 import ping


CARBON_SERVER = 'graphite'
CARBON_PORT = 2003

services = [
    {'name':'hephaistos','url':'hephaistos.lpp.polytechnique.fr','port':443},
    {'name':'redmine','url':'https://hephaistos.lpp.polytechnique.fr/redmine'},
    {'name':'rhodecode','url':'https://hephaistos.lpp.polytechnique.fr/rhodecode'},
    {'name':'teamcity','url':'https://hephaistos.lpp.polytechnique.fr/teamcity'},
    {'name':'jupyter','url':'https://hephaistos.lpp.polytechnique.fr/jupyter'},
    {'name':'compiler-explorer','url':'http://compiler-explorer.lpp.polytechnique.fr'},
    {'name':'ElabFTW','url':'https://elabftw.lpp.polytechnique.fr'},
    {'name':'SciQLop_web','url':'http://sciqlop.lpp.polytechnique.fr'},
    {'name':'SciQLop_cache','url':'http://sciqlop.lpp.polytechnique.fr/cache'},

    {'name':'k8s','url':'k8s','port':6443},
    {'name':'k8s-registry','url':'k8s','port':32219},
    {'name':'k8s-master1','url':'k8s-master1','ping':True},
    {'name':'k8s-master2','url':'k8s-master2','ping':True},
    {'name':'k8s-master3','url':'k8s-master3','ping':True},
    {'name':'k8s-master4','url':'k8s-master4','ping':True},
    {'name':'k8s-node1','url':'k8s-node1','ping':True},
    {'name':'k8s-node2','url':'k8s-node2','ping':True},
    {'name':'k8s-node3','url':'k8s-node3','ping':True},
    {'name':'k8s-node4','url':'k8s-node4','ping':True},
    {'name':'k8s-node5','url':'k8s-node5','ping':True},
    {'name':'k8s-node6','url':'129.104.6.175','ping':True},
    {'name':'k8s-node7','url':'129.104.6.176','ping':True},
    
    #{'name':'Mail_IMAP','url':'129.104.27.1','port':993},
    #{'name':'Mail_POP3','url':'129.104.27.1','port':995},
    #{'name':'Mail_HTTPS','url':'129.104.27.1','port':443},
    #{'name':'Mail_SMTP','url':'129.104.27.1','port':25},
    #{'name':'Mail_SMTPS','url':'129.104.27.1','port':465},

    {'name':'VPN_Jussieu','url':'134.157.77.91','port':443},
    {'name':'VPN_Palaiseau','url':'129.104.27.6','port':443},

    {'name':'Passerelle_Jussieu','url':'134.157.77.254','ping':True},
    {'name':'Passerelle_Palaiseau','url':'129.104.27.64','ping':True},

    {'name':'Webmail','url':'129.104.27.2','port':443}
]

def publish(results, dry_run=False):
    if not dry_run:
        sock = socket.socket()
        sock.connect((CARBON_SERVER, CARBON_PORT))

    for result in results:
        if result:
            message = 'lpp_services.status.{name} {status} {time}\n'.format(name=result['name'], status=result['status'], time=int(time.time()))
            if not dry_run:
                sock.sendall(message.encode())
            else:
                print(message)

    if not dry_run:
        sock.close()


def test_service(address, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.5)
        result = sock.connect_ex((address, port))
        return result == 0
    except:
        print(time.asctime())
        traceback.print_exc(file=sys.stdout)
        return False


def test_page(url):
    try:
        request = requests.get(url, timeout=2)
        if request.status_code in [200, 301, 308, 401]:
            return True
        return False
    except:
        print(time.asctime())
        traceback.print_exc(file=sys.stdout)
        return False

def test_ping(url):
    try:
        return ping(url)
    except:
        print(time.asctime())
        traceback.print_exc(file=sys.stdout)
        return False

def test(item):
    if 'port' in item:
        return {'name':item['name'], 'status': 1 if test_service(item['url'], item['port']) else 0}
    elif 'ping' in item:
        return {'name':item['name'], 'status': 1 if test_ping(item['url']) else 0}
    else:
        return {'name':item['name'], 'status': 1 if test_page(item['url']) else 0}
        
def main():
    pool = Pool(len(services))
    while 1:
        try:
            results = pool.map(test, services)
            for _ in range(20):
                begin = time.time()
                publish(results, dry_run=False)
                end = time.time()
                spent_time = end - begin
                time.sleep(max(0.1,3.- spent_time))
        except:
            print(time.asctime())
            traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    main()
    

