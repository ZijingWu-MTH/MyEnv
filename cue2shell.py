import sys
import util
import re
import string
import os
import tempfile

def winShellEscape(value):
    value = value.replace("%", "%%");
    value = value.replace("^", "^^");
    value = value.replace("&", "^&");
    value = value.replace("<", "^<");
    value = value.replace(">", "^>");
    value = value.replace("|", "^|");
    value = value.replace("'", "^'");
    value = value.replace("`", "^`");
    value = value.replace(",", "^,");
    value = value.replace(";", "^;");
    value = value.replace("=", "^=");
    value = value.replace("(", "^(");
    value = value.replace(")", "^)");
    value = value.replace("!", "^^!");
    value = value.replace("[", "\\[");
    value = value.replace("]", "\\]");
    return value;

def getAliasValue(alias, translatedValueMap):
    if (alias in translatedValueMap):
        return translatedValueMap[alias]
    raise Exception("Unknown alias %s referenced." % alias)

translatedValueMap = {}

def replaceLambda(matchobj):
    return getAliasValue(matchobj.group(1), translatedValueMap)

def translateMacAlias(name, value, translatedValueMap):
    #check if the string contains parameter, if it contains we will translate it as function for mac
    value = re.sub("env{([^}]*)}", "$\\1", value)
    value = re.sub("{path_sep}", "/", value)
    value = re.sub("{source}", ".", value)
    value = re.sub("{shell_ext}", "sh", value)
    value = re.sub("{equal}", "=", value)
    if (value.find("$1") >= 0):
        pass
    else:
        value = re.sub("{command_sep}", "&&", value)
        value = re.sub("alias{([^}]*)}", replaceLambda, value)
    return value
   
def translateWinAlias(name, value, translatedValueMap):
    # because we have % in the result, so lets first do winShellEscape
    # because we write to file, so we doesn't need to do shell escape.
    value = re.sub("env{([^}]*)}", "%\\1%", value)
    value = re.sub("{source}", "call", value)
    value = re.sub("{path_sep}", "\\\\", value)
    value = re.sub("{source}", "call", value)
    value = re.sub("{shell_ext}", "cmd", value)
    value = re.sub("{command_sep}", "$T", value)
    value = re.sub("alias{([^}]*)}", replaceLambda, value)
    #value = re.sub("\$(\d)", "$args[\\1]", value)

    return value

def translatedValueToShell(name, value):
    lines = []
    if (util.getPlatformName() == "win32"):
	lines = lines + ["doskey %s=%s" % (name, value)]
    else:
	lines = lines + ["alias %s='%s'" % (name, value)]
    return lines


fileName = sys.argv[1]
outputFile = sys.argv[2]
cueLines = []
try:
    cueLines = open(fileName).readlines()
except Exception:
    pass

for cueLine in cueLines:
    separatorIndex = cueLine.find("=")
    if (separatorIndex > 0 and cueLine[0] != '#'):
        name = cueLine[0:separatorIndex].strip()
        value = cueLine[(separatorIndex + 1):].strip()
        havePlatformSpecifier = len(value.split("::")) >= 2
        if (havePlatformSpecifier):
            platform = value.split("::")[1]
            if (not platform.strip().lower() == util.getPlatformName()):
                continue
            value = value.split("::")[0].strip()
        #try:
        if (util.getPlatformName() == "win32"):
            translatedValue = translateWinAlias(name, value, translatedValueMap)
        elif (util.getPlatformName() == "mac"):
            translatedValue = translateMacAlias(name, value, translatedValueMap)
        elif (util.getPlatformName() == "linux"):
            translatedValue = translateMacAlias(name, value, translatedValueMap)
        else:
            raise Exception("Unsupportted platform.")
            
        translatedValueMap[name] = translatedValue

outputFd = open(outputFile, 'w')
if (util.getPlatformName() == "win32"):
    tempFileName = os.path.join(tempfile.gettempdir(), util.id_generator());
    f = open(tempFileName, 'w')
    for (name, value) in translatedValueMap.items():
        f.write("%s=%s\n" %(name, value))
    f.close()

    outputFd.write("echo read alias from %s\n" % (tempFileName))
    outputFd.write("doskey /MACROFILE=%s\n" % (tempFileName))
    #outputFd.write("del %s" % (tempFileName))

else:
    for (name, value) in translatedValueMap.items():
        if (value.find("$1") >= 0):
            commands = value.split("{command_sep}")
            outputFd.write("function %s(){\n" % (name))
            for command in commands:
                command = re.sub("alias{([^}]*)}", replaceLambda, command)
                outputFd.write(command.strip() + "\n")
            outputFd.write("}\n")
        else:
            outputFd.write("alias %s='%s'\n" % (name, value))
outputFd.close();
