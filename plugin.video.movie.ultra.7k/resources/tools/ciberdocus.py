# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie Ultra 7K
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

plugintools.setview("tvshows")


url = 'http://www.ciberdocumentales.com/'
url_ref = 'http://www.ciberdocumentales.com/'

mi_firma = "Movie Ultra 7K"

def ciberdocus0(params):
	plugintools.log("[%s %s] Parser CiberDocumentales.com... %s " % (addonName, addonVersion, repr(params)))

	thumbnail = 'https://copy.com/JhmdrPEUNmNGq1YQ'
	fanart = 'https://copy.com/CYGZetMiHo02ghWK'

	plugintools.add_item(action="",url="",title="[COLOR blue][B]CiberDocumentales[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="ciberdocus3",url="",title="[COLOR red][B]····Buscar····[/B][/COLOR]",thumbnail="https://copy.com/anmVpVwPvkB4c4YP", extra="1", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Historia[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/2/historia/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Deportes[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/3/deporte/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Misterio[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/1/misterio/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Arte y Cine[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/5/arte-y-cine/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Ciencia[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/4/ciencia/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Música[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/12/musica/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Naturaleza[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/6/naturaleza/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Política[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/9/politica/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Psicología[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/8/psicologia/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Religión[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/7/religion/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Salud[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/11/salud/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Sociedad[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/10/sociedad/",thumbnail="https://copy.com/NHz9BwJDJPax8ViT", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="ciberdocus1",title="[COLOR white][B]Tecnología[/B][/COLOR]", url="http://www.ciberdocumentales.com/videos/13/tecnologia/",thumbnail="https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAC762LvSCy-22vgzrd9oPHea/documentales.jpg", fanart=fanart, folder=True, isPlayable=False)

	
	
	
## Cargo las Diferentes Categorías
def ciberdocus1(params):
	plugintools.setview("tvshows")

	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	data = plugintools.read(url)	
	
	group_channel = plugintools.find_single_match(data,'var xajaxRequestUri="(.*?)<div id="paginador">')
	plugintools.log("group_channel= "+group_channel)
	cada_canal = plugintools.find_multiple_matches(group_channel,'<div class="fotonoticia">(.*?)data-layout="standard"')	

	for item in cada_canal:
		plugintools.log("item= "+item)
		
		url_canal=plugintools.find_single_match(item,'" data-href="(.*?)"')
		titulo_canal=plugintools.find_single_match(item,'alt="(.*?)"')
		caratula_canal='http://www.ciberdocumentales.com'+plugintools.find_single_match(item,'src="(.*?)"')

		##Capturo la Sinopsis en un Diccionario para usarla en "plugintools.add_item(" mediante la variable "info_labels"
		sinopsis = plugintools.find_single_match(item,'h3></a><br /><br />(.*?)</div>')
		plugintools.log("Sinopsis= "+sinopsis)
		datamovie = {}
		datamovie["Plot"]=sinopsis
		
		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=caratula_canal, info_labels=datamovie , fanart=fanart, folder = False, isPlayable=True)

	#Resuelvo la posibilidad de mas de 1 Página en la Categoría

	mas_pag = plugintools.find_single_match(data,'<div class="pagination">(.*?)</div>')

	#En busca meto la url (http://www.ciberdocumentales.com/videos/2/historia/) "menos" la cadena del comienzo (http://www.ciberdocumentales.com/) para obtener esto "videos/2/historia/"
	busca = url.lstrip(url_ref)
	
	lista_paginas = plugintools.find_multiple_matches(mas_pag,busca+'([^/]+)')
	#Con esto te devuelve una lista: ['2' , '3', '4', ... '41', '2']... y como el q me interesa es el penúltimo (41)... lo obtengo así:
	ult_pag = int(lista_paginas[-2])
	
	for num_pag in range(2, ult_pag+1):
		
		url_pag = url+str(num_pag)+'/'  ## Obtengo las páginas así: http://www.ciberdocumentales.com/videos/2/historia/3
		plugintools.add_item(action="ciberdocus2",title="[COLORred][B]Página Numero: " + str(num_pag) + "  [/B][/COLOR]", url=url_pag,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)


		
