#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 14/Mar/16 14:50
Description:
This is a simple program that redirect command from ethernet to serial and vice versa

This will mainly used as gateway
Parse cmd and return result

python3 main.py /dev/cu.usbserial-A4008UPt 115200

change the device to your /dev/ttyUSB0 on laptop or /dev/ttyO1 on BBB
"""

import sys
import socket
import serial
import serial.threaded
import threading


class ReaderThread(threading.Thread):
    def __init__(self, ser):
        super(ReaderThread, self).__init__()
        self.ser = ser
        self.clients = []
        self.buffer = ''

    def run(self):
        while self.ser.is_open:
            try:
                # read all that is there or wait for one byte (blocking)
                data = self.ser.read(self.ser.in_waiting or 1)
                data = str(data, encoding='utf-8')
                self.buffer += data
                if '\n' in data:  # this will combine all fragments together until new line shows
                    for client in self.clients:
                        client.send(self.buffer.encode())
                    self.buffer = ''

            except serial.SerialException:
                # probably some I/O problem such as disconnected USB serial
                # adapters -> exit
                break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'SERIALPORT',
        help="serial port name")

    parser.add_argument(
        'BAUDRATE',
        type=int,
        nargs='?',
        help='set baud rate, default: %(default)s',
        default=9600)

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress non error messages',
        default=False)

    group = parser.add_argument_group('serial port')

    group.add_argument(
        "--parity",
        choices=['N', 'E', 'O', 'S', 'M'],
        type=lambda c: c.upper(),
        help="set parity, one of {N E O S M}, default: N",
        default='N')

    group.add_argument(
        '--rtscts',
        action='store_true',
        help='enable RTS/CTS flow control (default off)',
        default=False)

    group.add_argument(
        '--xonxoff',
        action='store_true',
        help='enable software flow control (default off)',
        default=False)

    group.add_argument(
        '--rts',
        type=int,
        help='set initial RTS line state (possible values: 0, 1)',
        default=None)

    group.add_argument(
        '--dtr',
        type=int,
        help='set initial DTR line state (possible values: 0, 1)',
        default=None)

    group = parser.add_argument_group('network settings')

    group.add_argument(
        '-P', '--localport',
        type=int,
        help='local TCP port',
        default=7777)

    args = parser.parse_args()

    # connect to serial port
    ser = serial.serial_for_url(args.SERIALPORT, do_not_open=True)
    ser.baudrate = args.BAUDRATE
    ser.parity = args.parity
    ser.rtscts = args.rtscts
    ser.xonxoff = args.xonxoff

    if args.rts is not None:
        ser.rts = args.rts

    if args.dtr is not None:
        ser.dtr = args.dtr

    if not args.quiet:
        sys.stderr.write(
            '--- TCP/IP to Serial redirect on {p.name}  {p.baudrate},{p.bytesize},{p.parity},{p.stopbits} ---\n'
            '--- type Ctrl-C / BREAK to quit\n'.format(p=ser))

    try:
        ser.open()
    except serial.SerialException as e:
        sys.stderr.write('Could not open serial port {}: {}\n'.format(ser.name, e))
        sys.exit(1)

    serial_reader = ReaderThread(ser)
    serial_reader.start()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('', args.localport))
    srv.listen(1)
    try:
        while True:
            sys.stderr.write('Waiting for connection on {}...\n'.format(args.localport))
            client_socket, addr = srv.accept()
            sys.stderr.write('Connected by {}\n'.format(addr))
            try:
                serial_reader.clients.append(client_socket)
                # enter network <-> serial loop
                while True:
                    try:
                        data_from_socket = client_socket.recv(1024)
                        if not data_from_socket:
                            break
                        print('received data from socket: ', data_from_socket, type(data_from_socket))
                        ser.write(data_from_socket)  # get a bunch of bytes and send them
                        ser.write(b'\n')
                    except socket.error as msg:
                        sys.stderr.write('ERROR: %s\n' % msg)
                        # probably got disconnected
                        break
            except socket.error as msg:
                sys.stderr.write('ERROR: {}\n'.format(msg))
            finally:

                sys.stderr.write('Disconnected\n')
                client_socket.close()
    except KeyboardInterrupt:
        pass

    sys.stderr.write('\n--- exit ---\n')
    serial_reader.join()
