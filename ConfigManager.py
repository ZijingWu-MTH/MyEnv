import sys
if (sys.version_info[0] == 2):
    import ConfigParser as configparser
else:
    import configparser
import io
import sys
import os

class ConfigManager:
    def __init__(self, dirPath, fileName = 'setting.ini'):
        if (not dirPath):
            dirPath = os.path.dirname(__file__)
        self.parser = configparser.RawConfigParser()
        settingFile = os.path.join(dirPath, fileName)
        self.parser.read(settingFile)

    def get(self, section, item):
        return self.parser.get(section, item)
