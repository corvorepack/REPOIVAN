# -*- coding: utf-8 -*-
#------------------------------------------------------------
# TV Ultra 7K Parser de OurMatch
# Version 0.3 (2015.10.27)
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

thumbnail = 'https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AAC2_yoVZMtpYTd9Q0Tqw6Bba/Resumenes%20deportivos.jpg'
fanart    = 'https://dl.dropbox.com/sh/i4ccoqhgk7k1t2v/AAChTJOeg7LsgPDxxos5NSyva/fondo tv.jpg'
referer   = 'http://ourmatch.net/'


def ourmatch0(params):

    plugintools.log('[%s %s] Parseando OurMatch.net %s' % (addonName, addonVersion, repr(params)))
    titulo_pantalla("Resumenes Deportivos", thumbnail, fanart)
    
    r    = requests.get(referer)
    data = r.content

    lista_regiones = plugintools.find_multiple_matches(data, '<div class="division">(.*?)</div>')
    for region in lista_regiones:
    	nombre = plugintools.find_single_match(region, 'title="(.*?)"')
    	plugintools.add_item(action="", title=h2("#" + nombre), url="", thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
    	lista_ligas = plugintools.find_multiple_matches(region,'<li class="hover-tg">(.*?)</li>')
    	for liga in lista_ligas:
    		url_liga  = plugintools.find_single_match(liga,'<a href="(.*?)">')
    		name_liga = plugintools.find_single_match(liga,'">(.*?)</a>')
    		plugintools.add_item(action="ourmatchliga", title="   - " + name_liga, url=url_liga, extra=name_liga, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)


def ourmatchliga(params):
	url   = params.get("url")
	extra = params.get("extra").upper()
	r     = requests.get(url)
	data  = r.content

	titulo_pantalla(extra, thumbnail, fanart)

	bloque_paginacion = plugintools.find_single_match(data, '<div class="loop-nav pag-nav">(.*?)<!-- end .loop-nav -->')
	hay_paginacion = (bloque_paginacion != "")
	if not hay_paginacion:
		plugintools.log(">>> NO HAY PAGINACION")
	else:
		pag_actual = plugintools.find_single_match(bloque_paginacion, "<span class='current'>(.*?)</span>")
		pag_total  = plugintools.find_single_match(bloque_paginacion, "<span class='pages'>(.*?)/span>")
		pag_total  = plugintools.find_single_match(pag_total, 'of (.*?)<')
		plugintools.log(">>>PAGINA ACTUAL:"+pag_actual+" de " +pag_total)

		url_prev   = plugintools.find_single_match(bloque_paginacion, '<a class="previouspostslink"(.*?)</a>')
		url_prev   = plugintools.find_single_match(url_prev, 'href="(.*?)">')
		plugintools.log(">>>URL PREV:"+url_prev)
		
		url_next   = plugintools.find_single_match(bloque_paginacion, '<a class="nextpostslink"(.*?)</a>')
		url_next   = plugintools.find_single_match(url_next, 'href="(.*?)">')
		plugintools.log(">>>URL NEXT:" + url_next)

	if hay_paginacion and url_prev != "":
		plugintools.add_item(action="ourmatchliga", title="[COLOR red][B]« Página Anterior[/B][/COLOR]", url=url_prev, extra=extra, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

	bloque_partidos = plugintools.find_single_match(data, '<div id="main-content">(.*?)<footer id="footer">')
	lista_partidos  = plugintools.find_multiple_matches(bloque_partidos, '<div class="vidthumb">(.*?)<p class="desc">')
	plugintools.log(">>>NUMERO DE PARTIDOS:"+str(len(lista_partidos)))
	for partido in lista_partidos:
		name_partido = plugintools.find_single_match(partido,'title="(.*?)">')
		url_partido  = plugintools.find_single_match(partido,'<a href="(.*?)"')
		date_partido = plugintools.find_single_match(partido,'<span class="time">(.*?)</span>').replace("<br />", "")
		img_partido  = plugintools.find_single_match(partido,'<img src="(.*?)"')
		plugintools.add_item(action="playwire", title=h2(name_partido)+" ("+date_partido.strip()+")", url=url_partido, extra=name_partido, thumbnail=img_partido, fanart=fanart, folder=True, isPlayable=False)

	if hay_paginacion and url_next != "":
		plugintools.add_item(action="ourmatchliga", title="[COLOR red][B]Página Siguiente »[/B][/COLOR]", url=url_next, extra=extra, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
	if hay_paginacion:
		plugintools.add_item(action="miprueba4", title="[COLOR blue][B]Inicio[/B][/COLOR]", url="", thumbnail=thumbnail, extra=extra, fanart=fanart, folder=True, isPlayable=False)	


def ourmatchpartido(params):
	url   = params.get("url")
	extra = params.get("extra")
	r     = requests.get(url)
	data  = r.content

	logo = plugintools.find_single_match(data,'<meta property="og:image" content="(.*?)"/>')
	
	titulo_pantalla(extra, logo, fanart)

	bloque_videos = plugintools.find_single_match(data, '<div class="video-tabs-labels">(.*?)<div class="second-row">')
	lista_videos = plugintools.find_multiple_matches(bloque_videos, '<li(.*?)</li>')
	plugintools.log(">>>NUMERO DE ENLACES:"+str(len(lista_videos)))
	for video in lista_videos:
		chorrazo = plugintools.find_single_match(video, 'data-script-content="(.*?)"')
		titulo   = plugintools.find_single_match(video, '<a href="#">(.*?)</a>').replace(" <br> ","").replace("( ","(").replace(" )", ")")
		titulo1 = titulo[:titulo.find(" (")]
		titulo2 = titulo[titulo.find(" (")+1:]
		plugintools.log(">>>VIDEO:" + titulo + " --- " + chorrazo)
		plugintools.add_item(action="", title=h2(titulo1) + " " + titulo2, url="", thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)


def playwire(params):
    plugintools.log("[%s %s] Playwire en Ourmatch.net %s " % (addonName, addonVersion, repr(params)))
    #Creada por Juarrox

    url=params.get("url")
    extra=params.get("extra")
    r=requests.get(url)
    data=r.content

    logo = plugintools.find_single_match(data,'<meta property="og:image" content="(.*?)"/>')
    titulo_pantalla(extra, logo, fanart)

    video_contents=plugintools.find_single_match(data, 'var video_contents = {(.*?)</script>')
    items_video=plugintools.find_multiple_matches(video_contents, '{(.*?)}')
    for entry in items_video:        
        url_zeus=plugintools.find_single_match(entry, 'config.playwire.com/(.*?)&quot;')
        zeus='http://config.playwire.com/'+url_zeus
        type_item=plugintools.find_single_match(entry, "type\':\'([^']+)")
        lang=plugintools.find_single_match(entry, "lang:\'([^']+)")
        title_item='[COLOR lightgreen]'+type_item+' - '+lang
        print zeus,title_item
        url_media=[];posters=[]
        r=requests.get(zeus)
        data=r.content
        url_f4m=plugintools.find_single_match(data, 'f4m\":\"(.*?)f4m');url_f4m=url_f4m+'f4m'
        poster=plugintools.find_single_match(data, 'poster\":\"(.*?)png');poster=poster+'png'
        posters.append(poster)
        url_media.append(url_f4m)
        url_videos=dict.fromkeys(url_media).keys()
        url_poster=dict.fromkeys(posters).keys()
        r=requests.get(url_videos[0])
        data=r.content
        print data
        burl=plugintools.find_single_match(data, '<baseURL>([^<]+)</baseURL>')
        media_item=plugintools.find_multiple_matches(data, '<media(.*?)"/>')
        i=1
        while i<=len(media_item):
            for item in media_item:
                plugintools.log("item= "+item)
                media=plugintools.find_single_match(item, 'url="([^"]+)')
                bitrate=plugintools.find_single_match(item, 'bitrate="([^"]+)')
                url_media=burl+'/'+media
                title_fixed = title_item+'[/COLOR] [I]('+bitrate+' kbps)[/I]'
                plugintools.add_item(action="play", title=title_fixed, url=url_media, thumbnail=url_poster[0], fanart=fanart, folder=False, isPlayable=True)
                i=i+1                
                

def titulo_pantalla(nombre, logo, fondo):
	plugintools.add_item(action="", title="[COLOR green][B]" + nombre + "[/B][/COLOR]", url="", thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)
	plugintools.add_item(action="", title="", url="", thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

def h2(texto):
	return "[COLOR blue][B]" + texto + "[/B][/COLOR]"
