# sudo python atuador.py 192.168.0.35 5050

import getopt
import socket
import sys
import time

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

from sense_emu import SenseHat

sense = SenseHat()

red = (255, 0, 0)
white = (255, 255, 255)

path = "coap://" + sys.argv[1] + ":" + sys.argv[2] + "/atuador"
host, port, path_atuador = parse_uri(path)

pixels = [None] * 64

client = HelperClient(server=(host, port))


def atuador_observer():
    print 'Atuador Value Updated'
    global client
    response = client.get(path_atuador)
    for i in range(64):
        pixels[i] = white
        if response.payload[i] == "1":
            pixels[i] = red
    sense.set_pixels(pixels)


def main():
    global client

    while True:
        time.sleep(1)
        atuador_observer()


if __name__ == '__main__':
    main()