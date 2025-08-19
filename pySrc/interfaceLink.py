import json
import controller


def commandData(jData):
    data = json.loads(jData)
    return runCommand(data.get("function"),data.get("args"))
def runCommand(functionName,args):
    func = getattr(controller,functionName)
    return func(*args)
