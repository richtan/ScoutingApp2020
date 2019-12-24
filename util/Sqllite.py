import sqlite3
from .DataScraper import datascraper

class SqlUtil:
    current_columns = [("ID", "INT"), ("TEAMNUM", "TEXT"), ("MATCH", "INT"),
                       ("CARGO", "INT"), ("HATCH", "INT"), ("CLIMB", "REAL"), ("COMMENTS", "CHAR(50)")]

    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        table_columns = [(e[1], e[2]) for e in self.conn.execute(
            "PRAGMA table_info(data)").fetchall()]
        not_added_yet_columns = [e for e in self.current_columns if e not in table_columns]
        print(not_added_yet_columns)
        for column in not_added_yet_columns:
            self.conn.execute('ALTER TABLE data ADD %s %s' %
                              (column[0], column[1]))
        self.conn.commit()
        self.current_columns = [(e[1], e[2]) for e in self.conn.execute(
            "PRAGMA table_info(data)").fetchall()]

    def get_current_columns(self):
        return [e[0] for e in self.current_columns]
    def get_team_info(self, team_number):
        team_matches = self.conn.execute("SELECT %s FROM data WHERE TEAMNUM=%s" % (','.join(self.get_current_columns()), team_number)).fetchall()
        
        average_stats = [0 if (e[1]=="INT" or e[1]=="REAL") and e[0]!="ID" else None for e in self.current_columns]
        team_number_index = next((c for c,e in enumerate(self.current_columns) if e[0]=="TEAMNUM"))
        
        average_stats[team_number_index] = team_number

        if team_matches==[]: return average_stats

        for match in team_matches:
            for count, stat in enumerate(match):
                if average_stats[count] != None and count!=team_number_index:
                    average_stats[count] += stat
        average_stats = [stat/len(team_matches) if stat!=None else None for stat in average_stats]
        return average_stats

    def get_match_info(self, matchNumber):
        #available_teams = [self.conn.execute("SELECT %s FROM data WHERE MATCH=%s" % (','.join(self.get_current_columns()), matchNumber)).fetchall()]
        teams = datascraper.getMatchTeams(matchNumber)
        return {place:{self.current_columns[c][0]:e for c,e in enumerate(self.get_team_info(teams[place])) if e!=None} for place in teams}

    def give_headers(self):
        return self.current_columns
    def close(self):
        self.conn.close()


#sql = SqlUtil()
#print(sql.give_headers())
#print(sql.get_match_info(1))
#sql.close()