# python client.py 192.168.0.35 5050 s1 10 10 10

import getopt
import socket
import sys
import time

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

path_atuador = "/atuador"

# limite da temperatura
h_lim = int(sys.argv[4])
t_lim = int(sys.argv[5])

path = "coap://" + sys.argv[1] + ":" + sys.argv[2] + "/" + sys.argv[3]
host, port, path = parse_uri(path)
led = sys.argv[4]

client = HelperClient(server=(host, port))


def sensor_observer(response):
    print 'Sensor Value Updated'
    global client
    global path_atudador
    try:
        p = response.payload.split("-")
        humidity = int(p[0])
        temp = int(p[1])
        if (humidity > h_lim and temp > t_lim):
            print ("humidity and temperature outside the limit range...:" + humidity +"/"+ temp)
            response = client.put(path_atuador, led + "-1")
        else:
            print ("humedad y temperatura dentro del rango limite...:" + humidity +"/"+ temp)
            response = client.put(path_atuador, led + "-0")
    except:
        print('Humidity in not a number')


def main():
    global client
    client.observe(path, sensor_observer)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "sa"
        sys.exit()