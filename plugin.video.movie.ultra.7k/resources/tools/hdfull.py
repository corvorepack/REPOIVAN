# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de http://hdfull.tv/
# Version 0.2 (2015.10.27)
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

import re,urllib,urllib2,sys,requests
import plugintools

from resources.tools.resolvers import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://dl.dropbox.com/s/x38opm5keluwq9c/PelSerHD.jpg?dl=0'
fanart_series ='http://cine.netknowsl.netdna-cdn.com/cine/wp-content/uploads/2014/08/14.jpg'
fanart = 'https://dl.dropboxusercontent.com/s/cqayvlwm22bape3/fondo%20movies.jpg'
referer = 'http://hdfull.tv/'

url_estrenos   = "http://hdfull.tv/peliculas-estreno"
url_pelis_abc  = "http://hdfull.tv/peliculas/abc/1"
url_series_abc = "http://hdfull.tv/series/abc"


def hdfull0(params):

    plugintools.log('[%s %s] Parseando HDFULL %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",title="[COLOR blue][B]HDFULL.TV[/B][/COLOR]",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
    plugintools.add_item(action="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
    plugintools.add_item(action="hdfull_seccion",title="[COLOR white][B]Estrenos de cine[/B][/COLOR]", url=url_estrenos, thumbnail=thumbnail, extra="Estrenos de cine", fanart=fanart,folder=True,isPlayable=False)
    plugintools.add_item(action="hdfull_seccion",title="[COLOR white][B]Cine de la A a la Z[/B][/COLOR]",url=url_pelis_abc, extra="Cine de la A a la Z", thumbnail=thumbnail, fanart=fanart,folder=True,isPlayable=False)
    plugintools.add_item(action="hdfull_generos_cine", title="[COLOR white][B]Cine por género[/B][/COLOR]",url=url_estrenos, extra="Cine por géneros", thumbnail=thumbnail, fanart=fanart,folder=True,isPlayable=False)
    plugintools.add_item(action="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
    plugintools.add_item(action="hdfull_series_abc",title="[COLOR white][B]Series de la A a la Z[/B][/COLOR]",url=url_series_abc,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)


def hdfull_generos_cine(params):

	extra = params.get("extra")
	url   = params.get("url")
	r     = requests.get(url)
	data  = r.content

	plugintools.add_item(action="hdfull_generos_cine", title="[COLOR blue][B]Seleccione un género[/B][/COLOR]",url=url_estrenos, extra="Cine por géneros", thumbnail=thumbnail, fanart=fanart,folder=True,isPlayable=False)
	bloque_generos_cine = plugintools.find_single_match(data,'<a href="http://hdfull.tv/peliculas"(.*?)</ul>')
	lista_generos_cine = plugintools.find_multiple_matches(bloque_generos_cine,'<li>(.*?)</li>')
	for item in lista_generos_cine:
		etiqueta_genero_cine = plugintools.find_single_match(item,'">(.*?)</a>')
		enlace_genero_cine = plugintools.find_single_match(item,'<a href="(.*?)">') + "/abc/1"
		plugintools.add_item(action="hdfull_seccion", title=etiqueta_genero_cine ,url=enlace_genero_cine, extra="Películas de " + etiqueta_genero_cine, thumbnail=thumbnail, fanart=fanart,folder=True,isPlayable=False)


def hdfull_seccion(params):
	extra = params.get("extra")
	url   = params.get("url")
	r     = requests.get(url)
	data  = r.content

	#El título de la pantalla
	plugintools.add_item(action="", title="[COLOR blue][B]" + extra + "[/B][/COLOR]",thumbnail=thumbnail, fanart=fanart)
	#Primero comprobamos si hay paginación
	bloque_paginacion = plugintools.find_single_match(data,'<ul id="filter">(.*?)</ul>')
	url_paginas       = plugintools.find_multiple_matches(bloque_paginacion,'href="(.*?)">')
	hay_paginacion = (len(url_paginas) > 1)
	#Si no estamos en la primera página ponemos el enlace a la página anterior
	if hay_paginacion and url != url_paginas[0]:
		plugintools.add_item(action = "hdfull_seccion", title = "[COLORred][B] <<< Página anterior [/B][/COLOR]", url = url_paginas[0], thumbnail=thumbnail, fanart=fanart, folder = True, isPlayable = False)
	#Buscamos los enlaces de las películas
	bloque_peliculas = plugintools.find_single_match(data,'<div class="main-wrapper">(.*?)<div class="center filter-title myfilter">')
	lista_peliculas = plugintools.find_multiple_matches(bloque_peliculas,'<div class="item" style="text-align:center">(.*?)</div>')

	for item in lista_peliculas:
		titulo_peli = plugintools.find_single_match(item,'alt="(.*?)"')
		enlace_peli = plugintools.find_single_match(item,'<a href="(.*?)"')
		poster_peli = plugintools.find_single_match(item,'src="(.*?)"')
		plugintools.add_item(action="hdfull_ficha_pelicula", title=titulo_peli, url=enlace_peli, thumbnail=poster_peli, fanart=fanart, extra=titulo_peli, folder=True, isPlayable=False)

	#Si no estamos en la última página ponemos el enlace a la página siguiente
	if (hay_paginacion and url != url_paginas[len(url_paginas)-1]):
		plugintools.add_item(action = "hdfull_seccion", title = "[COLORred][B] Página siguiente >>>[/B][/COLOR]", url=url_paginas[len(url_paginas)-1], thumbnail=thumbnail, fanart=fanart, extra=extra, folder=True, isPlayable=False)

	#Para que el usuario introduzca una página concreta.
	if hay_paginacion:
		plugintools.add_item(action="ir_a",url=url,title="[COLORred] [B]Ir a página... (1-"+str(len(url_paginas))+")[/B][/COLOR]", extra=extra, thumbnail=thumbnail, fanart=fanart,folder=True, isPlayable=False)


def ir_a(params):
	vextra = params.get("extra")
	extra = vextra[0]
	maxpag =vextra[1]
	url   = params.get("url")
	#Eliminamos el número de página de la URL para poder contruir la nueva
	url = url[:url.rfind("/")]	
	#Pedimos al usuario la página
	mipagina = plugintools.keyboard_input()

	if not mipagina.isdigit():
		plugintools.message("ERROR", "Por favor, introduzca un número.")
		plugintools.add_item(action="ir_a",url=url,title="[COLORred][B] Ir a página...[/B][/COLOR]", extra=extra, thumbnail=thumbnail, fanart=fanart,folder=True, isPlayable=False)
	else:
		miurl = url + '/' + mipagina
		plugintools.add_item(action = "hdfull_seccion", title ="[COLORred][B] Continúa a la página " + str(mipagina) + "[/B][/COLOR]" , url=miurl, thumbnail=thumbnail, fanart=fanart, extra=extra, folder=True, isPlayable=False)


def hdfull_ficha_pelicula(params):

    url    = params.get("url")
    titulo = params.get("extra")
    r      = requests.get(url)
    data   = r.content

    poster = plugintools.find_single_match(data,'<meta property="og:image" content="(.*?)" />')
    fondo  = poster.replace("thumbs","fanart")

    plugintools.add_item(action="", title="[COLOR blue][B]" + titulo + "[/B][/COLOR]",thumbnail=poster, fanart=fondo)
    lista_enlaces = plugintools.find_multiple_matches(data,'<div class="embed-movie">(.*?)</ul>')

    for item in lista_enlaces:
        idioma   = plugintools.find_single_match(item,'</b> (.*?)\n')
        idioma   = idioma.replace("&iacute;","í").replace("&ntilde;","ñ")
        servidor = plugintools.find_single_match(item,'Servidor:</b>(.*?)/b>')
        servidor = plugintools.find_single_match(servidor,'>(.*?)<')
        calidad  = plugintools.find_single_match(item,'<b class="key">Calidad: </b> (.*?)\n')
        enlace1  = plugintools.find_single_match(item,'reportMovie(.*?)target="_blank"')
        enlace   = plugintools.find_single_match(enlace1,'<a href="(.*?)"')

        title  = "[COLOR white]" + idioma + " | " + calidad + " | " + servidor + "[/COLOR]"

        if enlace.startswith("http://www.nowvideo.to") == True:
            plugintools.add_item(action="nowvideo", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://streamin.to") == True:
            plugintools.add_item(action="streaminto", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://turbovideos.net") == True:
            plugintools.add_item(action="turbovideos", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://streamcloud.eu") == True:
            plugintools.add_item(action="streamcloud", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://www.flashx.tv") == True:
            plugintools.add_item(action="flashx", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://www.nowvideo.tv") == True:
            plugintools.add_item(action="flashx", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://gamovideo.com") == True:
            plugintools.add_item(action="gamovideo", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://www.streamable.ch") == True:
            plugintools.add_item(action="streamable", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://videomega.tv") == True:
            plugintools.add_item(action="videomega", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://realvid.net") == True:
            plugintools.add_item(action="realvid", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://www.movshare.net") == True:
            plugintools.add_item(action="movshare", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        elif enlace.startswith("http://rocvideo.tv/") == True:
            plugintools.add_item(action="rocvideo", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
        else:
        	plugintools.log("Enlace no reproducible")
            #plugintools.add_item(action="", title= title, url=enlace, folder=False, isPlayable=False)


def hdfull_series_abc(params):
	abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '#']
	for i in range(0, len(abc)):
		plugintools.add_item(action="hdfull_series", title=abc[i], url=url_series_abc + "/" + abc[i], thumbnail=thumbnail, fanart=fanart_series, folder=True, isPlayable=False)


def hdfull_series(params):
	url   = params.get("url")
	r     = requests.get(url)
	data  = r.content

	bloque_series = plugintools.find_single_match(data,'<div class="container container-flex">(.*?)<div class="center filter-title myfilter">')
	lista_series  = plugintools.find_multiple_matches(bloque_series, '<div class="item"(.*?)</div>')

	for item in lista_series:
		enlace = plugintools.find_single_match(item, '<a href="(.*?)"')
		titulo = plugintools.find_single_match(item, 'alt="(.*?)"')
		poster = plugintools.find_single_match(item, 'src="(.*?)"')
		plugintools.add_item(action="hdfull_temporadas", title=titulo, url=enlace, thumbnail=poster, fanart=fanart_series, folder=True, isPlayable=False)


def hdfull_temporadas(params):
	url   = params.get("url")
	r     = requests.get(url)
	data  = r.content
	fondo = plugintools.find_single_match(data,'background-image:url\(  (.*?)  \)"')

	bloque_temporadas = plugintools.find_single_match(data,'<h3 class="section-title">(.*?)<script>')
	lista_temporadas  = plugintools.find_multiple_matches(bloque_temporadas, 'itemtype="http://schema.org/TVSeason"(.*?)</div>')
	for item in lista_temporadas:
		enlace = plugintools.find_single_match(item, "<a href='(.*?)'")
		titulo = plugintools.find_single_match(item, 'original-title="(.*?)"')
		poster = plugintools.find_single_match(item, 'src="(.*?)"')
		plugintools.add_item(action="hdfull_capitulos", title=titulo, url=enlace, thumbnail=poster, fanart=fondo, folder=True, isPlayable=False)


def hdfull_capitulos(params):
	url   = params.get("url")
	r     = requests.get(url)
	data  = r.content
	fondo = params.get("fanart")
	poster= params.get("thumbnail")

	capitulo_encontrado = True
	ep = 1
	while capitulo_encontrado:
		enlace = url + "/episodio-" + str(ep)

		r2 = requests.get(enlace)
		data2 = r2.content

		temp = plugintools.find_single_match(data2,'Episodio no encontrado(.*?)<br /><br /></center>')
		if len(temp)>0 or ep>100:
			capitulo_encontrado = False
		else:
			plugintools.add_item(action="hdfull_ficha_capitulo",title="Episodio " + str(ep), url=enlace, thumbnail=poster, fanart=fondo, folder=True, isPlayable=False)
			ep = ep + 1


def hdfull_ficha_capitulo(params):
	url   = params.get("url")
	r     = requests.get(url)
	data  = r.content

	lista_servidores = plugintools.find_multiple_matches(data,'<h5(.*?)</div>')
	fondo = plugintools.find_single_match(data,'background-image:url\(  (.*?)  \)"')
	poster = plugintools.find_single_match(data,'<img class="tv-screen" src="(.*?)">')

	for item in lista_servidores:
		idioma   = plugintools.find_single_match(item,'</b> (.*?)\n')
		idioma   = idioma.replace("&iacute;","í").replace("&ntilde;","ñ")
		servidor = plugintools.find_single_match(item,'Servidor:</b>(.*?)/b>')
		servidor = plugintools.find_single_match(servidor,'>(.*?)<')
		calidad  = plugintools.find_single_match(item,'<b class="key">Calidad: </b> (.*?)\n')
		enlace1  = plugintools.find_single_match(item,'reportEpisode(.*?)target="_blank"')
		enlace   = plugintools.find_single_match(enlace1,'<a href="(.*?)"')
		title  = "[COLOR white]" + idioma + " | " + calidad + " | " + servidor + "[/COLOR]"

		if enlace.startswith("http://www.nowvideo.to") == True:
			plugintools.add_item(action="nowvideo", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://streamin.to") == True:
			plugintools.add_item(action="streaminto", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://turbovideos.net") == True:
			plugintools.add_item(action="turbovideos", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://streamcloud.eu") == True:
			plugintools.add_item(action="streamcloud", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://www.flashx.tv") == True:
			plugintools.add_item(action="flashx", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://www.nowvideo.tv") == True:
			plugintools.add_item(action="flashx", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://gamovideo.com") == True:
			plugintools.add_item(action="gamovideo", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://www.streamable.ch") == True:
			plugintools.add_item(action="streamable", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://videomega.tv") == True:
			plugintools.add_item(action="videomega", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://realvid.net") == True:
			plugintools.add_item(action="realvid", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://www.movshare.net") == True:
			plugintools.add_item(action="movshare", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		elif enlace.startswith("http://rocvideo.tv/") == True:
			plugintools.add_item(action="rocvideo", title = title, url=enlace, thumbnail=poster, fanart=fondo, folder=False, isPlayable=True)
		else:
			plugintools.log("Enlace no reproducible")
			#plugintools.add_item(action="", title= title, url=enlace, folder=False, isPlayable=False)

