import socket
import sys
import random

import Checksum

DEST="rutherford.cs.berkeley.edu"
DPORT=33122
SPORT=random.randint(10000,40000)

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(('',SPORT))

seqno = 0
while True:
    msg = raw_input("Message:")
    msg_type = 'data'
    if seqno == 0:
        msg_type = 'syn'
    if msg == "done":
        msg_type = 'end'
    message = "%s|%d|%s|" % (msg_type,seqno,msg)
    checksum = Checksum.generate_checksum(message)
    packet = "%s%s" % (message,checksum)
    print "sent: %s" % packet
    socket.sendto(packet,(DEST,DPORT))
    response,address = socket.recvfrom(8192)
    if Checksum.validate_checksum(response):
        print "recv: %s" % response
    else:
        print "recv: %s <--- CHECKSUM FAILED" % response
    
    if msg_type == 'end':
        break
    else:
        seqno += 1