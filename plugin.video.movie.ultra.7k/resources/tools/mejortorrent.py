# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de http://www.mejortorrent.com
# Version 0.1 (02.11.2015)
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

#plugintools.modo_vista("tvshows")


url = 'http://www.mejortorrent.com'
url_ref = 'http://www.mejortorrent.com/'


def mejortorrent0(params):
	plugintools.log("[%s %s] MejorTorrent.com... %s " % (addonName, addonVersion, repr(params)))

	url = params.get("url")
	thumbnail = 'https://dl.dropbox.com/s/eu8lfp8l72j7ub9/mejortorrent.jpg'
	fanart = 'https://dl.dropbox.com/s/0bugq4xpa5an1h1/moviesultrafondo.jpg?dl=0'
	
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)
	#r = requests.get(url)	
	#data = r.content

	plugintools.add_item(action="",url="",title="[COLOR blue][B]MejorTorrent[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	
	plugintools.add_item(action="mejortorrent_busqueda",title="[COLOR red][B]Búsqueda[/B][/COLOR]", url=url,thumbnail="https://copy.com/tW3YpXz6OGycUhel", extra="", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="mejortorrent_categoria",title="[COLOR white][B]Películas[/B][/COLOR]", url="http://www.mejortorrent.com/torrents-de-peliculas.html",thumbnail="https://dl.dropbox.com/s/eu8lfp8l72j7ub9/mejortorrent.jpg", extra="Películas", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="mejortorrent_categoria",title="[COLOR white][B]Películas HD[/B][/COLOR]", url="http://www.mejortorrent.com/torrents-de-peliculas-hd-alta-definicion.html",thumbnail="https://dl.dropbox.com/s/eu8lfp8l72j7ub9/mejortorrent.jpg", extra="Películas HD", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="mejortorrent_categoria",title="[COLOR white][B]Series[/B][/COLOR]", url="http://www.mejortorrent.com/torrents-de-series.html",thumbnail="https://dl.dropbox.com/s/eu8lfp8l72j7ub9/mejortorrent.jpg", extra="Series", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="mejortorrent_categoria",title="[COLOR white][B]Series HD[/B][/COLOR]", url="http://www.mejortorrent.com/torrents-de-series-hd-alta-definicion.html",thumbnail="https://dl.dropbox.com/s/eu8lfp8l72j7ub9/mejortorrent.jpg", extra="Series HD", fanart=fanart, folder=True, isPlayable=False)
	plugintools.add_item(action="mejortorrent_categoria",title="[COLOR white][B]Documentales[/B][/COLOR]", url="http://www.mejortorrent.com/torrents-de-documentales.html",thumbnail="https://dl.dropbox.com/s/eu8lfp8l72j7ub9/mejortorrent.jpg", extra="Documentales", fanart=fanart, folder=True, isPlayable=False)

'''
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="mejortorrent_salida",url="",title="Salir",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)



def mejortorrent_salida(params):

	sys.exit()
'''	


## Cargo las Diferentes Categorías
def mejortorrent_categoria(params):
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

	bloquede3_videos = plugintools.find_multiple_matches(data,"<td><div align='justify'>(.*?)</tr>")
	for item in bloquede3_videos:

		una_url = plugintools.find_multiple_matches(item,'href="/(.*?)"')  # Me da 6 o 4 o 2 (2 por cada video del grupo)
		un_logo_video = plugintools.find_multiple_matches(item,'<img src="/(.*?)"')  # Me da 3, 2 o 1 (uno por cada video del grupo)
		un_titulo_video = plugintools.find_multiple_matches(item , '.html">(.*?)</a>')  # Tambien Me da 6 o 4 o 2 (2 por cada video del grupo)
		una_calidad_video = plugintools.find_multiple_matches(item , '<b>(.*?)</b>')  # Me da 3, 2 o 1 (uno por cada video del grupo)... o NINGUNO si es Documentales

		if len(una_url) == 12:  # Grupo de 6 videos
			contador = [0,1,2,3,4,5]
			salto = 6
			
		if len(una_url) == 10:  # Grupo de 5 videos
			contador = [0,1,2,3,4]
			salto = 5
			
		if len(una_url) == 4:  # Grupo de 4 videos
			contador = [0,1,2,3]
			salto = 4
			
		if len(una_url) == 6:  # Grupo de 3 videos
			contador = [0,1,2]
			salto = 3
			
		if len(una_url) == 4:  # Grupo de 2 videos
			contador = [0,1]
			salto = 2
			
		if len(una_url) == 2:  # Grupo de 1 video
			contador = [0]
			salto = 1
			
		for item2 in contador:
			url_video = url_ref + una_url[item2]
			logo_video = url_ref + un_logo_video[item2].replace(" ","%20")
			if titulo == "Documentales" or titulo == "Series" or titulo == "Series HD":
				titulo_video = un_titulo_video[item2+salto]
			else:
				titulo_video = un_titulo_video[item2+salto] + "[COLOR green][B]    " + una_calidad_video[item2] + " [/COLOR][/B]"  # Pongo +salto xq los q valen son los 3 o 2 o 1 últimos
			
			titulo_video=titulo_video.decode('unicode_escape').encode('utf8')
			
			if titulo == "Series" or titulo == "Series HD":
				plugintools.add_item(action="mejortorrent_series_temporada", title=titulo_video, url=url_video, thumbnail=logo_video , fanart=fanart, folder = True, isPlayable=False)
			else:	
				plugintools.add_item(action="mejortorrent_video", title=titulo_video, url=url_video, thumbnail=logo_video , fanart=fanart, folder = False, isPlayable=True)

	##Resuelvo la Paginación
	paginacion = plugintools.find_single_match(data,"class='nopaginar'(.*?)class='paginar'")
	pag_actual = plugintools.find_single_match(paginacion,">(.*?)<")
	url_pag_siguiente = plugintools.find_single_match(paginacion,"href='/(.*?)'")

	if len(url_pag_siguiente) > 0:
		pag_proxima = str(int(pag_actual)+1)
		titulo_prox = titulo.replace("   Pag. " +pag_actual , "") + "   Pag. " + pag_proxima
		plugintools.add_item(action="mejortorrent_categoria",title="[COLORred][B]Página: " + pag_proxima + "  >>>[/B][/COLOR]", url=url_ref+url_pag_siguiente, extra=titulo_prox, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
		plugintools.add_item(action="mejortorrent0",title="[COLOR blue][B]<<<  Ir a Menú Principal  >>>[/B][/COLOR]", url=url_ref, extra="", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
	
			

def mejortorrent_series_temporada(params):
	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	titulo = params.get("extra")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)

	r = requests.get(url)	
	data = r.content

	bloque_episodios = plugintools.find_single_match(data,"<form name='episodios(.*?)function seleccionar")
	titulo_serie = plugintools.find_single_match(data,"<title>(.*?) Torrent").decode('unicode_escape').encode('utf8')

	url_episodio = plugintools.find_multiple_matches(bloque_episodios,"href='/(.*?)'")
	numero_episodio = plugintools.find_multiple_matches(bloque_episodios,".html'>(.*?) -</a")
	fecha_episodio = plugintools.find_multiple_matches(bloque_episodios,">Fecha: (.*?)</div>")

	plugintools.add_item(action="",url="",title="[COLOR blue][B]····· "+titulo_serie+" ·····[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	
	i = 0
	for item in url_episodio:
		url_completa = url_ref + url_episodio[i]
		descripcion = "Episodio: " + numero_episodio[i] + "   [COLOR green][B](del " + fecha_episodio[i] + ") [/B][/COLOR]"
	
		plugintools.add_item(action="mejortorrent_video", title=descripcion, url=url_completa, thumbnail=thumbnail , fanart=fanart, folder = False, isPlayable= True)
		i = i + 1

	numero_temporada = plugintools.find_single_match(bloque_episodios,".html'>(.*?)x")
	if int(numero_temporada) > 1:
		acota_atras = " - "+numero_temporada
		busqueda = plugintools.find_single_match(data,"<title>(.*?)"+acota_atras).decode('unicode_escape').encode('utf8')
		
		plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
		plugintools.add_item(action="mejortorrent_busqueda",url="",title="[COLOR red][B]>>> Buscar Otras Temporadas <<<[/B][/COLOR]",extra=busqueda,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)
		
	
	
			
def mejortorrent_video(params):
	url = params.get("url")
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	titulo = params.get("extra")
	#headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url}
	#r=requests.get(url, headers=headers)

	r = requests.get(url)	
	data = r.content

	##Obtengo la página Intermedia para conseguir la final q es donde está el torrent
	pag_intermedia=plugintools.find_single_match(data,"<b>Torrent:</b></span>&nbsp; &nbsp; &nbsp; <a href='(.*?)'")
	
	r2 = requests.get(url_ref + pag_intermedia)	
	data2 = r2.content
	
	url_torrent=plugintools.find_single_match(data2,"Pincha <a href='/(.*?)'")
	
	##Lanzo la llamada para el Torrent
	lanza_torrent = 'plugin://plugin.video.pulsar/play?uri=' + url_ref + url_torrent
	plugintools.play_resolved_url(lanza_torrent)
	#params= plugintools.get_params();params[url]=url_ref + url_torrent;launch_torrent(params)
	
	
	
	
	
def mejortorrent_busqueda(params):

	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	traigo_busqueda = params.get("extra")

	if len(traigo_busqueda) > 0:
		buscar = traigo_busqueda.replace(" ", "+")
	else:	
		buscar=""
		buscar = plugintools.keyboard_input().replace(" ", "+")
		
	url_busca="http://www.mejortorrent.com/secciones.php?sec=buscador&valor="+buscar
	cabecera_buscar = buscar.replace("+", " ")

	r = requests.get(url_busca)	
	data = r.content
	
	bloque_busca=plugintools.find_single_match(data,"Se han encontrado(.*?)</table>")
	bloque_video=plugintools.find_multiple_matches(bloque_busca,"<td>(.*?)</tr>")
	
	plugintools.add_item(action="",url="",title="[COLOR red][B]····· Búsqueda: [COLOR blue]"+cabecera_buscar+"[COLOR red] ·····[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	for item in bloque_video:

		url_video=plugintools.find_single_match(item,"href='/(.*?)'")
		titulo_video=plugintools.find_single_match(item,"none';(.*?)</a>").replace('">',"").replace("<font Color='darkblue'>","[COLOR white]").replace("</font>","[/COLOR]")
		calidad_video=plugintools.find_single_match(item,"style='color:gray;'>(.*?)</a>")
		tipo_video=plugintools.find_single_match(item,"width='20%'>(.*?)</td>").decode('unicode_escape').encode('utf8')
		
		url_video = url_ref + url_video
		descripcion = titulo_video + "  [COLOR red][B]" + calidad_video + "[/COLOR]  " + "[COLOR green]   -" + tipo_video + "-[/B][/COLOR]"
		
		if tipo_video != "Juego PC":
			if tipo_video == "Serie":
				plugintools.add_item(action="mejortorrent_series_temporada", title=descripcion, url=url_video, thumbnail=thumbnail , fanart=fanart, folder = True, isPlayable=False)
			else:	
				plugintools.add_item(action="mejortorrent_video", title=descripcion, url=url_video, thumbnail=thumbnail , fanart=fanart, folder = False, isPlayable=True)
	

	
	
	
	
	
	
	