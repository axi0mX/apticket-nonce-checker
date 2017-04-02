#!/usr/bin/python
# Script which parses 32-bit SHSH/APTickets and prints the APTicket nonce, if any.
# Compatible with macOS and Linux. Requires openssl.
# Author: @axi0mX (March 28, 2017)

import binascii, plistlib, subprocess, sys

def print_apticket_nonce(data):
	try:
		p = subprocess.Popen(['openssl', 'asn1parse', '-inform', 'DER'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		(stdout, stderr) = p.communicate(data)
	except OSError as e:
		print 'ERROR: Something went wrong executing openssl! Details:', e
		sys.exit(1)

	if 'SEQUENCE' not in stdout:
		print 'ERROR: OpenSSL returned unexpected output when parsing APTicket.'
		sys.exit(1)

	for line in stdout.split('\n'):
		if 'prim: cont [ 18 ]' in line:
			tokens = line.split()
			assert tokens[2] == 'l='
			tokens0 = tokens[0].split(':')
			assert tokens0[1][:2] == 'd='
			tokens1 = tokens[1].split('=')
			assert tokens1[0] == 'hl'

			offset = int(tokens0[0])
			header_length = int(tokens1[1])
			data_length = int(tokens[3])
			nonce = data[offset + header_length:offset + header_length + data_length]

			print 'APTicket has a nonce.'
			print 'Nonce (hex dump): %s' % binascii.hexlify(nonce)
			print 'Nonce length:     %s bytes' % len(nonce)
			return

	print 'APTicket does not have a nonce.'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'ERROR: Provide path to SHSH or APTicket as argument to this script.'
		sys.exit(1)
	data = open(sys.argv[1], 'rb').read()
	if '<plist version=' in data:
		print 'Parsing APTicket from SHSH file.'
		shsh = plistlib.readPlistFromString(data)
		print_apticket_nonce(shsh['APTicket'].data)
	else:
		print 'Parsing APTicket.'
		print_apticket_nonce(data)

