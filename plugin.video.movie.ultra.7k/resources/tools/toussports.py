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

__icons__ = art + '/icons/'


def tous0(params):
    plugintools.setview("tvshows")
    plugintools.log("[%s %s] Toussports.info " % (addonName, addonId))

    #thumbnail = 'https://lh3.googleusercontent.com/-y0hsXXgY85s/Us0yFusFBOI/AAAAAAAABIA/8nbdAE7SajA/s630-fcrop64=1,00000000fe89ffff/CoverG%252BA.jpg'
    thumbnail = 'https://pbs.twimg.com/profile_images/1649525603/tous-sports_400x400.jpg'
    #fanart = 'http://hdwallpapersmart.com/wp-content/uploads/2014/10/bein-sports1.jpg'
    #fanart = 'http://www.pix2.tv/wp-content/uploads/2013/09/BEIN-Sport-12.jpg'
    fanart = 'http://img0.cfstatic.com/wallpapers/6fb443ad681c037b2ce4008d98994e7d_large.jpeg'

    plugintools.add_item(action="", title= '[COLOR blue][B]TOU[COLOR white]SS[COLOR red]PORTS [/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    plugintools.add_item(action="tous2", title= '[COLOR lightyellow]Click aquí para ver [I][B]canales LIVE[/B][/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = True, isPlayable = False)

    url = 'http://www.streaming-foot.info/schedule.php'
    referer = 'http://www.toussports.info'

    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)

    matches = plugintools.find_single_match(data, '<ul>(.*?)</ul>')
    #plugintools.log("matches= "+matches)

    event = plugintools.find_multiple_matches(matches, '<li class="list-group-item"(.*?)</li>')
    jornada = ""  # Control para imprimir día del evento una sola vez
    sin_eventos = 0  # Control para evitar impresión del día sin eventos programados
    for entry in event:
        plugintools.log("entry= "+entry)
        time_event = plugintools.find_single_match(entry, '<span style="display:none">(.*?)</span>')
        time_event = time_event.strip()
        plugintools.log("time_event= "+time_event)
        time_fixed = time_event.split(" ")
        if len(time_fixed) >= 2:
            time_fixed = time_fixed[0]
            time_fixed = time_fixed.split("-")
            time_event = time_fixed[2]+"/"+time_fixed[1]
            plugintools.log("time_event= "+time_event)

        if jornada == "" or jornada != time_event:
            plugintools.add_item(action="",title='[COLOR lightyellow][B][ '+time_event+' ][/B][/COLOR]',url="", thumbnail = thumbnail, fanart = fanart , folder=False, isPlayable=False)
            jornada = time_event
            plugintools.log("jornada= "+jornada)
            
        hora_event = plugintools.find_single_match(entry, '<span style="">(.*?)</span>')
        categ_event = plugintools.find_single_match(entry, '<span class="categorie">(.*?)</span>')
        name_event = plugintools.find_single_match(entry, '<span class="name_match">(.*?)</span>')
        ch_event = plugintools.find_single_match(entry, '<span class="links">(.*?)</span>')
        ch_event_fixed = ch_event.replace(" -", "").strip()
        title_fixed = '[COLOR orange][B]'+hora_event.strip()+'[/B][COLOR lightyellow]'+categ_event+' '+name_event+' [I][COLOR lightgreen]['+ch_event_fixed+'][/I][/COLOR]'
        channels = ch_event_fixed.split(" ")
        canales = []
        for item in channels:
            canales.append(item)
        datamovie = {}
        
        if title_fixed.find("Stream 24/24 7/7 gratuit")< 0:
            if ch_event_fixed != "":
                title_fixed = '[COLOR gold][I]'+hora_event.strip()+'  [/I][COLOR lightyellow][B]'+categ_event+':[/B] [I]'+name_event+'  [COLOR lightgreen][ '+ch_event_fixed+' ][/I][/COLOR]'
                datamovie["Plot"] = '[COLOR white][B]'+categ_event+':[/B] [I]'+name_event+'\n[COLOR lightgreen][ '+ch_event_fixed+' ][/I][/COLOR]'
                datamovie["Plot"] = datamovie["Plot"].replace("&nbsp;", "").strip()
                #title_fixed = title_fixed.replace("Stream 24/24 7/7 gratuit", "[COLOR orange][24h][/COLOR]")
            else:
                title_fixed = '[COLOR gold][I]'+hora_event.strip()+'  [/I][COLOR lightyellow][B]'+categ_event+':[/B] [I]'+name_event+'  [COLOR red][Sin enlaces][/I][/COLOR]'
                datamovie["Plot"] = '[COLOR white][B]'+categ_event+':[/B] [I]'+name_event+'[/I][/COLOR]'
                datamovie["Plot"] = datamovie["Plot"].replace("&nbsp;", "").strip()
                #title_fixed = title_fixed.replace("Stream 24/24 7/7 gratuit", "[COLOR orange][24h][/COLOR]")

            thumbnail = set_icon(categ_event)

            title_fixed = title_fixed.replace("&nbsp;", "").strip() 
            plugintools.add_item(action="tous1", title=title_fixed, url="", thumbnail = thumbnail, info_labels = datamovie, fanart = fanart, folder = False, isPlayable=True)
            


   



