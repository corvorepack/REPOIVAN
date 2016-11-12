# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie Ultra 7K
# Version 0.1 (05.02.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
# Creditos.
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

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


url = "http://canalcocina.es/video-recetas"
fanart = 'http://canalcocina.es/medias/images/1409RecetasPor5EBegonaRodrigo5.jpg'
thumbnail = 'https://dl.dropbox.com/s/fv88ojq0xxtxgm9/cocina.jpg'

def canalcocina(params):
	r = requests.get(url)	
	data = r.content

	categorias = plugintools.find_multiple_matches(data,'class="recipesTypesLnk(.*?)<')
	plugintools.add_item(action="",url="",title="[COLOR blue][B]             	Recetas [COLOR white]Canal [COLOR blue]Cocina... [COLOR white]¡¡A la Carta!![/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	for item in categorias:
		nom_categoria = item.replace('" rel="subsection">','').replace('">','')
		plugintools.add_item(action="cocina_listacategoria",url=url,title=nom_categoria,extra=item,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
	
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="cocina_busqueda",url="",title="[COLOR red][B]···· Buscar ····[/B][/COLOR]",thumbnail="https://www.cubbyusercontent.com/pl/buscar_cocina.jpg/_8149547852ab4d7288881970522446c4", extra="1", fanart=fanart, folder=True, isPlayable=False)
	
	
	
	
	
def cocina_listacategoria(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	url = params.get("url")
	categoria = params.get("title")
	acotacion = params.get("extra")
	acotacion = 'class="recipesTypesLnk' + acotacion


	r = requests.get(url)	
	data = r.content

	plugintools.add_item(action="",url="",title="[COLOR red][B]        ····· Categoría:  [COLOR blue]"+categoria+" ·····[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	
	bloque_categoria = plugintools.find_single_match(data,acotacion+'(.*?)</li>')
	if ">Cocineros" in acotacion:
		cada_grupo = plugintools.find_multiple_matches(bloque_categoria,'<dd class(.*?)</dd>')
		tipo_codigo = 2
	elif ">Programas" in acotacion:
		cada_grupo = plugintools.find_multiple_matches(bloque_categoria,'<dd class(.*?)</dd>')
		tipo_codigo = 2
	else:
		cada_grupo = plugintools.find_multiple_matches(bloque_categoria,'<dd>(.*?)</dd>')
		tipo_codigo = 1

	for item in cada_grupo:
		url_grupo = plugintools.find_single_match(item,'href="(.*?)"')
		url_grupo = "http://canalcocina.es"+url_grupo
		
		if tipo_codigo == 1:
			titulo = plugintools.find_single_match(item,'">(.*?)<')
			titulo = titulo.replace("(" , "   [COLOR green][B](").replace(")" , ")[/B][/COLOR]")
		else:  # es de tipo 2
			titulo = plugintools.find_single_match(item,'title="(.*?)"')
			num_recetas1 = plugintools.find_single_match(item,titulo+'">(.*?)</a>').replace("(","QQQ").replace(")","WWW")
			num_recetas2 = plugintools.find_single_match(num_recetas1,'QQQ(.*?)WWW')
			if len(num_recetas2) == 0:
				num_recetas2 = "Nº Indeterminado"
				
			num_recetas2 = "   [COLOR blue][B](" + num_recetas2 + ")[/B][/COLOR]"
			titulo = titulo + num_recetas2

		plugintools.add_item(action="cocina_listavideos",url=url_grupo,title=titulo,extra="",thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

		


def cocina_listavideos(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	url = params.get("url")
	titulo = params.get("title")
	extra_cabecera = params.get("extra")

	pagina_actual = "1"
	if "/pag/" in url:  # viene de páginación
		pagina_actual = plugintools.find_single_match(url,'/pag/(.*?)/')
		
	
	r = requests.get(url)	
	data = r.content

	if pagina_actual == "1":
		extra_cabecera = titulo
		cabecera = "[COLOR red][B]·····"+titulo+" ····· [/COLOR]"
	else:
		cabecera ="[COLOR red][B] ····· "+extra_cabecera+"[COLOR green]  [B]Pagina. "+pagina_actual+" ·····[/B][/COLOR]"
		
	plugintools.add_item(action="",url="",title=cabecera,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	
	bloque_videos = plugintools.find_single_match(data,'<h3 class=(.*?)class="letter-filter cube pagination')
	cada_video = plugintools.find_multiple_matches(bloque_videos,'<a(.*?)/p>')

	for item in cada_video:
	
		titulo_vid = plugintools.find_single_match(item,'class="icon(.*?)/span>')
		titulo_video = plugintools.find_single_match(titulo_vid,'</i>(.*?)<')
		
		url_video = plugintools.find_single_match(item,'href="(.*?)"')
		url_video = "http://canalcocina.es"+url_video
		cocinero = plugintools.find_single_match(item,'chef20"></i>(.*?)<').strip()
		logo = plugintools.find_single_match(item,'src="(.*?)"')
		
		titulo_completo = titulo_video + "   [COLOR blue][B](" + cocinero + ")[/B][/COLOR]"

		plugintools.add_item(action="lanza_video",url=url_video,title=titulo_completo,extra="",thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)

	#Resuelvo la posibilidad de mas de 1 Página en la Categoría
	#Como la paginación no funciona en la web, tengo q hacerlo de forma "manual"... y como no se cual es la ultima página, no tengo mas remedio que
	#ir llamando a la sig. pág hasta que descubra que no existe.
	pagina_prox = str(int(pagina_actual) + 1)
	busqueda = "/pag/" + pagina_prox + "/"
	if busqueda in data:  # es que hay al menos otra página mas
		if pagina_actual == "1":
			url_proxima = url + busqueda
		else:
			url_proxima = plugintools.find_single_match(url,'http(.*?)/pag/')
			url_proxima = "http" + url_proxima + busqueda

		plugintools.add_item(action="cocina_listavideos",url=url_proxima,title="[COLORred][B]Página Numero: " + pagina_prox + "  [/B][/COLOR]",extra=extra_cabecera,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
		



		
def lanza_video(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	url = params.get("url")
	titulo = params.get("title")

	r = requests.get(url)	
	data = r.content

	video_id = plugintools.find_single_match(data,'data-video-id="(.*?)"')
	pub_id = plugintools.find_single_match(data,'data-account="(.*?)"')
	
	url_lanza = "http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=" + video_id + "&pubId=" + pub_id
	print "***********************************************"
	print url_lanza
	
	params["url"] = url_lanza
	plugintools.play_resolved_url(url_lanza)
	


def cocina_busqueda(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	recursividad = params.get("extra")

	if recursividad == "1":
		buscar=""
		buscar = plugintools.keyboard_input().replace(" ", "+")
		url_busca="http://canalcocina.es/video-recetas?buscarEn=videoRecetas&q="+buscar
		buscar = buscar.replace("+"," ")
		cabecera = "[COLOR lightgreen][B]Búsqueda: "+buscar+"    [COLOR yellow][I]Pag. 1"+"[/I][/B][/COLOR]"
	else:
		url_busca = params.get("url")
		buscar = plugintools.find_single_match(url_busca,'buscarEn=videoRecetas&q=(.*?)')
		cabecera = recursividad

	r = requests.get(url_busca)	
	data = r.content

	plugintools.add_item(action="",url="",title=cabecera,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	bloque_videos = plugintools.find_single_match(data,'<h3 class=(.*?)class="letter-filter cube pagination')
	cada_video = plugintools.find_multiple_matches(bloque_videos,'<a(.*?)/p>')

	for item in cada_video:
	
		titulo_vid = plugintools.find_single_match(item,'class="icon(.*?)/span>')
		titulo_video = plugintools.find_single_match(titulo_vid,'</i>(.*?)<')
		
		url_video = plugintools.find_single_match(item,'href="(.*?)"')
		url_video = "http://canalcocina.es"+url_video
		cocinero = plugintools.find_single_match(item,'chef20"></i>(.*?)<').strip()
		logo = plugintools.find_single_match(item,'src="(.*?)"')
		
		titulo_completo = titulo_video + "   [COLOR green][B](" + cocinero + ")[/I][/COLOR]"

		plugintools.add_item(action="lanza_video",url=url_video,title=titulo_completo,extra="",thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)

	
	#Resuelvo la posibilidad de mas de 1 Página en la Búsqueda
	
	pag_sig = plugintools.find_single_match(data,'<!--<span>...</span>-->(.*?)title=')
	
	pagina_prox = plugintools.find_single_match(pag_sig,'href="(.*?)"')
	##if len(pagina_prox) <> 0:  # Es que hay otra página en la búsqueda
	if "http://canalcocina.es" in pagina_prox:  # Es que hay otra página en la búsqueda
		num_prox_pag = plugintools.find_single_match(pagina_prox,'/pag/(.*?)/')
		
		plugintools.add_item(action="cocina_busqueda",url=pagina_prox,title="[COLORFFFF0759]Página: " + num_prox_pag + "  >>>[/COLOR]",extra="[COLOR lightgreen][B]Búsqueda: "+buscar+"    [COLOR yellow][I]Pag. "+num_prox_pag+"[/I][/B][/COLOR]",thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

	






















	