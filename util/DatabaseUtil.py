from .DataScraper import datascraper
import os


class DatabaseUtil:
    variableStorage = {}
    teamData = {"972": {}}
    year = "2019"
    compy = "sfr"

    # mydb.close()

    @staticmethod
    def storeVariable(name, value):
        DatabaseUtil.variableStorage[name] = value

    @staticmethod
    def getVariable(name):
        return DatabaseUtil.variableStorage[name]


# DatabaseUtil.addBATeamData('972')
# print(DatabaseUtil.getTeamData("972"))
# print(DatabaseUtil.getMatches())
# :(-|--<
# :)-|--<
#A picture of you bellypoking you