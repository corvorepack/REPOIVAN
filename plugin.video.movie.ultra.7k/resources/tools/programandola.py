# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Programando.la Movie Ultra 7K
# Version 0.1 (23.11.2015)
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

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

#plugintools.modo_vista("tvshows")


url = 'http://programando.la/'
url_ref = 'http://programando.la/'

mi_firma = "Movie Ultra 7K"

def programandola0(params):
	plugintools.log("[%s %s] Parser Programando.la... %s " % (addonName, addonVersion, repr(params)))

	thumbnail = 'http://nodogeek.com/wp-content/uploads/2013/01/programando-la-cursos-gratis-programacion.jpg'
	fanart = 'http://www.comolohago.cl/wp-content/uploads/2008/05/phpcode.jpg'
	
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	r = requests.get(url)	
	data = r.content

	plugintools.add_item(action="",url="",title="[COLOR blue][B]Programando [COLOR white](VideoTutoriales)[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	cada_categoria = plugintools.find_multiple_matches(data,'title="Dificultad(.*?)/h2>')	
	for item in cada_categoria:
		categoria = plugintools.find_single_match(item,'">(.*?)<')
		plugintools.add_item(action="pilla_tutos",title="[COLOR white][B]"+categoria+"[/B][/COLOR]", extra=categoria, url=url,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
		

	
	
	
## Cargo las Diferentes Categorías
def pilla_tutos(params):
	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	titulo = params.get("extra")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	r = requests.get(url)	
	data = r.content
	
	plugintools.add_item(action="",url="",title="[COLOR blue][B]····· "+titulo+" ·····[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	acota = '">'+titulo+'(.*?)'+'</ul>'
	grupo_videos = plugintools.find_single_match(data,acota)
	cada_video = plugintools.find_multiple_matches(grupo_videos,'class="video_es"(.*?)/a>')	

	for item in cada_video:
		
		url_video=plugintools.find_single_match(item,'href="(.*?)"')
		titulo_video=plugintools.find_single_match(item,'_blank">(.*?)<').replace("&oacute;","ó").replace("&eacute;","é").replace("&iacute;","í").replace("&ntilde;","ñ").replace("&aacute;","á").replace("&aacute;","í")
		
		if url_video.startswith("http://www.youtube.com")== True:
			referencia = "http://www.youtube.com/"
		else:
			referencia = url_ref
			
		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_video+'%26referer='+referencia
		plugintools.add_item(action="runPlugin", title="[COLOR white][B]"+titulo_video+"[/B][/COLOR]", url=url_montada, thumbnail=thumbnail, fanart=fanart, folder = False, isPlayable=True)


		
	