import os
import sys
import util
import subprocess
import codecs
import logging
import argparse
import getpass
import sys
import telnetlib
import signal
import time

def handle_pdb(sig, frame):
    import pdb
    pdb.Pdb().set_trace(frame)
signal.signal(signal.SIGUSR1, handle_pdb)

HOST = os.environ.get('REMOTE_SHELL')
PORT = os.environ.get('REMOTE_SHELL_PORT')
tn = telnetlib.Telnet(HOST, PORT)
# we cannot read_until for Username, because server may cache the data, and waiting for vim user right now, got dead lock
#tn.set_debuglevel(100)
print(' '.join(sys.argv[1:]) + "\n")
tn.write("vim user" + "\n")
tn.write(' '.join(sys.argv[1:]) + "\n")
tn.write("exit\n")
tn.read_until("Goodbye")
tn.close()

