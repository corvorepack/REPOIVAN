# -*- coding: utf-8 -*-
#------------------------------------------------------------
# TV Ultra 7K parser de mebuscan.net
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

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools

from __main__ import *


thumbnail = 'https://dl.dropbox.com/s/au5yyg825zaoo1k/Acestream%20sport.jpg'
fanart = 'http://metcalfmultisports.co.uk/images/bg.jpg'



def mebuscan(params):
    plugintools.log("[tv.ultra.7k].Mebuscan.net( "+repr(params))
    plugintools.add_item(action="", title = '[B][COLOR blue]Acestream Sports Playlist[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)    

    url = params.get("url")
    data = plugintools.read(url)
    plugintools.log("data= "+data)

    matches = plugintools.find_multiple_matches(data, '<td  class="classcelda"(.*?)</td>')    
    for entry in matches:
        plugintools.log("entry= "+entry)
        canal_url = plugintools.find_single_match(entry, 'onclick=(.*?)><strong>')
        canal_url = canal_url.replace("ventananueva(", "")
        canal_url = canal_url.replace(")", "")
        canal_url = 'http://www.mebuscan.net/kos/Depo'+canal_url+'.php'
        plugintools.log("canal_url= "+canal_url)
        thumb_canal = plugintools.find_single_match(entry, 'src="([^"]+)')
        thumb_canal = 'http://www.mebuscan.net/'+thumb_canal
        plugintools.log("thumb_canal= "+thumb_canal)
        canal_title = plugintools.find_single_match(entry, '<br>(.*?)</strong>')
        plugintools.log("canal_title= "+canal_title)
        plugintools.add_item(action="mebuscan_geturl" , title = canal_title, url = canal_url , thumbnail = thumb_canal , fanart = fanart , isPlayable = True, folder = False)

        
def mebuscan_geturl(params):
    plugintools.log("[tv.ultra.7k].mebuscan_geturl( "+repr(params))

    url = params.get("url")
    title = params.get("title")
    data = plugintools.read(url)
    plugintools.log("data= "+data)

    # Control Acestream
    ace_id = plugintools.find_single_match(data, 'var httpid="([^"]+)')
    plugintools.log("ace_id= "+ace_id)
    url = 'http://content.torrent-tv.ru/'+ace_id+'.acelive'
    title_fixed = parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
    url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='+title_fixed
    plugintools.log("url_ace= "+url)
    plugintools.play_resolved_url(url)
    
