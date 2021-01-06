#!/usr/bin/env python3

import argparse
import socket
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import sys
=======
# import sys
>>>>>>> d9fb2f1384b0a2af92680723e360214b85c5781f
=======
import sys
>>>>>>> e277d24e0d06ba7f16504561e9dbfabb5ceaa18f
=======
import sys
>>>>>>> ecf7772500298b18ca90372ff171f8ed29dce072
from controller import NetworkedController
from grid_player import GridPlayer

parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, help='The host to connect to')
parser.add_argument('port', type=int, help='The port to listen on')
args = parser.parse_args()

sock = socket.socket()
sock.connect((args.host, args.port))

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
sys.stdout = None

=======
>>>>>>> d9fb2f1384b0a2af92680723e360214b85c5781f
=======
sys.stdout = None

>>>>>>> e277d24e0d06ba7f16504561e9dbfabb5ceaa18f
=======
sys.stdout = None

>>>>>>> ecf7772500298b18ca90372ff171f8ed29dce072
player = GridPlayer()
controller = NetworkedController(sock, player)

while controller.tick():
    pass

sock.close()
