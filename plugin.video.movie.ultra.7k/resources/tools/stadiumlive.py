# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie Ultra 7K Parser de Stadium-live.biz
# Version 0.1 (17.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#
# Todos los canales se reproducen con el servidor playerapp1
#------------------------------------------------------------


import os
import urllib
import urllib2
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, scrapertools
import sys,traceback,urllib2,re

from __main__ import *


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

art = xbmc.translatePath(os.path.join(addonPath + '/art/', ''))
fanart = 'http://images.forwallpaper.com/files/thumbs/preview/20/200693__fan-football-stadium-sports_p.jpg'
thumbnail = art + 'stadiumlive.png'

burl = 'http://www.stadium-live.biz/'


def stadiumlivebiz0(params):
    plugintools.log('[%s %s] Initializing stadium-live.biz parser... %s' % (addonName, addonVersion, repr(params)))
    plugintools.add_item(action="stadiumlivebiz2", title="[COLOR lightgreen][B]stadium-live.biz[/B][/COLOR] [COLOR lightyellow][I](Click para abrir lista de canales)[/I][/COLOR]", url="" , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)    

    burl = params.get("url");headers = {"Referer": burl};r=requests.get(burl, headers=headers);r.encoding = 'utf-8';body=r.content
    #plugintools.log("body= "+body)
    schedule_bloque = plugintools.find_single_match(body, 'calendar_wrap(.*?)<!--')
    #plugintools.log("schedule= "+schedule_bloque)
    events = plugintools.find_multiple_matches(schedule_bloque, '<tr>(.*?)</a></p>\n</td>')
    for entry in events:
        plugintools.log("entry= "+entry)
        if entry != "":
            entry = entry.replace("&nbsp;", "")
            event_time = plugintools.find_single_match(entry, '<p class=\"sdfsf\">(.*?)</td>').strip()
            plugintools.log("event_time= "+event_time)
            event_title = plugintools.find_single_match(entry, '\" class="sdfsf">(.*?)</td>')
            event_title = event_title.replace("<p>","").replace("&uuml;", "ü").replace("&auml;", "ä").strip()
            ch_total = ""
            if event_title.startswith("Schedule") == False:
                event_channel = plugintools.find_single_match(entry, 'href="([^"]+)')
                event_channel = 'http://www.stadium-live.biz/'+event_channel
                ch = plugintools.find_multiple_matches(entry, '<span class="Linkch">(.*?)</span>')
                print ch
                for item in ch:
                    item=item.replace("Channel", "Ch").strip()
                    if ch_total == "":
                        ch_total = item
                    else:
                        ch_total = ch_total + ", " + item
                #plugintools.log("event_time= "+event_time)
                #plugintools.log("event_title= "+event_title)
                #plugintools.log("event_channel= "+event_channel)
                #plugintools.log("ch= "+ch)
                plugintools.add_item(action="stadiumlivebiz1", title='[COLOR orange][B]'+event_time+' [/B][COLOR lightyellow][I]'+event_title+'[/I][/COLOR]' , fanart = fanart , thumbnail = thumbnail , url=ch_total , folder = False, isPlayable = True)


def stadiumlivebiz1(params):
    plugintools.log('[%s %s] Initializing stadium-live.biz parser... %s' % (addonName, addonVersion, repr(params)))

    try:
        ref = burl;ch = params.get("url");ch_total = ch.split(", ");title = params.get("title")
        selector = plugintools.selector(ch_total, title)
        if selector >= -1:
            kanal = ch_total[selector]
            kanal = kanal.split("(")[0]
            kanal=burl+kanal.replace(" ","").replace("Ch", "Channel").strip()+'.html'
            print kanal
            headers = {"Referer": burl};r=requests.get(kanal, headers=headers);r.encoding = 'utf-8';body=r.content
            #plugintools.log("body= "+body)
            caster = plugintools.find_multiple_matches(body, '<!--<script type="text/javascript" src="([^"]+)')
            for entry in caster:
                if entry.find("autostart=true") >= 0:
                    #plugintools.log("entry= "+entry)
                    caster = entry
                    
            ref = kanal;url = ref.replace("Channel", "ch_").strip();url = url.replace(".html", "");url = url+'code.html'
            headers = {"Referer": burl};r=requests.get(url, headers=headers);r.encoding = 'utf-8';body=r.content    
            #plugintools.log("body= "+body)

            #<script type="text/javascript" src="http://www.playerapp1.pw/channel.php?file=118&width=800&height=450&autostart=true"></script>
            url = plugintools.find_single_match(body, 'src="([^"]+)')
            headers = {"Referer": 'http://www.stadium-live.biz/ch_1code.html'};r=requests.get(url, headers=headers);r.encoding = 'utf-8';body=r.content    
            url = plugintools.find_single_match(body, 'src="([^"]+)');url=url.strip()    
            #plugintools.log("url= "+url)
            #plugintools.log("ref= "+ref)
            headers = {"Referer": 'http://www.stadium-live.biz/ch_1code.html'};r=requests.get(url, headers=headers);r.encoding = 'utf-8';body=r.content
            print 'url',url
            print 'ref',ref            
            playerapp1(url,ref,body)

    except KeyboardInterrupt: pass;
    except IndexError: raise            

        
    
