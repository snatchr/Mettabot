import json


replist = {}

def Handle(Name, action, varname = None, data = None):
  if action == "add":
    o = checkInfo(Name, varname)
    if o == "Error":
      addentry(Name)
      addInfo(Name, varname, data)
    else:
      addInfo(Name, varname, data)
  elif action == "check":
    o = checkInfo(Name, varname)
    if o == "Error":
      return "User doesnt exist in database"
    else:
      return o
    


def savetojson(dict):
   with open('varStorage.json', 'w') as fp:
      json.dump(dict, fp)

def loadfromjson():
  try:
    with open('varStorage.json') as json_file: 
      global replist
      replist = json.load(json_file)
  except json.decoder.JSONDecodeError:
    addentry("Placeholder")


def addInfo(Name, varN, data):
  loadfromjson()
  if Name in replist:

      replist[Name][varN] = data
      savetojson(replist)
  else:
    return "Error"


def checkInfo(Name, varN):
  loadfromjson()
  try:
    return replist[Name][varN]
  except:
    return "Error"

    



def addentry(Name):
  replist[Name] = {}
  savetojson(replist)
  return "done"