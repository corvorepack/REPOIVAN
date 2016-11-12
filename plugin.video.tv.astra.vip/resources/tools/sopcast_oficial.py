# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de http://www.sopcast.com/chlist.xml (SopCast Oficial)
# Version 0.1 (12.11.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info) y a los tutoriales de Juarrox


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import requests
from resources.tools.resolvers import *

from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


url='http://www.sopcast.com/chlist.xml'


def sopcast_oficial0(params):
    plugintools.log("[%s %s] SopCast Oficial parser... %s " % (addonName, addonVersion, repr(params)))
  
    thumbnail = 'https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AAABgI_-Yd1k9MAJ0uiKMCsoa/sopcast%20oficial.jpg'
    fanart = 'https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AAChTJOeg7LsgPDxxos5NSyva/fondo tv.jpg'

    r = requests.get(url)
    data = r.content
    print data
    vers = plugintools.find_single_match(data,'<channels version="([^"]+)')
    plugintools.add_item(action="",url="",title="[COLOR blue][B]SopCast Official List[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    plugintools.add_item(action="",url="",title='[COLOR red][B]'+vers+'[/B][/COLOR]',thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
    group_channel = plugintools.find_multiple_matches(data,'<channel(.*?)</channel>')
    
    for item in group_channel:
        plugintools.log("item= "+item)
        url_sop = plugintools.find_single_match(item,'<item>(.*?)</item>')
        plugintools.log("url_sop= "+item)
        canal = plugintools.find_single_match(item,'<name en="([^"]+)').replace("&amp;", "&")
        plugintools.log("canal= "+canal)
        pais = plugintools.find_single_match(item,'<region en="([^"]+)')
        plugintools.log("pais= "+pais)
        genero = plugintools.find_single_match(item,'<class en="([^"]+)').strip()
        plugintools.log("genero= "+genero)
        kbps = plugintools.find_single_match(item,'<kbps>(.*?)</kbps>')
        plugintools.log("kbps= "+kbps)
        title = '[COLOR blue][B]['+genero+'][/COLOR]'+' [COLOR white] '+canal+' (' + pais + ') [/COLOR][COLOR green][' + kbps + ' Kbps]' + '[/B][/COLOR]'


	#url_montada = 'plugin://program.plexus/?mode=2&url=' + url_sop
	url_montada = p2p_builder_url(url_sop, title, "sop")
	plugintools.log("url_montada= "+url_montada)
	plugintools.add_item(action="play", title=title, url=url_montada, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)


      
   
