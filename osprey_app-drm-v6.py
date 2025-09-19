#!/usr/bin/python3.8

# LICENSE CREATIVE_COMMONS-ATTRIBUTION_SHARE_ALIKE
# https://creativecommons.org/licenses/by-sa/3.0/legalcode
# Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]

# Version 1.2.0

# Source: https://www.tutorialkart.com/python/python-read-file-as-string/

import subprocess
import hashlib
import re
import sys
from sys import exit
import os
from os import path
import socket
import base64
import uuid


def verify_valid_host_running_script_via_external():
	valid_hosts = ['204.244.181.88']

	def get_ip_address():
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    s.connect(("8.8.8.8", 80))
	    return s.getsockname()[0]

	ipaddress_by_socket = get_ip_address()

	if not ipaddress_by_socket in valid_hosts:
		if '10.' != ipaddress_by_socket[:3] and '192.168.' != ipaddress_by_socket[:8]:
			print('Host ("' + ipaddress_by_socket + '") was not found in valid list')
			exit(0)


verify_valid_host_running_script_via_external()


class CodecCipher():
	# default_values = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!abcdefghijklmnopqrstuvwxyz=-@#$%^&*()_+<>?,./;':\"[]{}~`"
	default_values = '68U2nKz9FMPJhaxlyd!3oWkGSOe07XjB=iVuHATYR1EDfcNrqmI4QpZCbsvLt5wg/\\+' + "-@#$%^&*()_<>?,.;':\"[]{}~`"
	base64_valid_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz=\\/+'
	stream = True
	debug = False

	def __get_return(self, ret):
		ret = ret[2:][:-1]
		ret = ret if len(ret) != 0 else False
		return ret

	def chunks(self,str, length):
		return [str[i:i+length] for i in range(0, len(str), length)]

	def get_data_type(self, data):

		data_set_list = sorted(set(list(data)))
		cipher_set_list = sorted(set(list(self.default_values)))
		base64_set_list = sorted(set(list(self.base64_valid_chars)))

		outside_matches_on_cipher = list(filter(lambda d: d not in cipher_set_list, data_set_list))
		outside_matches_on_base64 = list(filter(lambda d: d not in base64_set_list, data_set_list))

		if len(outside_matches_on_base64) == 0:
			return 'BASE64 OK'
		elif len(outside_matches_on_cipher) == 0:
			return 'DRM OK'
		else:
			return 'Unknown'

	def convert_base64_into_codec_ciphered_base64(self, codec, data, chunk_size):
		codec_ciphered_base64 = ''
		for chunk in self.chunks(data, chunk_size):
			for byte_position in range(0, chunk_size):	
				if byte_position < len(chunk):
					# Find the position of the byte in question within the cipher
					try:
						cipher_chunk_byte = self.default_values.index(chunk[byte_position])
					except:
						exit("Error 1: Unknown character found based on cipher to encrypt: " + chunk[byte_position])
					# Take the previous position found and add 
					ciphered_byte = self.default_values[cipher_chunk_byte+int(codec[byte_position])]
					codec_ciphered_base64 = codec_ciphered_base64 + str(ciphered_byte)

					if self.stream:
						print(str(ciphered_byte), end="")


		return codec_ciphered_base64

	def convert_codec_ciphered_base64_into_base64(self, codec, data, chunk_size):
		codec_ciphered_base64_reversed = ''
		for rev_chunk in self.chunks(data, chunk_size):
			for rev_byte_position in range(0, chunk_size):	
				if rev_byte_position < len(rev_chunk):
					rev_cipher_chunk_byte = self.default_values.index(rev_chunk[rev_byte_position])
					rev_ciphered_byte = self.default_values[rev_cipher_chunk_byte-int(codec[rev_byte_position])]
					codec_ciphered_base64_reversed = codec_ciphered_base64_reversed + str(rev_ciphered_byte)
					if self.stream:
						print(str(rev_ciphered_byte), end="")

		return codec_ciphered_base64_reversed

	def get_codec_string_sha2_512(self, string_or_hash):
		if self.debug:
			cmd = '/home/nate/OneDrive/code/osprey.app/divideme.app/osprey_app-divide_me-v5.py 1 ' + string_or_hash
		else:
			cmd = 'osprey_app-divide_me-v5 1 "' + string_or_hash + '"'

		divide_me = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
		divide_me_return = self.__get_return(str(divide_me.stdout))

		if not divide_me_return:
			print("osprey_app-divide_me-v5 script not found")
			exit(0)

		codec = int.from_bytes(hashlib.sha512(divide_me_return.encode('utf-8')).digest(), 'big')
		return str(codec)

	def get_codec_string_sha3_512(self, string_or_hash):
		if self.debug:
			cmd = '/home/nate/OneDrive/code/osprey.app/divideme.app/osprey_app-divide_me-v5.py 1 ' + string_or_hash
		else:
			cmd = 'osprey_app-divide_me-v5 1 "' + string_or_hash + '"'

		divide_me = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
		divide_me_return = self.__get_return(str(divide_me.stdout))

		if not divide_me_return:
			print("osprey_app-divide_me-v5 script not found")
			exit(0)

		codec = int.from_bytes(hashlib.sha3_512(divide_me_return.encode('utf-8')).digest(), 'big')
		return str(codec)

	def get_codec_string_sha2_256(self, string_or_hash):
		if self.debug:
			cmd = '/home/nate/OneDrive/code/osprey.app/divideme.app/osprey_app-divide_me-v5.py 1 ' + string_or_hash
		else:
			cmd = 'osprey_app-divide_me-v5 1 "' + string_or_hash + '"'

		divide_me = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
		divide_me_return = self.__get_return(str(divide_me.stdout))

		if not divide_me_return:
			print("osprey_app-divide_me-v5 script not found")
			exit(0)

		codec = int.from_bytes(hashlib.sha256(divide_me_return.encode('utf-8')).digest(), 'big')
		return str(codec)

	def get_codec_string_sha3_256(self, string_or_hash):
		if self.debug:
			cmd = '/home/nate/OneDrive/code/osprey.app/divideme.app/osprey_app-divide_me-v5.py 1 ' + string_or_hash
		else:
			cmd = 'osprey_app-divide_me-v5 1 "' + string_or_hash + '"'

		divide_me = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
		divide_me_return = self.__get_return(str(divide_me.stdout))

		if not divide_me_return:
			print("osprey_app-divide_me-v5 script not found")
			exit(0)

		codec = int.from_bytes(hashlib.sha3_256(divide_me_return.encode('utf-8')).digest(), 'big')
		return str(codec)

	def get_codec_file_sha2_512(self, string_or_hash):

		if not path.exists(string_or_hash):
			print("get_codec_file_sha2_512 failed, file doesn't exist.")
			exit(0)

		cmd = 'openssl dgst -sha512 "' + string_or_hash + '"'
		openssl_sha = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
		openssl_sha_return = self.__get_return(str(openssl_sha.stdout))
		matches = re.match(r'(.*)\)=\s([a-fA-F0-9]+)', openssl_sha_return)
		openssl_sha_return_actual = matches[2]
		codec = int.from_bytes(openssl_sha_return_actual.encode('utf-8'), 'big')
		return str(codec)

	def get_codec_file_sha3_512(self, string_or_hash):

		if not path.exists(string_or_hash):
			print("get_codec_file_sha3_512 failed, file doesn't exist.")
			exit(0)

		cmd = 'openssl dgst -sha3-512 "' + string_or_hash + '"'
		openssl_sha = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
		openssl_sha_return = self.__get_return(str(openssl_sha.stdout))
		matches = re.match(r'(.*)\)=\s([a-fA-F0-9]+)', openssl_sha_return)
		openssl_sha_return_actual = matches[2]
		codec = int.from_bytes(openssl_sha_return_actual.encode('utf-8'), 'big')
		return str(codec)

	def get_codec_file_sha2_256(self, string_or_hash):

		if not path.exists(string_or_hash):
			print("get_codec_file_sha2_256 failed, file doesn't exist.")
			exit(0)

		cmd = 'openssl dgst -sha256 "' + string_or_hash + '"'
		openssl_sha = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
		openssl_sha_return = self.__get_return(str(openssl_sha.stdout))
		matches = re.match(r'(.*)\)=\s([a-fA-F0-9]+)', openssl_sha_return)
		openssl_sha_return_actual = matches[2]
		codec = int.from_bytes(openssl_sha_return_actual.encode('utf-8'), 'big')
		return str(codec)

	def get_codec_file_sha3_256(self, string_or_hash):

		if not path.exists(string_or_hash):
			print("get_codec_file_sha3_256 failed, file doesn't exist.")
			exit(0)

		cmd = 'openssl dgst -sha3-256 "' + string_or_hash + '"'
		openssl_sha = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
		openssl_sha_return = self.__get_return(str(openssl_sha.stdout))
		matches = re.match(r'(.*)\)=\s([a-fA-F0-9]+)', openssl_sha_return)
		openssl_sha_return_actual = matches[2]
		codec = int.from_bytes(openssl_sha_return_actual.encode('utf-8'), 'big')
		return str(codec)

	def get_codec_hash(self, hash_type, string_or_hash):
		if hash_type == 'hash_uuid':
			if re.match(r'[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}', string_or_hash):
				return str(int(string_or_hash.replace('-', ''), 16))
			else:
				print('Invalid hash')
				exit(0)
		elif hash_type == 'hash_sha2_512':
			if re.match(r'[a-fA-F0-9]{128}', string_or_hash):
				return str(int(string_or_hash, 16))
			else:
				print('Invalid hash')
				exit(0)
		elif hash_type == 'hash_sha3_512':
			if re.match(r'[a-fA-F0-9]{128}', string_or_hash):
				return str(int(string_or_hash, 16))
			else:
				print('Invalid hash')
				exit(0)
		elif hash_type == 'hash_sha2_256':
			if re.match(r'[a-fA-F0-9]{64}', string_or_hash):
				return str(int(string_or_hash, 16))
			else:
				print('Invalid hash')
				exit(0)
		elif hash_type == 'hash_sha3_256':
			if re.match(r'[a-fA-F0-9]{64}', string_or_hash):
				return str(int(string_or_hash, 16))
			else:
				print('Invalid hash')
				exit(0)
		else:
			print('Invalid hash type: ' + hash_type)
			exit(0)


