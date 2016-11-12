# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie Ultra 7K Parser de Sport7.ru
# Version 0.1 (17.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


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

import plugintools
import json

from __main__ import *
from resources.tools.media_analyzer import *


addonName = xbmcaddon.Addon().getAddonInfo("name")
addonVersion = xbmcaddon.Addon().getAddonInfo("version")
addonId = xbmcaddon.Addon().getAddonInfo("id")
addonPath = xbmcaddon.Addon().getAddonInfo("path")

thumbnail="http://sport7.ru/images/sport_logo.png"
fanart = "http://2.cdn.nhle.com/lightning/v2/ext/wallpaper/arena_fans_wallpaper_1680x1050.jpg"


def sport7_0(params):
    plugintools.log("[%s %s] SPORT7.ru %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="", title='[COLOR white][B]SPORT[COLOR green]7[/B][/COLOR].ru[/COLOR]' , url="", thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)    
    data = plugintools.read('http://sport7.ru/onlain_sopcast')
    bloque = plugintools.find_single_match(data, '<div class="block_news">(.*?)<div id="r_okno">')
    matches = plugintools.find_multiple_matches(bloque, 'href="http://sport7.ru/match/([^"]+)')
    for entry in matches:
        url_event='http://sport7.ru/match/'+entry
        title_event=plugintools.find_single_match(bloque, entry+'\"\>(.*?)</a>')
        plugintools.add_item(action="sport7_1", title='[COLOR white]'+title_event+' [/COLOR][COLOR blue][I]Live![/I][/COLOR]', url=url_event, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

    # Canales Acestream/Sopcast
    matches = plugintools.find_single_match(data, 'class=\"head-match\"(.*?)class=\"mar-top5 jus\"')
    title = plugintools.find_multiple_matches(matches, '<h2>(.*?)</h2>')
    for entry in title:
        plugintools.log("entry= "+entry)
        canal = plugintools.find_single_match(matches, '<h2>'+entry+'(.*?)class=\"com_bl utext\"')
        plugintools.log("canal= "+canal)
        title = convertrus(entry)
        plugintools.log("title= "+title)
        bitrate = plugintools.find_single_match(canal, '<div class=\"rc\">(.*?)</div>')
        plugintools.log("bitrate= "+bitrate)
        url_p2p = 'sop://'+plugintools.find_single_match(canal, "sop://([^\?]+)")
        plugintools.log("url_p2p= "+url_p2p)
        type_p2p = plugintools.find_single_match(canal, 'alt="([^ ]+)')
        plugintools.log("type_p2p= "+type_p2p)
        if type_p2p.startswith("Sopcast") == True:
            title = '[COLOR lightyellow]' + title + ' [/COLOR][COLOR lightblue] [Sopcast] [/COLOR][COLOR green][I]['+bitrate+'][/I][/COLOR]'
            url_media=p2p_builder_url(url_p2p, 'sport7', p2p="sop")
            plugintools.add_item(action="play", title=title, url=url_media, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
        elif type_p2p.startswith("Acestream)") == True:
            title = '[COLOR lightyellow]' + title + ' [/COLOR][COLOR lightblue] [Acestream] [/COLOR][COLOR green][I]['+bitrate+'][/I][/COLOR]'
            data = plugintools.read(url_p2p)
            url_media=plugintools.find_single_match(data, '<a href="([^"]+)')
            plugintools.log("url_media= "+url_media)
            url_media=p2p_builder_url(url_media, 'sport7', p2p="sop")
            plugintools.add_item(action="play", title=title, url=url_media, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
        


def sport7_1(params):
    plugintools.log("[%s %s] SPORT7.ru %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    data = plugintools.read(url)

    # Eventos LIVE                       
    bloque = plugintools.find_single_match(data, 'dellink(.*?)<div class')
    plugintools.log("bloque= "+bloque)
    urls=plugintools.find_multiple_matches(bloque, 'href="([^"]+)')
    i=1
    for entry in urls:
        data=plugintools.read(entry)
        url_media=plugintools.find_single_match(data, '<a href="([^"]+)')
        if url_media.startswith("acestream") == True:
            url=p2p_builder_url(url_media, 'sport7', p2p="ace")
            plugintools.add_item(action="", title='Link '+str(i)+' [COLOR lightblue][Acestream][/COLOR]', url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
            i=i+1
        elif url_media.startswith("sop") == True:
            url=p2p_builder_url(url_media, 'sport7', p2p="sop")
            plugintools.add_item(action="", title='Link '+str(i)+' [COLOR red][Sopcast][/COLOR]', url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
            i=i+1
        
    

def convertrus(title):
    plugintools.log("[%s %s].Sport7.ru convert-rus: %s" % (addonName, addonVersion, title))

    title = title.strip()

    if title == "КХЛ ТВ":
        title = 'KHL HD'
    if title == 'Трансляции матчей КХЛ':
        title = 'KHL'
    if title == 'Трансляции матчей НХЛ':
        title = 'KHL'
    if title.find("футбол") >= 0:
        title = title.replace("футбол", "Fútbol")

    return title        
  
