# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie Ultra 7K Parser de onhockey.tv
# Version 0.4 (05.11.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys
import plugintools

from __main__ import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'http://cs419622.vk.me/v419622246/ad9a/6lhLpe59E2Q.jpg'
fanart = 'http://www.wallpapersbee.com/sports/NHL-hockey-stick-widescreen-2560x1600-wallpaper.jpg'

'''
<subchannel>
        <name>OnHockey.TV</name>
        <thumbnail>http://cs419622.vk.me/v419622246/ad9a/6lhLpe59E2Q.jpg</thumbnail>
        <fanart>http://www.zastavki.com/pictures/1920x1200/2011/Sport_Hockey_Jose_Theodore__NHL_027113_.jpg</fanart>
        <update>19/10/2015 00:55</update>
        <version>0.2</version>
        <author>Juarrox</author>
        <changelog>[B]OnHockey.TV[/B] es un portal ruso que recoge enlaces de streaming de alta calidad de todos los partidos de Hockey de las principales ligas del Mundo.[CR][CR][COLOR red]NOTA:[/COLOR] Bugs o sugerencias a [B]juarrox@gmail.com[/B]</changelog>
        <path>resources/tools/peliculasdk.py</path>
        <url>https://copy.com/oGKXnuuOel2HPnHR</url>
</subchannel>

'''

