# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Filmon
# Version 0.1 (2016.07.02)
# Author: PM
# Changelog: 0.1 - Versión inicial
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import os, re, urllib, urllib2, sys, requests
import plugintools

from resources.tools.resolvers import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

art = addonPath + "/art/"
web   = 'http://www.filmon.com/tv/live'
fondo = 'https://wallpaperscraft.com/image/points_cubes_background_light_91691_1920x1080.jpg'
logo  = 'http://i.imgur.com/oEx3yEs.png'


def filmon0(params):
    plugintools.log("[%s %s] Parser FilmON " % (addonName, addonVersion))
    titulo_pantalla("FilmON Categories", logo, fondo)

    data = requests.get(web).content
    grupos = plugintools.find_multiple_matches(data,'{"group_id":(.*?)"channels_count"')
    for item in grupos :
        titulo = plugintools.find_single_match(item,'"title":"(.*?)",')
        codigo = plugintools.find_single_match(item,'"id":"(.*?)",')
        thumb  = plugintools.find_single_match(item,'"logo_148x148_uri":"(.*?)",').replace("\\","")
        plugintools.add_item(action="filmon_group", title=h2(titulo), extra=item, fanart=fondo, thumbnail=thumb, folder=True, isPlayable=False)
    plugintools.add_item(action="", title="", fanart=fondo, thumbnail=logo, folder=False, isPlayable=False)
    plugintools.add_item(action="", title=h5("Version 0.1"), fanart=fondo, thumbnail=logo, folder=False, isPlayable=False)



def filmon_group(params):
    grupo   = params.get("title")
    bloque  = params.get("extra")
    titulo_pantalla(grupo,logo, fondo)
    canales = plugintools.find_multiple_matches(bloque,'{"id"(.*?)}')
    for item in canales :
        titulo = plugintools.find_single_match(item,'"title":"(.*?)",').replace("\u2013"," - ")
        alias  = plugintools.find_single_match(item,'"alias":"(.*?)",')
        thumb  = plugintools.find_single_match(item,'"big_logo":"(.*?)",').replace("\\","")
        tipo   = plugintools.find_single_match(item,'"type":"(.*?)",')
        adult  = plugintools.find_single_match(item,'"is_adult":(.*?),')
        enlace = 'http://www.filmon.com/tv/' + alias
        if tipo == "standard" :
            titulo = h2(titulo) + h4(" [LIVE]")
        else :
            titulo = h2(titulo) + h4(" ["+tipo.upper()+"]")
        if adult == "true":
            titulo = titulo + "[COLOR red] [+18][/COLOR]"
        plugintools.add_item(action="filmon", title=titulo, url=enlace, fanart=fondo, thumbnail=thumb, folder=False, isPlayable=True)

# Funciones auxiliares para dar un formato homogéneo
def titulo_pantalla(nombre, logo, fondo):
    plugintools.add_item(action="", title=h1(nombre), url="", thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)
    plugintools.add_item(action="", title="", url="", thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

def h1(mititulo):
    mititulo = mititulo.replace("[COLOR lightblue]","").replace("[/COLOR]","")
    return "[COLOR yellow][B]" + mititulo.upper() + "[/B][/COLOR]"

def h2(mititulo):
    return "[COLOR lightblue]" + mititulo + "[/COLOR]"

def h3(mititulo):
    return "[COLOR lime][B]" + mititulo + "[/B][/COLOR]"

def h4(mititulo):
     return "[COLOR steelblue]" + mititulo + "[/COLOR]"

def h5(mititulo):
     return "[COLOR gray][I]" + mititulo + "[/I][/COLOR]"
