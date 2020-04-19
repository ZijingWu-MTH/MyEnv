import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../tools/six"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../tools/redis"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../tools/retask"))
import ConfigManager

from retask import task
from retask import queue
import time

orignalPath = sys.argv[1]
resultOrignalPath = sys.argv[2]

inputFile = open(orignalPath, "r")
outputFile = open(resultOrignalPath, "w")

crashString = inputFile.read()

config = ConfigManager.ConfigManager(None)
redisServer = config.get("crashreport", "redisServer")
config = {
    'host': redisServer,
    'port': 6379,
    'db': 0,
    'password': None,}
queue = queue.Queue("crash-report-task-queue", config)
queue.connect()
task = task.Task({'data': crashString})
job = queue.enqueue(task)
job.wait(60)
result = job.result
if (result == None):
    result = crashString
outputFile.write(result)
inputFile.close()
outputFile.close()
