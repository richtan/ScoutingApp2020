from .DataScraper import datascraper
import os
try:
    import mysql.connector as pymysql
except:
    print("Please install mysql connector")


class DB:
    conn = None
    cursor = None
    ip = None  # MySQL connection IP
    port = None  # MySQL connection port (e.g. 3306)
    user = None  # MySQL user account (e.g. root)
    pw = None  # MySQL user password
    db_name = None  # Database name in MySQL
    charset = None  # Character encoding (default: utf8)

    def __init__(self, host, user, password, auth_plugin, database):
        self.ip = host
        self.user = user
        self.pw = password
        self.db_name = database
        self.auth_plugin = auth_plugin

    def connect(self):
        self.conn = pymysql.connect(host=self.ip, user=self.user,
                                    password=self.pw, database=self.db_name, auth_plugin=self.auth_plugin)
        self.cursor = self.conn.cursor(buffered=True)

    def execute(self, sql, sql_tuple=None):
        try:
            if sql_tuple is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, sql_tuple)
        except (AttributeError, pymysql.errors.DatabaseError):
            self.connect()
            if sql_tuple is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, sql_tuple)
        return self.cursor

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        return self.conn.commit()

    def get_connection(self):
        return self.conn


class DatabaseUtil:
    variableStorage = {}
    teamData = {"972": {}}
    year = "2019"
    compy = "sfr"

    try:
        mydb = DB(
            host="167.99.26.126",
            user="scouting",
            password=os.environ["mypass"],
            auth_plugin="mysql_native_password",
            database="app_test"
        )

        if (mydb):
            mycursor = mydb
            mycursor.execute("SELECT * FROM team_info_"+year)
            # print([e for e in mycursor.fetchall()])
            mydb.commit()
        else:
            print(
                "NO SQL. you may need to obtain the password and put it into the env variable mypass")
    except Exception as e:
        print(e)
        print("NO SQL. you may need to obtain the password and put it into the env variable mypass")

    # mydb.close()

    @staticmethod
    def storeVariable(name, value):
        DatabaseUtil.variableStorage[name] = value

    @staticmethod
    def addTeam(dictOfValues):
        keys = [e for e in dictOfValues]
        DatabaseUtil.mycursor.execute('INSERT INTO team_info_'+DatabaseUtil.year+'('+','.join(keys)+''')
                         VALUES(
                             '''+','.join(["%s" for key in keys])+''')
                         ''', tuple([dictOfValues[key] for key in keys]))
        DatabaseUtil.mydb.commit()

    @staticmethod
    def modifyTeam(teamnumber, dictOfValues):
        keys = ','.join([e+'="'+dictOfValues[e]+'"' for e in dictOfValues])
        DatabaseUtil.mycursor.execute('''UPDATE team_info_'''+DatabaseUtil.year+'''
        SET '''+keys+'''
        WHERE TeamNumber='''+teamnumber)
        DatabaseUtil.mydb.commit()

    @staticmethod
    def getTeam(teamnumber):
        DatabaseUtil.mycursor.execute(
            "SELECT * FROM team_info_"+DatabaseUtil.year+" where TeamNumber="+teamnumber)
        return [e for e in DatabaseUtil.mycursor.fetchall()]

    @staticmethod
    def getTeamMatchPerformance(teamNumber):
        DatabaseUtil.mycursor.execute(
            "SELECT * FROM team_performance_"+DatabaseUtil.year+"_"+DatabaseUtil.compy+" WHERE teamNumber = " + str(teamNumber))
        return [e for e in DatabaseUtil.mycursor.fetchall()]

    @staticmethod
    def getHatchAvg(teamNumber):
        DatabaseUtil.mycursor.execute(
            "SELECT ROUND(AVG(topH + midH + lowH + carH), 2) FROM team_performance_" + DatabaseUtil.year + "_" + DatabaseUtil.compy + " WHERE teamNumber = " + str(teamNumber))
        return DatabaseUtil.mycursor.fetchall()[0][0]

    @staticmethod
    def getCargoAvg(teamNumber):
        DatabaseUtil.mycursor.execute(
            "SELECT ROUND(AVG(topC + midC + lowC + carC), 2) FROM team_performance_" + DatabaseUtil.year + "_" + DatabaseUtil.compy + " WHERE teamNumber = " + str(teamNumber))
        return DatabaseUtil.mycursor.fetchall()[0][0]

    @staticmethod
    def matchExists(matchNumber):
        DatabaseUtil.mycursor.execute(
            'SELECT COUNT(1) FROM match_info WHERE `MatchID` = "' + matchNumber + '";')
        count = DatabaseUtil.mycursor.fetchall()[0][0]
        if(count == 0):
            return False
        elif(count == 1):
            return True
        else:
            print('Duplicate Matches!')
            quit()

    @staticmethod
    def createMatch(matchNumber):  # returns dictionary of teams
        teamDict = datascraper.getMatchTeams(matchNumber)
        if teamDict == None:
            return None
        DatabaseUtil.mycursor.execute(
            "INSERT INTO match_info (MatchID) VALUES ('"+matchNumber+"');")
        for key, value in teamDict.items():
            DatabaseUtil.mycursor.execute(
                "UPDATE match_info SET " + key + " = '" + str(value) + "' WHERE MatchID = '" + matchNumber + "';")
        DatabaseUtil.mydb.commit()
        return teamDict

    @staticmethod
    def addMatchRecord(dictOfValues):
        # DatabaseUtil.mycursor.execute(
        #    'select * from team_performance where `TeamNumber`='+dictOfValues['TeamNumber'])
        keys = [e for e in dictOfValues]
        #print(["'"+dictOfValues[key]+"'" for key in keys])
        DatabaseUtil.mycursor.execute(
            'DELETE FROM team_performance_'+DatabaseUtil.year+'_'+DatabaseUtil.compy+' WHERE MatchID = %s AND TeamNumber = %s', (dictOfValues['MatchID'], dictOfValues['TeamNumber']))
        DatabaseUtil.mycursor.execute('INSERT INTO team_performance_'+DatabaseUtil.year+'_'+DatabaseUtil.compy+'('+','.join(keys)+''')
                         VALUES(
                             '''+','.join(["%s" for key in keys])+''')
                         ''', tuple([dictOfValues[key] for key in keys]))
        DatabaseUtil.mydb.commit()

    @staticmethod
    def getMatches():
        DatabaseUtil.mycursor.execute(
            "SELECT * FROM match_info")
        return DatabaseUtil.mycursor.fetchall()

    @staticmethod
    def getVariable(name):
        return DatabaseUtil.variableStorage[name]

    @staticmethod
    def writeToTeam(number, attribute, value):
        DatabaseUtil.teamData[str(number)][attribute] = value

    @staticmethod
    def getTeamData(number):
        return DatabaseUtil.teamData[str(number)]

    @staticmethod
    def addBATeamData(number):
        DatabaseUtil.teamData[number] = {}
        DatabaseUtil.teamData[number]['compResults'] = datascraper.getTeamInfo(
            number, DatabaseUtil.year)
        secretinfo = datascraper.getSecretTeamInfo(
            number)
        DatabaseUtil.teamData[number]['teamInfo'] = secretinfo
        DatabaseUtil.mycursor.execute("insert ignore general_team_info(Team_Number, Name, Website, Location) values(%s,%s,%s,%s);", (str(
            number), secretinfo['nickname'], secretinfo['website'], secretinfo['city']+', '+secretinfo['state_prov']))
        DatabaseUtil.mydb.commit()


# DatabaseUtil.addBATeamData('972')
# print(DatabaseUtil.getTeamData("972"))
# print(DatabaseUtil.getMatches())
