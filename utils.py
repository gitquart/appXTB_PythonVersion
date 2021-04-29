import json

def openFile(file):
    with open(file) as json_file:
        return json.load(json_file)