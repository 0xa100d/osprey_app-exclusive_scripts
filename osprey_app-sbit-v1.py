#!/usr/local/bin/python3.8

import re
import subprocess

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

eg = "1.639629710710792858755732690E-47 Hz (p.v8.0.0) [1 ÷ We did it! Woohoo ;)]"
print(eg)
# 082fd134ceb4f6e8ff8d65a227e57e6d2ecaffe38a97aa88c4bc3ba3985d3a97
hz_matches = re.match(r"((\d+\.\d+)([E]?[-+]?)(\d+))\sHz", eg)
head = hex(int(hz_matches[2].replace('.', '')))
tail = hex(int(hz_matches[4]))

coin = str(head.replace('0x', '')) + hz_matches[3] + str(tail.replace('0x', ''))

print(coin)
# 54c4518b8a1f126d47d14d2E-2f

coin_value = int.from_bytes(coin.encode('utf-8'), 'big')

print(coin_value)
# 21887118876010347795183703788327694437338207134076983283882472038

cmd = "echo '" + coin + "' | openssl dgst -sha3-256 | awk '{print $NF}'"
sha3_256_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
sha3_256 = sha3_256_proc.stdout.read().decode('utf-8').strip()
sha3_256_proc.terminate()

print(sha3_256)
# 2405b9434de85ad20bb85dedc9350aeb941387e0e7718cb5c14a87484494a468