codec_cipher = CodecCipher()

if len(sys.argv) >= 2:
	algo_unverified = sys.argv[1]
	if algo_unverified == 'string_sha2_512':
		algo = algo_unverified
	elif algo_unverified == 'string_sha3_512':
		algo = algo_unverified
	elif algo_unverified == 'string_sha2_256':
		algo = algo_unverified
	elif algo_unverified == 'string_sha3_256':
		algo = algo_unverified
	elif algo_unverified == 'hash_uuid':
		algo = algo_unverified
	elif algo_unverified == 'hash_sha2_512':
		algo = algo_unverified
	elif algo_unverified == 'hash_sha3_512':
		algo = algo_unverified
	elif algo_unverified == 'hash_sha2_256':
		algo = algo_unverified
	elif algo_unverified == 'hash_sha3_256':
		algo = algo_unverified
	elif algo_unverified == 'file_sha2_512':
		algo = algo_unverified
	elif algo_unverified == 'file_sha3_512':
		algo = algo_unverified
	elif algo_unverified == 'file_sha2_256':
		algo = algo_unverified
	elif algo_unverified == 'file_sha3_256':
		algo = algo_unverified
	elif algo_unverified == 'get_data_type':
		algo = algo_unverified
	else:
		print("Unknown algorithm to run DRM. Try passing the first value 'string_sha2_512'")
		exit(0)
