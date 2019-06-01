import requests
import json
import datetime
#import tbapy


class DataScraper:
    baseUrl = "https://www.thebluealliance.com/api/v3"
    apiKey = "1CQGBNHADuOcI5xDHmLjpIBdQwxTHzZmPpDohm1gNs79gDtN5BrGgIt1bPzAlx2N"
    #tba = tbapy.TBA(apiKey)
    SVReventKey = ""
    SFeventKey = ""
    Year = ""

    def __init__(self):
        self.SVReventKey = '2019casf'
        self.SFeventKey = '2019casf'
        self.Year = "2019"

    def getEvent(self, year, name):
        year = self.Year
        events = json.loads(requests.get(self.baseUrl + "/events/" +
                                         year + '?X-TBA-Auth-Key='+self.apiKey).text)
        return next((e for e in events if e['name'] == name))

    def getTeamInfo(self, team, year):
        year = self.Year
        return json.loads(requests.get(self.baseUrl + "/team/frc"+team+"/events/" +
                                       year+"/statuses" + '?X-TBA-Auth-Key='+self.apiKey).text)

    def getSecretTeamInfo(self, team):
        return json.loads(requests.get(self.baseUrl + '/team/frc'+team+'?X-TBA-Auth-Key='+self.apiKey).text)

    def getTeams(self, year, id):
        year = self.Year
        return json.loads(requests.get(self.baseUrl + "/event/" + id + "/teams" + '?X-TBA-Auth-Key=' + self.apiKey).text)

    def getTeamEventStatus(self, team, event_key):
        return json.loads(requests.get(self.baseUrl + '/team/frc'+team+'/event/'+event_key+'/status'+'?X-TBA-Auth-Key='+self.apiKey).text)

    def eventAlliances(self, event_key):
        return json.loads(requests.get(self.baseUrl + '/event/'+event_key+'/alliances'+'?X-TBA-Auth-Key='+self.apiKey).text)

    def getTeamMatches(self, team, event_key):
        return json.loads(requests.get(self.baseUrl + '/team/frc'+team+'/event/'+event_key+'/matches'+'?X-TBA-Auth-Key='+self.apiKey).text)

    def getWebcastUrl(self, event_key):
        return 'https://player.twitch.tv/?channel='+json.loads(requests.get(self.baseUrl + '/event/'+event_key+'?X-TBA-Auth-Key='+self.apiKey).text)['webcasts'][0]['channel']

    def getMatches(self, event_key, now):
        mat = json.loads(requests.get(self.baseUrl + '/event/'+event_key +
                                      '/matches/simple'+'?X-TBA-Auth-Key='+self.apiKey).text)
        mat = [{'alliances': e['alliances'], 'key':e['key'], 'time':e['time'], 'ptime':e['predicted_time']}
               for e in mat if 'frc972' in e['alliances']['red']['team_keys']+e['alliances']['blue']['team_keys'] and e['time'] > now]
        newlist = sorted(mat, key=lambda k: k['time'])
        return newlist

    def getMatchTeams(self, matchNumber):
        matchNumber = self.SFeventKey+"_qm"+str(matchNumber)
        data = json.loads(requests.get(
            self.baseUrl + '/match/'+matchNumber+'?X-TBA-Auth-Key='+self.apiKey).text)
        print(data)
        try:
            red = [e[3:] for e in data['alliances']['red']['team_keys']]
            blue = [e[3:] for e in data['alliances']['blue']['team_keys']]
        except Exception as e:
            print(e)
            return None
        return {
            "R1": red[0],
            "R2": red[1],
            "R3": red[2],
            "B1": blue[0],
            "B2": blue[1],
            "B3": blue[2]
        }


datascraper = DataScraper()
# print(datascraper.getEvent("2019", "San Francisco Regional"))
# print(datascraper.getTeamInfo("254", "2018"))
# print(datascraper.eventAlliances(datascraper.SFeventKey))
# print(datascraper.SVReventKey)
# print(datascraper.getTeams("2019", datascraper.SFeventKey))
