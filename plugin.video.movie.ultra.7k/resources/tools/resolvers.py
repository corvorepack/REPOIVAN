# -*- coding: utf-8 -*-
#------------------------------------------------------------

#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------


import os, sys, urllib, urllib2, re, string, shutil, zipfile, time, urlparse, random
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import plugintools, unpackerjs, requests, jsunpack, base64, json, wiz, cookielib

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

from __main__ import *
'''para UNPACK'''
from wiz import *

art = addonPath + "/art/"
temp = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))

def urlr(url):
    plugintools.log('[%s %s] Probando URLR con... %s' % (addonName, addonVersion, url))

    import urlresolver
    host = urlresolver.HostedMediaFile(url)
    print 'host',host
    if host:
        resolver = urlresolver.resolve(url)
        print 'URLR',resolver
        return resolver
    else:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "URL Resolver: Servidor no soportado", 3 , art+'icon.png'))

def novamov(params): auroravid(params)
def movshare(params): wholecloud(params)
def videoweed(params): bitvid(params)
def waaw(params): netu(params)
def noslocker(params): nosvideo(params)
def cloudzilla(params): neodrive(params)
  
def allmyvideos(params):
    plugintools.log('[%s %s] Allmyvideos %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not 'embed' in page_url:
        #http://amvtv.net/embed-3hn5sihfhp5o-728x400.html
        page_url = page_url.replace("https://allmyvideos.net/", "http://amvtv.net/embed-")
        page_url = page_url.replace("http://allmyvideos.net/", "http://amvtv.net/embed-")+'-728x400.html'   
    r = requests.get(page_url)
    data = r.content

    #########################  ############################
    #######################  #########################

    if "Access denied" in data:
        # url = "http://www.anonymousbrowser.xyz/hide.php"
        # post = "go=%s" % page_url
        url = "http://www.videoproxy.co/hide.php"
        post = "go=%s" % page_url
        
        r = requests.get(url,data=post,allow_redirects=False)#,headers=headers)
        data = r.content
        location = r.headers['location']
        #url=http://www.videoproxy.co/go/247005/nph-proxy.cgi/en/20/http//amvtv.net/embed-jwvvkc14b0xr-728x400.html
        page_url = page_url.replace('http://','')
        url = "http://www.videoproxy.co/" + location+page_url
        
        r = requests.get(url)
        data = r.content 
        # Extrae la URL
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')
        for item in media:
            if item.endswith('mp4?v2'):
                #http://www.videoproxy.co/go/91523/nph-proxy.cgi/en/20/http//d6066.allmyvideos.net/d/4smooougyq5dh6lnatf4x2osp67jyomdwvaivwqtp3qfmryett6sf56t677cvdq/video.mp4?v2&direct=false
                item = item.replace('http://','')
                media_url = "http://www.videoproxy.co/" + location+item+'&direct=false'
                print '<'*10+'- Movies Ultra -'+'>'*10
                print '$'*80+'- Movies Ultra -'+'$'*80,media_url,'$'*179          
    else:
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')
        for item in media:
            if item.endswith('mp4?v2'):
                media_url = item+'&direct=false'
                print '<'*10+'- Movies Ultra -'+'>'*10
                print '$'*65+'- Movies Ultra -'+'$'*65,media_url,'$'*149

    #########################  ############################
    #######################  #########################
                
    plugintools.play_resolved_url(media_url)

def streamcloud(params):
    plugintools.log('[%s %s]Streamcloud %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")

    try:
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
        #plugintools.log("data= "+body)

        # Barra de progreso para la espera de 10 segundos
        progreso = xbmcgui.DialogProgress()
        progreso.create("Movies Ultra 7K", "Abriendo Streamcloud..." , url )

        i = 13000
        j = 0
        percent = 0
        while j <= 13000 :
            percent = ((j + ( 13000 / 10.0 )) / i)*100
            xbmc.sleep(i/10)  # 10% = 1,3 segundos
            j = j + ( 13000 / 10.0 )
            msg = "Espera unos segundos, por favor... "
            percent = int(round(percent))
            print percent
            progreso.update(percent, "" , msg, "")
        

        progreso.close()
    
        media_url = plugintools.find_single_match(body , 'file\: "([^"]+)"')
    
        if media_url == "":
            op = plugintools.find_single_match(body,'<input type="hidden" name="op" value="([^"]+)"')
            usr_login = ""
            id = plugintools.find_single_match(body,'<input type="hidden" name="id" value="([^"]+)"')
            fname = plugintools.find_single_match(body,'<input type="hidden" name="fname" value="([^"]+)"')
            referer = plugintools.find_single_match(body,'<input type="hidden" name="referer" value="([^"]*)"')
            hashstring = plugintools.find_single_match(body,'<input type="hidden" name="hash" value="([^"]*)"')
            imhuman = plugintools.find_single_match(body,'<input type="submit" name="imhuman".*?value="([^"]+)">').replace(" ","+")

            post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
            request_headers.append(["Referer",url])
            body,response_headers = plugintools.read_body_and_headers(url, post=post, headers=request_headers)
            plugintools.log("data= "+body)
        

            # Extrae la URL
            media_url = plugintools.find_single_match( body , 'file\: "([^"]+)"' )
            plugintools.log("media_url= "+media_url)
            plugintools.play_resolved_url(media_url)

            if 'id="justanotice"' in body:
                plugintools.log("[streamcloud.py] data="+body)
                plugintools.log("[streamcloud.py] Ha saltado el detector de adblock")
                return -1
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def playedto(params):
    plugintools.log('[%s %s] Played.to %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    url = url.split("/")
    url_fixed = "http://played.to/embed-" + url[3] +  "-640x360.html"
    plugintools.log("url_fixed= "+url_fixed)

    try:
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url_fixed, headers=request_headers)
        body = body.strip()
    
        if body == "<center>This video has been deleted. We apologize for the inconvenience.</center>":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Enlace borrado...", 3 , art+'icon.png'))
        elif body.find("Removed for copyright infringement") >= 0:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Removed for copyright infringement", 3 , art+'icon.png'))
        else:
            r = re.findall('file(.+?)\n', body)
            for entry in r:
                entry = entry.replace('",', "")
                entry = entry.replace('"', "")
                entry = entry.replace(': ', "")
                entry = entry.strip()
                plugintools.log("vamos= "+entry)
                if entry.endswith("flv"):
                    media_url = entry             
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def vidspot(params):
    plugintools.log('[%s %s] Vidspot %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    if not 'embed' in page_url:
        page_url = page_url.replace("http://vidspot.net/", "http://vidspot.net/embed-")+".html"   
    r = requests.get(page_url)
    data = r.content

    ######################### ############################
    #######################  #########################
    
    if "Access denied" in data:
        # url = "http://www.anonymousbrowser.xyz/hide.php"
        # post = "go=%s" % page_url
        url = "http://www.videoproxy.co/hide.php"
        post = "go=%s" % page_url
        
        r = requests.get(url,data=post,allow_redirects=False)
        data = r.content
        location = r.headers['location']
        #url=http://www.videoproxy.co/go/247005/nph-proxy.cgi/en/20/http//amvtv.net/embed-jwvvkc14b0xr-728x400.html
        page_url = page_url.replace('http://','')
        url = "http://www.videoproxy.co/" + location+page_url
        r = requests.get(url)
        data = r.content 
        # Extrae la URL
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')
        for item in media:
            if item.endswith('mp4?v2'):
                #http://www.videoproxy.co/go/91523/nph-proxy.cgi/en/20/http//d6066.allmyvideos.net/d/4smooougyq5dh6lnatf4x2osp67jyomdwvaivwqtp3qfmryett6sf56t677cvdq/video.mp4?v2&direct=false
                item = item.replace('http://','')
                media_url = "http://www.videoproxy.co/" + location+item+'&direct=false'
                print '<'*10+'- Movies Ultra -'+'>'*10
                print '$'*80+'- Movies Ultra -'+'$'*80,media_url,'$'*179

    else:
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')
        for item in media:
            if item.endswith('mp4?v2'):
                media_url = item+'&direct=false'
                print '<'*10+'- Movies Ultra -'+'>'*10
                print '$'*65+'- Movies Ultra -'+'$'*65,media_url,'$'*149

    #########################  ############################
    #######################  #########################
               
    plugintools.play_resolved_url(media_url)
				
def vk(params):
    plugintools.log('[%s %s] Vk %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        page_url = page_url.replace('http://lidplay.net/jwplayer/video_ext.php?','http://new.vk.com/video_ext.php?')
        page_url = page_url.replace('http://vkontakte.ru/video_ext.php?','http://new.vk.com/video_ext.php?')
        page_url = page_url.replace('http://f6.videosxd.org/v.php?v=','http://new.vk.com/video_ext.php?oid=')

        ######################## Public Video #########################
        try:
            id_vid = plugintools.find_single_match(page_url,'video(.*_.*)')
            url = 'http://vk.com/al_video.php?act=show_inline&al=1&video='+id_vid
            headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
            r = requests.get(url)#,headers=headers)
            data = r.content
            recompile_url = plugintools.find_multiple_matches(data,'source src="(.*?)"')
            media_url = recompile_url[0]
        ###############################################################   
        ######################## Private Video ########################   
        except:
            extrac_params = page_url.split("=")
            #http://vk.com/video_ext.php?oid=295239104&id=171117835&hash=2425e0df405e816a&hd=2
            extrac_oid = plugintools.find_single_match(extrac_params[1],'(\w{9})')
            extrac_id = plugintools.find_single_match(extrac_params[2],'(\w{9})')
            extrac_hash = plugintools.find_single_match(extrac_params[3],'(\w{16})')
            url = 'http://api.vk.com/method/video.getEmbed?oid='+extrac_oid+'&video_id='+extrac_id+'&embed_hash='+extrac_hash
            r = requests.get(url)
            data = r.content
            data_js = json.loads(data)
            oid = data_js['error']['request_params'][2]['value']
            id = data_js['error']['request_params'][3]['value']
            hash = data_js['error']['request_params'][4]['value']
            url_js = 'http://vk.com/al_video.php?act=show_inline&al=1&video='+oid+'_'+id
            r = requests.get(url_js)#,headers=headers)
            data = r.content
            recompile_url = plugintools.find_multiple_matches(data,'source src="(.*?)"')
            media_url = recompile_url[0]
        ###############################################################
        print '$'*90+'- By Movies Ultra -'+'$'*90,media_url,'$'*199
        plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def nowvideo(params):
    plugintools.log('[%s %s] Nowvideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if "embed" in page_url:
            page_url = page_url.replace("http://embed.nowvideo.sx/embed/?v=","http://www.nowvideo.sx/")
        r = requests.get(page_url)
        data = r.content
        
        stepkey = plugintools.find_single_match(data, 'name="stepkey" value="(.*?)"')
        submit = "submit"
        post = 'stepkey='+stepkey+'&submit='+submit
        headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12', "Referer": params.get("url")}
    
        body,response_headers = plugintools.read_body_and_headers(page_url,headers=headers,post=post,follow_redirects=True)
        data = body
        
        if "no longer exists" in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "El archivo no está en disponible", 3 , art+'icon.png'))        
        else:
            domain = plugintools.find_single_match(data, 'flashvars.domain="([^"]+)"')
            video_id = plugintools.find_single_match(data, 'flashvars.file="([^"]+)"')
            filekey = plugintools.find_single_match(data, 'flashvars.filekey=([^;]+);')
            token_txt = 'var '+filekey
            token = plugintools.find_single_match(data, filekey+'=\"([^"]+)"')
            token = token.replace(".","%2E").replace("-","%2D")
        
            if video_id == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "El archivo no está en disponible", 3 , art+'icon.png'))
            else:
                #http://www.nowvideo.sx/api/player.api.php?user=undefined&pass=undefined&cid3=undefined&numOfErrors=0&cid2=undefined&key=83%2E47%2E1%2E12%2D8d68210314d70fb6506817762b0d495e&file=b5c8c44fc706f&cid=1
                url = 'http://www.nowvideo.sx/api/player.api.php?user=undefined&pass=undefined&cid3=undefined&numOfErrors=0&cid2=undefined&key='+token+'&file='+video_id+'&cid=1'
                r = requests.get(url)
                data = r.content

                referer = 'http://www.nowvideo.sx/'
                request_headers=[]
                request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
                request_headers.append(["Referer",referer])
                body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
                
                body = body.replace("url=", "")
                body = body.split("&")
                if len(body) >= 0:
                    media_url = body[0]
                    print '$'*45+'-  -'+'$'*45,media_url,'$'*109       
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

'''

def tumi(params):
    plugintools.log('[%s %s] Tumi %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        data = scrapertools.cache_page(page_url)
    
        if "Video is processing now" in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "El archivo está en proceso", 3 , art+'icon.png'))       
        else:
            try:
                x = scrapertools.find_single_match(data, "\|type\|(.*?)\|file\|").replace("||","|").split("|")
                n = scrapertools.find_single_match(data, "//k.j.h.([0-9]+):g/p/v.o")

                printf = "http://%s.%s.%s.%s:%s/%s/%s.%s"
                if n:
                    url = printf % (x[3], x[2], x[1],    n, x[0], x[8], "v", x[7])
                else:
                    url = printf % (x[4], x[3], x[2], x[1], x[0], x[9], "v", x[8])
            except:
                media_url = scrapertools.find_single_match(data, "file:'([^']+)'")        
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

'''
    
def veehd(params):
    plugintools.log('[%s %s] VeeHD %s' % (addonName, addonVersion, repr(params)))
    
    uname = plugintools.get_setting("veehd_user")
    pword = plugintools.get_setting("veehd_pword")
    if uname == '' or pword == '':
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Debes configurar el identificador para Veehd.com", 3 , art+'icon.png'))
        return
    url = params.get("url")
    url_login = 'http://veehd.com/login'

    try:
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        request_headers.append(["Referer",url])
    
        post = {'ref': url, 'uname': uname, 'pword': pword, 'submit': 'Login', 'terms': 'on'}
        post = urllib.urlencode(post)
    
        body,response_headers = plugintools.read_body_and_headers(url_login, post=post, headers=request_headers, follow_redirects=True)
        vpi = plugintools.find_single_match(body, '"/(vpi.+?h=.+?)"')
        if not vpi:
            if 'type="submit" value="Login" name="submit"' in body:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Error al identificarse en Veehd.com", 3 , art+'icon.png'))
            else:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Error buscando el video en Veehd.com", 3 , art+'icon.png'))            
            return
        req = urllib2.Request('http://veehd.com/'+vpi)
        for header in request_headers:
            req.add_header(header[0], header[1]) # User-Agent
        response = urllib2.urlopen(req)
        body = response.read()
        response.close()

        va = plugintools.find_single_match(body, '"/(va/.+?)"')
        if va:
            req = urllib2.Request('http://veehd.com/'+va)
            for header in request_headers:
                req.add_header(header[0], header[1]) # User-Agent
            urllib2.urlopen(req)

        req = urllib2.Request('http://veehd.com/'+vpi)
        for header in request_headers:
            req.add_header(header[0], header[1]) # User-Agent
        response = urllib2.urlopen(req)
        body = response.read()
        response.close()

        video_url = False
        if 'application/x-shockwave-flash' in body:
            video_url = urllib.unquote(plugintools.find_single_match(body, '"url":"(.+?)"'))
        elif 'video/divx' in body:
            video_url = urllib.unquote(plugintools.find_single_match(body, 'type="video/divx"\s+src="(.+?)"'))

        if not video_url:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Error abriendo el video en Veehd.com", 3 , art+'icon.png'))
            return  
        media_url = video_url
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def turbovideos(params):
    plugintools.log('[%s %s] Turbovideos %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        url = page_url.replace('/embed-', '/')
        url = re.compile('//.+?/([\w]+)').findall(url)[0]
        url = 'http://turbovideos.net/embed-%s.html' % url
        #result = client.request(url)
        result = requests.get(url).content
        url = re.compile('file *: *"(.+?)"').findall(result)
        if len(url) > 0: plugintools.play_resolved_url(url[0])  

        result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
        result = unpack(result)
        #url = client.parseDOM(result, 'embed', ret='src')
        url += re.compile("file *: *[\'|\"](.+?)[\'|\"]").findall(result)
        url = [i for i in url if not i.endswith('.srt')]
        media_url = url[0]  
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def streaminto(params):
    plugintools.log('[%s %s] streaminto %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://streamin.to/","http://streamin.to/embed-") +'.html'
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
        r = requests.get(page_url, headers=headers)
        data = r.content
        if data == "File was deleted":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))        
        else:
            media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
            print '$'*38+'- By Movies Ultra -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)     
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
       
def powvideo(params):
    plugintools.log('[%s %s] Powvideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    #Evitando Error si la url entra com embed-
    if 'embed' in page_url:
        id_vid = plugintools.find_single_match(page_url,'http://powvideo.net/embed-(.*?)-')
        page_url = 'http://powvideo.net/'+id_vid  
    try:
        if not "iframe" in page_url:
            page_iframe = page_url.replace("http://powvideo.net/","http://powvideo.xyz/iframe-") + "-1920x920.html"
        ref = page_iframe.replace('iframe','embed')
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer': ref}
        r = requests.get(page_iframe,headers=headers)
        data = r.text
        if not 'File was deleted' in data:
            data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data = wiz.unpack(data)
        else:
            page_url = params.get("url")
            if not "preview" in page_url:
                page_preview = page_url.replace("http://powvideo.net/","http://powvideo.net/preview-") + "-1920x920.html"
            r = requests.get(page_preview)
            data = r.content
            ref = page_preview
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer': ref}
            page_iframe = page_preview.replace('preview','iframe')
            r = requests.get(page_iframe,headers=headers)
            data = r.text
            data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data = wiz.unpack(data)
            #print data
        sources = plugintools.find_multiple_matches(data,"image:image,tracks:tracks,src:'(.*?)'")
        #print sources
        if sources !="":
            id_vid = plugintools.find_single_match(sources[-1],'(/[0-9a-z]([0-9a-z]{40,}))')
            new_id = id_vid[-1]
            url_options =[]
            ### RTMP ###
            try:
                #rtmp://178.33.238.147:19350/vod/ playpath=mp4:01/00458/wzb1oas8oup3_n?h=hjmohokshjaikkfn2mdip2iyfg3yf62p3wkebwbae3tc7b55yvr7o75axr4 swfUrl=http://powvideo.net/player6/jwplayer.flash.swf pageUrl=http://powvideo.net/wzb1oas8oup3
                #rtmp://5.39.69.236:19350/vod/mp4:01/00305/v6jql5rhtvvp_n?h=uj4ohomxypuikkfn2mav72isjhyr5amti4cdgn7vk72axekxvgbbwy7ldlm
                swfurl = 'swfUrl=http://powvideo.net/player6/jwplayer.flash.swf'; pageurl = 'pageUrl='+page_iframe
                url_rtmp = plugintools.find_single_match(sources[0],'(rtmp.*?=)')
                url_rtmp = url_rtmp.replace('mp4:',' playpath=mp4:')+new_id
                media_rtmp = url_rtmp+'|'+swfurl+'|'+pageurl
                url_options.append(media_rtmp)
            except:pass
            ### M3U8 ###
            try:
                media_m3u8 = plugintools.find_single_match(sources[1],'(http://.*?/)')+new_id+'.m3u8|User-Agent='+headers['User-Agent']
                url_options.append(media_m3u8)
            except:pass
            ### MP4 ###
            try:
                media_mp4 = media_url = plugintools.find_single_match(sources[2],'(http://.*?/)')+new_id+'/v.mp4'
                url_options.append(media_mp4)
            except:pass
        if len(sources) >1:
                options = []
                opct = '[COLORlightyellow]Opcion rtmp[/COLOR]';options.append(opct)   
                opct = '[COLORlightyellow]Opcion m3u8[/COLOR]';options.append(opct)  
                opct = '[COLORlightyellow]Opcion mp4[/COLOR]';options.append(opct)
                select_option = plugintools.selector(options,'Movies Ultra **Powvideo**')
                ######### Evitamos el error de cancelacion con valor -1 ########
                if select_option >=0:  
                    i = select_option
                    media_url = url_options[i]    
                    print '$'*110+'- By Movies Ultra -'+'$'*110,media_url,'$'*239
                    plugintools.play_resolved_url(media_url)
                else: pass
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url 

def mailru(params):
    plugintools.log('[%s %s] Mail.ru %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    
    #http://my.mail.ru/mail/anny.cam/video/_myvideo/1589.html 
    page_url = page_url.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed/')
    page_url = page_url.replace('/videoapi.my.mail.ru/', '/api.video.mail.ru/')
    try:
        r = requests.get(page_url)
        data = r.content
    
        new_url = plugintools.find_single_match(data,'metaUrl":.*?"([^"]+)"').strip()
        new_url = new_url+"?ver=0.2.114"
    
        headers = {"Host": "my.mail.ru","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
        "Referer": "http://my1.imgsmail.ru/r/video2/uvpv3.swf?58"}
        #Cookie: video_key=16d3637ca27c94312812741024af82f6015a8f80 |Cookie=video_key="
        r = requests.get(new_url,headers=headers)
        data_js = r.text
        cookie_vidkey = r.cookies['video_key']
        js = json.loads(data_js)
        media = js['videos'][0]['url'].replace('%3A',':').replace('%2F','/').replace('%3D','=').replace('%3F','?').replace('%26','&')
        if media == "":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            media_url = 'http:'+media + "|Cookie=video_key=" + cookie_vidkey
            #media_url = media + "|Cookie=video_key=" + cookie_vidkey
            print '$'*110+'-  -'+'$'*110,media_url,'$'*239 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)

def mediafire(params):
    plugintools.log('[%s %s] Mediafire %s' % (addonName, addonVersion, repr(params)))

    # Solicitud de página web
    url = params.get("url")
    data = plugintools.read(url)

    # Espera un segundo y vuelve a cargar
    plugintools.log("[Movies Ultra] Espere un segundo...")
    import time
    time.sleep(1)
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    pattern = 'kNO \= "([^"]+)"'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        plugintools.log("entry= "+entry)
    # Tipo 1 - http://www.mediafire.com/download.php?4ddm5ddriajn2yo
    pattern = 'mediafire.com/download.php\?([a-z0-9]+)'
    matches = re.compile(pattern,re.DOTALL).findall(data)    
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 1 = "+url)
            
'''
    # Tipo 2 - http://www.mediafire.com/?4ckgjozbfid
    pattern  = 'http://www.mediafire.com/\?([a-z0-9]+)'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 2 = "+url)
        
    # Tipo 3 - http://www.mediafire.com/file/c0ama0jzxk6pbjl
    pattern  = 'http://www.mediafire.com/file/([a-z0-9]+)'
    plugintools.log("[mediafire.py] find_videos #"+pattern+"#")
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 3 = "+url)

'''
          
def auroravid(params):
    plugintools.log('[%s %s] Novamov (Antes: Novamov) %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")

    if 'novamov' in page_url:
        page_url = page_url.replace('http://www.novamov.com','http://www.auroravid.to')
    try:
        headers = {"Host": "www.auroravid.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content

        videoid = plugintools.find_single_match(page_url,"http://www.auroravid.to/video/([a-z0-9]+)")
        stepkey = plugintools.find_single_match(data,'name="stepkey" value="([^"]+)"')
        ref = page_url
        post = "stepkey="+stepkey+"&submit=submit"
        
        headers = {"Host": "www.auroravid.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0","Referer":page_url}
        body,response_headers = plugintools.read_body_and_headers(page_url, post=post)
        
        #http://www.auroravid.to/api/player.api.php?file=d0f559fe7f8ec&key=87.219.239.45-bb8140bed80d5abe821ce4f61781c1f7&cid2=undefined&numOfErrors=0&cid3=auroravid.to&user=undefined&pass=undefined&cid=1
        stream_url = plugintools.find_single_match(body,'flashvars.filekey="(.*?)"')
        cid1 = plugintools.find_single_match(body,'flashvars.cid="(.*?)"')
        headers = {"Host": "www.auroravid.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
        "Referer":"http://www.auroravid.to/player/cloudplayer.swf"} 
        
        url = "http://www.auroravid.to/api/player.api.php?file="+videoid+"&key="+stream_url+"&cid2=undefined&numOfErrors=0&cid3=auroravid.to&user=undefined&pass=undefined&cid="+str(cid1)
        r=requests.get(url,headers=headers)
        data=r.content
        if data != "":
            media_url = plugintools.find_single_match(data,'url=(.*?)&title')
            print '$'*45+'-  -'+'$'*45,media_url,'$'*109
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "El Archivo no esta disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url    
      
    plugintools.play_resolved_url(media_url)

def gamovideo(params):
    plugintools.log('[%s %s] Gamovideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        if "File was deleted" in data or "File Not Found" in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "El Archivo no esta disponible", 3 , art+'icon.png'))
        else:
            bloq_vid = plugintools.find_single_match(data,"playlist: \[\{(.*?)</script>")
            if bloq_vid !="":
                bloq_file = plugintools.find_multiple_matches(bloq_vid,'file: "([^"]+)"')
                media_url = bloq_file[-1]+'|Referer='+page_url
                print '$'*68+'- By Movies Ultra -'+'$'*68,media_url,'$'*155
                plugintools.play_resolved_url(media_url)  
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def moevideos(params):
    plugintools.log('[%s %s] Moevideos %s' % (addonName, addonVersion, repr(params)))

    # No existe / borrado: http://www.moevideos.net/online/27991
    page_url = params.get("url")

    try:
        data = scrapertools.cache_page(page_url)
        plugintools.log("data= "+data)
        if "<span class='tabular'>No existe</span>" in data:
            return False,"No existe o ha sido borrado de moevideos"
        else:
            # Existe: http://www.moevideos.net/online/18998
            patron  = "<span class='tabular'>([^>]+)</span>"
            headers = []
            headers.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
            data = scrapertools.cache_page( page_url , headers=headers )            
            # Descarga el script (no sirve para nada, excepto las cookies)
            headers.append(['Referer',page_url])
            post = "id=1&enviar2=ver+video"
            data = scrapertools.cache_page( page_url , post=post, headers=headers )
            code = scrapertools.get_match(data,'<iframe width="860" height="440" src="http://moevideo.net/framevideo/([^\?]+)\?width=860\&height=440" frameborder="0" allowfullscreen ></iframe>')
            plugintools.log("code="+code)

            # API de letitbit
            headers2 = []
            headers2.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
            ### Modificado 12-6-2014
            url = "http://api.letitbit.net"
            #url = "http://api.moevideo.net"
            post = 'r=["tVL0gjqo5",["preview/flv_image",{"uid":"'+code+'"}],["preview/flv_link",{"uid":"'+code+'"}]]'
            data = scrapertools.cache_page(url,headers=headers2,post=post)
            plugintools.log("data="+data)
            if ',"not_found"' in data:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo borrado!", 3 , art+'icon.png'))
            else:
                data = data.replace("\\","")
                plugintools.log("data="+data)
                patron = '"link"\:"([^"]+)"'
                matches = re.compile(patron,re.DOTALL).findall(data)
                video_url = matches[0]+"?ref=www.moevideos.net|User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:15.0) Gecko/20100101 Firefox/15.0.1&Range=bytes:0-"
                plugintools.log("[moevideos.py] video_url="+video_url)

                video_urls = []
                video_urls.append( [ scrapertools.get_filename_from_url(video_url)[-4:] + " [moevideos]",video_url ] )
                media_url = video_url[1]
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)
     
def wholecloud(params):
    plugintools.log('[%s %s] Wholecloud (Antes: Movshare) %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if "http://www.movshare.net/" in page_url:
        page_url = page_url.replace("http://www.movshare.net/","http://www.wholecloud.net/")

    try:
        headers = {"Host": "www.wholecloud.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content
       
        videoid = plugintools.find_single_match(page_url,"http://www.wholecloud.net/video/([a-z0-9]+)")
        stepkey = plugintools.find_single_match(data,'name="stepkey" value="([^"]+)"')
        ref = page_url
        post = "stepkey="+stepkey+"&submit=submit"
        headers = {"Host": "www.wholecloud.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":page_url}
        
        body,response_headers = plugintools.read_body_and_headers(page_url, post=post)
        
        #http://www.wholecloud.net/api/player.api.php?key=87.218.124.147-49d804aa90e1b1e0d6c9f6032fefd671&numOfErrors=0&user=undefined&pass=undefined&cid=1&file=p2x88vrlfli8g&cid3=wholecloud.net&cid2=undefined
        stream_url = plugintools.find_single_match(body,'flashvars.filekey="(.*?)"')
        cid1 = plugintools.find_single_match(body,'flashvars.cid="(.*?)"')
        headers = {"Host": "www.wholecloud.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
        "Referer":"http://www.wholecloud.net/player/cloudplayer.swf"} 
        url = "http://www.wholecloud.net/api/player.api.php?key="+stream_url+"&numOfErrors=0&user=undefined&pass=undefined&cid="+str(cid1)+"&file="+videoid+"&cid3=wholecloud.net&cid2=undefined"
        r=requests.get(url,headers=headers)
        data=r.content
        
        pass_err = plugintools.find_single_match(data,'url=(.*?)&title')
        new_url = url ="http://www.wholecloud.net/api/player.api.php?key="+stream_url+"&numOfErrors=1&user=undefined&errorUrl="+pass_err+"pass=undefined&cid="+str(cid1)+"&file="+videoid+"&cid3=wholecloud.net&cid2=undefined&errorCode=404"
        r=requests.get(new_url,headers=headers)
        data=r.content
        if data != "":
            media_url = plugintools.find_single_match(data,'url=(.*?)&title')
            print '$'*45+'-  -'+'$'*45,media_url,'$'*109
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "El Archivo no esta disponible", 3 , art+'icon.png'))     
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url    
      
    plugintools.play_resolved_url(media_url)

def movreel(params):
    plugintools.log('[%s %s] Movreel %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    try:
        video_urls = []
        data = scrapertools.cache_page(page_url)

        op = plugintools.find_single_match(data,'<input type="hidden" name="op" value="([^"]+)">')
        file_code = plugintools.find_single_match(data,'<input type="hidden" name="file_code" value="([^"]+)">')
        w = plugintools.find_single_match(data,'<input type="hidden" name="w" value="([^"]+)">')
        h = plugintools.find_single_match(data,'<input type="hidden" name="h" value="([^"]+)">')
        method_free = plugintools.find_single_match(data,'<input type="submit" name="method_free" value="([^"]+)">')

        #op=video_embed&file_code=yrwo5dotp1xy&w=600&h=400&method_free=Close+Ad+and+Watch+as+Free+User
        #post = 'op=video_embed&file_code='+file_code+'+&w='+w+'&h='+h+'$method_free='+method_free
        post = urllib.urlencode( {"op":op,"file_code":file_code,"w":w,"h":h,"method_free":method_free} )
        print 'post',post

        data = scrapertools.cache_page(page_url,post=post)
        #plugintools.log("data="+data)
        data = unpackerjs.unpackjs(data)
        #plugintools.log("data="+data)
        media_url = plugintools.find_single_match(data,'file\:"([^"]+)"')
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def videobam(params):
    plugintools.log('[%s %s] Videobam %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    try:
        data = scrapertools.cache_page(page_url)
        videourl = ""
        match = ""
        if "Video is processing" in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible temporalmente!", 3 , art+'icon.png'))
        else:
            patronHD = " high: '([^']+)'"
            matches = re.compile(patronHD,re.DOTALL).findall(data)
            for match in matches:
                media_url = match
                plugintools.log("Videobam HQ :"+match)

            if videourl == "":
                patronSD= " low: '([^']+)'"
                matches = re.compile(patronSD,re.DOTALL).findall(data)
                for match in matches:
                    media_url = match
                    plugintools.log("Videobam LQ :"+match)

                if match == "":
                    if len(matches)==0:
                        # "scaling":"fit","url":"http:\/\/f10.videobam.com\/storage\/11\/videos\/a\/aa\/AaUsV\/encoded.mp4
                        patron = '[\W]scaling[\W]:[\W]fit[\W],[\W]url"\:"([^"]+)"'
                        matches = re.compile(patron,re.DOTALL).findall(data)
                        for match in matches:
                            videourl = match.replace('\/','/')
                            videourl = urllib.unquote(videourl)
                            plugintools.log("Videobam scaling: "+videourl)
                            if videourl != "":
                                media_url = videourl              
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def vimeo(params):
    plugintools.log('[%s %s] Vimeo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    #https://vimeo.com/101182831
    #https://player.vimeo.com/video/101182831
    if not "player" in page_url:
        page_url = page_url.replace("https://vimeo.com/","https://player.vimeo.com/video/")  
    try:
        headers = {'Host':'player.vimeo.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
        r = requests.get(page_url,headers=headers)
        data = r.content
        data_js = plugintools.find_single_match(data,'\(function\(e,a\){var t=(.*?);if')
        js = json.loads(data_js)
        try:
            media_urlhd = js['request']['files']['progressive'][1]['url']
            media_url = media_urlhd
        except:
            media_urlsd = js['request']['files']['progressive'][0]['url']
            media_url = media_urlsd
            if media_url == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        print "$"*100+"- By Movies Ultra -"+"$"*100,media_url,"$"*214
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)
    
def veetle(params):
    plugintools.log('[%s %s] Veetle %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    try:         
        # Obtenemos ID del canal de Veetle
        if url.startswith("http://veetle.com/index.php/channel/view") == True: #http://veetle.com/index.php/channel/view/4c1b0ef0a2122/9b4e33e576fc832c2989fcab575d245a (la URL incluye el ID de Veetle)
            id_veetle = plugintools.find_single_match(url, 'view/([^/]+)')
            # Buscamos enlaces de video...
            url_veetle ='http://veetle.com/index.php/stream/ajaxStreamLocation/'+id_veetle+'/android-hls'
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
            r = requests.get(url_veetle, headers=headers)
            data = r.text
            if data != "":    
                media_url = plugintools.find_single_match(data, '"."([^"]+)').replace("\\", "")
                print '$'*30+'-  -'+'$'*30,media_url,'$'*79
            else:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png')) 
        
        elif url.startswith("http://veetle.com/index.php/profile/") == True:  #http://veetle.com/index.php/profile/1106863793?play=6641a57fb8e116d1c29d50bb6de27d44 (hay que buscar ID del canal de Veetle)
            live_id = url.split("play=")[1]
            #http://veetle.com/index.php/ajax/videoService/getVideo?sessionId=f0383d44b0c1dce1a74dcba794e9074b
            url_veetle = 'http://veetle.com/index.php/ajax/videoService/getVideo?sessionId='+ live_id
            headers = {'Host': 'veetle.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            'Referer': url}
            r = requests.get(url_veetle, headers=headers)
            data_js = r.text
            js = json.loads(data_js)
            #flvBaseUrl:"http://38.108.161.80/flv/5181c9b1e655b.f0383d44b0c1dce1a74dcba794e9074b/0"
            #http://38.108.161.80/flv/5181c9b1e655b.f0383d44b0c1dce1a74dcba794e9074b/0/1454839584.ce2a7459271e9c8beaca8bac38b097d7
            media = js['playbackInfo']['flvBaseUrl']
            if media != "":
                token = js['playbackInfo']['playbackAccessToken']
                media_url = media+'/'+token
                print '$'*50+'-  -'+'$'*50,media_url,'$'*119
            else:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url    
                
    plugintools.play_resolved_url(media_url)

def bitvid(params):
    plugintools.log('[%s %s] Bitvid (Antes: Videoweed) %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    if 'www.videoweed' in page_url:
        page_url = page_url.replace('http://www.videoweed.es','http://www.bitvid.sx')

    try:
        headers = {"Host": "www.bitvid.sx","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
        r = requests.get(page_url, headers=headers)
        data = r.text
        # print data
        parametro = plugintools.find_single_match(data,'name="stepkey" value="([^"]+)"')
        post = "stepkey="+parametro+"&submit=submit"

        headers = {"Host": "www.bitvid.sx","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": page_url}
        body,response_headers = plugintools.read_body_and_headers(page_url,headers=headers,post=post)
        
        url = "http://www.bitvid.sx/api/player.api.php?"
        cid3 = plugintools.find_single_match(body,'flashvars.cid3="([^"]+)"')
        if cid3 == "":
            cid3 = "bitvid.sx"
        file_id = plugintools.find_single_match(body,'flashvars.file="([^"]+)"')
        filekey = plugintools.find_single_match(body,'flashvars.filekey="([^"]+)"').replace(".","%2E").replace("-","%2D")
        if filekey == "":
            filekey = plugintools.find_single_match(body,'fkz="([^"]+)"')
        parametros = "&cid2=undefined&numOfErrors=0"
        parametros2 = "&user=undefined&pass=undefined&cid=1"
        #http://www.bitvid.sx/api/player.api.php?file=993ec886f277e&key=188.76.69.238-a7e6a0affe4dd7f89398b495e512e276&cid2=undefined&numOfErrors=0&cid3=bitvid.sx&user=undefined&pass=undefined&cid=1
    
        urlfull = url+"file="+file_id+"&key="+filekey+parametros+"&cid3="+cid3+parametros2
        print urlfull               
        ref = "http://www.bitvid.sx/player/cloudplayer.swf"
        headers = {"Host": "www.bitvid.sx","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": ref}
        r = requests.get(urlfull, headers=headers)
        data = r.text
        media_url = plugintools.find_single_match(data,"url=(.*?)&title=")
        if media_url != "":
            print '$'*45+'-  -'+'$'*45,media_url,'$'*109
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))        
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)

def streamable(params):
    plugintools.log('[%s %s] Streamable %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("https://streamable.com/","https://streamable.com/e/")
        headers = { "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"}
        r = requests.get(page_url)
        data = r.content
        media = plugintools.find_single_match(data,'<source src="(.*?)"')
        media=media.replace('-mobile','')
        if media !="":
            media_url = 'http:'+media
            print '$'*18+'- Movies Ultra -'+'$'*18,media_url,'$'*55
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))   
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def rocvideo(params):
    plugintools.log('[%s %s] Rocvideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://rocvideo.tv/","http://rocvideo.tv/embed-") + ".html"

    try:
        headers = { "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14" }
        r=requests.get(page_url, headers=headers);data=r.text
        data = plugintools.find_single_match(data,"<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d.*?)</script>")
        data = unpackerjs.unpackjs(data)
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"').strip()
        plugintools.log("media_url= "+media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)
    
def realvid(params):
    plugintools.log('[%s %s] Realvid %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://realvid.net/","http://realvid.net/embed-") + ".html"
        headers = { "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14" }
        r=requests.get(page_url, headers=headers);data=r.text
        if data.find("File was deleted") >= 0:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo borrado!", 3 , art+'icon.png'))
        else:
            media_url = plugintools.find_single_match(data,'file: "([^"]+)",').strip()
            plugintools.log("media_url= "+media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)
        
####################################################################################
##  Netu - Waaw - Hqq
####################################################################################       

def netu(params):
    plugintools.log('[%s %s] Netu %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    if "http://netu.tv/" in page_url:
        page_url = page_url.replace("netu","hqq")
    elif "http://waaw.tv/" in page_url:
        page_url = page_url.replace("waaw","hqq")

    ## Encode a la url para pasarla como valor de parámetro con hqq como host
    urlEncode = urllib.quote_plus(page_url)

    id_video = page_url.split("=")[1]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": params.get("url")}
    #http://hqq.tv/player/embed_player.php?vid=7NHXS7A81RU6&autoplay=no
    url_hqq = "http://hqq.tv/player/embed_player.php?vid="+id_video+"&autoplay=no"
    r=requests.get(url_hqq,headers=headers) 
    data_hqq =r.content
    data64 = plugintools.find_single_match(data_hqq,'base64,([^"]+)"')
    #print data64
    utf8_decode = double_b64(data64)
    #print utf8_decode
    at = plugintools.find_single_match(utf8_decode,'<input name="at" type="text" value="([^"]+)"')
    ## Recoger los bytes ofuscados que contiene la url del m3u8
    b_m3u8_2 = get_obfuscated(id_video,at,urlEncode,headers)
    ## Obtener la url del m3u8
    url_m3u8 = tb(b_m3u8_2)
    print url_m3u8
    media_url = url_m3u8 +"|User-Agent="+headers['User-Agent'] #m3u8
    
    plugintools.play_resolved_url(media_url)  

####################################################################################
## Decodificación b64 para Netu
####################################################################################

## Decode
def b64(text, inverse=False):
    if inverse:
        text = text[::-1]
    return base64.decodestring(text)

## Doble decode y unicode-escape
def double_b64(data64):
    b64_data_inverse = b64(data64)
    #print b64_data_inverse 
    data64_2 = plugintools.find_single_match(b64_data_inverse, "='([^']+)';")
    utf8_data_encode = b64(data64_2,True)
    utf8_encode = plugintools.find_single_match(utf8_data_encode, "='([^']+)';")
    utf8_decode = utf8_encode.replace("%","\\").decode('unicode-escape')
    return utf8_decode
    
## Recoger los bytes ofuscados que contiene el m3u8
def get_obfuscated(id_video,at,urlEncode,headers):
    
    url = "http://hqq.tv/sec/player/embed_player.php?vid="+id_video+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+urlEncode+"&pass="
    #url = "http://hqq.tv/sec/player/embed_player.php?vid="+id_video+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+urlEncode+"&pass="
    r=requests.get(url,headers=headers) 
    data =r.content
    
    match_b_m3u8_1 = plugintools.find_single_match(data,'</div>.*?<script>document.write[^"]+"([^"]+)"')
    b_m3u8_1 = urllib.unquote(plugintools.find_single_match(data, match_b_m3u8_1))
    if b_m3u8_1 == "undefined": 
        b_m3u8_1 = urllib.unquote(data)
    match_b_m3u8_2 = plugintools.find_single_match(b_m3u8_1,'"#([^"]+)"')
    b_m3u8_2 = plugintools.find_single_match(b_m3u8_1, match_b_m3u8_2)
    return b_m3u8_2

## Obtener la url del m3u8
def tb(b_m3u8_2):
    j = 0
    s2 = ""
    while j < len(b_m3u8_2):
        s2+= "\\u0"+b_m3u8_2[j:(j+3)]
        j+= 3
    return s2.decode('unicode-escape').encode('ASCII', 'ignore')

####################################################################################
## Fin Netu - Waaw - Hqq
####################################################################################

def videomega(params):
    plugintools.log('[%s %s] Videomega.tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    
    try:
        ref = page_url.split("ref=")[1]
        page_url = 'http://videomega.tv/view.php?ref='+ref+'&width=100%&height=400'
        #post = premium = False , user="" , password="", video_password=""
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0', 'Referer': page_url, "Accept-Encoding": "gzip, deflate, sdch" }        
        r = requests.get(page_url, headers=headers,premium=False,user="",password="",video_password="");data = r.text
        media_url = plugintools.find_single_match(data,'<source src="([^"]+)"')  
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)

def videott(params):
    plugintools.log("[%s %s] Videott %s " % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")    
    if page_url.startswith("http://www.video.tt/video/") == True:
        page_url = page_url.replace("http://www.video.tt/video/","http://www.video.tt/watch_video.php?v=")
          
    try:
        videoid = page_url.replace("http://www.video.tt/watch_video.php?v=","").replace("http://www.video.tt/video/","")
        timestamp=str(random.randint(1000000000,9999999999))
        hexastring = get_sha1(page_url) + get_sha1(page_url) + get_sha1(page_url) + get_sha1(page_url)
        hexastring = hexastring[:96]
        media_url = "http://gs.video.tt/s?v="+videoid+"&r=1&t="+timestamp+"&u=&c="+hexastring+"&start=0"
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)
    

###### Función auxiliar para conector video.tt ###################

def get_sha1(cadena):
    try:
        import hashlib
        devuelve = hashlib.sha1(cadena).hexdigest()
    except:
        import sha
        import binascii
        devuelve = binascii.hexlify(sha.new(cadena).digest())
    return devuelve

####################################################

def flashx(params):
    plugintools.log("[%s %s] Flashx %s " % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        page_url = page_url.replace("http://www.flashx.tv/","http://www.flashx.tv/playvid-")#.replace('.html','')
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
        r = requests.get(page_url,headers=headers)
        data = r.content
        if 'You try to access this video with Kodi' in data:
            url = plugintools.find_single_match(data,'(http://www.flashx.tv/reload.*?)">')
            r = requests.get(url,headers=headers);data = r.content
            r = requests.get(page_url,headers=headers);data = r.content   
        data = plugintools.find_single_match(data,"</table>.*?eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        media = plugintools.find_multiple_matches(data,'file:\"([^"]+)"')
        try:
            for item in media:
                if "mp4" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*49+'- By Movies Ultra -'+'$'*49,media_url,'$'*117
                        plugintools.play_resolved_url(media_url)
                elif "flv" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*49+'- By Movies Ultra -'+'$'*49,media_url,'$'*117
                        plugintools.play_resolved_url(media_url)
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def okru(params):
    plugintools.log("[%s %s] Ok.ru %s " % (addonName, addonVersion, repr(params)))
    
    page_url=params.get("url")
    headers = {'Host': 'ok.ru','user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    r = requests.get(page_url, headers=headers)
    data = r.content
    
    try:
        headers = {'Host': 'ok.ru','X-Requested-With': 'XMLHttpRequest','user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
        'Referer': page_url}
        hash_url=page_url.replace("http://ok.ru/videoembed/", "").strip()
        plugintools.log("hash= "+hash_url)
        url_json='http://ok.ru/dk?cmd=videoPlayerMetadata&mid='+hash_url
    
        r=requests.get(url_json,headers=headers) 
        data=r.content
    
        js=json.loads(data)
        videos=js["videos"]
        #opts={}
        for video in videos:
            #opts[video["name"]]=video["url"]
            if video['name'] == 'hd':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
            elif video['name'] == 'sd':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
            elif video['name'] == 'mobile':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
            elif video['name'] == 'lowest':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
            elif video['name'] == 'low':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url  

    plugintools.play_resolved_url(media_url)    

def vidtome(params):
    plugintools.log("[%s %s] Vidto.me %s " % (addonName, addonVersion, repr(params)))

    page_url=params.get("url")

    try:
        page_url = page_url.replace('/embed-', '/')
        page_url = re.compile('//.+?/([\w]+)').findall(page_url)[0]
        page_url = 'http://vidto.me/embed-%s.html' % page_url
        r=requests.get(page_url)
        data=r.content
        result = re.compile('(eval.*?\)\)\))').findall(data)[-1]
        result = unpackerjs.unpackjs(result)
        quality=plugintools.find_multiple_matches(result, 'label:"([^"]+)')
        url_media=plugintools.find_multiple_matches(result, 'file:"([^"]+)')
        media_url=url_media[len(quality)-1]
        
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)   
           
def playwire(params):
    plugintools.log("[%s %s] Playwire en Ourmatch.net %s " % (addonName, addonVersion, repr(params)))

    url=params.get("url")
    r=requests.get(url)
    data=r.content
    video_contents=plugintools.find_single_match(data, 'var video_contents = {(.*?)</script>')
    items_video=plugintools.find_multiple_matches(video_contents, '{(.*?)}')
    for entry in items_video:        
        url_zeus=plugintools.find_single_match(entry, 'config.playwire.com/(.*?)&quot;')
        zeus='http://config.playwire.com/'+url_zeus
        type_item=plugintools.find_single_match(entry, "type\':\'([^']+)")
        lang=plugintools.find_single_match(entry, "lang:\'([^']+)")
        title_item='[COLOR white]'+type_item+' [/COLOR][I][COLOR lightyellow]'+lang+'[/I][/COLOR]'
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
        #print data
        burl=plugintools.find_single_match(data, '<baseURL>([^<]+)</baseURL>')
        media_item=plugintools.find_multiple_matches(data, '<media(.*?)"/>')
        i=1
        while i<=len(media_item):
            for item in media_item:
                plugintools.log("item= "+item)
                media=plugintools.find_single_match(item, 'url="([^"]+)')
                bitrate=plugintools.find_single_match(item, 'bitrate="([^"]+)')
                url_media=burl+'/'+media
                title_fixed=title_item+' [COLOR lightblue][I]('+bitrate+' kbps)[/I][/COLOR]'
                plugintools.add_item(action="play", title=title_fixed, url=url_media, thumbnail=url_poster[0], fanart='http://images.huffingtonpost.com/2014-09-12-image1.JPG', folder=False, isPlayable=True)
                i=i+1                
    #http://config.playwire.com/17003/videos/v2/4225978/zeus.json
    #https://config.playwire.com/17003/videos/v2/4225978/manifest.f4m
    #https://cdn.phoenix.intergi.com/17003/videos/4225978/video-sd.mp4?hosting_id=17003


##################################### OPENLOAD ############################################
##############################  ################################

def openload(params):
    plugintools.log('[%s %s] Openload %s' % (addonName, addonVersion, repr(params)))

    try:
        myurl = params.get("url")
        if '/f/' in myurl:
            page_embed = plugintools.find_single_match(myurl,'(https://openload.co/f/.*?/)')
            myurl = page_embed.replace('/f/','/embed/')

        HTTP_HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Referer': myurl}  # 'Connection': 'keep-alive'
        
        r = requests.get(myurl, headers=HTTP_HEADER)
        data = r.content
        if 'We are sorry!' in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            mylink = get_mylink(data)
            if set('[<>=!@#$%^&*()+{}":;\']+$').intersection(mylink):
                time.sleep(2)
                r = requests.get(myurl, headers=HTTP_HEADER)
                data = r.content
                mylink = get_mylink(data)
                if set('[<>=!@#$%^&*()+{}":;\']+$').intersection(mylink):
                    time.sleep(2)
                    r = requests.get(myurl, headers=HTTP_HEADER)
                    data = r.content
                    mylink = get_mylink(data)
            videoUrl = 'https://openload.co/stream/{0}?mime=true'.format(mylink)
            headers = {'User-Agent': HTTP_HEADER['User-Agent'], 'Referer':myurl}
            req = urllib2.Request(videoUrl, None, headers)
            res = urllib2.urlopen(req)
            videoUrl = res.geturl()
            res.close()
            plugintools.play_resolved_url(videoUrl)           
    except Exception as e:
        #common.log_utils.log_notice('Exception during openload resolve parse: %s' % e)
        print("Error", e)
        raise

def get_mylink(data):

    try:
        data = data.encode('utf-8')
    except: pass
    n = re.findall('<span id="(.*?)">(.*?)</span>', data)
    print "y",n
    y = n[0][1]
    enc_data = HTMLParser().unescape(y)
    res = []
    for c in enc_data:
        j = ord(c)
        if j >= 33 and j <= 126:
            j = ((j + 14) % 94)
            j = j + 33
        res += chr(j)
    mylink = ''.join(res)
    tmp100 = plugintools.find_multiple_matches(data,'<script type="text/javascript">(ﾟωﾟ.*?)</script>')
    encdata = ''
    tmpEncodedData = tmp100[0].split('┻━┻')   
    for tmpItem in tmpEncodedData:  
        try:
            encdata += decodeOpenLoad(tmpItem)  
        except:pass 
    encnumbers = re.findall('return(.*?);', encdata, re.DOTALL)
    encnumbers1 = re.findall('(\d+).*?(\d+)', encnumbers[0])[0]
    encnumbers2 = re.findall('(\d+) \- (\d+)', encnumbers[1])[0]
    encnumbers4 = re.findall('(\d+)', encnumbers[3])[0]

    number1 = int(encnumbers1[0]) + int(encnumbers1[1])
    number2 = int(encnumbers2[0]) - int(encnumbers2[1]) + number1
    number4 = int(encnumbers4[0])
    number3 = number2 - number4

    print "num1", number1
    print "num2", number2
    print "num4", number4
    print "num3", number3
    print "a",len(mylink)-number2
        
    mynewlink1 = mylink[0:-number2]
    mynewlink2 = chr(ord(mylink[-number2])+number3)
    mynewlink3 = mylink[len(mylink)-number2+1:]
    print "my2", mynewlink1,mynewlink2,mynewlink3
    mynewlink = mynewlink1+mynewlink2+mynewlink3

    return mynewlink
        
def decode(encoded):
    tab = encoded.split('\\')
    ret = ''
    for item in tab:
        try:
            ret += chr(int(item, 8))
        except Exception:
            ret += item
    return ret

def base10toN(num, n):
    num_rep = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j', 20: 'k',
                21: 'l', 22: 'm', 23: 'n', 24: 'o', 25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't', 30: 'u', 31: 'v',
                32: 'w', 33: 'x', 34: 'y', 35: 'z'}
    new_num_string = ''
    current = num
    while current != 0:
        remainder = current % n
        if 36 > remainder > 9:
            remainder_string = num_rep[remainder]
        elif remainder >= 36:
            remainder_string = '(' + str(remainder) + ')'
        else:
            remainder_string = str(remainder)
        new_num_string = remainder_string + new_num_string
        current = current / n
    return new_num_string

def decodeOpenLoad(aastring):
        
    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]+(oﾟｰﾟo)+ ((c^_^o)-(c^_^o))+ (-~0)+ (ﾟДﾟ) ['c']+ (-~-~1)+", "")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "9")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ))", "8")
    aastring = aastring.replace("((ﾟｰﾟ) + (o^_^o))", "7")
    aastring = aastring.replace("((c^_^o)-(c^_^o))", "0")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟΘﾟ))", "5")
    aastring = aastring.replace("(ﾟｰﾟ)", "4")
    aastring = aastring.replace("((o^_^o) - (ﾟΘﾟ))", "2")
    aastring = aastring.replace("(o^_^o)", "3")
    aastring = aastring.replace("(ﾟΘﾟ)", "1")
    aastring = aastring.replace("(+!+[])", "1")
    aastring = aastring.replace("(c^_^o)", "0")
    aastring = aastring.replace("(0+0)", "0")
    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]", "\\")
    aastring = aastring.replace("(3 +3 +0)", "6")
    aastring = aastring.replace("(3 - 1 +0)", "2")
    aastring = aastring.replace("(!+[]+!+[])", "2")
    aastring = aastring.replace("(-~-~2)", "4")
    aastring = aastring.replace("(-~-~1)", "3")
    aastring = aastring.replace("(-~0)", "1")
    aastring = aastring.replace("(-~1)", "2")
    aastring = aastring.replace("(-~3)", "4")
    aastring = aastring.replace("(0-0)", "0")

    aastring = aastring.replace("(ﾟДﾟ).ﾟωﾟﾉ", "10")
    aastring = aastring.replace("(ﾟДﾟ).ﾟΘﾟﾉ", "11")
    aastring = aastring.replace("(ﾟДﾟ)[\'c\']", "12")
    aastring = aastring.replace("(ﾟДﾟ).ﾟｰﾟﾉ", "13")
    aastring = aastring.replace("(ﾟДﾟ).ﾟДﾟﾉ", "14")
    aastring = aastring.replace("(ﾟДﾟ)[ﾟΘﾟ]", "15")
    
    decodestring = re.search(r"\\\+([^(]+)", aastring, re.DOTALL | re.IGNORECASE).group(1)
    decodestring = "\\+" + decodestring
    decodestring = decodestring.replace("+", "")
    decodestring = decodestring.replace(" ", "")

    decodestring = decode(decodestring)
    decodestring = decodestring.replace("\\/", "/")

    if 'toString' in decodestring:
        base = re.compile(r"toString\(a\+(\d+)", re.DOTALL | re.IGNORECASE).findall(decodestring)[0]
        base = int(base)
        match = re.compile(r"(\(\d[^)]+\))", re.DOTALL | re.IGNORECASE).findall(decodestring)
        for repl in match:
            match1 = re.compile(r"(\d+),(\d+)", re.DOTALL | re.IGNORECASE).findall(repl)
            base2 = base + int(match1[0][0])
            repl2 = base10toN(int(match1[0][1]), base2)
            decodestring = decodestring.replace(repl, repl2)
        decodestring = decodestring.replace("+", "")
        decodestring = decodestring.replace("\"", "")
    return decodestring


def youtube(params):
    plugintools.log('[%s %s] Youtube %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    headers = {'Host': 'www.youtube.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'}
    if 'embed' in page_url:
        page_url = page_url.replace('http://www.youtube.com/embed/','https://www.youtube.com/watch?v=')
        page_url = page_url.replace('https://www.youtube.com/embed/','https://www.youtube.com/watch?v=')

    if (not 'http://www.youtube.com/' in page_url) and (not 'https://www.youtube.com/' in page_url):
        page_url = 'https://www.youtube.com/watch?v='+page_url
    try:
        r = requests.get(page_url,headers=headers)
        data = r.content
   
        fmt_stream_map = plugintools.find_single_match(data,'url_encoded_fmt_stream_map\":\"([^"]+)\"')
        if fmt_stream_map != "":
            fmt_stream_map = fmt_stream_map.split(",")
            urlfull = fmt_stream_map[0]
            url = urlfull.split('url=')
            url = url[-1]
            url = url.split("\\u")
            url_final = url[0].replace('%2C',",").replace('%3A',':').replace('%26','&').replace('%3D','=').replace('%2B','+').replace('%2F','/').replace('%3F','?').replace('%25','%')
            media_url = url_final
            print '$'*142+'-  -'+'$'*142,media_url,'$'*303
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def youwatch(params):
    plugintools.log('[%s %s] YouWatch %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        page_url = page_url.replace("http://youwatch.org/","http://msemen.info/")
        page_url = page_url.replace("http://chouhaa.info/","http://msemen.info/")
        if not "http://msemen.info/embed-" in page_url:
            page_url = page_url.replace("http://msemen.info/","http://msemen.info/embed-") + ".html"
        r = requests.get(page_url)
        data = r.content
        url_b64 = plugintools.find_single_match(data,'<iframe src="([^"]+)"')
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer': page_url}
        r = requests.get(url_b64,headers=headers)
        data = r.content
        media = plugintools.find_single_match(data,'file:"([^"]+)"').strip()
        if media !="":
            media_url = media +'|Referer='+ page_url
            print '$'*61+'- By Movies Ultra -'+'$'*61,media_url,'$'*141
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url


def vidggto(params):
    plugintools.log('[%s %s] Vidgg.to %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        print '$'*25,"[Movies Ultra] Respuesta= "+str(r.status_code),'$'*25
        # print data
    
        key = plugintools.find_single_match(data,'flashvars.filekey="(.*?)"')
        file_id = plugintools.find_single_match(data,'flashvars.file="(.*?)"')
        cid = plugintools.find_single_match(data,'flashvars.domain="(.*?)"')
        domain = plugintools.find_single_match(data,'flashvars.cid="(.*?)"')
        ref = "http://www.vidgg.to/player/cloudplayer.swf"

        headers = {"Host":"www.vidgg.to","User-Agent": '"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"', "Referer": ref}
        # http://www.vidgg.to/api/player.api.php?key=87.223.99.234-6e60102419de42e1a5550fd0119a211e&numOfErrors=0&user=undefined&pass=undefined&cid=1&file=288d5af5a64c0&cid3=seriesyonkis.sx&cid2=undefined
        url_new = "http://www.vidgg.to/api/player.api.php?key="+key+"&numOfErrors=0&user=undefined&pass=undefined&cid="+cid+"&file="+file_id+"&cid3="+domain+"&cid2=undefined"
    
        r = requests.get(url_new,headers=headers)
        data = r.content
        #print data
        #url=http://s240.zerocdn.to/dl/23a3e0c1ef50a88777fbee9ba554bc85/5686721b/ff1208c256562d03962845fb3af0655e16.flv&title=4N4T0M14.12x8.m720p%26asdasdas&site_url=http://www.vidgg.to/video/288d5af5a64c0&seekparm=&enablelimit=0
        media_url = plugintools.find_single_match(data,'url=(.*?)&title')
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def vimple(params):
    plugintools.log('[%s %s] Vimple %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    try:
        r = requests.get(page_url)
        data = r.content
        print '$'*25,"[Movies Ultra] Respuesta= "+str(r.status_code),'$'*25
        # print data

        url = plugintools.find_single_match(data,"dataUrl:'(.*?)'")
        url_new = "http://player.vimple.ru"+url
        ref = "http://videoplayer.ru/ru/player/spruto/player.swf?v=3.1.0.7" 
        headers = {"Host":"s13.vimple.ru:8081","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":ref}
    
        r = requests.get(url_new)
        data = r.content
        user_id = r.cookies['UniversalUserID'];print user_id
    
        js = json.loads(data)
        media = js['sprutoData']['playlist'][0]['video'][0]['url']
        media_url = media+"|Cookie=UniversalUserID="+user_id
    
        #http://s13.vimple.ru:8081/vv52/716622.mp4?v=2c6a0a43-bfa1-469e-abf8-8b7d8df9769b&t=635872710621810000&d=7334&sig=6edab5d97959da7b3451444cb002a557
        #http://s15.vimple.ru:8081/vv65/698440.mp4?v=bfe4e467-2765-4be0-a479-22ee1e2ab515&t=635872785719935000&d=5987&sig=09ad419d594c1a674b4caaea3efca60f|Cookie=UniversalUserID=24259d8f030a42df9fe6eec1e80083b9
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def idowatch(params):
    plugintools.log('[%s %s] IdoWatch %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        headers = {"Host": "idowatch.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
    
        r = requests.get(page_url,headers=headers)
        data = r.content
        bloq_url = plugintools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
        media_url = plugintools.find_single_match(bloq_url,'file:"(.*?)"')
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def cloudtime(params):
    plugintools.log('[%s %s] CloudTime %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    
    try:
        headers = {"Host": "www.cloudtime.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
    
        r = requests.get(page_url,headers=headers)
        data = r.content
        
        stepkey = plugintools.find_single_match(data,'name="stepkey" value="([^"]+)"')
        submit = plugintools.find_single_match(data,'name="submit" class="btn" value="([^"]+)"')
        post = "stepkey="+stepkey+"&submit="+submit
    
        headers = {"Host": "www.cloudtime.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":page_url}
        body,response_headers = plugintools.read_body_and_headers(page_url,headers=headers,post=post)
        #print body
        #http://www.cloudtime.to/api/player.api.php?cid3=cloudtime.to&file=90c557483413b&key=87.223.99.234-08d874b967c90d5f298bbed5968d1dd9&numOfErrors=0&pass=undefined&user=undefined&cid2=undefined&cid=1
        #http://www.cloudtime.to/api/player.api.php?cid3=cloudtime%2Eto&file=90c557483413b&key=87%2E223%2E99%2E234%2D08d874b967c90d5f298bbed5968d1dd9&numOfErrors=0&pass=undefined&user=undefined&cid2=undefined&cid=1

        cid3 = "cloudtime%2Eto"
        file_id = plugintools.find_single_match(body,'flashvars.file="([^"]+)"').replace(".","%2E").replace("-","%2D")
        key = plugintools.find_single_match(body,'flashvars.filekey="([^"]+)"').replace(".","%2E").replace("-","%2D")
        new_url = "http://www.cloudtime.to/api/player.api.php?cid3="+cid3+"&file="+file_id+"&key="+key+"&numOfErrors=0&pass=undefined&user=undefined&cid2=undefined&cid=1"
        print new_url
        #http://www.cloudtime.to/api/player.api.php?cid3=cloudtime.to&file=90c557483413b&key=87.223.99.234-08d874b967c90d5f298bbed5968d1dd9&numOfErrors=0&pass=undefined&user=undefined&cid2=undefined&cid=1
        #http://www.cloudtime.to/api/player.api.php?cid3=cloudtime%2Eto&file=90c557483413b&key=87%2E223%2E99%2E234%2D08d874b967c90d5f298bbed5968d1dd9&numOfErrors=0&pass=undefined&user=undefined&cid2=undefined&cid=                                            

        ref = "http://www.cloudtime.to/player/cloudplayer.swf"
        headers = {"Host": "www.cloudtime.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":ref}
        r = requests.get(new_url,headers=headers)
        data = r.content
        #print data
        media = data.replace("url=","").split('&')
        media_url = media[0]
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def vidzitv(params):
    plugintools.log('[%s %s] Vidzi.tv %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        headers = {"Host": "vidzi.tv","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        
        media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
        
        if media =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            for item in media:
                try:
                    if "mp4" in item:
                            media_url = item.replace('\/','/')  
                            print '$'*38+'- By Movies Ultra -'+'$'*38,media_url,'$'*95
                except:
                    if "m3u8" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*38+'- By Movies Ultra -'+'$'*38,media_url,'$'*95                
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def vodlocker(params):
    plugintools.log('[%s %s] VodLocker %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")

    if not "embed" in page_url:
      page_url = page_url.replace("http://vodlocker.com/","http://vodlocker.com/embed-") + ".html"

    try:
        headers = {"Host": "vodlocker.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        print '$'*25,"[Movies Ultra] Respuesta= "+str(r.status_code),'$'*25
        #print data
        media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
        if media_url == "":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def streamenet(params):
    plugintools.log('[%s %s] Streame.net %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        page_url = page_url.replace("#","")
        if not "embed" in page_url:
            page_url = page_url.replace("http://streame.net/","http://streame.net/embed-") + ".html"
        headers = {"Host": "streame.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        if 'File was deleted' in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
            for item in media:
                if item.endswith(".mp4"): media_url = item
                elif item.endswith(".m3u8"): media_url = item
                elif item.endswith(".flv"): media_url = item
        print '$'*38+'- By Movies Ultra -'+'$'*38,media_url,'$'*95 
        plugintools.play_resolved_url(media_url)
                  
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def watchonline(params):
    plugintools.log('[%s %s] WatchOnLine %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    if not "embed" in page_url:
      page_url = page_url.replace("http://www.watchonline.to/","http://www.watchonline.to/embed-") + ".html"
    try:
        headers = {"Host": "www.watchonline.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
    
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        sources = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
        for link in sources:
            if link.endswith(".mp4"):
                media_url = link
            elif link.endswith(".m3u8"):
                media_url = link
            elif link.endswith(".mpd"):
                media_url = link
        print '$'*35+'- Movies Ultra -'+'$'*35,media_url,'$'*89  
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
       
    plugintools.play_resolved_url(media_url)

def allvid(params):
    plugintools.log('[%s %s] Allvid %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    
    if not "embed" in page_url:
      page_url = page_url.replace("http://allvid.ch/","http://allvid.ch/embed-") + ".html"
    # print page_url
    try:
        headers = {"Host": "allvid.ch","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url)
        data = r.text
        
        data = plugintools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
        data = wiz.unpack(data)
        #plugintools.log("data="+data)
        try:        
            bloq_urls = plugintools.find_single_match(data,'sources:\[\{(.*?)\}\]')
            if bloq_urls == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
            else:
                urls = plugintools.find_multiple_matches(bloq_urls,'file:"([^"]+)"')
                for item in urls:
                    if item.endswith(".mp4") == True:
                        media_url = item
                        print '$'*35+'-  -'+'$'*35,media_url,'$'*89
        except:
            url = plugintools.find_single_match(bloq_urls,'file:"([^"]+)')
            if url == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
            else:
                media_url = url
                print '$'*35+'-  -'+'$'*35,media_url,'$'*89         
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url 

    plugintools.play_resolved_url(media_url)

def streamplay(params):
    plugintools.log('[%s %s] StreamPlay %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")

    if not "embed" in page_url:
        page_url = page_url.replace("http://streamplay.to/","http://streamplay.to/embed-") + ".html"  
    
    try:        
        headers = {"Host": "streamplay.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.text  
        #print data

        data = plugintools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
        data = wiz.unpack(data)
        plugintools.log("data="+data)
        try:
            bloq_urls = plugintools.find_single_match(data,'sources:\[\{(.*?)\}\]')
            if bloq_urls == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
            else:
                urls = plugintools.find_multiple_matches(bloq_urls,'file:"([^"]+)"')
                for item in urls:
                    if item.endswith(".mp4") == True:
                        media_url = item
                        print '$'*35+'-  -'+'$'*35,media_url,'$'*89
        except:
            url = plugintools.find_single_match(bloq_urls,'file:"([^"]+)')
            if url == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
            else:
                media_url = url
                print '$'*35+'-  -'+'$'*35,media_url,'$'*89       
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def myvideoz(params):
    plugintools.log('[%s %s] MyvideoZ %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")

    try:
        headers = {"Host": "myvideoz.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
    
        r = requests.get(page_url,headers=headers)
        data = r.content
        sess = r.cookies['PHPSESSID']
        
        url = plugintools.find_single_match(data,"<meta property=\"og:video\" content='([^']+)'")
        if url == "":
            plugintools.log("Archivo borrado: "+page_url)
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "El Archivo ha sido borrado", 3 , art+'icon.png'))
        #http://myvideoz.net/nuevo/player/player.swf?config=http%3A%2F%2Fmyvideoz.net%2Fnuevo%2Fplayer%2Ffsb.php%3Fv%3D70764%26autostart%3Dno
        ref = url.replace('%3A',':').replace('%2F','/').replace('%3D','=').replace('%3F','?').replace('%26','&')
        new_url = ref.replace('http://myvideoz.net/nuevo/player/player.swf?config=','') 
        #http://myvideoz.net/nuevo/player/fsb.php?v=70764&autostart=no
        
        headers = {"Host": "myvideoz.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
        "Referer": ref,"PHPSESSID":sess}

        r = requests.get(new_url,headers=headers)
        data = r.content 
        media_url = plugintools.find_single_match(data,"<file>([^<]+)</file>")
        plugintools.log("Url= "+media_url)
        if media_url == "":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
   
    plugintools.play_resolved_url(media_url)

def rutube(params):
    plugintools.log('[%s %s] Rutube.ru %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        #http://rutube.ru/play/embed/8260464
        if not "embed" in page_url:
            page_url = page_url.replace("http://rutube.ru/video/","http://rutube.ru/play/embed/")

        r = requests.get(page_url)
        data = r.content
        #http://bl.rutube.ru/route/0c458bed8ae24747a0fcf2bf2178229d.m3u8?guids=5ea7c431-c830-4eda-b3a5-6c8c40e89353_768x416_700413_avc1.42c01e_mp4a.40.5&sign=yOeOwmU8kW3_KMYBd09T6g&expire=1454622396
        media = plugintools.find_single_match(data,'<div id="options" data-value="(.*?)<script>').replace('&quot;','').replace('amp;','')
        #print media
        m3u8 = plugintools.find_single_match(media,'m3u8:(.*?)}').strip()
        if m3u8 == "":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            media_url = m3u8
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def dailymotion(params):
    plugintools.log('[%s %s] Dailymotion %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
            page_url = page_url.replace("http://www.dailymotion.com/video/","http://www.dailymotion.com/embed/video/")
    try:
        r = requests.get(page_url)
        data = r.content
    
        bloq_link = plugintools.find_single_match(data,'qualities"(.*?)"reporting"').replace('\/','/')
        if '1080' in bloq_link:
            media_url = plugintools.find_single_match(data,'1080".*?url":"(.*?)"').strip().replace('\/','/')
        elif '720' in bloq_link:
            media_url = plugintools.find_single_match(data,'720".*?url":"(.*?)"').strip().replace('\/','/')
        elif '480' in bloq_link:
            media_url = plugintools.find_single_match(data,'480".*?url":"(.*?)"').strip().replace('\/','/')
        elif '380' in bloq_link:
            media_url = plugintools.find_single_match(data,'380".*?url":"(.*?)"').strip().replace('\/','/')
        elif '240' in bloq_link:
            media_url = plugintools.find_single_match(data,'240".*?url":"(.*?)"').strip().replace('\/','/')
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def vimeo_pl(params):
    plugintools.log('[%s %s] Vimeo playlists %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url");url_ref = "https://player.vimeo.com/video/"
    fanart = 'http://i.ytimg.com/vi/tOgaEAhfuYQ/maxresdefault.jpg'
    thumbnail = 'http://4k.com/wp-content/uploads/2015/01/vimeo.jpg'

    if "/videos" in url:
        NoHagoNada = True
    else:
        url = url + "/videos"
            
    r = requests.get(url)	
    data = r.content
    
    url_channel = url + "···"
    nom_canal = plugintools.find_single_match(url_channel,'channels/(.*?)···')
    plugintools.add_item(action="",url=url,title="[COLOR red]       Canal Vimeo: [COLOR yellow]" + nom_canal + "[/COLOR]",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
    #plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

    grupo_videos = plugintools.find_multiple_matches(data,'id="cli(.*?)srcset=')
    for item in grupo_videos:
        url_video = plugintools.find_single_match(item,'p_(.*?)"')
        url_video = url_ref + url_video
        
        titulo_video = plugintools.find_single_match(item,'title="(.*?)"').decode('unicode_escape').encode('utf8')
        
        logo_video = plugintools.find_single_match(item,'src="(.*?)"')
        
        plugintools.add_item(action="vimeo", title=titulo_video, url=url_video, thumbnail=logo_video, fanart=fanart, folder = False, isPlayable=True)
            
    if 'rel="next' in data:  # Hay mas páginas... así q la resuelvo
            url_pag = "https://vimeo.com" + plugintools.find_single_match(data,'rel="next" href="(.*?)"')
            url_pag_provi = url_pag+"···"
            pag_siguiente = plugintools.find_single_match(url_pag_provi,'page:(.*?)···') 
            pag_siguiente = "[COLORFFFF0759]Página " + pag_siguiente + " >>>[/COLOR]"
            plugintools.add_item(action="vimeo_pl",title=pag_siguiente, url=url_pag,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

def spruto(params):
    plugintools.log('[%s %s] Spruto.tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"Host":"www.spruto.tv","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        file_vid = plugintools.find_single_match(data,'file: "([^"]+)",\s+mediaid:').strip()
    
        if 'mp4' in file_vid:
            media_url = file_vid
            print '$'*35+'-  -'+'$'*35,media_url,'$'*89
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def stormo(params):
    plugintools.log('[%s %s] Stormo.tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"Host":"www.stormo.tv","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        file_vid = plugintools.find_single_match(data,'file: "([^"]+)",\s+type :').strip()
    
        if 'mp4' in file_vid:
            media_url = file_vid
            print '$'*35+'-  -'+'$'*35,media_url,'$'*89
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)


def myviru(params):
    plugintools.log('[%s %s] Myvi.ru %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        # print data
        url = plugintools.find_single_match(data,"dataUrl:'(.*?)'")
        if url !="":
            url_new = "http://myvi.ru"+url
            ref = "http://videoplayer.ru/ru/player/spruto/player.swf?v=3.1.0.24" 
            headers = {"Host":"fs.myvi.ru","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":ref}
    
            r = requests.get(url_new)
            data = r.content
            user_id = r.cookies['UniversalUserID']
    
            js = json.loads(data)
            media = js['sprutoData']['playlist'][0]['video'][0]['url']
            media_url = media+"|Cookie=UniversalUserID="+user_id
            print '$'*75+'-  -'+'$'*75,media_url,'$'*169
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)
    

def filmon(params):
    plugintools.log('[%s %s] Filmon %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
   
    r = requests.get(page_url)
    data = r.content
    channel_id = plugintools.find_single_match(data,"current_channel_id= last_clicked_channel_id = '([^']+)'")

    ref = 'https://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FacebookPlayer.swf?channel_id='+channel_id
    page_url = 'https://www.filmon.com/tv/channel/info/'+channel_id
    headers = {'Host': 'www.filmon.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': ref}
    r = requests.get(page_url,headers=headers)
    data_js = r.text
    try:
        js = json.loads(data_js)
        media = js['data']['streams'][1]['url'].replace('%3A',':').replace('%2F','/').replace('%3D','=').replace('%3F','?').replace('%26','&')
        #playpath = js['data']['streams'][1]['name']
        playpath = channel_id+'.low.stream'
        media_url = media+'&playpath='+playpath+'&pageUrl=https://www.filmon.com/tv/channel/info/'+channel_id+'&swfUrl=https://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=28'
        print '$'*255+'-  -'+'$'*255,media_url,'$'*529
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Canal no disponible", 3 , art+'icon.png'))

    plugintools.play_resolved_url(media_url)

def thevideome(params):
    plugintools.log('[%s %s] TheVideo.me %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://thevideo.me/","http://thevideo.me/embed-") + ".html"
    try: 
        r = requests.get(page_url)
        data = r.text

        sources = plugintools.find_single_match(data,"sources: \[(.*?)\],")
        media_file = plugintools.find_multiple_matches(sources,"file: '([^']+)'")
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*142+'-  -'+'$'*142,media_url,'$'*303
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

##################################### VIDEOWOOD #########################################

def videowood(params):
    plugintools.log('[%s %s] Videowood.Tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://videowood.tv/video/","http://videowood.tv/embed/")
    try: 
        r = requests.get(page_url)
        data = r.content
        
        data_encode = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data_decode = decode_videowood(data_encode)
        if 'http' or 'https' in data_decode:
            media_url = plugintools.find_single_match(data_decode,"\'(.*?)\'")
            print '$'*36+'- Movies Ultra -'+'$'*36,media_url,'$'*91
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))                 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def decode_videowood(text):
    text = re.sub(r"\s+|/\*.*?\*/", "", text)
    data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
    chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]

    txt = ""
    for char in chars:
        char = char \
            .replace("(oﾟｰﾟo)","u") \
            .replace("c", "0") \
            .replace("(ﾟДﾟ)['0']", "c") \
            .replace("ﾟΘﾟ", "1") \
            .replace("!+[]", "1") \
            .replace("-~", "1+") \
            .replace("o", "3") \
            .replace("_", "3") \
            .replace("ﾟｰﾟ", "4") \
            .replace("(+", "(")
        char = re.sub(r'\((\d)\)', r'\1', char)

        c = ""; subchar = ""
        for v in char:
            c+= v
            try: x = c; subchar+= str(eval(x)); c = ""
            except: pass
        if subchar != '': txt+= subchar + "|"
    txt = txt[:-1].replace('+','')

    txt_result = "".join([ chr(int(n, 8)) for n in txt.split('|') ])

    return toStringCases(txt_result)

def toStringCases(txt_result):
    sum_base = ""
    m3 = False
    if ".toString(" in txt_result:
        if "+(" in  txt_result:
            m3 = True
            sum_base = "+"+find_single_match(txt_result,".toString...(\d+).")
            txt_pre_temp = find_multiple_matches(txt_result,"..(\d),(\d+).")
            txt_temp = [ (n, b) for b ,n in txt_pre_temp ]
        else:
            txt_temp = find_multiple_matches(txt_result, '(\d+)\.0.\w+.([^\)]+).')
        for numero, base in txt_temp:
            code = toString( int(numero), eval(base+sum_base) )
            if m3:
                txt_result = re.sub( r'"|\+', '', txt_result.replace("("+base+","+numero+")", code) )
            else:
                txt_result = re.sub( r"'|\+", '', txt_result.replace(numero+".0.toString("+base+")", code) )
    return txt_result

def toString(number,base):
    string = "0123456789abcdefghijklmnopqrstuvwxyz"
    if number < base:
        return string[number]
    else:
        return toString(number//base,base) + string[number%base]

#########################################################################################

def neodrive(params):
    plugintools.log('[%s %s] NeoDrive %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    page_url = page_url.replace('http://www.cloudzilla.to/','http://neodrive.co/')
    if not "embed" in page_url:
        page_url = page_url.replace("http://neodrive.co/share/file/","http://neodrive.co/embed/")
    try:
        r = requests.get(page_url)
        data = r.content
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        media = plugintools.find_single_match(data,'var vurl="([^"]+)"')
        if media !="":
            media_url = media
            print '$'*45+'- Movies Ultra -'+'$'*45,media_url,'$'*109
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)

def thevideobee(params):
    plugintools.log('[%s %s] TheVideobee.to %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://thevideobee.to/","http://thevideobee.to/embed-")   
    try: 
        r = requests.get(page_url)
        data = r.content
        media_file = plugintools.find_single_match(data,'<source src="(.*?)"')
        if media_file =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else: media_url = media_file
        print '$'*38+'-  -'+'$'*38,media_url,'$'*95     
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url) 
    
def fileshow(params):
    plugintools.log('[%s %s] Fileshow.Tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            id_vid = plugintools.find_single_match(page_url,'http://fileshow.tv/(.*?)/')
            page_url = "http://bestream.tv/plugins/mediaplayer/site/_embed_fileshow.php?u="+id_vid

        r = requests.get(page_url)
        data = r.content

        media = plugintools.find_single_match(data,'file: "([^"]+)"')
        if media !="":
            media_url = media
            print '$'*80+'-  -'+'$'*80,media_url,'$'*179
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def vid(params):
    plugintools.log('[%s %s] Vid.ag %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://vid.ag/","http://vid.ag/embed-")   
    try: 
        r = requests.get(page_url)
        data = r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)

        sources = plugintools.find_single_match(data,"sources:\[(.*?)\],")
        media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*38+'-  -'+'$'*38,media_url,'$'*95   
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def vidxtreme(params):
    plugintools.log('[%s %s] Vidxtreme.to %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://vidxtreme.to/","http://vidxtreme.to/embed-")+'.html'   
    try: 
        r = requests.get(page_url)
        data = r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)

        sources = plugintools.find_single_match(data,"sources:\[(.*?)\],")
        media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*38+'-  -'+'$'*38,media_url,'$'*95   
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def vidup(params):
    plugintools.log('[%s %s] Vidup.me %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://beta.vidup.me/","http://beta.vidup.me/embed-")+'.html' 
        r = requests.get(page_url)
        data = r.content
    
        sources = plugintools.find_single_match(data,"sources: \[(.*?)\]")
        media_file = plugintools.find_multiple_matches(sources,"file: '([^']+)'")
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*140+'- By Movies Ultra -'+'$'*140,media_url,'$'*299
        plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
		
def watchvideo(params):
    plugintools.log('[%s %s] watchvideo.us %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://watchvideo.us/","http://watchvideo.us/embed-")
    try:
        headers = {"Host": "watchvideo.us","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.text
        media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
        if media =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            for item in media:
                try:
                    if "mp4" in item:
                            media_url = item.replace('\/','/')  
                            print '$'*38+'-  -'+'$'*38,media_url,'$'*95
                except:
                    if "m3u8" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*38+'-  -'+'$'*38,media_url,'$'*95                
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def speedvid(params):
    plugintools.log('[%s %s] Speedvid.net %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://www.speedvid.net/","http://www.speedvid.net/embed-")+'.html'   
    try:
        headers = {"Host": "www.speedvid.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content
        media = plugintools.find_multiple_matches(data,"file:'([^']+)'")
        if media =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            for item in media:
                try:
                    if "mp4" in item:
                            media_url = item.replace('\/','/')  
                            print '$'*38+'-  -'+'$'*38,media_url,'$'*95
                except:
                    if "m3u8" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*38+'-  -'+'$'*38,media_url,'$'*95   
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def exashare(params):
    plugintools.log('[%s %s] Exsahare %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://chefti.info/","http://chefti.info/embed-")+'.html' 

        r = requests.get(page_url)
        data = r.content
        url64 = plugintools.find_single_match(data,'<iframe src="(.*?)"')

        headers = {'Host': 'chefti.info','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer': page_url}
        r = requests.get(url64,headers=headers)
        data = r.content
        sources = plugintools.find_single_match(data,"sources: \[\{(.*?)\}\],")
        media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*38+'-  -'+'$'*38,media_url,'$'*95
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def vodbeast(params):
    plugintools.log('[%s %s] Vodbeast.com %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://vodbeast.com/","http://vodbeast.com/embed-")+'.html'   
    try: 
        r = requests.get(page_url)
        data = r.content

        sources = plugintools.find_single_match(data,"sources: \[\{(.*?)\}\],")
        media_file = plugintools.find_multiple_matches(sources,'file: "([^"]+)"')
        for item in media_file:
            try:
                if "mp4" in item:
                    media_url = item.replace('\/','/')  
                    print '$'*38+'-  -'+'$'*38,media_url,'$'*95
                elif "m3u8" in item:
                    media_url = item.replace('\/','/')  
                    print '$'*38+'-  -'+'$'*38,media_url,'$'*95
            except: 
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png')) 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def nosvideo(params):
    plugintools.log('[%s %s] Nosvideo.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        if not 'embed' in page_url:
            page_url = page_url.replace("http://nosvideo.com/","http://nosvideo.com/embed/")
            page_url = page_url.replace("http://noslocker.com/","http://nosvideo.com/embed/")
        r = requests.get(page_url)#,headers=headers)
        data = r.content
        #http://on14serverfiles.loma.com.nosvideo.com/alrso4krwu6xshtdgsdrq6b7o2s6aflrbvmlull6ldmpmkeqehwazff3w225tl7rppgr6jm7v64blshfmz2n3rxveokqbmjp2ammz3ro6bdzdyxtrts4xmv5ezqydbz5/v.mp4
        media_url = plugintools.find_single_match(data,'<script>var W2t=.*?(http:.*?mp4)')
        if media_url !="":
            print '$'*81+'- Movies Ultra -'+'$'*81,media_url,'$'*181
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
      
    plugintools.play_resolved_url(media_url)

def up2stream(params):
    plugintools.log('[%s %s] Up2stream.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        #http://up2stream.com/view.php?ref=L20vlMXyo22oyXMlv02L.php&width=100%&height=400
        page_url = page_url.replace('http://up2stream.com/','http://up2stream.com/view.php')+'.php&width=100%&height=400'
        r=requests.get(page_url)
        data=r.content
        try:
            data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data = wiz.unpack(data)
            #http://abi.cdn.vizplay.org/v2/21b2424f1826eedc944e1eddc3168ce6.mp4?st=o_J3dk6gSLduHjyZ4qtBCQ&hash=orl-amZyOR7ybXDOJ46XGg
            media_url = plugintools.find_single_match(data,'src","([^"]+)"')
            print '$'*51+'-  -'+'$'*51,media_url,'$'*121
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
               
    plugintools.play_resolved_url(media_url)


def thevideobee(params):
    plugintools.log('[%s %s] TheVideobee.to %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://thevideobee.to/","http://thevideobee.to/embed-")   
    try: 
        r = requests.get(page_url)
        data = r.content
        bloq_media = plugintools.find_single_match(data,'sources: \[\{(.*?)\}\]')
        media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
    
        if bloq_media =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else: 
            media_url = media[-1]
            print '$'*38+'-  -'+'$'*38,media_url,'$'*95    
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url) 
    

def exashare(params):
    plugintools.log('[%s %s] Exsahare %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        if 'http://chefti.info/' in page_url:
            page_url = page_url.replace("http://chefti.info/","http://bojem3a.info/")

        if not "embed" in page_url:
            page_url = page_url.replace("http://bojem3a.info/","http://bojem3a.info/embed-")+'.html' 

        r = requests.get(page_url)
        data = r.content
        url64 = plugintools.find_single_match(data,'<iframe src="(.*?)"')
    
        headers = {'Host': 'bojem3a.info','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer': page_url}
        r = requests.get(url64,headers=headers)
        data = r.content

        sources = plugintools.find_single_match(data,"sources: \[\{(.*?)\}\],")
        media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*38+'-  -'+'$'*38,media_url,'$'*95
    
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)
    
def smartvid(params):
    plugintools.log('[%s %s] Smartvid.Tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://smartvid.tv/","http://smartvid.tv/embed-")
    try: 
        r = requests.get(page_url)
        data = r.text
        sources = plugintools.find_single_match(data,"sources: \[(.*?)\],")
        media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*37+'-  -'+'$'*37,media_url,'$'*93
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def greevid(params):
    plugintools.log('[%s %s] Greevid.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        r=requests.get(page_url)
        data=r.content
        page_url = plugintools.find_single_match(data,'<iframe width="100%" height="500" frameborder="0" src="(.*?)"').split('?')
        page_url = page_url[-1]
   
        headers = {"Host": "vidzi.tv","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
        if media =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            for item in media:
                try:
                    if "mp4" in item:
                            media_url = item.replace('\/','/')  
                            print '$'*35+'-  -'+'$'*35,media_url,'$'*89
                except:
                    if "m3u8" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*38+'-  -'+'$'*38,media_url,'$'*95                              
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def letwatch(params):
    plugintools.log('[%s %s] Letwatch.us %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://letwatch.us/","http://letwatch.us/embed-")+'.html'   
    try:
        r = requests.get(page_url)
        data = r.content
        sources = plugintools.find_single_match(data,'sources: \[\{file:"(.*?)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
        else: media_url = sources
        print '$'*35+'-  -'+'$'*35,media_url,'$'*89 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)
	
def yourupload(params):
    plugintools.log('[%s %s] Yourupload.com %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("/watch/","/embed/")   
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url)
        data = r.content
        source = plugintools.find_single_match(data,"file: '(.*?)'")
        #http://cdn.oose.io/8Q35CHT5RSNP0Gi26M8c7N52ECSA87hvPNPO70GqapTb1wUum6gx4ny10J6lrkgG/video.mp4
        if source:
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Referer":"http://www.yourupload.com/jwplayer/jwplayer.flash.swf"}
            r = requests.get(source,headers=headers,allow_redirects=False)
            data = r.headers
            media_url = data['Location']
            media_url = media_url.replace('?null&start=0','')
            print '$'*38+'- Movies Ultra -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)       
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))          
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
         
def zalaa(params):
    plugintools.log('[%s %s] Zalaa.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
      
    if not "embed" in page_url:
        id_vid = plugintools.find_single_match(page_url,'zalaa.com/(.*?)/')
        page_url = 'http://www.zalaa.com/embed-'+id_vid+'.html'
    try:
        headers = {"Host": "www.zalaa.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content
        media = plugintools.find_single_match(data,"file','([^']+)'")
        try:
            #http://ww1.zalaa.com:182/d/sigddcn5vsulzrqm5hnl5gvtbvh6qxq7qvxef5zb7zha5pqkz7tqkadc/greys.anatomy.1217.hdtv-lol.mp4?start=0
            media_url = media+'|Referer='+params.get("url")
            print '$'*87+'- Movies Ultra -'+'$'*87,media_url,'$'*193
            plugintools.play_resolved_url(media_url)
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))                                
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def uploadc(params):
    plugintools.log('[%s %s] Uploadc %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://www.uploadc.ch/","http://uploadc.com/embed-").replace('htm','html')
        page_url = page_url.replace("http://uploadc.ch/","http://uploadc.com/embed-").replace('htm','html')
    if not 'html' in page_url: page_url = page_url+'.html'
    try:
    
        headers = {"Host": "uploadc.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content
        media = plugintools.find_single_match(data,"file','([^']+)'") 
        try:
            media_url = media+'|Referer='+params.get("url")
            print '$'*71+'- Movies Ultra -'+'$'*71,media_url,'$'*161
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))                                
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def mp4upload(params):
    plugintools.log('[%s %s] Uploadc %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
      
    if not "embed" in page_url:
        page_url = page_url.replace("http://www.mp4upload.com/","http://www.mp4upload.com/embed-")+'.html'
    try:
        headers = {"Host": "www.mp4upload.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content
        #http://www8.mp4upload.com:182/d/rwxt7m2pz3b4quuorkubypckiujjgfp63lucunp2gbkiiq2auoezqg3a/video.mp4
        media = plugintools.find_multiple_matches(data,'file": "([^"]+)"') 
        try:
            media_url = media[0]+'|Referer='+params.get("url")
            print '$'*68+'- Movies Ultra -'+'$'*68,media_url,'$'*155
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))                                    
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def rapidvideo(params):
    plugintools.log('[%s %s] RapidVideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    if not "embed" in page_url:
        page_url = page_url.replace("http://rapidvideo.ws/","http://rapidvideo.ws/embed-") + '.html'
    try:
        r = requests.get(page_url)
        data = r.content
        try:
            data_eval = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data_packed  = wiz.unpack(data_eval)
            n_files = plugintools.find_multiple_matches(data_packed,'file:"([^"]+)"')
            if len(n_files)>1: media_url = n_files[0]
            else: media_url = plugintools.find_single_match(data_packed,'file:"([^"]+)"')
            print '$'*35+'- Movies Ultra -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def yourvideohost(params):
    plugintools.log('[%s %s] YourVidoeHost %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    if not "embed" in page_url:
        page_url = page_url.replace("http://yourvideohost.com/","http://yourvideohost.com/embed-") + '.html'
    try:
        r = requests.get(page_url)
        data = r.content
        try:
            media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
            print '$'*38+'- Movies Ultra -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def watchers(params):
    plugintools.log('[%s %s] Watchers %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    if not "embed" in page_url:
        page_url = page_url.replace("http://watchers.to/","http://watchers.to/embed-") + '.html'
    try:
        r = requests.get(page_url)
        data = r.content
        try:
            data_eval = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data_packed  = wiz.unpack(data_eval)
            full_files = plugintools.find_single_match(data_packed,'sources:\[\{(.*?)\}\]')
            n_files = plugintools.find_multiple_matches(full_files,'file:"([^"]+)"')
            media_url = n_files[0]
            if 'm3u8' in media_url: print '$'*53+'- Movies Ultra -'+'$'*53,media_url,'$'*125
            elif 'mp4' in media_url: print '$'*38+'- Movies Ultra -'+'$'*38,media_url,'$'*95 
            plugintools.play_resolved_url(media_url)   
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def vidtodo(params):
    plugintools.log('[%s %s] Vidtodo.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")

    if not "embed" in page_url:
        page_url = page_url.replace("http://vidtodo.com/","http://vidtodo.com/embed-") + '.html'
    try:
        r = requests.get(page_url)
        data = r.content
        try:
            n_files = plugintools.find_single_match(data,'sources: \[\{(.*?)\}\]')
            sources = plugintools.find_multiple_matches(n_files,'file: "([^"]+)"')
            for item in sources:
                if 'mp4' in item: media_url = item
            else: media_url = sources[-1]
            print '$'*36+'- Movies Ultra -'+'$'*36,media_url,'$'*91
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def izanagi(params):
    plugintools.log('[%s %s] Izanagi %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        url_js = plugintools.find_single_match(data,"\.get\('(.*?)'")
        url_js = urllib.unquote(url_js) 
        r = requests.get(url_js,headers=headers)
        data_js = r.content
        try:
            js = json.loads(data_js)
            media_url = js["file"]
            print '$'*45+'- Movies Ultra -'+'$'*45,media_url,'$'*109
            plugintools.play_resolved_url(media_url)        
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png')) 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def yotta(params):
    plugintools.log('[%s %s] Yotta %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        url_js = plugintools.find_single_match(data,"\.get\('(.*?)'")
        url_js = urllib.unquote(url_js) 
        r = requests.get(url_js,headers=headers)
        data_js = r.content
        try:
            js = json.loads(data_js)
            media_url = js["sources"][0]['file']
            print '$'*218+'- Movies Ultra -'+'$'*218,media_url,'$'*455
            plugintools.play_resolved_url(media_url)      
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def kami(params):
    plugintools.log('[%s %s] Yotta %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        sources = plugintools.find_single_match(data,"sources: \[\{(.*?)\}\],")
        media_url = plugintools.find_multiple_matches(sources,'file: "([^"]+)"')
        try:
            media_url = media_url[0] 
            print '$'*43+'- Movies Ultra -'+'$'*43,media_url,'$'*105
            plugintools.play_resolved_url(media_url)    
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
       
def touchfile(params):
    plugintools.log('[%s %s] Touchfile.tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            id_vid = plugintools.find_single_match(page_url,'http://touchfile.tv/(.*?)/')
            page_url = 'http://bestream.tv/plugins/mediaplayer/site/_embed_touchfile.php?u='+id_vid
            #file: "http://bs131b1.bestream.tv/4Xav/file.webm?hash=9c2d02cdbf7ab9abf822834d84c9143c&time=1468663470&download_token=d0beec289188c131647ed6fbefc6c61435e90d05cf4966f35b41d682fd4eafbf",
        r = requests.get(page_url)
        data = r.text
        media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
        if media_url !="":
            print '$'*80+'- Movies Ultra -'+'$'*80,media_url,'$'*179 
            plugintools.play_resolved_url(media_url)  
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def zstream(params):
    plugintools.log('[%s %s] Zstream.to %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://zstream.to/","http://zstream.to/embed-") + ".html"
   
        r = requests.get(page_url)
        data = r.content
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"')
        if media_url !="":
            print '$'*35+'- Movies Ultra -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url       
    
def vodlock(params):
    plugintools.log('[%s %s] Vodlock.co %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://vodlock.co/","http://vodlock.co/embed-")
        if not 'html' in page_url: page_url = page_url+'.html'
        r = requests.get(page_url)
        data = r.content
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"')
        if media_url !="":
            print '$'*35+'- Movies Ultra -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url       
    
def goodvideohost(params):
    plugintools.log('[%s %s] Goodvideohost.com %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://goodvideohost.com/","http://goodvideohost.com/embed-") + '.html'
        r = requests.get(page_url)
        data = r.content
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"')
        if media_url !="":
            print '$'*35+'- Movies Ultra -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url       
    
def happystreams(params):
    plugintools.log('[%s %s] Happystreams.net %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        post_url = plugintools.find_single_match(data,"<Form method=\"POST\" action='(.*?)'")
        post_op = plugintools.find_single_match(data,'name="op" value="(.*?)"') 
        post_id = plugintools.find_single_match(data,'name="id" value="(.*?)"') 
        post_fname = plugintools.find_single_match(data,'name="fname" value="(.*?)"')
        post_hash = plugintools.find_single_match(data,'name="hash" value="(.*?)"')
        post = {'op': post_op, 'usr_login': '', 'id': post_id, 'fname': post_fname, 'referer': '', 'hash': post_hash, 'imhuman': 'Proceed+to+video'} 
        headers = {'Host': 'happystreams.net','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Referer': page_url}
        r = requests.post(post_url,data=post)
        data = r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"')
        if media_url !="":
            print '$'*38+'- Movies Ultra -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movies Ultra', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url       
    