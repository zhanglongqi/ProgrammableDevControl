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
    'remote_off': b'CONF:REM OFF',
    'CONF AUTO LOAD ON': b'CONF:AUTO:LOAD ON',
}


class Chroma63211(object):
    def __init__(self, ip, port):
        self.cmds = cmds
        self.BUFFER_SIZE = 1024

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

    def turn_on(self):
        self.conn.send(self.cmds['load_on'])
        # data = self.conn.recv(self.BUFFER_SIZE)
        # return data

    def turn_off(self):
        self.conn.send(self.cmds['load_off'])
        # data = self.conn.recv(self.BUFFER_SIZE)
        # return data

    def set_power(self, power):
        pass

    def check_model(self):
        self.conn.send(self.cmds['check_model'])
        data = self.conn.recv(self.BUFFER_SIZE)
        return data

    def remote_off(self):
        self.conn.send(self.cmds['remote_off'])
        data = self.conn.recv(self.BUFFER_SIZE)
        return data

    def auto_load_on(self):
        self.conn.send(self.cmds['CONF AUTO LOAD ON'])
        data = self.conn.recv(self.BUFFER_SIZE)
        return data

    def query_vol(self):
        self.conn.send(self.cmds['CONF AUTO LOAD ON'])
        data = self.conn.recv(self.BUFFER_SIZE)
        return data