def tous1(params):
    plugintools.setview("tvshows")
    plugintools.log("[%s %s] tous1 " % (addonName, addonId))

    canales = [];referer = 'http://www.toussports.info';ref=referer
    title = params.get("title");plugintools.log("title= "+title)
    chs = plugintools.find_multiple_matches(title, 'Ch[0-9]+ ')
    for entry in chs:
        plugintools.log("entry= "+entry)
        canales.append(entry)

    print 'canales',canales

    try:
        plugintools.setview("tvshows")
        dia = plugintools.selector(canales, 'Toussports.info')
        ch = canales[dia]
        ch = ch.replace("Ch", "http://www.toussports.info/lecteur.php?id=").strip();print ch
        datos='''data=gethttp_referer_headers(ch,referer);referer=ch;p='src="([^"]+)';ch=plugintools.find_single_match(data,p);#print data,url,referer''';
        exec(datos);exec(datos);exec(datos);exec(datos);
        datos='''data=gethttp_referer_headers(ch,referer);p='src="([^"]+)';rurl=ch;ch=plugintools.find_single_match(data,p);''';exec(datos);exec(datos);
		###DINOZAP###
        hidd='type="hidden".*?value="([^"]*)';hidd=plugintools.find_multiple_matches(data,hidd);
        try:
		 y=hidd[0].decode('base64');x=hidd[1].decode('base64');w='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';
		 z=plugintools.find_single_match(x,'(vod.*)');
		 
        except: xbmcgui.Dialog().ok('ATENCION','Cambios en la web,\nno puedo sacar el enlace!');plugintools.setview("tvshows");pass;
        try: q=x+' app='+z+' playpath='+y+' swfUrl='+w+' swfVfy=true live=true token=@@stop-stole@@ flashver=WIN\2013,0,0,214 timeout=15 pageUrl='+rurl;
        except: xbmcgui.Dialog().ok('ATENCION','Este canal no emite!');sys.exit();plugintools.setview("tvshows");pass;
        print q;plugintools.play_resolved_url(q);plugintools.setview("tvshows");sys.exit();

    except KeyboardInterrupt: pass;
    except IndexError: raise;
    except: pass


    


