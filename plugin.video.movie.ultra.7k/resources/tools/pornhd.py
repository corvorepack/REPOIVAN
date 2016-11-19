# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de PornHD (+18)
# Version 0.2 (2015.12.29)
# Changelog: 0.1 - Versión inicial
#            0.2 - Eliminados enlaces de baja calidad
#            0.3 - Cambios en la web
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os, sys, urllib, urllib2, re, requests
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import plugintools

from resources.tools.resolvers import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://pbs.twimg.com/profile_images/527104689444093952/PbRNZmMT.png'
fanart    = 'http://www.widewallpapers.ru/mod/babes/1920x1080/wide-wallpaper-1920x1080-005.jpg'
referer   = 'http://www.pornhd.com'

sec = { 'ULTIMOS'    : 'http://www.pornhd.com/',
        'POPULAR'    : 'http://www.pornhd.com/videos/mostpopular',
        'PUNTUACION' : 'http://www.pornhd.com/videos/toprated',
        'CATEGORIAS' : 'http://www.pornhd.com/category',
        'PORNSTARS'  : 'http://www.pornhd.com/pornstars?order=video_count&gender=female',
        'CANALES'    : 'http://www.pornhd.com/channel',
        'BUSCADOR'   : 'http://www.pornhd.com/search?search='
      }

reg = { 'ULTIMOS'    : '<ul class="thumbs">(.*?)</ul>',
        'POPULAR'    : '<ul class="thumbs">(.*?)</ul>',
        'PUNTUACION' : '<ul class="thumbs">(.*?)</ul>',
        'CATEGORIAS' : '<ul class="categories-all">(.*?)</ul>',
        'PORNSTARS'  : '<ul class="pornstar-tag-list">(.*?)</ul>',
        'CANALES'    : '<ul class="tag-150-list">(.*?)</ul>',
        'BUSCADOR'   : ''
      }

def pornhd(params):
    titulo_pantalla("PornHD (+18)", thumbnail, fanart)

    #for name, value in sec.iteritems():
    #    plugintools.add_item(action="pornhd_seccion", title=h2("- "+name.title()+" -"), extra=name, url=value, fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)

    plugintools.add_item(action="pornhd_videos", title=h2("- Novedades -"), extra="PornHD - Novedades", url=sec["ULTIMOS"], fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)
    plugintools.add_item(action="pornhd_videos", title=h2("- Populares -"), extra="PornHD - Populares", url=sec["POPULAR"], fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)
    plugintools.add_item(action="pornhd_videos", title=h2("- Destacados -"), extra="PornHD - Destacados", url=sec["PUNTUACION"], fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)
    plugintools.add_item(action="", title="", url="", fanart=fanart, thumbnail=thumbnail, folder=False, isPlayable=False)
    plugintools.add_item(action="pornhd_seccion", title=h2("- Categorías -"), extra="CATEGORIAS", url=sec["CATEGORIAS"], fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)
    plugintools.add_item(action="pornhd_seccion", title=h2("- Pornstars -"), extra="PORNSTARS", url=sec["PORNSTARS"], fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)
    plugintools.add_item(action="pornhd_canales", title=h2("- Canales -"), extra="CANALES", url=sec["CANALES"], fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)
    plugintools.add_item(action="", title="", url="", fanart=fanart, thumbnail=thumbnail, folder=False, isPlayable=False)
    plugintools.add_item(action="pornhd_buscador", title=h2("- Buscador -"), extra="BUSCADOR", url=sec["BUSCADOR"], fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)

def pornhd_seccion(params):
    data = requests.get(params.get("url")).content
    regex_bloque = reg[params.get("extra")]
    regex_lista  = '<li(.*?)</li>'
    bloque = plugintools.find_single_match(data,regex_bloque)
    lista  = plugintools.find_multiple_matches(bloque,regex_lista)
    for item in lista:
        enlace = plugintools.find_single_match(item, 'href="(.*?)"')
        enlace = 'http://www.pornhd.com' + enlace
        titulo = plugintools.find_single_match(item, 'alt="(.*?)"')
        logo   = plugintools.find_single_match(item, 'data-original="(.*?)"')
        plugintools.add_item(action="pornhd_videos", title=h2(titulo), url=enlace, extra=titulo, thumbnail=logo, fanart=fanart, folder=True, isPlayable=False)

def pornhd_canales(params):
    data = requests.get(params.get("url")).content
    regex_bloque = reg[params.get("extra")]
    regex_lista  = '<li(.*?)</li>'
    bloque = plugintools.find_single_match(data, regex_bloque)
    lista  = plugintools.find_multiple_matches(bloque, regex_lista)
    for item in lista:
        nombre = plugintools.find_single_match(item, '<span class="name">(.*?)</span>')
        enlace = 'http://www.pornhd.com/channel/' + nombre
        logo   = plugintools.find_single_match(item, 'src="(.*?)"')
        plugintools.add_item(action="pornhd_videos", title=h2(nombre), url=enlace, extra=nombre, thumbnail=logo, fanart=fanart, folder=True, isPlayable=False)

