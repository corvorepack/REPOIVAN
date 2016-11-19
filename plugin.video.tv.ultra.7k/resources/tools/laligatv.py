# -*- coding: utf-8 -*-
#------------------------------------------------------------
# TV Ultra 7K Parser de laligatv.es
# Version 0.1 (18.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)

from __main__ import *

def laligatv0(params):
    plugintools.log("[tv.ultra.7k-0.3.0].laligatv.es Playlist Sport Channels( "+repr(params))

    thumbnail = params.get("thumbnail")
    plugintools.log("thumbnail= "+thumbnail)
   
    plugintools.add_item(action="", title = '[B][I][COLOR darkviolet]LALIGATV.ES[/B][/I][/COLOR]', url = "", thumbnail = 'http://files.lfp.es/201402/640x360_06172611noticia-la-liga-tv.es.jpg' , fanart = 'https://fbcdn-sphotos-b-a.akamaihd.net/hphotos-ak-ash3/556377_550288405007723_1790184113_n.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="", title = '[B][I][COLOR white]Las emisiones comenzarán 15 minutos antes de cada partido[/B][/I][/COLOR]', url = "", thumbnail = 'http://files.lfp.es/201402/640x360_06172611noticia-la-liga-tv.es.jpg' , fanart = 'https://fbcdn-sphotos-b-a.akamaihd.net/hphotos-ak-ash3/556377_550288405007723_1790184113_n.jpg' , folder = True, isPlayable = False)
    
    url = 'http://www.lfp.es/laligatv'
    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    title = params.get("title")
    plugintools.log("title= "+title)
    data = plugintools.read(url)
    match_total = plugintools.find_single_match(data, 'id=\"coming-soon\"(.*?)fb-root')
    plugintools.log("match_total= "+match_total)
    matches_dia = plugintools.find_single_match(data, 'id=\"coming-soon\"(.*?)</div></div>')
    plugintools.log("matches_dia= "+matches_dia) 
    jornada = plugintools.find_multiple_matches(match_total, 'class=\"title_jornada\">(.*?)</div>')
    if not jornada:eval(noevent);exit()
    #print 'jornada',jornada       
    matches = plugintools.find_multiple_matches(matches_dia, '<a class=\'directo-webtv clearfix\' href="(.*?)<\/a>')
    plugintools.add_item(action="" , title = '[COLOR yellow][B]' + jornada[0] + '[/B][/COLOR]' , thumbnail = thumbnail , folder = False , isPlayable = False)
    
    for entry in matches:
        plugintools.log("entry= "+entry)
        url_partido = entry.split('"')
        url_partido = url_partido[0]
        url_partido = url_partido.strip()
        plugintools.log("url_partido= "+url_partido)
        hora = plugintools.find_single_match(entry, 'hora_partido_otras_competiciones\">(.*?)</span>')
        plugintools.log("hora= "+hora)
        try:
         local = plugintools.find_single_match(entry, 'partido_aspire".*?>(.*?)</span>')
         plugintools.log("local= "+local)
         plugintools.add_item(action="adelante_geturl" , title = '[COLOR lightyellow][B](' + hora + ')[/B][/COLOR][COLOR white] ' + local + ' [/COLOR]' , url = url_partido , thumbnail = params.get("thumbnail") , folder = False , isPlayable = True)
        except:
         local = plugintools.find_single_match(entry, 'equipo_local_otras_competiciones\">(.*?)</span>')
         visitante = plugintools.find_single_match(entry, 'equipo_visitante_otras_competiciones\">(.*?)</span>')
         plugintools.log("local= "+local)
         plugintools.log("viistante= "+visitante)
         plugintools.add_item(action="adelante_geturl" , title = '[COLOR lightyellow][B](' + hora + ')[/B][/COLOR][COLOR white] ' + local + ' - ' + visitante + ' [/COLOR]' , url = url_partido , thumbnail = params.get("thumbnail") , folder = False , isPlayable = True)

    for i in range(1,len(jornada),1):
        plugintools.add_item(action="" , title = '[COLOR yellow][B]' + jornada[i] + '[/B][/COLOR]' , thumbnail = thumbnail , folder = False , isPlayable = False)
        matches_dia = plugintools.find_single_match(match_total, jornada[i]+'(.*?)</div></div>')
        #plugintools.log("matches_dia= "+matches_dia)
        matches = plugintools.find_multiple_matches(matches_dia, '<a class=\'directo-webtv clearfix\' href="(.*?)<\/a>')
        for entry in matches:
            plugintools.log("entry2= "+entry)
            url_partido = entry.split('"')
            url_partido = url_partido[0]
            url_partido = url_partido.strip()
            plugintools.log("url_partido2= "+url_partido)
            hora = plugintools.find_single_match(entry, 'hora_partido_otras_competiciones\">(.*?)</span>')
            plugintools.log("hora2= "+hora)
            try:
             local = plugintools.find_single_match(entry, 'partido_aspire".*?>(.*?)</span>')
             plugintools.log("local2= "+local)
             plugintools.add_item(action="adelante_geturl" , title = '[COLOR lightyellow][B](' + hora + ')[/B][/COLOR][COLOR white] ' + local + ' [/COLOR]' , url = url_partido , thumbnail = params.get("thumbnail") , folder = False , isPlayable = True)
            except:
             local = plugintools.find_single_match(entry, 'equipo_local_otras_competiciones\">(.*?)</span>')
             visitante = plugintools.find_single_match(entry, 'equipo_visitante_otras_competiciones\">(.*?)</span>')
             plugintools.log("local2= "+local)
             plugintools.log("viistante2= "+visitante)
             plugintools.add_item(action="adelante_geturl" , title = '[COLOR lightyellow][B](' + hora + ')[/B][/COLOR][COLOR white] ' + local + ' - ' + visitante + ' [/COLOR]' , url = url_partido , thumbnail = params.get("thumbnail") , folder = False , isPlayable = True)       
    
        
               


def adelante_geturl(params):
    plugintools.log("[tv.ultra.7k-0.3.0].LaLigatv.es getURL: "+repr(params))

    data = plugintools.read(params.get("url"))
    #plugintools.log("data= "+data)
    '''
    try: url = plugintools.find_single_match(data, 'src: escape\(\"(.*?)\"')
    except: url=plugintools.find_single_match(data,'stream:\s?\'([^\'"]+)')	
    '''
    #url=plugintools.find_single_match(data,'stream:\s?\'([^\'"]+)')	
    try:
     url = plugintools.find_single_match(data, 'src: escape\(\"(.*?)\"')    
     plugintools.log("URL PARTIDO= "+url)
    except:pass
    plugintools.play_resolved_url(url) if url else eval(nolink)
        
        
