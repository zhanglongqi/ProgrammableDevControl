#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 14/Mar/16 15:25
Description:
This is the control client
It will work with GUI

"""
# !/usr/bin/env python

import socket
from dev import chroma_63211
from time import sleep

TCP_IP = '127.0.0.1'
TCP_PORT = 7777
BUFFER_SIZE = 1024
MESSAGE = chroma_63211.cmds['check_model']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_IP, TCP_PORT))

while True:
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    # if len(data) > 0:
    print("received data:", data)
    # sleep(1)
s.close()

