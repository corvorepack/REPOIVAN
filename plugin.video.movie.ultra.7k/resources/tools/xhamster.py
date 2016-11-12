# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de XHamster
# Version 0.3 (02.07.2016)
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
import requests

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR yellow]";ec3 = "[/COLOR]"
version = " [0.1]"

web = "http://es.xhamster.com/channels.php"
url_ref = "http://es.xhamster.com/channels.php"
thumbnail = 'http://logonoid.com/images/xhamster-logo.png'
fanart = 'https://pornpurity.files.wordpress.com/2014/12/image4.jpeg'
logo_pag = 'http://i63.tinypic.com/x6emic.jpg'
logo_cuadrado='http://media.steampowered.com/steamcommunity/public/images/avatars/a6/a6c5d93c6982a1fd72ddab0d2b21e6a92d155fc1_full.jpg'

DEFAULT_HEADERS = []
DEFAULT_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"] )
DEFAULT_HEADERS.append( ["Referer","http://es.xhamster.com/"] )

# Código de activación de Xhamster: 0001

def xhamster0(params):
    plugintools.log('[%s %s] Parseando XHamter %s' % (addonName, addonVersion, repr(params)))

    name = 'XHamster'
    update = '02/07/2016 18:00'
    Autor = 'PM'
    url = 'http://stec-site.xhcdn.com/images/logo/logo.png'

    r=requests.get(web)
    data=r.content
    #print data
    
    plugintools.addDir(action="",url="",title='[COLOR lightblue][B]Xhamster[/B]'+version+'[/COLOR]',thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    plugintools.addDir(action="xhamster_bus",url=web,title=sc2 +'Buscar Canal >>'+ec2,thumbnail=thumbnail,fanart=fanart,folder=True,isPlayable=False)

    if plugintools.get_setting("xh_hetero") == "true":
        categoria_het = plugintools.find_single_match(data, 'class="title">Heterosexual</div>(.*?)class="catName"')
        categ_het = plugintools.find_multiple_matches(categoria_het, 'class="btnBig"(.*?)<a')
        datamovie = {}
        for entry in categ_het:
            # plugintools.log("entry= "+entry)
            datamovie["Plot"] = plugintools.find_single_match(entry, 'hint="([^"]+)')        
            url_item = plugintools.find_single_match(entry, 'href="([^"]+)').strip()     
            title_item = plugintools.find_single_match(entry, '</div>(.*?)</a>').strip()
            if title_item == "":
                title_item = plugintools.find_single_match(entry, '>(.*?)</a>').strip()
            if title_item:
                    plugintools.addDir(action="xhamster1",url=url_item,title=sc + title_item + ec + "[COLOR green] [Hetero][/COLOR]",thumbnail=thumbnail,fanart=fanart,info_labels=datamovie,folder=True,isPlayable=False)
                    datamovie["Plot"] = ""  # Vaciamos esta variable para que actualice valor en la siguiente entrada                
            xbmcplugin.addSortMethod(int(sys.argv[1]), 1)

    if plugintools.get_setting("xh_trans") == "true":
        categoria_trans = plugintools.find_single_match(data, '<div class="title">Transexuales</div>(.*?)class="catName"')
        categ_trans = plugintools.find_multiple_matches(categoria_trans, 'class="btnBig"(.*?)<a')
        datamovie = {}
        for entry in categ_trans:
            # plugintools.log("entry= "+entry)
            datamovie["Plot"]= plugintools.find_single_match(entry, 'hint="([^"]+)')        
            url_item = plugintools.find_single_match(entry, 'href="([^"]+)').strip()        
            title_item = plugintools.find_single_match(entry, '</div>(.*?)</a>').strip()
            if title_item == "":
                title_item = plugintools.find_single_match(entry, '>(.*?)</a>').strip()
            if title_item:
                    plugintools.addDir(action="xhamster1",url=url_item,title=sc + title_item + ec + "[COLOR yellow] [Transexuales][/COLOR]",thumbnail=thumbnail,fanart=fanart,info_labels=datamovie,folder=True,isPlayable=False)
                    datamovie["Plot"] = ""  # Vaciamos esta variable para que actualice valor en la siguiente entrada                
            xbmcplugin.addSortMethod(int(sys.argv[1]), 1)

    if plugintools.get_setting("xh_gay") == "true":
        categoria_gay = plugintools.find_single_match(data, '<div class="title">Gays</div>(.*?)<div id="footer">')
        categ_gay = plugintools.find_multiple_matches(categoria_gay, 'class="btnBig"(.*?)<a')
        datamovie = {}
        for entry in categ_gay:
            # plugintools.log("entry= "+entry)
            datamovie["Plot"]= plugintools.find_single_match(entry, 'hint="([^"]+)')        
            url_item = plugintools.find_single_match(entry, 'href="([^"]+)').strip()        
            title_item = plugintools.find_single_match(entry, '</div>(.*?)</a>').strip()
            if title_item == "":
                title_item = plugintools.find_single_match(entry, '>(.*?)</a>').strip()
            if title_item:
                    plugintools.addDir(action="xhamster1",url=url_item,title=sc + title_item + ec +"[COLOR red] [Gays][/COLOR]",thumbnail=thumbnail,fanart=fanart,info_labels=datamovie,folder=True,isPlayable=False)
                    datamovie["Plot"] = ""  # Vaciamos esta variable para que actualice valor en la siguiente entrada                
            xbmcplugin.addSortMethod(int(sys.argv[1]), 1)
    
   
def xhamster1(params):
    plugintools.log('[%s %s] Parseando XHamter %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    #print url
    r = requests.get(url)
    data = r.content
    #print data

    # Buscando el número de página y el total de páginas de la sección...
    num_pag = plugintools.find_single_match(url, '\-([0-9]*).html').strip()  # Extraemos el número de la página actual
    total = params.get("extra")

    pager = plugintools.find_single_match(data, "<div class='pager'>(.*?)</table>")
    cons = plugintools.find_single_match(pager, "(</div>Próximo</a>)") # Etiqueta proximo en el codigo fuente verifica que no es la ultima pag..
    if cons != "":
        # plugintools.log("pager= "+pager)
        paginas = plugintools.find_multiple_matches(pager, "html'>([^<]+)") 
        total = paginas[-1]         
    else:
        total = plugintools.find_single_match(pager, "<span>(.*?)</span>") # Si la etiqueta del codigo fuente Proximo no esta es la ultima pag. = a pagina actual

    plugintools.add_item(action="xhamster_pag", title="[COLOR white]Ir a página... [CR]("+num_pag+"/"+total+")[/COLOR]", url=url, extra=total, thumbnail=logo_pag, fanart=fanart,folder=True, isPlayable=False)
    plugintools.add_item(action="xhamster0", title="[COLOR red]<< Menu Principal >>[/COLOR]", url=web,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png", fanart=fanart,folder=True, isPlayable=False)
    
    # Bloque de vídeos promocionados
    bloque_promo = plugintools.find_single_match(data,'<div class="boxC videoList clearfix">(.*?)<div class="vAds">')
    vid_promo = plugintools.find_multiple_matches(bloque_promo,'<div class="video">(.*?)/div></div></div>')
   
    #print vid_promo
    for item in vid_promo:
        title = plugintools.find_single_match(item,"<u>(.*?)</u>")
        url_vid = plugintools.find_single_match(item,'<a href="(.*?)"')
        img = plugintools.find_single_match(item,"<img src='(.*?)'")
        time = plugintools.find_single_match(item,"<b>(.*?)</b>")
        val = plugintools.find_single_match(item,'class="fr">(.*?)<')
        views = plugintools.find_single_match(item,'class="views-value">(.*?)<')
        quality = plugintools.find_single_match(item,'<div class="hSprite(.*?)"')
        if quality !="":
            quality = "[COLOR lightblue][B][I][HD][/I][/B][/COLOR]"
            titlefull = '[COLOR gold][B]['+str(val)+'][/B][/COLOR][COLOR white][I] '+str(views)+' views[/I] ' +quality+ "[CR]" +title + " - [" + str(time) + '][/COLOR]'
        else:
            titlefull = '[COLOR gold][B]['+str(val)+'][/B][/COLOR][COLOR white][I] '+str(views)+' views[/I][CR]' + title + " - [" + str(time) + '][/COLOR]'
        plugintools.addPic(action="xhamster2", title=titlefull, url=url_vid, thumbnail=img, fanart=fanart,folder=True, isPlayable=False)

    bloque_date = plugintools.find_single_match(data,"<div class='clear'></div>.*?<div class=\"video new-date\">(.*?)class='pager'><table")
    vid = plugintools.find_multiple_matches(bloque_date,'<a href="(.*?)/div></div></div>')
    
    for item in vid:
        title = plugintools.find_single_match(item,"<u>(.*?)</u>")
        url_vid = plugintools.find_single_match(item,'(.*?)"')
        img = plugintools.find_single_match(item,"<img src='(.*?)'")
        time = plugintools.find_single_match(item,"<b>(.*?)</b>")
        val = plugintools.find_single_match(item,'class="fr">(.*?)<')
        views = plugintools.find_single_match(item,'class="views-value">(.*?)<')
        quality = plugintools.find_single_match(item,'<div class="hSprite(.*?)"')
        if quality !="":
            quality = "[COLOR lightblue][B][I][HD][/I][/B][/COLOR]"
            titlefull = '[COLOR gold][B]['+str(val)+'][/B][/COLOR][COLOR white][I] '+str(views)+' views[/I] ' +quality+ "[CR]" +title + " - [" + str(time) + '][/COLOR]'
        else:
            titlefull = '[COLOR gold][B]['+str(val)+'][/B][/COLOR][COLOR white][I] '+str(views)+' views[/I][CR]' + title + " - [" + str(time) + '][/COLOR]'
        plugintools.addPic(action="xhamster2", title=titlefull, url=url_vid, thumbnail=img, fanart=fanart,folder=True, isPlayable=False)
        

# Paginador --------------------------->>
    
    url = params.get("url")

    # pagina anterior
    url_ant = plugintools.find_single_match(pager, "<div><a href='(.*?)'")
    if url_ant != "":
        pag_ant = plugintools.find_single_match(url_ant, '\-([0-9]*).html').strip()
        plugintools.addPic(action="xhamster1",title="[COLOR red]Anterior << [" +pag_ant+ "/" +total+ "][/COLOR]",url=url_ant,extra=total,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png",fanart=fanart,folder=True,isPlayable=False)
    # Pagina Inicio
    if int(num_pag) >= 2:
        pag_inic = url.replace(num_pag,"1")
        plugintools.addPic(action="xhamster1",title="[COLOR red]<< Inicio >>[/COLOR]",url=pag_inic,extra=total,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png",fanart=fanart,folder=True,isPlayable=False)
    # pagina Siguiente
    sig = plugintools.find_single_match(pager, "<span>.*?</span><a href='(.*?)'>(.*?)</a>")
    if sig != "":
        url_sig = sig[0]
        pag_sig = sig[1]
        plugintools.addPic(action="xhamster1",title="[COLOR red]Siguiente >> [" +pag_sig+ "/" +total+ "][/COLOR]",url=url_sig,extra=total,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png",fanart=fanart,folder=True,isPlayable=False)
    else:
        pag_sig = total
        url_sig = ""
        plugintools.addPic(action="xhamster1",title="[COLOR red][" +pag_sig+ "/" +total+ "][/COLOR]",url=url_sig,extra=total,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png",fanart=fanart,folder=True,isPlayable=False)
    
    
# Resolviendo enlaces ----------------->>

def xhamster2(params):
    plugintools.log('[%s %s] Parseando XHamter %s' % (addonName, addonVersion, repr(params)))
    
    
    url = params.get("url")
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url_ref}
    r=requests.get(url, headers=headers)
    data = r.content
 
    vid = params.get("title")
    img = params.get("thumbnail")
    
    bloque_link = plugintools.find_single_match(data,'players:(.*?)allowFullScreen:')
    
    link1 = plugintools.find_single_match(bloque_link,'file":"(.*?)"').replace("\\","")
    plugintools.add_item(action="", url="", title=vid, thumbnail=img, fanart=fanart, folder=False, isPlayable=False)
    plugintools.add_item(action="", title='[COLOR lightblue]-- Ver en Xhamster.com --[/COLOR]', url="", thumbnail=img, fanart=fanart, folder=False, isPlayable=False)
    plugintools.add_item(action="play", url=link1, title=sc + "Opción 1: [COLOR gold][I]240p[/I][COLOR]" + ec, thumbnail=img, fanart=fanart, folder=False, isPlayable=True)

    link2 = plugintools.find_single_match(bloque_link,'"videoUrls".*?480p.*?http:(.*?)"').replace("\\","")
    link2full = "http:" + link2
    if link2 != "":
        plugintools.add_item(action="play", url=link2full, title=sc + "Opción 2: [COLOR gold][I]480p[/I][COLOR]" + ec, thumbnail=img, fanart=fanart, folder=False, isPlayable=True)
    
    link3 = plugintools.find_single_match(bloque_link,'720p.*?http:(.*?)"').replace("\\","")
    link3full = "http:" + link3
    if link3 != "":
        plugintools.add_item(action="play", url=link3full, title=sc + "Opción 3: [COLOR gold][I]720p[/I][COLOR]" + ec, thumbnail=img, fanart=fanart, folder=False, isPlayable=True)  

# Enlaces a la web videater---------->>
    try:
        url_videater = 'http://videater.com/download/?url='+urllib.unquote_plus(url)  # Enlaces de Videater (Downloader Xhamster videos) ;)
        # plugintools.log("URL Videater= "+url)
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url_ref}
        r=requests.get(url_videater, headers=headers)
        data = r.content
        video=plugintools.find_single_match(data, 'var video = (.*?)}];')
        quality=[]
        item_quality=plugintools.find_multiple_matches(video, 'quality\":\"([^"]+)')
    
        for item in item_quality:
            item=item.replace("\/", "/")
            quality.append(item)
        urls=[]
        item_url=plugintools.find_multiple_matches(video, 'url\":\"([^"]+)')
        for item in item_url:
            item=item.replace("\/", "/")
            urls.append(item)
        thumbnail = plugintools.find_single_match(video, 'thumb\":\"([^"]+)')
        thumbnail=thumbnail.replace("\/", "/")
        plugintools.add_item(action="", title='[COLOR lightblue]-- Ver en Videater.com --[/COLOR]', url="", thumbnail=img, fanart=fanart, folder=False, isPlayable=False)
        i = 0
        total=len(urls)-1
        while i < total:
            plugintools.add_item(action="play", title='[COLOR white]Opción '+str(i+1)+': [COLOR gold][I]'+quality[i]+'[/I][/COLOR]', url=urls[i], thumbnail=img, fanart=fanart, folder=False, isPlayable=True)
            #plugintools.log("URL= "+urls[i])
            i = i + 1
            # print i
    except: pass
       
# Funcion buscadora de paginas---->>

def xhamster_pag(params):
    plugintools.log('[%s %s] Buscando página... %s' % (addonName, addonVersion, repr(params)))

    total = params.get("extra")
    plugintools.log("Número total de páginas: "+total)
    user_pag="";#user_pag = plugintools.keyboard_input(user_pag)  
    user_pag = xbmcgui.Dialog().numeric(0,'Introduzca núm. entre 1 y ' + total)  # Solicitamos al usuario número de página a mostrar
    plugintools.log("Página solicitada: "+user_pag)
    if user_pag == "":
        errormsg = plugintools.message("Movie Ultra 7K","Por favor, introduzca la pagina a buscar")
    else:
        try:
            if int(user_pag) <= int(total):
                url = params.get("url")  # Cogemos la URL del diccionario params
                num_pag = plugintools.find_single_match(url, '\-([0-9]*).html').strip()  # Extraemos el número de la página actual
                new_pag = url.replace(num_pag, user_pag).strip()  # Reemplazamos página actual por la que el usuario desea
                params = plugintools.get_params()
                params["url"] = new_pag
                xhamster1(params)    
            else:
                errormsg = plugintools.message("Movie Ultra 7K","Introduzca un valor inferior o igual a %s " % (total))        
        except ValueError:
            errormsg = plugintools.message("Movie Ultra 7K","Por favor, introduzca un valor numérico")
    

# Funcion Buscador global------>>

def xhamster_bus(params):
    plugintools.log('[%s %s] Buscando videos... %s' % (addonName, addonVersion, repr(params)))
    texto="";texto = plugintools.keyboard_input(texto)
    texto = texto.lower()  # Pasamos el texto a minúsculas para evitar problemas
    if texto == "":
        errormsg = plugintools.message("Movie Ultra 7K","Por favor, introduzca el canal a buscar")
        #return errormsg
    else:
        texto = texto.lower().strip()
        texto = texto.replace(" ", "+")
        url_bus = 'http://es.xhamster.com/search.php?from=&q='+texto+'&qcat=video'
        params = plugintools.get_params() 
        params["url"] = url_bus
        xhamster_bus1(params)  # pasando los resultados a xhamster_bus1
    

def xhamster_bus1(params):
    plugintools.log('[%s %s] Buscando videos... %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    r = requests.get(url)
    data = r.content

    pager = plugintools.find_single_match(data, "<div class='pager'>(.*?)</table>")
    
    # Buscando el número de página y el total de páginas de la sección...
    num_pag = plugintools.find_single_match(pager, '<span>([0-9]*)</span>').strip()  # Extraemos el número de la página actual
    
    total = params.get("extra")

    # Capturando el cambio de codigo fuente de la ultima pag
    cons = plugintools.find_single_match(pager, "(</div>Próximo</a>)") # Etiqueta proximo en codigo fuente para saber que no es ultima pag.
    if cons != "":
        # plugintools.log("pager= "+pager)
        paginas = plugintools.find_multiple_matches(pager, "qcat=video&amp;page=([0-9]*)'>") 
        total = paginas[-1]
    else:
        total = plugintools.find_single_match(pager, "<span>(.*?)</span>") # Falta la etiqueta proximo en el codigo fuente, es la ultima pag.
            
    plugintools.add_item(action="xhamster_buspag", title="[COLOR white]Ir a página... [CR]("+num_pag+"/"+total+")[/COLOR]", url=url, extra=total, thumbnail=logo_pag, fanart=fanart,folder=True, isPlayable=False)
    plugintools.add_item(action="xhamster0", title="[COLOR red]<< Menu Principal >>[/COLOR]", url=web,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png", fanart=fanart,folder=True, isPlayable=False)
    
    bloque_buscado = plugintools.find_single_match(data,"Resultados de busqueda(.*?)<div class='pager'>")
    vid = plugintools.find_multiple_matches(bloque_buscado,"<a href='(.*?)/div></div></div>")

    for item in vid:
        title = plugintools.find_single_match(item,"<u>(.*?)</u>")
        url_vid = plugintools.find_single_match(item,'(.*?)"')
        img = plugintools.find_single_match(item,"<img src='(.*?)'")
        time = plugintools.find_single_match(item,"<b>(.*?)</b>")
        val = plugintools.find_single_match(item,'class="fr">(.*?)<')
        views = plugintools.find_single_match(item,'class="views-value">(.*?)<')
        quality = plugintools.find_single_match(item,'<div class="hSprite(.*?)"')
        if quality !="":
            quality = "[COLOR lightblue][B][I][HD][/I][/B][/COLOR]"
            titlefull = '[COLOR gold][B]['+str(val)+'][/B][/COLOR][COLOR white][I] '+str(views)+' views[/I] ' +quality+ "[CR]" +title + " - [" + str(time) + '][/COLOR]'
        else:
            titlefull = '[COLOR gold][B]['+str(val)+'][/B][/COLOR][COLOR white][I] '+str(views)+' views[/I][CR]' + title + " - [" + str(time) + '][/COLOR]'
        plugintools.add_item(action="xhamster2", title=titlefull, url=url_vid, thumbnail=img, fanart=fanart,folder=True, isPlayable=False)

    # Paginador------------>>

    # pagina anterior
    url_ant = plugintools.find_single_match(pager, "<div><a href='(.*?)'").replace("amp;","")
    pag_ant = plugintools.find_single_match(pager, "<div><a href='(.*?)qcat=video&amp;page=([0-9]*)'")
    if url_ant != "":
        pag_ant = plugintools.find_single_match(url_ant, 'page=([0-9]*)').strip()
        if pag_ant == "":
            pag_ant = "1"
        plugintools.add_item(action="xhamster_bus1",title="[COLOR red]Anterior << [" +pag_ant+ "/" +total+ "][/COLOR]",url=url_ant,extra=total,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png",fanart=fanart,folder=True,isPlayable=False)

    # Pagina Inicio
    buscado = plugintools.find_single_match(pager, "<a href='(.*?)page=([0-9])'")
    url_inic = buscado[0].replace("amp;","")
    pag = buscado[1].replace(buscado[1],"1") 
    pag_inic = url_inic+"page="+pag                                                                                                    
    if int(num_pag) >= 2:
        plugintools.add_item(action="xhamster_bus1",title="[COLOR red]<< Inicio >>[/COLOR]",url=pag_inic,extra=total,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png",fanart=fanart,folder=True,isPlayable=False)
    
    # pagina Siguiente
    sigfull = plugintools.find_single_match(pager, "<span>.*?</span><a href='([^']*)'>([^<]*)</a>") 
    if cons != "":
        sig = [sigfull[0].replace("amp;",""),sigfull[1]]
        url_sig = sig[0]
        pag_sig = sig[1]
        if pag_sig == "...":
            pag_sig = (int(num_pag)+1)  # Reemplazando el resultado ... de la paginacion por pagina actual +1
        plugintools.add_item(action="xhamster_bus1",title="[COLOR red]Siguiente >> [" +str(pag_sig)+ "/" +str(total)+ "][/COLOR]",url=url_sig,extra=total,thumbnail="http://stec-site.xhcdn.com/images/logo/logo.png",fanart=fanart,folder=True,isPlayable=False)   
    else:
        pag_sig = total
        url_sig = ""
    
    
def xhamster_buspag(params):
    plugintools.log('[%s %s] Buscando página... %s' % (addonName, addonVersion, repr(params)))

    total = params.get("extra")
    plugintools.log("Número total de páginas: "+total)
    user_pag="";#user_pag = plugintools.keyboard_input(user_pag)  
    user_pag = xbmcgui.Dialog().numeric(0,'Introduzca núm. entre 1 y ' + total)  # Solicitamos al usuario número de página a mostrar
    plugintools.log("Página solicitada: "+user_pag)
    if user_pag == "":
        errormsg = plugintools.message("Movie Ultra 7K","Por favor, introduzca la pagina a buscar")
    else:
        try:
            if int(user_pag) <= int(total):
                url = params.get("url")  # Cogemos la URL del diccionario params
                num_pag = plugintools.find_single_match(url, 'page=([0-9]*)').strip()  # Extraemos el número de la página actual
                if num_pag == "":
                    num_pag = "1"
                new_pag = url.replace(num_pag, user_pag).strip()  # Reemplazamos página actual por la que el usuario desea
                params = plugintools.get_params()
                params["url"] = new_pag
                xhamster_bus1(params)    
            else:
                errormsg = plugintools.message("Movie Ultra 7K","Introduzca un valor inferior o igual a %s " % (total))            
        except ValueError:
            errormsg = plugintools.message("Movie Ultra 7K","Por favor, introduzca un valor numérico")
    
          
# ---------------------------------------------------------------------------------------------------------------------------------------------