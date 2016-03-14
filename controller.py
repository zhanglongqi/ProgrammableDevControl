#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 14/Mar/16 15:25
Description:
This is the controller side
It will work with GUI in the future

"""
# !/usr/bin/env python

import socket
from dev import chroma_63211
from time import sleep

TCP_IP = '127.0.0.1'
TCP_PORT = 7777
BUFFER_SIZE = 1024
MESSAGE = chroma_63211.cmds['check_model']

chroma_63211_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

chroma_63211_conn.connect((TCP_IP, TCP_PORT))

while True:
    chroma_63211_conn.send(MESSAGE)
    data = chroma_63211_conn.recv(BUFFER_SIZE)
    print("received data:", data)
    # sleep(1)
chroma_63211_conn.close()
