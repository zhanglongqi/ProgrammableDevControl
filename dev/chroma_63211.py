#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 14/Mar/16 14:52
Description:


"""
import socket

cmds = {
    'check_model': b'*IDN?',
    'load_on': b'LOAD ON',
    'load_off': b'LOAD OFF',
}


class Chroma63211(object):
    def __init__(self, ip, port):
        self.cmds = cmds
        self.BUFFER_SIZE = 1024

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

    def turn_on(self):
        pass

    def set_power(self, power):
        pass

    def check_model(self):
        self.conn.send(self.cmds['check_model'])
        data = self.conn.recv(self.BUFFER_SIZE)
        return data
