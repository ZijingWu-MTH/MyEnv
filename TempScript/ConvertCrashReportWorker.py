import os
import sys
import ConvertCrashReport
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), "../tools/redis"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../tools/retask"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../tools/six"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../tools/tendo"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from retask import task
from retask import queue
import ConfigManager

import singleton
single = singleton.SingleInstance()

config = ConfigManager.ConfigManager(None)
redisServer = config.get("crashreport", "redisServer")
config = {
    'host': redisServer,
    'port': 6379,
    'db': 0,
    'password': None,}
queue = queue.Queue("crash-report-task-queue", config)
queue.connect()
while 1:
    try:
        task = queue.wait()
        if task:
            print task.data
            result = ConvertCrashReport.convertCrashReport(task.data["data"])
            queue.send(task, result)
    except KeyboardInterrupt:
        break
    except:
        traceback.print_exc()

