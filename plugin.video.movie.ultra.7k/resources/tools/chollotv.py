# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie Ultra 7K
# Version 0.2 (09.01.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


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




url = 'http://www.chollotv.com/page/2/'
url_ref = 'http://iframe.chollotv.com/'

def chollotv0(params):
	plugintools.log("[%s %s] Parser CholloTV.com... %s " % (addonName, addonVersion, repr(params)))

	thumbnail = 'https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg'
	fanart = 'https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AAChTJOeg7LsgPDxxos5NSyva/fondo tv.jpg'

	plugintools.add_item(action="",url="",title="[COLOR blue][B]Chollo [COLOR white]TV[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]Cine y Series[/B][/COLOR]", url="http://www.chollotv.com/category/cine-y-series/",thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", extra="Cine y Series", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]Deportes[/B][/COLOR]", url="http://www.chollotv.com/category/deportes/",thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", extra="Deportes", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]Infantiles[/B][/COLOR]", url="http://www.chollotv.com/category/infantiles/",thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", extra="Infantiles", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]Documentales[/B][/COLOR]", url="http://www.chollotv.com/category/documentales/",thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", extra="Documentales", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]Entretenimiento[/B][/COLOR]", url="http://www.chollotv.com/category/entretenimiento/",thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", extra="Entretenimiento", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]Música[/B][/COLOR]", url="http://www.chollotv.com/category/musica/",thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", extra="Música", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]TDT[/B][/COLOR]", url="http://www.chollotv.com/category/nacionales/",thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", extra="TDT", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]Autonómicas[/B][/COLOR]", url="http://www.chollotv.com/category/autonomicas/",thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", extra="Autonómicas", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR white][B]Extranjeras[/B][/COLOR]", url="http://www.chollotv.com/category/internacionales/", extra="Extranjeras", thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="chollo_categoria",title="[COLOR red][B]Adultos[/B][/COLOR]", url="http://www.chollotv.com/category/adultos/", extra="Adultos", thumbnail="https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AABmQBAUIKDt_k89dKnUP6nGa/Chollo%20tv.jpg", fanart=fanart, folder=True, isPlayable=False)

	
	
	
## Cargo las Diferentes Categorías
def chollo_categoria(params):
	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	titulo = params.get("extra")
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	r=requests.get(url, headers=headers)
	#r = requests.get(url)	
	data = r.content

	
	plugintools.add_item(action="",url="",title="[COLOR blue][B]·····"+titulo+"·····[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	group_channel = plugintools.find_single_match(data,'Categorias</a></li><li class="active"(.*?)class="pagination')
	cada_canal = plugintools.find_multiple_matches(group_channel,'<li class="col-lg-6">(.*?)<p class="details">')	

	for item in cada_canal:
		
		''' caracteres especiales en A&E !!!   Cipri'''
		titulo_canal=plugintools.find_single_match(item,'title="(.*?)"')
		caratula_canal=plugintools.find_single_match(item,'src="(.*?)"')
		url_primaria=plugintools.find_single_match(item,'href="(.*?)/"')
		plugintools.add_item(action="chollo_enlaces",title=titulo_canal,url=url_primaria,thumbnail=caratula_canal,fanart=fanart,folder=False,isPlayable=False)

		#En vez de localizar al principio TODAS las Url_Final (q ralentiza mucho pues paso x 3 webs),
		#guardo tan solo la Url_Primaria y cuando de seleccione el canal en concreto, es cuando lo mando
		#a Chollo_Enlaces() para localizar la Url_Final y lanzarla... Acelera el proceso q te cagas!!!.... GRACIAS CIPRI!!!

		
	#Resuelvo la posibilidad de mas de 1 Página en la Categoría Versión Cipri
	try:
	 mas_pag='<ul\sclass=[\'"]pagination pagination-success[\'"]>(.*?)<\/ul>'
	 mas_pag=plugintools.find_single_match(data,mas_pag);
	 
	 current='<li\sclass=[\'"]active[\'"]><a\shref=[\'"]\#[\'"]>(\d)<\/a><\/li>.*?href=[\'"]([^\d]+)'
	 current=plugintools.find_multiple_matches(data,current)
	 link=current[0][1];current=current[0][0];
	 tot_pag='>(\d)<\/a>'
	 tot_pag=plugintools.find_multiple_matches(data,tot_pag)
	 for x in xrange(int(current),len(tot_pag)):
		it=link+str(x+1)+'/';
		plugintools.add_item(action='chollo_categoria',title="[COLORred][B]Página: " + str(x+1) + "  >>>[/B][/COLOR]", url=it, extra=titulo, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False);
	except:pass


	
def chollo_enlaces(params):
	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")

	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	r1=requests.get(url, headers=headers)
	data1 = r1.content
	#saco una url así: http://iframe.chollotv.com/channel/ver-canal-plus-liga-2-d que TAMPOCO sirve para llamada SportsDevil
	url_sec=plugintools.find_single_match(data1,'src="http://iframe(.*?)" frameborder')
	url_secundaria='http://iframe'+url_sec

	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url_secundaria}
	r2=requests.get(url_secundaria, headers=headers)
	data2 = r2.content
	#saco una url así: http://iframe.chollotv.com/embed/watch-bt-sport-2-live-streaming-online que ESTA SÍ sirve para llamada SportsDevil
	url_final=plugintools.find_single_match(data2,'var url = "(.*?)";')
	
	#09/01/2015: Como estan añadiendo algunos canales q no son PrivateStream ni DinoZap, sino m3u8, por si acaso leo tb esta última web y detecto si es uno de los m3u8 cuya estructura en la web es diferente
	#Sería así: src="http://iframe.chollotv.com/stream.php?file=http://a3live-lh.akamaihd.net/i/a3shds/geoa3series_1@122775/master.m3u8&title=atreseries"  y me quedaría con el enlace hasta el .m3u8
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url_secundaria}
	r2=requests.get(url_final, headers=headers)
	data2 = r2.content

	url_control=plugintools.find_single_match(data2,'id="video_display"(.*?)</div>')
	if "file=" in url_control:  # Es q NO es un PrivateStream, dinozap, etc... es un m3u8
		url_final=plugintools.find_single_match(url_control,'file=(.*?)&title')
	else:
		url_final=plugintools.find_single_match(url_control,'src="(.*?)"')

	
	url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_final+'%26referer='+url_ref

	##La lanzo directamente
	xbmc.executebuiltin('XBMC.RunPlugin('+url_montada+')');

