#!/usr/bin/env python3

import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

parser = argparse.ArgumentParser()

parser.add_argument("port", help="Port used to serve up content", default=2121, type=int)
parser.add_argument("-f", "--folder", help="Folder to serve content from", default="/tmp/")
parser.add_argument("-u", "--user", help="User used to authenticate", default="ftp")
parser.add_argument("-p", "--password", help="Password used to authenticate", default="password")

args = parser.parse_args()

PORT = args.port
UPLOAD_FOLDER = args.folder
USERNAME = args.user
PASSWORD = args.password


def main():
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(USERNAME, PASSWORD, UPLOAD_FOLDER, perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Optionally specify range of ports to use for passive connections.
    #handler.passive_ports = range(60000, 65535)

    address = ('', PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()


if __name__ == '__main__':
    main()