def playerapp1(url,ref,body):
    k=url;hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);#print hidd;
    swfUrl='http://www.playerapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));    
    app=plugintools.find_single_match(hidd[1][1].decode('base64').replace('\\',''),'1735\/([^"]+)');#app=app.replace("vod", "redirect")
    q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto    
    w=hidd[1][1].decode('base64').replace('\\','').replace("vod","redirect")+' app='+app+' playpath='+hidd[0][1].decode('base64')+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+k+' live=1 timeout=15'
    plugintools.play_resolved_url(w);sys.exit()
    
   
def stadiumlivebiz2(params):
    plugintools.log('[%s %s] stadiumlivebiz2 %s' % (addonName, addonVersion, repr(params)))
    
    headers = {"Referer": burl};r=requests.get(burl, headers=headers);r.encoding = 'utf-8';body=r.content
    #plugintools.log("body= "+body)
    channel_bloque = plugintools.find_single_match(body, '<ul id="main"(.*?)</ul>')
    channel = plugintools.find_multiple_matches(channel_bloque, '<li>(.*?)</li>')
    lista_ch = []
    url_ch = []

    for entry in channel:
        if entry != "":
            #plugintools.log("entry= "+entry)
            url_channel = plugintools.find_single_match(entry, '<a href="([^"]+)')
            url_channel = 'http://www.stadium-live.biz/'+url_channel
            title_channel = plugintools.find_single_match(entry, '<a href[^>]+>(.*?)</a>')
            #plugintools.log("title_channel= "+title_channel)
            lista_ch.append(title_channel)
            url_ch.append(url_channel)
            #plugintools.log("url_channel= "+url_channel)
            #plugintools.add_item(action="stadiumlivebiz1", title='[COLOR white]'+title_channel+'[/COLOR]', url=url_channel , thumbnail = art + 'stadiumlive.png' , fanart = fanart , folder = False, isPlayable = True)

    try:
        select_ch = plugintools.selector(lista_ch, 'Stadium-live.biz')
        if select_ch >= -1:
            kanal = lista_ch[select_ch]
            kanal=burl+kanal.replace(" ","")+'.html'
            print kanal
            headers = {"Referer": burl};r=requests.get(kanal, headers=headers);r.encoding = 'utf-8';body=r.content
            caster = plugintools.find_multiple_matches(body, '<!--<script type="text/javascript" src="([^"]+)')
            for entry in caster:
                if entry.find("autostart=true") >= 0:
                    #plugintools.log("entry= "+entry)
                    caster = entry

            ref = kanal;url = ref.replace("Channel", "ch_").strip();url = url.replace(".html", "");url = url+'code.html'
            headers = {"Referer": burl};r=requests.get(url, headers=headers);r.encoding = 'utf-8';body=r.content    
            #<script type="text/javascript" src="http://www.playerapp1.pw/channel.php?file=118&width=800&height=450&autostart=true"></script>
            url = plugintools.find_single_match(body, 'src="([^"]+)')
            headers = {"Referer": 'http://www.stadium-live.biz/ch_1code.html'};r=requests.get(url, headers=headers);r.encoding = 'utf-8';body=r.content    
            url = plugintools.find_single_match(body, 'src="([^"]+)');url=url.strip()    
            #plugintools.log("url= "+url)
            #plugintools.log("ref= "+ref)
            headers = {"Referer": 'http://www.stadium-live.biz/ch_1code.html'};r=requests.get(url, headers=headers);r.encoding = 'utf-8';body=r.content
            print 'url',url
            print 'ref',ref
            playerapp1(url,ref,body)


            

    except KeyboardInterrupt: pass;
    except IndexError: raise            