def ciberdocus2(params):
	plugintools.setview("tvshows")
	
	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	data = plugintools.read(url)	
		
	group_channel = plugintools.find_single_match(data,'var xajaxRequestUri="(.*?)<div id="paginador">')
	plugintools.log("group_channel= "+group_channel)
	cada_canal = plugintools.find_multiple_matches(group_channel,'<div class="fotonoticia">(.*?)data-layout="standard"')	

	for item in cada_canal:
		plugintools.log("item= "+item)
		
		url_canal=plugintools.find_single_match(item,'" data-href="(.*?)"')
		titulo_canal=plugintools.find_single_match(item,'alt="(.*?)"')
		caratula_canal='http://www.ciberdocumentales.com'+plugintools.find_single_match(item,'src="(.*?)"')

		##Capturo la Sinopsis en un Diccionario para usarla en "plugintools.add_item(" mediante la variable "info_labels"
		sinopsis = plugintools.find_single_match(item,'h3></a><br /><br />(.*?)</div>')
		plugintools.log("Sinopsis= "+sinopsis)
		datamovie = {}
		datamovie["Plot"]=sinopsis

		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=caratula_canal, info_labels=datamovie , fanart=fanart, folder = False, isPlayable=True)


		
def ciberdocus3(params):
	plugintools.setview("tvshows")

	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	recursividad = params.get("extra")

	if recursividad == "1":
		buscar=""
		buscar = plugintools.keyboard_input().replace(" ", "+")
		url_busca="http://www.ciberdocumentales.com/index.php?keysrc="+buscar+"&categoria=0"

	else:
		url_busca = params.get("url")

	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	data = plugintools.read(url_busca)	
	

	
	group_channel = plugintools.find_single_match(data,'var xajaxRequestUri="(.*?)<div id="paginador">')
	plugintools.log("group_channel= "+group_channel)
	cada_canal = plugintools.find_multiple_matches(group_channel,'<div class="fotonoticia">(.*?)>Ha sido visto')	

	for item in cada_canal:
		plugintools.log("item= "+item)
		
		url_canal=plugintools.find_single_match(item,'<div class="opcionesbot"><a target="_blank" href="(.*?)"')
		titulo_canal=plugintools.find_single_match(item,'alt="(.*?)"')
		caratula_canal='http://www.ciberdocumentales.com'+plugintools.find_single_match(item,'src="(.*?)"')

		##Capturo la Sinopsis en un Diccionario para usarla en "plugintools.add_item(" mediante la variable "info_labels"
		sinopsis = plugintools.find_single_match(item,'h3></a><br /><br />(.*?)</div>')
		plugintools.log("Sinopsis= "+sinopsis)
		datamovie = {}
		datamovie["Plot"]=sinopsis
		
		url_montada = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_canal+'%26referer='+url_ref
		plugintools.add_item(action="runPlugin", title=titulo_canal, url=url_montada, thumbnail=caratula_canal, info_labels=datamovie , fanart=fanart, folder = False, isPlayable=True)

	
	if recursividad == "1":
		#Resuelvo la posibilidad de mas de 1 Página en la Busqueda
		
		mas_pag = plugintools.find_single_match(data,'<div class="pagination">(.*?)</div>')
		##Si no está vacio... es decir, q hay mas de 1 página
		if len(mas_pag) > 1:
			cadena_busqueda='/index.php?keysrc='+buscar+'&categoria=0&page='
			total_pag=plugintools.find_multiple_matches(mas_pag, 'a href="([^"]+)')
			#Con esto te devuelve una lista: ['/index.php?keysrc=cine&categoria=0&page=2', '/index.php?keysrc=cine&categoria=0&page=3', '/index.php?keysrc=cine&categoria=0&page=2']

			ult_pag=int(total_pag[-2].replace(cadena_busqueda, ""))
			
			for num_pag in range(2, ult_pag+1):
				recursividad="0"
				url_pag=url_ref+'index.php?keysrc='+buscar+'&categoria=0&page='+str(num_pag)  ## Obtengo las páginas así: http://www.ciberdocumentales.com/index.php?keysrc=cine&categoria=0&page=2
				print url_pag
				plugintools.add_item(action="ciberdocus3",title="[COLORred][B]Página Numero: " + str(num_pag) + "  [/B][/COLOR]", url=url_pag, extra=recursividad,  thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

		
	
