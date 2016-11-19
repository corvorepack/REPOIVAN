# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de TousSports.info para TV Ultra 7K
# Version 0.1 (05.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a Juarrox


import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import plugintools
import urllib2
import HTMLParser
import urllib,urlparse
import ssl

from BeautifulSoup import BeautifulSoup as bs
import json

from __main__ import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

def read_url(url):
    net = Net()

    html=net.http_GET(url).content
    
    h = HTMLParser.HTMLParser()
    html = h.unescape(html)
    return html


def rojap2p0(params):
    plugintools.log("[%s %s] Roja Directa P2P " % (addonName, addonVersion))

    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    url = params.get("url")
    headers={"Referer": 'http://www.tarjetarojaonline.me/'}
    r=requests.get(url, headers=headers);data=r.content;print data
    plugintools.add_item(action="", title='[B][COLOR orange]RojaDirecta [I]P2P[/I][/B][/COLOR] [COLOR lightyellow] - En exclusiva en [B]TV Ultra 7K[/B][/COLOR]', url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

    if data:
        match = re.findall('<span class="(\d+)".*?<div class="menutitle".*?<span class="t">([^<]+)</span>(.*?)</div>',data,re.DOTALL)
        for id,time,eventtmp in match:
            try:                
                import datetime
                from utils import pytzimp
                d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2014, 6, 7, hour=int(time.split(':')[0]), minute=int(time.split(':')[-1])))
                timezona= addon.get_setting('timezone_new')
                my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
                convertido=d.astimezone(my_location)
                fmt = "%H:%M"
                time=convertido.strftime(fmt)
            except:
                pass
            eventnospanish = plugintools.find_multiple_matches(eventtmp, '<span class="es">(.+?)</span>')
            if eventnospanish:
                for spanishtitle in eventnospanish:
                    eventtmp = eventtmp.replace('<span class="es">' + spanishtitle + '</span>','')
            eventclean=eventtmp.replace('<span class="en">','').replace('</span>','').replace(' ()','').replace('</time>','').replace('<span itemprop="name">','')
            matchdois = plugintools.find_multiple_matches(eventclean, '(.*)<b>\s*(.*?)\s*</b>')
            for sport,event in matchdois:
                express = '<span class="submenu" id="sub' + id+ '">.*?</span>\s*</span>'
                streams = plugintools.find_multiple_matches(data, express)
                for streamdata in streams:
                    p2pstream = re.compile('<td>P2P</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td>([^<]*)</td>\n.+?<td><b><a.+?href="(.+?)"').findall(streamdata)
                    already = False
                    for canal,language,tipo,qualidade,urltmp in p2pstream:
                        if "Sopcast" in tipo or "Acestream" in tipo:
                            if already == False:
                                title="[B][COLOR gold]"+time+ " - " + sport + " - " + event + "[/B][/COLOR]"
                                plugintools.add_item(action="", title=title, url="", thumbnail="", fanart="", extra= urllib.quote_plus(event), folder=False, isPlayable=False)
                                already = True
                            print qualidade
                            tipo=tipo.replace("(web)", "").strip()
                            qualidade.replace("<","").replace(">","")+" Kbs)";qualidade='[COLOR lightgreen][I]'+qualidade+' kbps[/I][/COLOR]'
                            canal=canal.replace("<","").replace(">","");canal='[COLOR lightyellow][B]'+canal+'[/B][/COLOR]'
                            tipo='[COLOR lightgreen]['+tipo.replace("<","").replace(">","")+'][/COLOR] '
                            language='[COLOR white]('+language.replace("<","").replace(">","")+')[/COLOR]'
                            title=tipo+canal+" - "+language+" - "+qualidade
                            url='http://rojadirecta.tn.my/'+urltmp
                            plugintools.log("URL= "+url)
                            plugintools.add_item(action="rojap2p1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
                            p2pdirect = re.compile('<td>P2P</td><td></td><td></td><td>(.+?)</td><td></td><td>.+?href="(.+?)"').findall(streamdata)
                            for tipo,link in p2pdirect:
                                if tipo == "SopCast" and "sop://" in link:
                                    url='plugin://program.plexus/?mode=2&url=%s&name=%s'%(link,urllib.quote_plus(event))
                                    plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

                    

def rojap2p1(params):
    plugintools.log("[%s %s] Roja Directa getting link... " % (addonName, addonVersion))
    url = params.get("url")
    url = url.replace("rojadirecta.tn.my/goto/", "").strip()
    name = params.get("extra")

    plugintools.log("URL= "+url)
    plugintools.log("Name= "+name)
    
    if 'serbia' in url:
        source = get_page_source(url)
        soup=bs(source)
        urls=soup.findAll('iframe')
        for urly in urls:
            if 'ttv.net' in urly['src']:
                url=urly['src']
                params["url"]=url
                params["title"]=name
                rojap2p1(params)
                return
    
    if "sop://" not in url and "acestream://" not in url:
        if "http://" not in url: 
            url="http://"+url
            
        if 'arenavision' in url:
            headers = {
                "Cookie" : "beget=begetok; has_js=1;"
            }
            
            source = requests.get(url,headers=headers).text
        else:
            source = get_page_source(url)
        if 'click here..' in source.lower():
            try:
                url=re.compile('<a href="(.+?)">click here...').findall(source)[0]                
                params["url"]=url
                params["title"]=name
                rojap2p1(params)
                return
            except:
            	pass
        elif 'iframe' in source:
        	
        	soup=bs(source)
        	urls=soup.findAll('iframe')
        	for urly in urls:
        		try:
        			cc=urly['id']
        		except:
        			cc=''
        		if 'free' in urly['src'] or 'timeanddate' in urly['src']:
        			pass
        		else:
        			if (cc=='refresh' or cc=='ifi'):
        				url=url+ '/'+ urly['src']
        				resolve_roja(url,name)
        				return
	        		elif 'ttv.net' in urly['src']:
	        			url=urly['src']
	            		params["url"]=url
	            		params["title"]=name
	            		rojap2p1(params)
	            		return

        matchsop = re.compile('sop://(.+?)"').findall(source)
        if matchsop: 
            url='plugin://program.plexus/?mode=2&url=sop://%s&name=%s'%(matchsop[0],urllib.quote_plus(name))
            xbmc.Player().play(url)
        else:
            match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
            if match: 
                url='plugin://program.plexus/?mode=1&url=%s&name=%s'%(match[0],urllib.quote_plus(name))
                xbmc.Player().play(url)
            else:
            	xbmcgui.Dialog().ok('No stream','No stream available!')
    elif "sop://" in url:
        title_fixed=params.get("title");title_fixed=parser_title(title).replace(" ", "+").strip()
        url = p2p_builder_url(url, title_fixed, p2p="sop")
        xbmc.Player().play(url)
    elif "acestream://" in url:
        title_fixed=params.get("title");title_fixed=parser_title(title).replace(" ", "+").strip()
        url = p2p_builder_url(url, title_fixed, p2p="ace")
        xbmc.Player().play(url)
    else: xbmcgui.Dialog().ok('No stream','No stream available!') 
    

def cleanex(text):
    text = text.replace(u'\xda','U').replace(u'\xc9','E').replace(u'\xd3','O').replace(u'\xd1','N').replace(u'\xcd','I').replace(u'\xc1','A').replace(u'\xf8','o').replace(u'\xf1','n')
    return text 

def get_page_source(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def p2p_builder_url(url, title_fixed, p2p):

    if p2p == "ace":
        p2p_launcher = plugintools.get_setting("p2p_launcher")
        #plugintools.log("p2p_launcher= "+p2p_launcher)        
        if p2p_launcher == "0":
            url = 'plugin://program.plexus/?url='+url+'&mode=1&name='+title_fixed
        else:
            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed

    elif p2p == "sop":
        p2p_launcher = plugintools.get_setting("p2p_launcher")
        #plugintools.log("p2p_launcher= "+p2p_launcher)
        if p2p_launcher == "0":
            url = 'plugin://program.plexus/?url='+url+'&mode=2&name='+title_fixed
        else:
            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=2&name='+title_fixed

    elif p2p == "torrent":
        url = urllib.quote_plus(url)
        addon_torrent = plugintools.get_setting("addon_torrent")
        if addon_torrent == "Stream":  # Stream (por defecto)
            url = 'plugin://plugin.video.stream/play/'+url
        elif addon_torrent == "Pulsar":  # Pulsar
            url = 'plugin://plugin.video.pulsar/play?uri=' + url        

    elif p2p == "magnet":
        addon_magnet = plugintools.get_setting("addon_magnet")
        if addon_magnet == "0":  # Stream (por defecto)
            url = 'plugin://plugin.video.stream/play/'+url
        elif addon_magnet == "1":  # Pulsar
            url = 'plugin://plugin.video.pulsar/play?uri=' + url
        elif addon_magnet == "2":  # Kmediatorrent
            url = 'plugin://plugin.video.kmediatorrent/play/'+url

    plugintools.log("[%s %s] Creando llamada para URL P2P... %s " % (addonName, addonVersion, url))
    return url
