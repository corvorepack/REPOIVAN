# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Gnula Cine Movie Ultra 7K
# Version 0.3 (05.01.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#
# 

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

thumbnail = 'http://listas.eleconomista.es/system/items/000/046/152/medium/gnula.jpg?1417804682'
fanart = 'http://claqueta.net/wp-content/uploads/2015/08/gnula.png'
sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR lightyellow]";ec3 = "[/COLOR]"
version = " [COLOR red][B][0.3][/B][/COLOR]"

web = "http://gnula.nu/"

def gnula0(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	name = 'Gnula Cine'
	update = '05/01/2016 18:00'
	Autor = 'Movie Ultra 7K'
	url = 'https://copy.com/EBOFFiOTqMAUE3vx'

	r = requests.get(web)
	data = r.content

# Secciones Home ------------------------------>>

	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 
	
	url_online = 'http://gnula.nu/peliculas-online/lista-de-peliculas-online-parte-1/'
	url_recomendadas = 'http://gnula.nu/peliculas-online/lista-de-peliculas-recomendadas/'
	
	plugintools.add_item(action="resolvers_1",url=url_online,title=sc + "- Peliculas Online -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="resolvers_1",url=url_recomendadas,title=sc + "- Peliculas Recomendadas -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="estrenos",url="",title=sc + "- Estrenos de Cine -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)	
	plugintools.add_item(action="novedades",url="",title=sc + "- Novedades de Peliculas -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="newvose",url="",title=sc + "- New VOSE -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="newlatino",url="",title=sc + "- New Latino -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="newcastellano",url="",title=sc + "- New Castellano -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="newdvdr",url="",title=sc + "- Estrenos DVD-R -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="newcalidad",url="",title=sc + "- New Calidad -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
	plugintools.add_item(action="newdvds",url="",title=sc + "- Estrenos DVD-S -" + ec,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)

# Estrenos ------------------------------------>>

def estrenos(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 
	bloque_estrenos = plugintools.find_single_match(data,'<strong>ESTRENOS DE CINE</strong></div>(.*?)</table>')
	estreno = plugintools.find_multiple_matches(bloque_estrenos,'<a(.*?)></a>')
	for item in estreno:
		title = plugintools.find_single_match(item,'title="(.*?) -').replace("VOSE",sc2+"V.O"+ec2).replace("VS",sc2+"Sub"+ec2).replace("VC",sc2+"Esp"+ec2).replace("VL",sc2+"Lat"+ec2).replace("OV",sc2+"Otros"+ec2)
		calidad = plugintools.find_single_match(item,'title="(.*?) -')
		img = plugintools.find_single_match(item,'" src="(.*?)"')
		url = plugintools.find_single_match(item,'href="(.*?)"')
		plugintools.addPeli(action="resolvers_2",url=url,title=sc + title + ec,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)

# Novedades ----------------------------------->>

def novedades(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	bloque_novedades = plugintools.find_single_match(data,'<strong>NOVEDADES DE PELÍCULAS</strong></div>(.*?)</table>')
	novedad = plugintools.find_multiple_matches(bloque_novedades,'<a(.*?)></a>')
	for item in novedad:
		title = plugintools.find_single_match(item,'title="(.*?) -').replace("VOSE",sc2+"V.O"+ec2).replace("VS",sc2+"Sub"+ec2).replace("VC",sc2+"Esp"+ec2).replace("VL",sc2+"Lat"+ec2).replace("OV",sc2+"Otros"+ec2)
		calidad = plugintools.find_single_match(item,'title="(.*?) -')
		img = plugintools.find_single_match(item,'" src="(.*?)"')
		url = plugintools.find_single_match(item,'href="(.*?)"')
		plugintools.addPeli(action="resolvers_2",url=url,title=sc + title + ec,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)

# New Vose ------------------------------------>>

def newvose(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))
	
	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	bloque_newvose = plugintools.find_single_match(data,'<h2>New VOSE</h2>(.*?)</div>')
	vose = plugintools.find_multiple_matches(bloque_newvose,'<a(.*?)></a>')
	for item in vose:
		title = plugintools.find_single_match(item,'title="(.*?) -').replace("VOSE",sc2+"V.O"+ec2).replace("VS",sc2+"Sub"+ec2).replace("VC",sc2+"Esp"+ec2).replace("VL",sc2+"Lat"+ec2).replace("OV",sc2+"Otros"+ec2)
		calidad = plugintools.find_single_match(item,'title="(.*?) -')
		img = plugintools.find_single_match(item,'" src="(.*?)"')
		url = plugintools.find_single_match(item,'href="(.*?)"')
		plugintools.addPeli(action="resolvers_2",url=url,title=sc3 + title + ec3,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)	

# New Latino ---------------------------------->>

def newlatino(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	bloque_newlatino = plugintools.find_single_match(data,'<h2>New Latino</h2>(.*?)</div>')
	latino = plugintools.find_multiple_matches(bloque_newlatino,'<a(.*?)></a>')
	for item in latino:
		title = plugintools.find_single_match(item,'title="(.*?) -').replace("VOSE",sc2+"V.O"+ec2).replace("VS",sc2+"Sub"+ec2).replace("VC",sc2+"Esp"+ec2).replace("VL",sc2+"Lat"+ec2).replace("OV",sc2+"Otros"+ec2)
		calidad = plugintools.find_single_match(item,'title="(.*?) -')
		img = plugintools.find_single_match(item,'" src="(.*?)"')
		url = plugintools.find_single_match(item,'href="(.*?)"')
		plugintools.addPeli(action="resolvers_2",url=url,title=sc3 + title + ec3,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)

# New Castellano ------------------------------>>

def newdvdr(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	bloque_newdvdr = plugintools.find_single_match(data,'<h2>Estrenos DVD-R</h2>(.*?)</div>')
	dvdr = plugintools.find_multiple_matches(bloque_newdvdr,'<a(.*?)></a>')
	for item in dvdr:
		title = plugintools.find_single_match(item,'title="(.*?) -').replace("VOSE",sc2+"V.O"+ec2).replace("VS",sc2+"Sub"+ec2).replace("VC",sc2+"Esp"+ec2).replace("VL",sc2+"Lat"+ec2).replace("OV",sc2+"Otros"+ec2)
		calidad = plugintools.find_single_match(item,'title="(.*?) -')
		img = plugintools.find_single_match(item,'" src="(.*?)"')
		url = plugintools.find_single_match(item,'href="(.*?)"')
		plugintools.addPeli(action="resolvers_2",url=url,title=sc3 + title + ec3,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)	

# Estrenos DVD-R ------------------------------>>

def newcastellano(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	bloque_newcastellano = plugintools.find_single_match(data,'<h2>New Castellano</h2>(.*?)</div>')
	castellano = plugintools.find_multiple_matches(bloque_newcastellano,'<a(.*?)></a>')
	for item in castellano:
		title = plugintools.find_single_match(item,'title="(.*?) -').replace("VOSE",sc2+"V.O"+ec2).replace("VS",sc2+"Sub"+ec2).replace("VC",sc2+"Esp"+ec2).replace("VL",sc2+"Lat"+ec2).replace("OV",sc2+"Otros"+ec2)
		calidad = plugintools.find_single_match(item,'title="(.*?) -')
		img = plugintools.find_single_match(item,'" src="(.*?)"')
		url = plugintools.find_single_match(item,'href="(.*?)"')
		plugintools.addPeli(action="resolvers_2",url=url,title=sc3 + title + ec3,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)	

# New Calidad --------------------------------->>

def newcalidad(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	bloque_newcalidad = plugintools.find_single_match(data,'<h2>New Calidad</h2>(.*?)</div>')
	calidad = plugintools.find_multiple_matches(bloque_newcalidad,'<a(.*?)></a>')
	for item in calidad:
		title = plugintools.find_single_match(item,'title="(.*?) -').replace("VOSE",sc2+"V.O"+ec2).replace("VS",sc2+"Sub"+ec2).replace("VC",sc2+"Esp"+ec2).replace("VL",sc2+"Lat"+ec2).replace("OV",sc2+"Otros"+ec2)
		calidad = plugintools.find_single_match(item,'title="(.*?) -')
		img = plugintools.find_single_match(item,'" src="(.*?)"')
		url = plugintools.find_single_match(item,'href="(.*?)"')
		plugintools.addPeli(action="resolvers_2",url=url,title=sc3 + title + ec3,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)	

# New Calidad --------------------------------->>

def newdvds(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	bloque_newdvds = plugintools.find_single_match(data,'<h2>Estrenos DVD-S</h2>(.*?)</div>')
	dvds = plugintools.find_multiple_matches(bloque_newdvds,'<a(.*?)></a>')
	for item in dvds:
		title = plugintools.find_single_match(item,'title="(.*?) -').replace("VOSE",sc2+"V.O"+ec2).replace("VS",sc2+"Sub"+ec2).replace("VC",sc2+"Esp"+ec2).replace("VL",sc2+"Lat"+ec2).replace("OV",sc2+"Otros"+ec2)
		calidad = plugintools.find_single_match(item,'title="(.*?) -')
		img = plugintools.find_single_match(item,'" src="(.*?)"')
		url = plugintools.find_single_match(item,'href="(.*?)"')
		plugintools.addPeli(action="resolvers_2",url=url,title=sc3 + title + ec3,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)	
		
# Resolviendo listas -------------------------->>
	
def resolvers_1(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))
	
	web = params.get("url")
	r = requests.get(web)
	data = r.content
	# print data
	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	bloque_peli = plugintools.find_single_match(data,'<span style="font-weight: bold;">(.*?)<p><span style="font-weight: bold;">')
	peli = plugintools.find_multiple_matches(bloque_peli,'class="Ntooltip"(.*?)</strong><br/>')

	for item in peli:
		title = plugintools.find_single_match(item,'href=".*?">(.*?)<span><br/>')
		img = plugintools.find_single_match(item,'<img src="(.*?)"')
		calidad = plugintools.find_single_match(item,'<span style="color: #ffcc99;">(.*?)<')
		audio = plugintools.find_single_match(item,'<span style="color: #33ccff;.*?</span> <span(.*?)</span>]')
		# print audio
		audio1 = plugintools.find_single_match(item,'<span style="color: #33ccff;.*?</span> <span.*?(VO).*?</span>]').replace("VO","[V.O]")
		audio2 = plugintools.find_single_match(item,'<span style="color: #33ccff;.*?</span> <span.*?(VS).*?</span>]').replace("VS","[Substitulos]")
		audio3 = plugintools.find_single_match(item,'<span style="color: #33ccff;.*?</span> <span.*?(VC).*?</span>]').replace("VC","[España]")
		audio4 = plugintools.find_single_match(item,'<span style="color: #33ccff;.*?</span> <span.*?(VL).*?</span>]').replace("VL","[Latinos]")
		audio5 = plugintools.find_single_match(item,'<span style="color: #33ccff;.*?</span> <span.*?(OV).*?</span>]').replace("OV","[Otros]")
		audiofull = audio1 + " " + audio2 + " " + audio3 + " " + audio4 + " " + audio5
	
		titlefull = title + "  "  + sc2 + "[" + calidad + "]" + ec2 + " " + sc3 + audiofull + ec3
		url = plugintools.find_single_match(item,'href="(.*?)"')
		
		plugintools.addPeli(action="resolvers_2",url=url,title=sc + titlefull + ec,thumbnail=img,fanart=fanart,folder=True,isPlayable=False)
		
# Resolviendo Enlaces ------------------------->>

def resolvers_2(params):
	plugintools.log("[%s %s] Gnula Cine parser... %s " % (addonName, addonVersion, repr(params)))

	web = params.get("url")
	r = requests.get(web)
	data = r.content

	plugintools.add_item(action="",url="",title="[COLOR blue][B]Gnula Cine[/B][/COLOR]"+version+"",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False) 	
	title = plugintools.find_single_match(data,'<h2><a.*?title=".*?>(.*?)</a></h2>').replace("Ver","").replace("online","")
	sinopsis = plugintools.find_single_match(data,'<p align="center"><img.*?<p>(.*?)</p>')
	# plugintools.log("Sinopsis= "+sinopsis)
	datamovie = {}
	datamovie["Plot"] = sinopsis

# 1 Opcion de Audio --------------------------->>
	
	bloque_link1 = plugintools.find_single_match(data,'<div class="contenedor_tab">(.*?)</table>')
	opc1 = plugintools.find_single_match(data,'<em>(.*?)</em></p>')
	img = plugintools.find_single_match(data,'<div class="entry">.*?src="(.*?)"')
	linka = plugintools.find_multiple_matches(bloque_link1,'<iframe.*?src="(.*?)"')
	linkb = plugintools.find_multiple_matches(bloque_link1,'<a href="(.*?)"')
	link1full = linka + linkb
	
	plugintools.addPeli(action="",url="",title=sc + title + ec,info_labels=datamovie,thumbnail=img,fanart=fanart,folder=False,isPlayable=False)
	plugintools.addPeli(action="",url="",title=sc2 + opc1 + ec2,info_labels=datamovie,thumbnail=img,fanart=fanart,folder=False,isPlayable=False)
	for link in link1full:
		# plugintools.log("Link= "+link)
		if ("http://player.vimple.ru/") in link:
			servidor = sc3 + "[Vimple]" + ec3
			plugintools.addPeli(action="vimple",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://ok.ru/") in link:
			servidor = sc3 + "[Ok.ru]" + ec3
			plugintools.addPeli(action="okru",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://hqq.tv/") in link:
			link = link.replace("http://hqq.tv/player/embed_player.php?vid=","http://waaw.tv/watch_video.php?v=").replace("&#038;autoplay=no","")
			servidor = sc3 + "[Netu]" + ec3				
			plugintools.addPeli(action="netu",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://flashx.tv/") in link:
			servidor = sc3 + "[Flashx]" + ec3
			plugintools.addPeli(action="flashx",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamcloud.eu/") in link:
			servidor = sc3 + "[Streamcloud]" + ec3
			plugintools.addPeli(action="streamcloud",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("https://openload.co/") in link:
			servidor = sc3 + "[OpenLoad]" + ec3
			plugintools.addPeli(action="openload",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamin.to/") in link:
			servidor = sc3 + "[Streamin.to]" + ec3
			plugintools.addPeli(action="streaminto",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://powvideo.net/") in link:
			servidor = sc3 + "[Powvideo]" + ec3
			plugintools.addPeli(action="powvideo",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://allmyvideos.net/") in link:
			servidor = sc3 + "[Allmyvideos]" + ec3
			plugintools.addPeli(action="allmyvideos",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamin.to/") in link:
			servidor = sc3 + "[Streamin.to]" + ec3
			plugintools.addPeli(action="streaminto",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

# 2 Opciones de Audio ------------------------->>

	bloque_link2 = plugintools.find_single_match(data,'<p></br></p>(.*?)</table>')
	opc2 = plugintools.find_single_match(bloque_link2,'<p><em>(.*?)</em></p>')
	plugintools.addPeli(action="",url="",title=sc2 + opc2 + ec2,info_labels=datamovie,thumbnail=img,fanart=fanart,folder=False,isPlayable=False)
	
	linka = plugintools.find_multiple_matches(bloque_link2,'<iframe.*?src="(.*?)"')
	linkb = plugintools.find_multiple_matches(bloque_link2,'<a href="(.*?)"')
	link2full = linka + linkb

	for link in link2full:
		# plugintools.log("Link= "+link)
		if ("http://player.vimple.ru/") in link:
			servidor = sc3 + "[Vimple]" + ec3
			plugintools.addPeli(action="vimple",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://ok.ru/") in link:
			servidor = sc3 + "[Ok.ru]" + ec3
			plugintools.addPeli(action="okru",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://hqq.tv/") in link:
			link = link.replace("http://hqq.tv/player/embed_player.php?vid=","http://waaw.tv/watch_video.php?v=").replace("&#038;autoplay=no","")
			servidor = sc3 + "[Netu]" + ec3				
			plugintools.addPeli(action="netu",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://flashx.tv/") in link:
			servidor = sc3 + "[Flashx]" + ec3
			plugintools.addPeli(action="flashx",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamcloud.eu/") in link:
			servidor = sc3 + "[Streamcloud]" + ec3
			plugintools.addPeli(action="streamcloud",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("https://openload.co/") in link:
			servidor = sc3 + "[OpenLoad]" + ec3
			plugintools.addPeli(action="openload",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamin.to/") in link:
			servidor = sc3 + "[Streamin.to]" + ec3
			plugintools.addPeli(action="streaminto",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://powvideo.net/") in link:
			servidor = sc3 + "[Powvideo]" + ec3
			plugintools.addPeli(action="powvideo",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://allmyvideos.net/") in link:
			servidor = sc3 + "[Allmyvideos]" + ec3
			plugintools.addPeli(action="allmyvideos",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamin.to/") in link:
			servidor = sc3 + "[Streamin.to]" + ec3
			plugintools.addPeli(action="streaminto",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

# 3 Opciones de Audio ------------------------->>

	bloque_link3 = plugintools.find_single_match(data,'<p></br></p>.*?<p></br></p>(.*?)</table>')
	opc3 = plugintools.find_single_match(bloque_link3,'<p><em>(.*?)</em></p>')
	plugintools.addPeli(action="",url="",title=sc2 + opc3 + ec2,info_labels=datamovie,thumbnail=img,fanart=fanart,folder=False,isPlayable=False)
	
	linka = plugintools.find_multiple_matches(bloque_link3,'<iframe.*?src="(.*?)"')
	linkb = plugintools.find_multiple_matches(bloque_link3,'<a href="(.*?)"')
	link3full = linka + linkb

	for link in link3full:
		# plugintools.log("Link= "+link)
		if ("http://player.vimple.ru/") in link:
			servidor = sc3 + "[Vimple]" + ec3
			plugintools.addPeli(action="vimple",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://ok.ru/") in link:
			servidor = sc3 + "[Ok.ru]" + ec3
			plugintools.addPeli(action="okru",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://hqq.tv/") in link:
			link = link.replace("http://hqq.tv/player/embed_player.php?vid=","http://waaw.tv/watch_video.php?v=").replace("&#038;autoplay=no","")
			servidor = sc3 + "[Netu]" + ec3				
			plugintools.addPeli(action="netu",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://flashx.tv/") in link:
			servidor = sc3 + "[Flashx]" + ec3
			plugintools.addPeli(action="flashx",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamcloud.eu/") in link:
			servidor = sc3 + "[Streamcloud]" + ec3
			plugintools.addPeli(action="streamcloud",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("https://openload.co/") in link:
			servidor = sc3 + "[OpenLoad]" + ec3
			plugintools.addPeli(action="openload",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamin.to/") in link:
			servidor = sc3 + "[Streamin.to]" + ec3
			plugintools.addPeli(action="streaminto",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://powvideo.net/") in link:
			servidor = sc3 + "[Powvideo]" + ec3
			plugintools.addPeli(action="powvideo",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://allmyvideos.net/") in link:
			servidor = sc3 + "[Allmyvideos]" + ec3
			plugintools.addPeli(action="allmyvideos",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)

		if ("http://streamin.to/") in link:
			servidor = sc3 + "[Streamin.to]" + ec3
			plugintools.addPeli(action="streaminto",url=link,title=sc + "Ver en: " + ec + " " + servidor,thumbnail=img,fanart=fanart,folder=False,isPlayable=True)


# ------------------------------------------------------- Movie Ultra 7K ---------------------------------------------------		