'''
As of now program will display the connections whenever program runs

Cron Job: we can create a cron job to run this program for every 10 seconds 

Steps to Improve: Need to maintain a DB or centralized file which will have unique data of the connections, 
                Need to implement a function to push the connections only if it is not exist in the db or centralized file and 
                based on weather data is inserted to db or not, we will display that particular connection - by this way we can get new connections
'''
import re
import sys
import datetime

def process_file(procnet):
    sockets = procnet.split('\n')[1:-1]
    return [line.strip() for line in sockets]

def split_every_n(data, n):
    return [data[i:i+n] for i in range(0, len(data), n)]

def convert_linux_netaddr(address):

    hex_addr, hex_port = address.split(':')

    addr_list = split_every_n(hex_addr, 2)
    addr_list.reverse()

    addr = ".".join(map(lambda x: str(int(x, 16)), addr_list))
    port = str(int(hex_port, 16))

    return "{}:{}".format(addr, port)

def format_output(data):
    return (("%s: New connection: %s -> %s" %(str(datetime.datetime.now()).split('.')[0], data['local'], data['remote'])) + "\n")

with open('/proc/net/tcp') as f:
    sockets = process_file(f.read())

rv = []
for info in sockets:
    _ = re.split(r'\s+', info)

    _tmp = {
        'local': convert_linux_netaddr(_[1]),
        'remote': convert_linux_netaddr(_[2]),
    }
    rv.append(_tmp)

if len(rv) > 0:
    for _ in rv:
        sys.stdout.write(format_output(_))