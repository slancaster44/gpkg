import datetime

class modifcationLogEntry:
    def __init__(self, message):
        self.timestamp = datetime.datetime.now()
        self.message = message

    def __str__(self):
        return "[" + str(self.timestamp) + "] " + self.message + "\n"