def tous2(params):
    plugintools.setview("tvshows")    
    url = 'http://www.streaming-foot.info/schedule.php'
    referer = 'http://www.toussports.info'
    thumbnail = 'https://pbs.twimg.com/profile_images/1649525603/tous-sports_400x400.jpg'
    fanart = 'http://img0.cfstatic.com/wallpapers/6fb443ad681c037b2ce4008d98994e7d_large.jpeg'
    
    plugintools.add_item(action="", title= '[COLOR blue][B]TOU[COLOR white]SS[COLOR red]PORTS [/B][COLOR lightyellow][I]Live channels[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)

    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)

    matches = plugintools.find_single_match(data, '<ul>(.*?)</ul>')
    #plugintools.log("matches= "+matches)

    event = plugintools.find_multiple_matches(matches, '<li class="list-group-item"(.*?)</li>')
    for entry in event:
        plugintools.log("entry= "+entry)
        time_event = plugintools.find_single_match(entry, '<span style="display:none">(.*?)</span>')
        time_event = time_event.strip()
        plugintools.log("time_event= "+time_event)
        time_fixed = time_event.split(" ")
        if len(time_fixed) >= 2:
            time_fixed = time_fixed[0]
            time_fixed = time_fixed.split("-")
            time_event = time_fixed[2]+"/"+time_fixed[1]
            plugintools.log("time_event= "+time_event)
            
        hora_event = plugintools.find_single_match(entry, '<span style="">(.*?)</span>')
        categ_event = plugintools.find_single_match(entry, '<span class="categorie">(.*?)</span>')
        name_event = plugintools.find_single_match(entry, '<span class="name_match">(.*?)</span>')
        ch_event = plugintools.find_single_match(entry, '<span class="links">(.*?)</span>')
        ch_event_fixed = ch_event.replace(" -", "").strip()
        title_fixed = '[COLOR orange][B]'+hora_event.strip()+'[/B][COLOR lightyellow]'+categ_event+' '+name_event+' [I][COLOR lightgreen][ '+ch_event_fixed+' ][/I][/COLOR]'
        channels = ch_event_fixed.split(" ")
        canales = []
        for item in channels:
            canales.append(item)
        print canales   
        
        if title_fixed.find("Stream 24/24 7/7 gratuit") >= 0:
            if ch_event_fixed[0] != "":
                title_fixed = '[COLOR lightyellow]'+name_event+' [I][COLOR lightgreen][ '+ch_event_fixed+' ][/I][/COLOR]'
                title_fixed = title_fixed.replace("Stream 24/24 7/7 gratuit", "")
            else:
                title_fixed = '[COLOR lightyellow]'+name_event+' [I][COLOR red][Sin enlaces][/I][/COLOR]'
                title_fixed = title_fixed.replace("Stream 24/24 7/7 gratuit", "")

            title_fixed = title_fixed.replace("&nbsp;", "").strip()
            plugintools.add_item(action="tous1", title=title_fixed, url="", thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable=False)
            

        

def set_icon(sport):
    plugintools.setview("tvshows")
    sport = sport.replace("&nbsp;", "").lower()
    plugintools.log("sport: "+sport)
    
    if sport.find("football") >= 0:
        thumbnail = __icons__ + 'futbol.png'
    elif sport.find("basketball") >= 0:
        thumbnail = __icons__ + 'basketball.png'
    elif sport.find("hockey") >= 0:
        thumbnail = __icons__ + 'hockey.png'
    elif sport.find("judo") >= 0:
        thumbnail = __icons__ + 'judo.gif'
    elif sport.find("darts") >= 0:
        thumbnail = __icons__ + 'dardos.png'
    elif sport.find("tennis") >= 0:
        thumbnail = __icons__ + 'tenis.png'
    elif sport.find("volleyball") >= 0:
        thumbnail = __icons__ + 'voleibol.png'
    elif sport.find("rugby") >= 0:
        thumbnail = __icons__ + 'rugby.png'
    elif sport.find("cyclisme") >= 0:
        thumbnail = __icons__ + 'ciclismo.png'
    elif sport.find("formule") >= 0:
        thumbnail = __icons__ + 'formula1.png'
    elif sport.find("handball") >= 0:
        thumbnail = __icons__ + 'handball.png'
    elif sport.find("boxe") >= 0:
        thumbnail = __icons__ + 'boxeo.png'         
    else:
        thumbnail = 'https://pbs.twimg.com/profile_images/1649525603/tous-sports_400x400.jpg'

    plugintools.setview("tvshows")
    return thumbnail

	
def gethttp_referer_headers(url,referer):
    plugintools.setview("tvshows");request_headers=[]
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
     plugintools.setview("tvshows")
    return body
