import re

_album = None
_artist = None

def initConversation():
    _album = None
    _artist = None

def isValidCommand(spokenText):
    initConversation()
    album = re.search(r'play album from artist (.*)', spokenText)
    return True

def executeCommand(param):
    pass