else:
	algo = 'string_sha_512'


if len(sys.argv) >= 3:
	string_or_hash = sys.argv[2]
else:
	print('String or hash is empty. Pass the third value as a string or hex value of a number')
	exit(0)

reverse_override = False

if len(sys.argv) >= 4:
	file = sys.argv[3]

	if not path.exists(file):
		print("File does not exists: " + file)
		exit(0)

	cmd = 'file "' + file + '"'
	file_type = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
	file_type_return = str(file_type.stdout.decode('utf-8').strip())

	if 'ASCII' in file_type_return:	
		file_handle = open(file, "r")

		#read whole file to a string
		file_data = file_handle.read().strip()
		file_data = re.sub(r'(\r\n|\r|\n)', '', file_data)

		#close file
		file_handle.close()

		file_data_type = (codec_cipher.get_data_type(file_data))
		if file_data_type == 'BASE64 OK':
			# do nothing
			reverse_override = False
		elif file_data_type == 'DRM OK':
			# process this file in reverse
			reverse_override = True
		else:
			print("Unknown ASCII file encryption")
			exit(0)
	else:
		# Process this file as an actual file that needs to get base64'd first
		data = open(file, "rb").read()
		encoded = base64.b64encode(data)
		file_data = re.sub(r'(\r\n|\r|\n)', '', encoded.decode('utf-8'))
