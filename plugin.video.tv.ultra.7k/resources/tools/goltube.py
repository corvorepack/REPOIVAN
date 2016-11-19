# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de TousSports.info para TV Ultra 7K
# Version 0.1 (05.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a Juarrox


import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import plugintools

from __main__ import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


def goltube0(params):
    plugintools.log("[%s %s] GolTube " % (addonName, addonVersion))

    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    url = params.get("url")    
    
    plugintools.add_item(action="", title= '[COLOR white][B]Gol[/COLOR][COLOR red]Tube[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    
    data = gethttp_referer_headers(url,url)
    plugintools.log("data= "+data)

    categorias = plugintools.find_single_match(data, '<div class="standard-menu">(.*?)</span></a></li></ul>')
    plugintools.log("categorias= "+categorias)
    cats = plugintools.find_multiple_matches(categorias, '<a class="parent-item "(.*?)<span class="down-arrow">')
    for entry in cats:
        plugintools.log("entry= "+entry)
        url_cat = plugintools.find_single_match(entry, 'href="([^"]+)')
        url_title = plugintools.find_single_match(entry, '<span class="category-title">([^<]+)')
        plugintools.log("url_cat= "+url_cat)
        plugintools.log("url_title= "+url_title)
        if url_title != "Blog":
            plugintools.add_item(action="goltube1", title=url_title, url=url_cat, thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable =False)


def goltube1(params):
    plugintools.log("[%s %s] GolTube " % (addonName, addonVersion))

    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    url = params.get("url")

    data = gethttp_referer_headers(url,url)
    plugintools.log("data= "+data)
    title_head = plugintools.find_single_match(data, '<h1 class="main-title archive-title">(.*?)</h1>')
    plugintools.log("title_head= "+title_head)
    plugintools.add_item(action="", title='[COLOR white][B]Gol[/COLOR][COLOR red]Tube[/COLOR][COLOR lightyellow] / '+title_head+'[/B][/COLOR]', url="", thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable =False)

    bloque = plugintools.find_single_match(data, '<h1 class="main-title archive-title">(.*?)<div class="load-more">')
    plugintools.log("bloque= "+bloque)

    items = plugintools.find_multiple_matches(bloque, '<div class="article-panel(.*?)</span></div></div></div>')
    for entry in items:
        plugintools.log("entry= "+entry)
        title_item = plugintools.find_single_match(entry, '<h2><a href=[^>]+([^<]+)').replace(">", "").upper().strip()
        url_item = plugintools.find_single_match(entry, 'href="([^"]+)')
        thumb_cat_id = plugintools.find_single_match(entry, 'category-icon-([0-9]+)')
        thumb_cat_item = plugintools.find_single_match(data, thumb_cat_id+'{background:url\(([^)]+)')
        thumb_item = plugintools.find_single_match(entry, '<img src="([^"]+)')
        # http://canalplus.es/recorte.php?xref=20150830plucanftb_7&type=Ies&id=REC200
        # http://canalplus.es/recorte.php/?id=20150305plucanftb_1&id=REC200
        # http://canalplus.es/recorte.php?xref=20150305plucanftb_1.Ies&r=REC200
        thumb_item = thumb_item.replace("&amp;", "&").strip()
        # thumb_item = thumb_item.replace("http://canalplus.es/recorte//?id=", "http://canalplus.es/recorte.php?xref=").replace(".Ies", "&type=Ies").replace("&amp;t=se&amp;v=", "").replace("&amp;r=", "&id=").strip()
        datamovie = {}
        sinopsis = plugintools.find_single_match(entry, 'VIDEO DEL PARTIDO:(.*?)</div>')
        datamovie["plot"] = sinopsis.replace("u00e1", "á").replace("u00ed", "í").replace("u00e9", "é").replace("u00f3", "ó").replace("u00a1", "¡").replace("00f1", "ñ").replace("&oacute;", "ó").replace("&#8212;", "-").replace("&Aacute;","Á").replace("&eacute;", "é").replace("&iacute;", "í").replace("&aacute;", "á").strip()
        plugintools.add_item(action="goltube2", title=title_item, url=url_item, thumbnail=thumb_item, fanart=fanart, info_labels = datamovie, folder=False, isPlayable=True)
        
        plugintools.log("title_item= "+title_item)
        plugintools.log("url_item= "+url_item)
        plugintools.log("thumb_cat_item= "+thumb_cat_item)
        plugintools.log("thumb_item= "+thumb_item)


def goltube2(params):
    plugintools.log("[%s %s] GolTube " % (addonName, addonVersion))

    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    url = params.get("url")

    data = gethttp_referer_headers(url,url)
    url_item = plugintools.find_single_match(data, '<iframe src="([^"]+)')
    plugintools.log("url_item= "+url_item)
    data = gethttp_referer_headers(url_item,url_item)
    plugintools.log("data= "+data)

    urls = []
    titles = []
    url_media = plugintools.find_multiple_matches(data, '<source src="([^"]+)')
    i = 1
    for entry in url_media:
        plugintools.log("Media: "+entry)
        quality = plugintools.find_single_match(entry, 'Ves_[0-9]+').replace("Ves_", "")
        urls.append(entry)
        titles.append('Opción '+str(i)+' [COLOR lightyellow][I]('+quality+')[/I][/COLOR]')
        i = i + 1
        
    print urls
    seleccion = plugintools.selector(titles, 'GolTube')
    if seleccion >= 0:
        plugintools.play_resolved_url(urls[seleccion])
    
    
    
        
	
def gethttp_referer_headers(url,referer):
    plugintools.modo_vista("tvshows");request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);
    try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
    except: pass
    try: r='\'location\',\s\'([^\']+)';loc=plugintools.find_single_match(str(response_headers),r);
    except: pass
    if loc:
     request_headers.append(["Referer",url]);
     if jar: request_headers.append(["Cookie",jar]);#print jar
     body,response_headers=plugintools.read_body_and_headers(loc,headers=request_headers);
     try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
     except: pass
     plugintools.modo_vista("tvshows")
    return body
