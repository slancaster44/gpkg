
class repoSpecs:
    def __init__(self, location):
        self.location = location
        self.pkgs = []
        self.modificationLog = []

    def __str__(self):
        rtrnVal = "[Repository]\n"
        rtrnVal += "Location: " + self.location + "\n"

        rtrnVal += "-- Modification Log --\n"
        for i in self.modificationLog:
            rtrnVal += str(i)

        rtrnVal += "\n-- Packages --\n"
        for i in self.pkgs:
            rtrnVal += "\n" + str(i) + "\n"

        return rtrnVal