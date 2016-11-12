# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Elitetorrent para Movie Ultra 7K
# Version 0.1 (18.10.2014)
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

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://dl.dropbox.com/sh/60p8ad35vzoyua4/AAD9R-DK8LC5rpAa8UIoa1rDa/elitetorrent.jpg'
fanart = 'http://i.imgur.com/SaIORL1.jpg'


def elite0(params):
    plugintools.log("[%s %s] Elitetorrent últimos estrenos %s " % (addonName, addonVersion, repr(params)))

    thumbnail = params.get("thumbnail")
   
    plugintools.add_item(action="elite1", title = '[COLOR blue][B]EliteTorrent[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="elite1", title = '[COLOR white][B]Subidas Destacadas[/B][/COLOR]', url = "http://www.elitetorrent.net/ajax/pestana.php?op=0", thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="elite1", title = '[COLOR white][B]Últimos Estrenos[/B][/COLOR]', url = "http://www.elitetorrent.net/ajax/pestana.php?op=1", thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="elite1", title = '[COLOR white][B]Pelis HDrip[/B][/COLOR]', url = "http://www.elitetorrent.net/ajax/pestana.php?op=2", thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="elite1", title = '[COLOR white][B]Pelis Recomendadas[/B][/COLOR]', url = "http://www.elitetorrent.net/ajax/pestana.php?op=4", thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)    
    plugintools.add_item(action="elite1", title = '[COLOR white][B]Series Destacadas[/B][/COLOR]', url = "http://www.elitetorrent.net/ajax/pestana.php?op=3", thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

       


def elite1(params):
    plugintools.log("[%s %s] Elitetorrent últimos estrenos %s " % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="", title='[B][COLOR white]Título[COLOR blue] (Fecha de subida) [COLOR green][Puntuación] [COLOR red][Video/Audio][/COLOR][/B]', url="", thumbnail= thumbnail, fanart=fanart, folder=False, isPlayable=False)
    
    url = params.get("url")
    r = plugintools.read(url)

    matches = plugintools.find_multiple_matches(r, '<li>(.*?)</li>')
    for entry in matches:
        if entry.find("loco-bingo-1.html") >= 0:
            pass
        else:
            url_torrent = plugintools.find_single_match(entry, '<a href="([^"]+)')
            url_torrent = 'http://www.elitetorrent.net'+url_torrent
            thumb_torrent = plugintools.find_single_match(entry, 'src="([^"]+)')
            thumb_torrent = thumb_torrent.replace("../", "")
            thumb_torrent = 'http://www.elitetorrent.net/'+thumb_torrent
            title_torrent = plugintools.find_single_match(entry, 'title="([^"]+)')
            age = plugintools.find_single_match(entry, '<span class="fecha">(.*?)</span>')
            nota = plugintools.find_single_match(entry, 'title="Valoracion media">([^<]+)')
            quality = plugintools.find_single_match(entry, '<span class="voto2"[^>]+>([^<]+)')            
            if nota == "": nota = "N/D"
            if quality == "": quality = "N/D"
            
            plugintools.add_item(action="elite2", title='[COLOR white][B]'+title_torrent+'[COLOR green] ('+age+') [COLOR red]['+nota+'] [COLOR blue]['+quality+'][/B][/COLOR]', url=url_torrent, thumbnail= thumb_torrent, fanart=fanart, folder=False, isPlayable=True)


def elite2(params):
    plugintools.log("[%s %s] Elitetorrent obteniendo url %s " % (addonName, addonVersion, repr(params)))   
    url = params.get("url")
    #r = requests.get(url)
    r = plugintools.read(url)
    url_magnet = plugintools.find_single_match(r, '<a href="magnet:([^"]+)');url_magnet = 'magnet:'+url_magnet;print url_magnet
    addon_magnet = plugintools.get_setting("addon_magnet")
    if addon_magnet == "0":  # Stream (por defecto)
        url = 'plugin://plugin.video.stream/play/'+url_magnet
    elif addon_magnet == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url_magnet
    elif addon_magnet == "2":  # Kmediatorrent
        url = 'plugin://plugin.video.kmediatorrent/play/'+url_magnet

    #url = urllib.unquote_plus(url)
    plugintools.log("Magnet URL= "+url)
    plugintools.play_resolved_url(url)       