def pornhd_buscador(params):
    parametros = {}
    clave = plugintools.keyboard_input("","Escriba las palabras a buscar").replace(" ","+")
    parametros["url"]   = sec["BUSCADOR"] + clave
    parametros["extra"] = 'PornHD - Resultados para: "' + clave + '"'

    pornhd_videos(parametros)

def pornhd_videos(params):
    url    = params.get("url")
    data   = requests.get(url).content
    titulo = params.get("extra")
    titulo_pantalla(titulo, thumbnail, fanart)

    if not titulo.startswith("PornHD"):
        url = url.replace('/mostpopular','').replace('/toprated','')
        plugintools.add_item(action="pornhd_videos", title=h4("Ordenar por fecha"), url=url, extra=titulo, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
        plugintools.add_item(action="pornhd_videos", title=h4("Ordenar por popularidad"), url=url+'/mostpopular', extra=titulo, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
        plugintools.add_item(action="pornhd_videos", title=h4("Ordenar por puntuación"), url=url+'/toprated', extra=titulo, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
        plugintools.add_item(action="", title="", url="", fanart=fanart, thumbnail=thumbnail, folder=False, isPlayable=False)


    regex_bloque = '<ul class="thumbs">(.*?)</ul>'
    regex_lista  = '<li(.*?)</li>'
    bloques = plugintools.find_multiple_matches(data,regex_bloque)
    for bloque in bloques :
        lista  = plugintools.find_multiple_matches(bloque,regex_lista)
        for item in lista:
            nombre = plugintools.find_single_match(item, 'alt="(.*?)"')
            enlace = plugintools.find_single_match(item, 'href="(.*?)"')
            enlace = 'http://www.pornhd.com' + enlace
            logo   = plugintools.find_single_match(item, 'data-original="(.*?)"')
            if nombre != "" :
                plugintools.add_item(action="pornhd_enlaces", title=h2(nombre), url=enlace, thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)

    # Paginación
    bloque_next = plugintools.find_single_match(data, '<li class="next ">(.*?)</li>')
    bloque_prev = plugintools.find_single_match(data, '<li class="previous ">(.*?)</li>')
    url_next = plugintools.find_single_match(bloque_next, 'href="(.*?)"')
    url_prev = plugintools.find_single_match(bloque_prev, 'href="(.*?)"')

    plugintools.add_item(action="", title="", url="", fanart=fanart, thumbnail=thumbnail, folder=False, isPlayable=False)
    if url_prev != "":
        url_prev = 'http://www.pornhd.com' + url_prev
        plugintools.add_item(action="pornhd_videos", title=h4("« Página anterior"), url=url_prev, extra=titulo, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    if url_next != "":
        url_next = 'http://www.pornhd.com' + url_next
        plugintools.add_item(action="pornhd_videos", title=h4("Página siguiente »"), url=url_next, extra=titulo, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="pornhd", title=h4("Inicio"), url="", fanart=fanart, thumbnail=thumbnail, folder=True, isPlayable=False)

def pornhd_enlaces(params):
    url   = params.get("url")
    data  = requests.get(url).content

    titulo = plugintools.find_single_match(data, '<meta name="description" content="(.*?)" />')
    logo   = plugintools.find_single_match(data, '<meta name="og:image" content="(.*?)" />')

    titulo_pantalla(titulo,logo, fanart)

    bloque    = plugintools.find_single_match(data, "players.push(.*?)}")
    video240  = plugintools.find_single_match(bloque,  "'240p'  : '(.*?)'")
    video480  = plugintools.find_single_match(bloque,  "'480p'  : '(.*?)'")
    video720  = plugintools.find_single_match(bloque,  "'720p'  : '(.*?)'")
    video1080 = plugintools.find_single_match(bloque, "'1800p'  : '(.*?)'")

    plugintools.play_resolved_url(video480)

'''
    if len(video240) > 0:
        plugintools.add_item(action="play", title=h2("Low Quality"), url=video240, thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)
    if len(video480) > 0:
        plugintools.add_item(action="play", title=h2("Standard Quality"), url=video480, thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)
    if len(video720) > 0:
        plugintools.add_item(action="play", title=h2("High Quality"), url=video720, thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)
    if len(video1080) > 0:
        plugintools.add_item(action="play", title=h2("Full HD Quality"), url=video1080, thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)
'''

# Funciones auxiliares para dar un formato homogéneo
def titulo_pantalla(nombre, logo, fondo):
	plugintools.add_item(action="", title=h1(nombre), url="", thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)
	plugintools.add_item(action="", title="", url="", thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

def h1(mititulo):
    return "[COLOR mediumvioletred][B]" + mititulo.upper() + "[/B][/COLOR]"

def h2(mititulo):
    return "[COLOR lightpink][B]" + mititulo + "[/B][/COLOR]"

def h3(mititulo):
    return "[COLOR lightgreen]" + mititulo + "[/COLOR]"

def h4(mititulo):
     return "[COLOR purple][I]" + mititulo + "[/I][/COLOR]"
