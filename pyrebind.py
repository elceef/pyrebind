import socket
from time import time

class DNSQuery:
	def __init__(self, data):
		self.data = data
		self.domain = ''
		self.qtype = 0

		opcode = (ord(data[2]) >> 3) & 15
		if opcode == 0:
			ini = 12
			lon = ord(data[ini])
			while lon != 0:
				self.domain += data[ini+1:ini+lon+1] + '.'
				ini += lon + 1
				lon = ord(data[ini])
			self.qtype = ord(data[12+len(self.domain)+2])

	def reply(self, ip):
		packet = ''
		if self.domain:
			packet += self.data[:2] + '\x81\x80'
			packet += self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'
			packet += self.data[12:12+len(self.domain)+5] # original question
			packet += '\xc0\x0c'
			packet += '\x00\x01\x00\x01\x00\x00\x00\x01\x00\x04' # response type, ttl, resource data length (4 bytes)
			packet += ''.join(chr(int(x)) for x in ip.split('.'))
		return packet

if __name__ == '__main__':
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp.bind(('',53))

	try:
		while 1:
			data, addr = udp.recvfrom(1024)
			p = DNSQuery(data)
			# only IN A questions are supported
			if p.domain and p.qtype == 1:
				d = p.domain.split('.')
				# basic validation
				if len(d) >= 4:
					if len(d[0].split('-')) == 4 and len(d[1].split('-')) == 4:
						ip = d[int(time()) % 2].replace('-', '.')
						print '%s -> %s' % (p.domain, ip)
						udp.sendto(p.reply(ip), addr)

	except KeyboardInterrupt:
		udp.close()
