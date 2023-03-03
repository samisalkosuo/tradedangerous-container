#extract options from environment variables

import os

def getOptionsFromEnvDoc():
    optionsDict = dict()
    for key, value in os.environ.items():
        if key.startswith("TD_") == True:
            optName = "--" + key.replace("TD_","").lower()
            optionsDict[optName] = value
    return optionsDict

def getOptionsFromEnv():
    options = []
    for key, value in os.environ.items():
        if key.startswith("TD_") == True:
            optName = "--" + key.replace("TD_","").lower()
            options.append(optName)
            options.append(value)
    return " ".join(options)

print(getOptionsFromEnv())
