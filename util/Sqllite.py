import sqlite3
#from .DataScraper import datascraper

class SqlUtil:
    current_columns = [("ID", "INT"), ("TEAMNUM", "INT"), ("MATCH", "INT"),
                       ("Name", "TEXT"), ("InitLine", "INT"), ("LowAuto", "INT"), ("HighAuto", "INT"), ("LowTele", "INT"), ("HighTele","INT"), ("ShotPos", "INT"),("RotControl", "INT"), ("PosControl", "INT"), ("Climb", "TEXT"), ("ClimbLevel", "TEXT"), ("BuddyCLimb", "TEXT"), ("DefenseAbility", "INT") ("TechIssues", "INT"), ("Comments", "TEXT")]

    def __init__(self):
        self.conn = sqlite3.connect('data.db', check_same_thread=False)
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
    def get_team_info(self, team_number, easy_info=False):
        team_matches = self.conn.execute("SELECT %s FROM data WHERE TEAMNUM=%s" % (','.join(self.get_current_columns()), team_number)).fetchall()
        
        average_stats = [0 if (e[1]=="INT" or e[1]=="REAL") and e[0]!="ID" else None for e in self.current_columns]
        team_number_index = next((c for c,e in enumerate(self.current_columns) if e[0]=="TEAMNUM"))
        
        

        if team_matches==[]: 
            average_stats[team_number_index] = team_number
            return average_stats

        for match in team_matches:
            for count, stat in enumerate(match):
                if average_stats[count] != None and count!=team_number_index:
                    if stat:
                        average_stats[count] += stat
                    else:
                        print(stat)
        print(average_stats)
        average_stats = [stat/len(team_matches) if stat!=None else None for stat in average_stats]
        average_stats[team_number_index] = team_number
        average_stats_dict = dict(zip([e[0] for e in self.current_columns], average_stats))
        filtered_average_stats = {k: v for k, v in average_stats_dict.items() if v is not None}
        if easy_info:
            return filtered_average_stats
        else:
            return average_stats
    
    def get_more_team_info(self, team_number):
        base_stats = self.get_team_info(team_number, easy_info=True)
        print(base_stats)
        team_comments = self.conn.execute("SELECT %s FROM data WHERE TEAMNUM=%s" % ('COMMENTS', team_number)).fetchall()
        base_stats.update({"team_comments": team_comments})
        return base_stats


    def get_match_info(self, matchNumber):
        #available_teams = [self.conn.execute("SELECT %s FROM data WHERE MATCH=%s" % (','.join(self.get_current_columns()), matchNumber)).fetchall()]
        teams = datascraper.getMatchTeams(matchNumber)
        return {place:{self.current_columns[c][0]:e for c,e in enumerate(self.get_team_info(teams[place])) if e!=None} for place in teams}

    def give_headers(self):
        return self.current_columns
    def close(self):
        self.conn.close()


sql = SqlUtil()
#print(sql.give_headers())
#print(sql.get_match_info(1))
#sql.close()