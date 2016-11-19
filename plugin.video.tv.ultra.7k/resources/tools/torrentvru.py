# -*- coding: utf-8 -*-
#------------------------------------------------------------
# TV Ultra 7K Parser de torrent-tv.ru
# Version 0.1 (17.10.2014) by Juarrox
# Version 0.2 (23.08.2015) by Queque (añadido cookie,canales en pruebas)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)

import time

from __main__ import *
baseurl='http://torrent-tv.ru/'
'''
try:
 p2p=xbmcaddon.Addon('plugin.video.p2p-streams')
 p2p_dir=xbmc.translatePath(p2p.getAddonInfo('path')+'\\resources\\core');#print p2p_dir
 sys.path.append(p2p_dir);import acestream as ace
except:
 p2p=xbmcaddon.Addon('program.plexus')
 p2p_dir=xbmc.translatePath(p2p.getAddonInfo('path')+'\\resources\\plexus');#print p2p_dir
 sys.path.append(p2p_dir);import acestream as
'''

# Общие = "General" (cat=5)
# Новостные = "Noticias" (cat=7)
# Развлекательные = "Entretenimiento" (cat=8)
# Детские = "Infantiles" (cat=1)
# Фильмы = "Cine" (cat=3)
# Спорт = "Deportes" (cat=4)
# Познавательные = "Documentales" (cat=6)
# Музыка = "Música" (cat=2)
# Мужские = "Para hombres" (cat=10)
# Региональные = "Regional" (cat=11)
# Религиозные = "religiosos" (cat=12)
# HD каналы = "Canales HD" (hd_channels.php)
# Каналы на модерации = "En moderación" (on_moderation.php)