def onhockey(params):
        plugintools.log("[movie.ultra.7k 0.3.0].Onhockey")

        datamovie = {}
        datamovie["Plot"]='[B]OnHockey.TV[/B] es un portal de streaming en vivo de las mejores ligas de Hockey, resultados en vivo y chat en varios idiomas.[CR][CR]En exclusiva en [COLOR lightyellow]movie.ultra.7k[/COLOR]'
	plugintools.addShow(action="", title= '[COLOR red][B]O N  [/COLOR][COLOR blue] H O C K E Y[/COLOR][COLOR white]  .T V[/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , info_labels=datamovie, fanart = fanart, folder = False, isPlayable = False)
	datamovie["Plot"]='La hora aparece de acuerdo al horario de Londres (GMT +1), mostrándose en color [B][COLOR green]verde[/B][/COLOR] cuando se activan los enlaces minutos antes del inicio de cada partido.'
	plugintools.addShow(action="", title= '[COLOR white][B]Horario de Londres (GMT +1)[/COLOR][/B]', url = "", thumbnail = thumbnail , fanart = 'https://scontent-mad1-1.xx.fbcdn.net/hphotos-ash2/v/t1.0-9/10154532_10203598321336679_8880512652119508392_n.jpg?oh=0c0a0f5a2fb411a8f5445e9149e4c8e0&oe=569B2B5B', info_labels=datamovie, folder = False, isPlayable = False)
	
	# Vamos a obtener la programación de OnHockey.TV
	url = 'http://onhockey.tv/schedule_table_eng.php?_=1444691616045'
	referer = 'http://www.onhockey.tv/'
	schedule = gethttp_referer_headers(url,referer)
	plugintools.log("programación?= "+schedule)
	NHL = plugintools.find_single_match(schedule, '<b>NHL</b>(.*?)<b>')
	if NHL == "":
                NHL = plugintools.find_single_match(schedule, '<b>NHL</b>(.*?)</table>')  # Se controla el caso en que solo haya eventos NHL
	hockeygames(NHL, 'NHL')
	KHL = plugintools.find_single_match(schedule, '<b>KHL</b>(.*?)<td class')
	if KHL == "":
                KHL = plugintools.find_single_match(schedule, '<b>KHL</b>(.*?)</table>')  # Se controla el caso en que solo haya eventos KHL
	hockeygames(KHL, 'KHL')
	KHC = plugintools.find_single_match(schedule, '<b>KHC</b>(.*?)<td class')
	Liiga = plugintools.find_single_match(schedule, '<b>Liiga</b>(.*?)<td class')
	hockeygames(Liiga, 'Liiga')
	PHL = plugintools.find_single_match(schedule, '<b>PHL</b>(.*?)<td class')
	hockeygames(PHL, 'PHL')
	SHL = plugintools.find_single_match(schedule, '<b>SHL</b>(.*?)<td class')
	hockeygames(SHL, 'SHL')
	VHL = plugintools.find_single_match(schedule, '<b>VHL</b>(.*?)<td class')
	hockeygames(VHL, 'VHL')
	Allsvenskan = plugintools.find_single_match(schedule, '<b>Allsvenskan</b>(.*?)<td class')
	#eventosVHL-B = plugintools.find_single_match(schedule, '<b>VHL-B</b>(.*?)</script>')

        xbmc.executebuiltin("Container.SetViewMode(515)")

    
def hockeygames(hockeyliga, nameliga):
    # Asociamos logo de la liga
    if nameliga == "NHL":
        thumbnail = 'http://www.sports-logos-screensavers.com/user/NHL_Logo_New2.jpg'
        fanart = 'http://www.zastavki.com/pictures/1920x1200/2011/Sport_Hockey_Jose_Theodore__NHL_027113_.jpg'
    elif nameliga == "KHL":
        thumbnail = 'https://upload.wikimedia.org/wikipedia/en/thumb/c/c1/KHL_logo_shield.svg/200px-KHL_logo_shield.svg.png'
        fanart = 'http://promoovertime.com/wp-content/uploads/2014/11/Arena-Zagreb-1080x675.jpg'
    elif nameliga == "Liiga":
        thumbnail = 'https://upload.wikimedia.org/wikipedia/en/c/cd/Liiga_logo.png'
        fanart = 'https://i.vimeocdn.com/video/448377853_640.jpg'
    elif nameliga == "SHL":
        thumbnail = 'http://testbed.krank.se/shl/shl_logga.jpg'
        fanart = 'http://i42.tinypic.com/qzj72g.jpg'
    elif nameliga == "VHL":
        thumbnail = 'https://upload.wikimedia.org/wikipedia/en/thumb/3/39/Supreme_Hockey_League.svg/180px-Supreme_Hockey_League.svg.png'
        fanart = 'http://www.stickwithcarter.com/wp-content/uploads/2010/07/goalie_making_save-1.jpg'
    elif nameliga == "PHL":
        thumbnail = 'https://upload.wikimedia.org/wikipedia/fr/6/64/PHL.png'
        fanart = 'http://www.przegladsportowy.pl/m/Repozytorium.Podglad.aspx/1200/0/przegladsportowy/635620528189574532.jpg'
        
    # Obtenemos lista de canales y su clave
    eventos = plugintools.find_multiple_matches(hockeyliga, '<tr(.*?)</div>')
    for entry in eventos:            
        canales_dict = []
        tipo_dict = []
        plugintools.log("EVENTO= "+entry)
        #<tr><td><text class="game_hour" align="left">00</text>:00</td><td>Philadelphia - New Jersey</td>
        hora = plugintools.find_single_match(entry, "<td>(.*?)</td><td>")
        hora = hora.replace("<text class='game_hour' align='left'>","")
        hora = hora.replace("</text>", "")
        plugintools.log("hora= "+hora)
        partido = plugintools.find_single_match(entry, '</td><td>(.*?)\n')
        title_fixed = partido.replace(" \x96 "," vs ")
        title_fixed = title_fixed.replace(" - "," vs ")
        partido = title_fixed.replace("vs"," ")  
        partido = title_fixed.replace("-","")
        partido = title_fixed.replace("\x96","")  
        #partido = title_fixed.replace(" ","")
        plugintools.log("partido= "+partido)
        channels = plugintools.find_multiple_matches(entry, "<a href='([^']+)")
        channelist = ""
        datamovie = {}
        for entry in channels:
            plugintools.log("channel= "+entry)
            entry='http://onhockey.tv/'+entry
            if channelist == "":
                channelist = entry
            else:
                channelist = channelist + ', '+entry

        print channelist
        datamovie["Plot"]=channelist
        if len(channelist) >= 1:
            plugintools.addShow(action="multihockey", title='[COLOR green][B]'+hora+'[/B][/COLOR] [COLOR lightyellow][B]'+nameliga+'[/B][/COLOR] [COLOR white]'+partido+'[/COLOR]', url="", thumbnail = thumbnail, fanart = fanart, plot=channelist, info_labels=datamovie, folder=False, isPlayable=True)
        else:
            plugintools.addShow(action="", title='[COLOR red][B]'+hora+'[/B][/COLOR] [COLOR lightyellow][B]'+nameliga+'[/B][/COLOR] [COLOR white]'+partido+'[/COLOR]', url="", thumbnail = thumbnail, fanart = fanart, folder=False, isPlayable=True)

        xbmc.executebuiltin("Container.SetViewMode(515)")

                             
def multihockey(params):
    plugintools.log("[%s %s] Onhockey multilink " % (addonName, addonVersion))
    channelist = params.get("plot")
    channelist = channelist.split(", ")
    partido = params.get("title")

    serverlist = []
    for item in channelist:
        if item.find("youtube") >= 0:
            serverlist.append(partido+" [Youtube]")
        elif item.find("castalba") >= 0:
            serverlist.append(partido+" [Castalba]")
        elif item.find("sawlive") >= 0:
            serverlist.append(partido+" [Sawlive]")
        elif item.find("acestream") >= 0:
            serverlist.append(partido+" [Acestream]")
        elif item.find("sopcast") >= 0:
            serverlist.append(partido+" [Sopcast]")
        elif item.find("liveall") >= 0:
            serverlist.append(partido+" [Liveall]")
        else:
            serverlist.append(partido+" [Flash]")

    xbmc.executebuiltin("Container.SetViewMode(515)")
    try:
            selector = plugintools.selector(serverlist, partido)
            if selector > -1:
                    url = channelist[selector]
                    if url.find("acestream") >= 0:
                        #http://onhockey.tv/youtube.php?channel=sDD697xbZ5A, http://onhockey.tv/liveall.php?channel=fbfdb35g, http://onhockey.tv/streamhd.php?channel=4, http://onhockey.tv/worldsport.php?channel=7, http://onhockey.tv/live9.php?channel=30, http://onhockey.tv/cricfree.php?channel=premiersports, http://onhockey.tv/acestream.php?channel=fb2080a96e762e926a33e61c70bd74edb2beabdf, http://onhockey.tv/acestream.php?channel=548d364053e6650458e3f347dfbda0dd852781da, http://onhockey.tv/sopcast.php?channel=146666
                        # http://onhockey.tv/acestream.php?channel=548d364053e6650458e3f347dfbda0dd852781da
                        ace=url.replace("http://onhockey.tv/acestream.php?channel=", "")
                        url = p2p_builder_url(ace, 'hockey', p2p="ace")
                        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
                    elif url.find("sopcast") >= 0:
                        # http://onhockey.tv/sopcast.php?channel=146666
                        sop=url.replace("http://onhockey.tv/sopcast.php?channel=", "")
                        url = p2p_builder_url(sop, 'hockey', p2p="sop")
                        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
                    elif url.find("youtube") >= 0:
                        # http://onhockey.tv/youtube.php?channel=sDD697xbZ5A
                        yt_url = url.replace("http://onhockey.tv/youtube.php?channel=", "")
                        url='plugin://plugin.video.youtube/play/?video_id='+yt_url
                        plugintools.log("URL= "+url)
                        plugintools.play_resolved_url(url)
                    else:
                        ref='http://onhockey.tv/'
                        url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url+'%26referer='+ref        
                        plugintools.log("URL= "+url)
                        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
                        
    except KeyboardInterrupt: pass;
    except IndexError: raise

    xbmc.executebuiltin("Container.SetViewMode(515)")
    
                    
def url_onhockey(url,tipo):
    plugintools.log("[movie.ultra.7k-0.3.0.URL_onHockey "+url)
    plugintools.log("tipo?= "+tipo)
    plugintools.log("url?= "+url)
    referer = 'http://www.onhockey.tv/'
    data = gethttp_referer_headers(url, referer)
    print data
    if data != -1:
        #plugintools.log("data= "+data)
        final_url = plugintools.find_single_match(data, '<iframe src="([^")]+)')
        if final_url == "":
            final_url = plugintools.find_single_match(data, 'SRC=\'(.*?)\'>')
            plugintools.log("final_url= "+final_url)
        else:
            plugintools.log("final_url= "+final_url)
            if final_url.find("sawlive") >= 0:
                referer = 'http://www.onhockey.tv/'
                from sawlive import *
                wizz1(final_url, referer)
            if url.find("castalba") >= 0:
                #http://castalba.tv/embed.php?cid=24411&wh=640&ht=410&r=onhockey.tv
                if final_url.find("channel") >= 0:
                    cid = final_url.split("=")
                    print cid
                    if len(final_url) >= 2:
                        cid = cid[1]
                        plugintools.log("cid= "+cid)
                else:
                    final_url = plugintools.find_single_match(data, 'src=\'(.*?)\'>')
                    channel = final_url.split("channel=")
                    print cid
                    if len(final_url) >= 2:
                        cid = cid[1]
                if cid != "":
                    final_url = 'swfUrl=http://static.castalba.tv/player5.9.swf pageUrl=http://castalba.tv/embed.php?cid='+cid+'&wh=640&ht=410&r=onhockey.tv'
                    from castalba import *
                    params = plugintools.get_params()
                    params["url"]=final_url
                    castalba(params)
                
    else:
        plugintools.log("Error URL del canal")

    xbmc.executebuiltin("Container.SetViewMode(515)")
        
   

def gethttp_headers(url):
        plugintools.log("movie.ultra.7k-0.3.0.gethttp_referer_headers "+url)
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
        return data
        xbmc.executebuiltin("Container.SetViewMode(515)")


def gethttp_referer_headers(url,referer):
        plugintools.log("movie.ultra.7k-0.3.0.gethttp_referer_headers "+url)
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        request_headers.append(["Referer",referer])
        data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
        return data
        xbmc.executebuiltin("Container.SetViewMode(515)")
        

