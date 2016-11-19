# -*- coding: utf-8 -*-
#------------------------------------------------------------
# lnfstv.es
# Version 0.1.0 (2016.04.15)
# Changelog: 0.1 - Versión inicial
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import os, re, urllib, urllib2, sys, requests
import plugintools

addonName    = xbmcaddon.Addon().getAddonInfo("name")
addonVersion = xbmcaddon.Addon().getAddonInfo("version")
addonArt     = xbmcaddon.Addon().getAddonInfo("path") + "/art/"

ver     = '0.1.0'
referer = 'http://www.lnfstv.es/'
fondo   = 'http://i.imgur.com/w6CjdqL.jpg'
logo    = 'http://i.imgur.com/w6CjdqL.jpg'

def lnfstv0(params):
    data = requests.get(referer).content
    titulo_pantalla("Liga Nacional Fútbol Sala - LNFSTV", logo, fondo)

    bloque = plugintools.find_single_match(data, '<div id="menu">(.*?)</div>')
    lista = plugintools.find_multiple_matches(bloque, '<li(.*?)</ul></li>')
    for item in lista :
        if 'Zona Técnica' in item :
            plugintools.add_item(action='lnfstv2', title=h3('Zona Técnica'), url='http://www.lnfstv.es/zona_tecnica/zona_tecnica/All', thumbnail=logo, fanart=fondo, folder=True, isPlayable=False)
        else :
            seccion = plugintools.find_single_match(item, '>(.*?)<ul>')
            plugintools.add_item(action='lnfstv1', title=h3(seccion), url=item, thumbnail=logo, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action='lnfstv4', title=h2('Directos'), url='http://www.lnfsdirecto.es/', thumbnail=logo, fanart=fondo, folder=True, isPlayable=False)

    plugintools.add_item(action="", title=h5("Version " + ver + " 0.1.0"), fanart=fondo, thumbnail=logo, folder=False, isPlayable=False)


def lnfstv1(params):
    bloque = params.get("url")
    titulo_pantalla(params.get("title"),logo,fondo)
    lista = plugintools.find_multiple_matches(bloque, '<li>(.*?)</li>')
    for item in lista :
        nombre = plugintools.find_single_match(item, '">(.*?)</a>')
        enlace = plugintools.find_single_match(item, 'href="(.*?)"')
        enlace = 'http://www.lnfstv.es' + enlace + '/All'
        plugintools.add_item(action="lnfstv2", title=h3(nombre), url=enlace, thumbnail=logo, fanart=fondo, folder=True, isPlayable=False)

def lnfstv2(params):
    web    = params.get("url")
    data  = requests.get(web).content

    titulo_pantalla(params.get("title"),logo,fondo)
    bloque = plugintools.find_single_match(data, '<div id="videosSeccion">(.*?)<div id="pie">')
    lista  = plugintools.find_multiple_matches(bloque, '<div class="video-secc">(.*?)</a></div>')
    for item in lista :
        nombre = plugintools.find_single_match(item,'title="(.*?)">')
        nombre = fixcode(nombre)
        enlace = 'http://www.lnfstv.es' + plugintools.find_single_match(item, 'href="(.*?)"')
        poster = 'http://www.lnfstv.es' + plugintools.find_single_match(item, '&img=(.*?)"')
        plugintools.add_item(action="lnfstv3",title=h3(nombre), url=enlace, fanart=fondo, thumbnail=poster, folder=False, isPlayable=True)

def lnfstv3(params):
    data   = requests.get(params.get("url")).content
    video  = plugintools.find_single_match(data, '<meta property="og:video"(.*?) />')
    enlace = plugintools.find_single_match(video, 'file=(.*?)&')
    plugintools.play_resolved_url(enlace)

def lnfstv4(params):
    titulo_pantalla(params.get("title"),logo,fondo)
    data   = requests.get(params.get("url")).content
    lista = plugintools.find_multiple_matches(data, '<div class="box (.*?)</iframe>')
    for item in lista :
        nombre = plugintools.find_single_match(item, '<div class="box-title"(.*?)</div>')
        nombre = nombre.replace("<span>VS</span>", "vs").replace(">","").strip()
        date   = plugintools.find_single_match(item, '<div class="box-date"(.*?)/div>')
        fecha  = plugintools.find_single_match(date, '>(.*?)<')
        enlace = plugintools.find_single_match(item, 'src="(.*?)"')
        if 'youtube' in enlace :
            enlace = "plugin://plugin.video.youtube/play/?video_id=" + enlace[30:41]
            plugintools.runAddon(action="play", title=h3(nombre+" ("+fecha+") ")+h4('[YouTube]'), url=enlace, thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)
        else :
            plugintools.add_item(action='', title=nombre+" ("+fecha+")", url= enlace, fanart=fondo, thumbnail=logo, folder=False, isPlayable=True)


def fixcode(texto):
    texto = texto.replace("&#170;","ª")
    texto = texto.replace("&#180;","'")
    texto = texto.replace("&#186;","º")
    texto = texto.replace("&#193;","Á")
    texto = texto.replace("&#201;","É")
    texto = texto.replace("&#205;","Í")
    texto = texto.replace("&#209;","Ñ")
    texto = texto.replace("&#211;","Ó")
    texto = texto.replace("&#218;","ª")
    texto = texto.replace("&#225;","á")
    texto = texto.replace("&#233;","é")
    texto = texto.replace("&#237;","í")
    texto = texto.replace("&#241;","ñ")
    texto = texto.replace("&#243;","ó")
    texto = texto.replace("&#250;","ú")

    return texto


# Funciones auxiliares para dar un formato homogéneo
def titulo_pantalla(nombre, logo, fondo):
    nombre = nombre.replace("[/COLOR]","").replace("[COLOR lightblue]","").replace("[COLOR steelblue]","").replace("[B]","").replace("[/B]","").replace("[/I]","").replace("[I]","")
    plugintools.add_item(title=h1(nombre), thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

def linea_blanco(logo, fondo): 
    plugintools.add_item(thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

def h1(mititulo): return "[COLOR yellow][B]"    + mititulo.upper() + "[/B][/COLOR]"
def h2(mititulo): return "[COLOR lightblue][B]" + mititulo         + "[/B][/COLOR]" 
def h3(mititulo): return "[COLOR lightblue]"    + mititulo         + "[/COLOR]" 
def h4(mititulo): return "[COLOR steelblue][I]" + mititulo         + "[/I][/COLOR]"
def h5(mititulo): return "[COLOR gray][I]"      + mititulo         + "[/I][/COLOR]" #firma