def torrentvru0(params):
    plugintools.log("[tv.ultra.7k-0.3.0].Torrent-TV.ru Playlist Sport Channels( "+repr(params))
    plugintools.add_item(action="", title = '[B][I][COLOR gold]Torrent-tv.ru[/B] [COLOR lightgreen]Acestream Sports Playlist[/I][/COLOR]', url = "", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)    

    url = params.get("url")
    plugintools.log("url= "+url)
    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    title = params.get("title")

    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Generalistas[/COLOR] [COLOR lightyellow][I](Общие)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=5", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Noticias[/COLOR] [COLOR lightyellow][I](Новостные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=7", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Entretenimiento[/COLOR] [COLOR lightyellow][I](Развлекательные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=8", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Infantiles[/COLOR] [COLOR lightyellow][I](Детские)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=1", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Cine[/COLOR] [COLOR lightyellow][I](Фильмы)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=3", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Deportes[/COLOR] [COLOR lightyellow][I](Спорт)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=4", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Documentales[/COLOR] [COLOR lightyellow][I](Познавательные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=6", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Música[/COLOR] [COLOR lightyellow][I](Музыка)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=2", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Para hombres[/COLOR] [COLOR lightyellow][I](Мужские)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=10", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Regionales[/COLOR] [COLOR lightyellow][I](Региональные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=11", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Religiosos[/COLOR] [COLOR lightyellow][I](Религиозные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=12", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Canales HD[/COLOR] [COLOR lightyellow][I](HD каналы)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "hd_channels.php", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]En pruebas[/COLOR] [COLOR lightyellow][I](Каналы на модерации)[/I][/COLOR] [COLOR red][/COLOR]', url = "http://torrent-tv.ru/on_moderation.php", extra = "on_moderation.php", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    


def torrentvru_section(params): 
    url = params.get("url");ref=baseurl;cook='';id = params.get("extra");#cook='BHC=;';#tok=X-BH-Token#http://torrent-tv.ru/banhammer/pid
    url=url+'?'+id if 'channels' in url else url
    data,resp = torrenttvru_get_HTML(url,ref,cook)
    match = plugintools.find_single_match(data, id+'(.*?)</ul></li>');
    if match:
     matches = plugintools.find_multiple_matches(match, '<a href="(.*?)</li>')
     for entry in matches:
         plugintools.log("entry= "+entry)
         entry = entry.split('"');
         url = 'http://www.torrent-tv.ru' + entry[0]
         url = url.strip();
         url_fixed = entry[0].replace("/", "")
         plugintools.log("url_fixed= "+url_fixed)
         chid = url.split("=")[1];print 'chid',chid
         try:thm=torrentvru_getlogo(url_fixed,data)
         except:thm='http://1ttv.org/images/logo.png';pass
         title = entry[1]
         title= title.replace("</a>", "")
         title= title.replace(">", "")
         title = title.strip()
         title_fixed = title.replace(" ", "+")
         plugintools.log("title= "+title)
         try:plugintools.add_item(action="torrentvru_channels", title = title, url = url, thumbnail = thm , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = False, isPlayable = True)
         except:pass
    else:
        print 'except'
        matches = plugintools.find_multiple_matches(data,'best-channels-content.*?href=[\'"]([^\'"]+).*?src=[\'"]([^\'"]+).*?<strong>\s([^\s]+)')
        for i in matches:
            plugintools.add_item(action="torrentvru_channels", title =i[2], url=baseurl+i[0], thumbnail=baseurl+i[1], fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = False, isPlayable = True)



def torrentvru_channels(params):
    #plugintools.log("[tv.ultra.7k-0.3.0].Torrent-tv.ru getAcestream: "+url)

    #data,resp = torrenttvru_get_HTML(params['url'],baseurl,'')
	url='http://api.torrent-tv.ru/v3/auth.php?username=anonymous&password=anonymous&typeresult=json&application=xbmc&guid=18e07270538011e595b5dca971aac3a4'
	data,resp = torrenttvru_get_HTML(url,baseurl,'');r='session":"([^"]+)';sess=plugintools.find_single_match(data,r);id='(\d{4,8})';
	id=plugintools.find_single_match(params['url'],id);url='http://api.torrent-tv.ru/v3/translation_stream.php?session='+sess+'&channel_id='+id+'&typeresult=json';data,resp=torrenttvru_get_HTML(url,url,'');s='source":"([^"]+)';s=plugintools.find_single_match(data,s);
	'''
	#ANTIGUO
	match = plugintools.find_multiple_matches(data, 'this.load(Player|Torrent)\s?\([\'|"]([^\'"]+)')
	flash = plugintools.find_single_match(data, '<a\shref=[\'"]([^\'"]+)')
	#data,resp = torrenttvru_get_HTML(baseurl+flash,params['url'],'');#print data;sys.exit()
	#print 'FLASH LINK',flash;
	url = match[0][1].strip()
	plugintools.log("ace= "+url)
	local_torrent=xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))+url.split('/')[3].replace('acelive','torrent')
	urllib.urlretrieve(url,local_torrent)
	ace.acestreams(params['title'],'',url)
	'''
	url = 'plugin://program.plexus/?url='+s.replace('/','')+'&mode=1&name='+params['title'];plugintools.play_resolved_url(url)
	#url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+params['title'];plugintools.play_resolved_url(url)
	sys.exit()

def torrentvru_getlogo(url_fixed, data):
    #plugintools.log("[tv.ultra.7k-0.3.0].Torrent-tv.ru getLogo: "+url_fixed)
    matches = plugintools.find_multiple_matches(data,'<a\shref=[\'"]'+re.escape(url_fixed)+'[\'"]>.*?<img\ssrc=[\'"]([^\'"]+)');#print matches;
    #http://web1.torrent-tv.ru/shots/_-11644_1444943103.png
    return baseurl+matches[0]
	
def torrenttvru_get_HTML(url,ref,cook):
    request_headers=[];
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36"])
    request_headers.append(["Connection","keep-alive"])
    request_headers.append(["Accept","*/*"])
    request_headers.append(["Accept-Encoding","gzip, deflate, sdch"])
    request_headers.append(["Referer",ref])
    request_headers.append(["X-Requested-With","XMLHttpRequest"])
    if cook:request_headers.append(["Cookie",cook])
    try:
        body,response_headers=plugintools.read_body_and_headers('http://torrent-tv.ru/banhammer/pid',headers=request_headers);
        if str(response_headers).find('x-bh-token')>=0:
            r='x-bh-token\',\s\'([^\']+)';cook=plugintools.find_single_match(str(response_headers),r);request_headers.append(["Cookie",'BHC='+cook])
            body,response_headers=plugintools.read_body_and_headers(url,headers=request_headers);
            return body,response_headers
    except:
        body, response_headers=plugintools.read_body_and_headers(url, headers=request_headers); return body, response_headers
