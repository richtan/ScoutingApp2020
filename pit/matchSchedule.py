from flask import render_template
import time
from flask import Markup


def matchSchedule(scraper):
    # currentTime = time.time()
    currentTime = time.time()
    scraper = scraper.DataScraper()
    url = scraper.getWebcastUrl(scraper.SFeventKey)
    print(url)
    results = scraper.getMatches(scraper.SFeventKey, currentTime)[0:2]

    a1 = results[0]
    a2 = results[1]
    AP1 = Markup(', '.join(['<a href="/scouting/teamPage/%s"><p style="display:inline">%s</p></a>' %
                            (e[3:], e[3:]) for e in a1['alliances']['red']['team_keys']]))
    OT1 = Markup(', '.join(['<a href="/scouting/teamPage/%s"><p style="display:inline">%s</p></a>' %
                            (e[3:], e[3:]) for e in a1['alliances']['blue']['team_keys']]))

    T1 = str(a1['time']-currentTime)
    C1 = ('lightblue' if '972' in str(OT1) else '#ff4141')

    AP2 = Markup(', '.join(['<a href="/scouting/teamPage/%s"><p style="display:inline">%s</p></a>' %
                            (e[3:], e[3:]) for e in a2['alliances']['red']['team_keys']]))
    OT2 = Markup(', '.join(['<a href="/scouting/teamPage/%s"><p style="display:inline">%s</p></a>' %
                            (e[3:], e[3:]) for e in a2['alliances']['blue']['team_keys']]))

    C2 = ('lightblue' if '972' in str(OT2) else '#ff4141')

    T2 = str(a2['time']-currentTime)
    return AP1, OT1, T1, AP2, OT2, T2, url, C1, C2