else:
	file_data = 'Lg==' # a dot

reverse = False

if not reverse_override:
	if len(sys.argv) >= 5:
		reverse = True if sys.argv[4] == 'reverse' else sys.argv[4]
else:
	codec_cipher.stream = False
	reverse = reverse_override

ouput_to_base64_on_reverse = True if len(sys.argv) >= 6 and sys.argv[5] == 'base64' else False

if ouput_to_base64_on_reverse:
	codec_cipher.stream = True

if algo == 'string_sha2_512':
	codec = codec_cipher.get_codec_string_sha2_512(string_or_hash)
elif algo == 'string_sha3_512':
	codec = codec_cipher.get_codec_string_sha3_512(string_or_hash)
elif algo == 'string_sha2_256':
	codec = codec_cipher.get_codec_string_sha2_256(string_or_hash)
elif algo == 'string_sha3_256':
	codec = codec_cipher.get_codec_string_sha3_256(string_or_hash)
elif algo == 'hash_uuid':
	codec = codec_cipher.get_codec_hash(algo, string_or_hash)
elif algo == 'hash_sha2_512':
	codec = codec_cipher.get_codec_hash(algo, string_or_hash)
elif algo == 'hash_sha3_512':
	codec = codec_cipher.get_codec_hash(algo, string_or_hash)
elif algo == 'hash_sha2_256':
	codec = codec_cipher.get_codec_hash(algo, string_or_hash)
elif algo == 'hash_sha3_256':
	codec = codec_cipher.get_codec_hash(algo, string_or_hash)
elif algo == 'file_sha2_512':
	codec = codec_cipher.get_codec_file_sha2_512(string_or_hash)
elif algo == 'file_sha3_512':
	codec = codec_cipher.get_codec_file_sha3_512(string_or_hash)
elif algo == 'file_sha2_256':
	codec = codec_cipher.get_codec_file_sha2_256(string_or_hash)
elif algo == 'file_sha3_256':
	codec = codec_cipher.get_codec_file_sha3_256(string_or_hash)
elif algo == 'get_data_type':
	print(codec_cipher.get_data_type(file_data))
	exit(0)
else:
	print("Unknown codec. Try using string_sha2_512")
	exit(0)

chunk_size = len(codec)


if not reverse:
	codec_ciphered_base64 = codec_cipher.convert_base64_into_codec_ciphered_base64(codec, file_data, chunk_size)

	if not codec_cipher.stream:
		print(codec_ciphered_base64, end="")
		exit(1)
	else:
		exit(1)
else:
	codec_ciphered_base64_reversed = codec_cipher.convert_codec_ciphered_base64_into_base64(codec, file_data, chunk_size)

	if not codec_cipher.stream:
		if not ouput_to_base64_on_reverse and codec_cipher.get_data_type(codec_ciphered_base64_reversed) == 'BASE64 OK':
			final_return = base64.b64decode(codec_ciphered_base64_reversed)
			sys.stdout.buffer.write(final_return)
		else:
			print(codec_ciphered_base64_reversed, end="")
		exit(1)
	else:
		exit(1)

# Sources:
# https://pythonexamples.org/python-split-string-into-specific-length-chunks/
# https://www.programiz.com/python-programming/methods/string/index
# https://unix.stackexchange.com/questions/347295/how-can-i-generate-sha3-if-there-is-no-sha3sum-command-in-coreutils
# https://www.guru99.com/python-check-if-file-exists.html#2
# https://stackoverflow.com/questions/3103178/how-to-get-the-system-info-with-python
# https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-from-nic-in-python
# https://stackoverflow.com/questions/31917595/how-to-write-a-raw-hex-byte-to-stdout-in-python-3
# https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in
# https://www.kite.com/python/examples/1892/base64-encode-a-file-in-%60base64%60
# https://stackoverflow.com/questions/17457793/sorting-a-set-of-values/17458090
# https://stackoverflow.com/questions/12897374/get-unique-values-from-a-list-in-python
# https://www.geeksforgeeks.org/extracting-mac-address-using-python/