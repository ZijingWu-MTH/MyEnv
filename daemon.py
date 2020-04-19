from datetime import date
from datetime import timedelta
from datetime import datetime
import traceback
import collections
#import ftp_server
import subprocess
#import telnet_server
import thread
import time
import xml.etree.cElementTree as ET
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/recordtype'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools/tendo'))
from recordtype import recordtype

#def FtpServerProc():
#    ftp_server.FtpServerMain()

#def TelentServerProc():
#    telnet_server.TelnetServerMain()

import singleton
single = singleton.SingleInstance()

Task = recordtype('Task', ['interval', 'script', 'lastExcuteTime', 'thread'])
def LoadDaemonTasks():
    xmldoc = ET.parse('daemon.config').getroot()
    tasks = xmldoc.findall(".//task") 
    result = []
    for task in tasks:
        try:
            script = task.text
            interval = int(task.get('interval'))
            thread = task.get('thread')
            result = result + [Task(interval, script, datetime(2000, 1, 1), thread)]
        except:
            # TODO by zijwu, show more detail information.
            print "load task failed."
            traceback.print_exc()
    return result

#try:
#    thread.start_new_thread(FtpServerProc, ())
#    thread.start_new_thread(TelentServerProc, ())
#except:
#    print "Error: unable to start thread."

try:
    import os
    import signal
    import sys
    import time
    def handle_pdb(sig, frame):
        import pdb
        pdb.Pdb().set_trace(frame)
    signal.signal(signal.SIGUSR1, handle_pdb)
except KeyboardInterrupt:
    logging.info("Server shut down.")

def taskThread(task, dummy):
    print ("New separate task thread")
    while 1:
        if (datetime.now() - task.lastExcuteTime > timedelta(seconds = task.interval)):
            try:
                task.lastExcuteTime = datetime.now() 
                subprocess.check_output(task.script, shell=True)
            except:
                #TODO by zijwu, add log.
                traceback.print_exc()
                pass
        time.sleep(1)

tasks = LoadDaemonTasks()
separateThreadTasks = []
shareThreadTasks = []

for task in tasks:
    if (task.thread == "separate"):
        separateThreadTasks = separateThreadTasks + [task];
    else:
        shareThreadTasks = shareThreadTasks + [task];

for task in separateThreadTasks:
    thread.start_new_thread(taskThread, (task, 0))
        
while 1:
    for task in shareThreadTasks:
        if (datetime.now() - task.lastExcuteTime > timedelta(seconds = task.interval)):
            try:
                task.lastExcuteTime = datetime.now() 
                print ("The shared thread loop.")
                print "try to run: " + task.script
                subprocess.check_output(task.script, shell=True)
            except:
                #TODO by zijwu, add log.
                traceback.print_exc()
                pass
        time.sleep(1)

