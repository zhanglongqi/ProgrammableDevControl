#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 14/Mar/16 15:25
Description:
This is the controller side
It will work with GUI in the future

"""

from dev.chroma_63211 import Chroma63211
from time import sleep

c3 = Chroma63211('127.0.0.1', 7777)

while True:
    data = c3.check_model()
    print("received data:", data)
    sleep(1)
    c3.turn_on()
    sleep(5)
    c3.turn_off()
