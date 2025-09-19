#!/usr/local/bin/python3.8

# MIT License
#
# Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import subprocess
import sys
from sys import exit
# import datetime.datetime
import time

sources = """
Sources:
https://stackoverflow.com/questions/3877623/can-you-have-variables-within-triple-quotes-if-so-how
"""

version = 'sbit-v2'

if len(sys.argv) == 1:
	motd_help = """
Welcome to OSPREY.app's {0}
-----------------------------------------------------
MIT License

Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[REQS] This is script is compiled to run on Ubuntu 16LTS and above with python3 support.

The purpose of this script is to find the encrpyted bit for a color in a hexadecimal 
format without the # as found in HTML and CSS.

To run this command, simply type a hex color as the first parameter.

eg: ./osprey_app-{0} FFFFFF

Optionally you may pre-fix this first command with a digest format on 
how you would like to see the data of the sbit.

-sha3-256 (default)
-sha3-256-hex
-sha3-512
-sha3-512-hex

eg: ./osprey_app-{0} -sha3-256-hex ffffff
"""
	print(motd_help.format(version))
	exit(0)

if len(sys.argv) == 2:
	color_hex = str(sys.argv[1])
	dgst_input = '-sha3-256'
else:
	color_hex = str(sys.argv[2])
	dgst_input = str(sys.argv[1])

# color_hex = 'FF00FF'

# data = str(sys.argv[1])

# datetime_now = str(datetime.datetime.now())

color_equation = str(int.from_bytes(color_hex.encode('utf-8'), 'big')).replace('0x', '')
# color_equation = '77267270125126'

cmd = '~/bin/osprey_app-divide_me-v8.py 1 "' + color_equation + '"'
# print(cmd)

dm = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
dm_log = dm.stdout.read().decode('utf-8').strip()
dm.terminate()

# print(dm_log)
# eg = "1.639629710710792858755732690E-47 Hz (p.v8.0.0) [1 ÷ We did it! Woohoo ;)]"
# print(eg)
# 082fd134ceb4f6e8ff8d65a227e57e6d2ecaffe38a97aa88c4bc3ba3985d3a97
hz_matches = re.match(r"(((\d+)\.(\d+))([E]?[-+]?)(\d+))\sHz", dm_log)
# print(hz_matches[3])
# exit(0)
head = hz_matches[3] + '-' + hex(int(hz_matches[4])).replace('0x', '')
tail = hex(int(hz_matches[6])).replace('0x', '')

# print(head)

coin = str(head) + '-' + hz_matches[5] + str(tail) + 'Hz'

# print(coin)

# exit(0)
# 54c4518b8a1f126d47d14d2E-2f

coin_value = int.from_bytes(coin.encode('utf-8'), 'big')

# print(coin_value)
# 21887118876010347795183703788327694437338207134076983283882472038

s_matches = re.match(r"((\d+\.\d+)([E]?[-+]?)(\d+))\sHz( \(p\.v\d+\.\d+\.\d+\) (\[.*\]))", dm_log)

# print(s_matches[6])
bit = s_matches[6].replace('1 ÷ ', '').replace('[', '').replace(']', '')

sbit_log = coin + ' ' + version + ' ' + bit

# print(sbit_log)

dgst_hex = False

if dgst_input == '-sha3-256-hex':
	dgst_input = '-sha3-256'
	dgst_hex = True 
elif dgst_input == '-sha3-512':
	 dgst = '-sha3-512'
	 dgst_hex = False
elif dgst_input == '-sha3-512-hex':
	dgst_input = '-sha3-512'
	dgst_hex = True 
else:
	dgst_input = '-sha3-256'
	dgst_hex = False 

cmd = "echo '" + str(sbit_log) + "' | openssl dgst " + dgst_input + " | awk '{print $NF}'"
sbit_sum_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
sbit_sum = sbit_sum_proc.stdout.read().decode('utf-8').strip()
sbit_sum_proc.terminate()

sbit = int.from_bytes(sbit_sum.encode('utf-8'), 'big')

if dgst_hex == True:
	print(sbit_sum, end="")
	exit(1)

sbit = int.from_bytes(sbit_sum.encode('utf-8'), 'big')
print(sbit, end="")
exit(1)