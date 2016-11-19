# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de TousSports.info para Movie Ultra 7K
# Version 0.1 (05.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a Juarrox


import plugintools, xbmcplugin, datetime
from __main__ import *
from resources.tools.msg import *

fanart = 'http://www.hdnicewallpapers.com/Walls/Big/Tennis/Amazing_Tennis_Sport_Game_Stadium_Wallpapers.jpg'
thumbnail = 'https://pbs.twimg.com/profile_images/588955468984266752/mk_kpDSQ.jpg'


def live9(params):
    plugintools.log("[%s %s] Iniciando Live9 ... " % (addonName, addonId))

    from datetime import datetime
    # Calculando día y hora actual
    ahora = datetime.now()
    mes = ahora.month
    if mes <= 9:
        mes = '0'+str(ahora.month)
    time_now = str(ahora.day) + '/' + str(mes)

    plugintools.add_item(action="", title= '[COLOR green][B]Live9[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    plugintools.add_item(action="", title= '[COLOR lightyellow][B]All times CET (GMT +2)[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    
    
    url = 'http://live9.net/'
    referer = 'http://live9.net/'

    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)

    dia_prog = plugintools.find_single_match(data, "<h4>(.*?)</h4>")

    matches = plugintools.find_single_match(data, '2015</h4>(.*?)</body>')
    plugintools.log("matches= "+matches)
    time_past=""

    event = plugintools.find_multiple_matches(matches, '(.*?)</a>')
    
    for entry in event:
        plugintools.log("entry= "+entry)
        if time_past == "":
            time_past = 0            
        sport_event = plugintools.find_single_match(entry, '<b>(.*?)</b>')
        time_event = plugintools.find_single_match(entry, '(.*?)<font');time_event=time_event.replace('<div class="list">', "").strip()
        plugintools.log("time_event= "+time_event)
        time_event = time_event.replace("<br/>", "").strip()
        hora_event=time_event[0:2]
        if hora_event == "00":
            hora_event = "24"
        plugintools.log("hora_event= "+hora_event)
        if hora_event == "":
            continue
        resta = int(hora_event) - int(time_past)
        print resta

        if resta < 0:
            fecha_hoy = datetime.strptime("hora_event", '%d/%m'); print 'fecha_hoy',fecha_hoy
            time_event = fecha_hoy + 1;time_event = str(time_event.day)+'/'+str(time_event.month)
            plugintools.log("time_event= "+time_event)
        else:
            time_past=time_event[0:2]
            plugintools.log("time_past= "+time_past)
        title_event = plugintools.find_single_match(entry, '</font> (.*?)<a')
        url_event = plugintools.find_single_match(entry, '<a href="([^"]+)')
        ch_event = plugintools.find_single_match(entry, '">Channel([^\n]+)');ch_event='Channel'+ch_event
        url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_event+'%26referer=http://live9.net'
        title = '[COLOR gold]'+time_now+'[/COLOR][COLOR orange][B] '+time_event+'[/B][/COLOR][COLOR lightyellow] '+sport_event +': '+ title_event+ '('+ch_event+')[/COLOR][COLOR lightgreen][I] [Live9][/I][/COLOR]'
        plugintools.log("time_event= "+time_event)
        plugintools.log("sport_event= "+sport_event)
        plugintools.log("URL= "+url)        
        plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)       
        
    plugintools.setview("files")
        
        
  	
def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);
    try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
    except: pass
    try: r='\'location\',\s\'([^\']+)';loc=plugintools.find_single_match(str(response_headers),r);
    except: pass
    if loc:
     request_headers.append(["Referer",url]);
     if jar: request_headers.append(["Cookie",jar]);#print jar
     body,response_headers=plugintools.read_body_and_headers(loc,headers=request_headers);
     try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
     except: pass

    plugintools.setview("files")
    return body
