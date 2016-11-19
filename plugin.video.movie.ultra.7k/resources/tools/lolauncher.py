# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie Ultra 7K Parser de SeriesFLV.com
# Version 0.1 (02.11.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)

""" lolabits.es
    2015 fightnight fork - edit aztuzeca"""


import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time,plugintools
from t0mm0.common.net import Net
net=Net()

addonName = xbmcaddon.Addon().getAddonInfo("name")
addonVersion = xbmcaddon.Addon().getAddonInfo("version")
addonId = xbmcaddon.Addon().getAddonInfo("id")
addonPath = xbmcaddon.Addon().getAddonInfo("path")

addon_id = 'plugin.video.movie.ultra.7k'
MainURL = 'http://lolabits.es/'
art_lola = addonPath + '\\art\\lola\\'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
icon= art_lola + 'icon.jpg'
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
#downloadPath = xbmc.translatePath('special://home/userdata/playlists/tmp').decode('utf-8')
downloadPath = selfAddon.getSetting('download-folder').decode('utf-8')
#pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
#cookies = os.path.join(pastaperfil, "cookies.lwp")
cookies = os.path.join(pastaperfil, "cookies.lwp")
username_lb = urllib.quote(selfAddon.getSetting('lolabits_user'))
                                            
status_lolabits='true'
lolabits_enable ='true'

fanart = 'https://lh3.googleusercontent.com/-UhgrYZCeNSY/Ul1dAlICQYI/AAAAAAAABe8/cXXLKfWG3Fc/s928-fcrop64=1,00310000ffcdffa6/lolabits_google_profileimage_1.jpg'


def lolauncher(params):
    plugintools.log('[%s %s] ---> Launching Lolabits... <--- ' % (addonName, addonVersion))

    if login_lolabits:
        menu_principal(1)


def login_lolabits(defora=False):
      username_lb = urllib.quote(selfAddon.getSetting('lolabits_user'))
      pwd_lb = selfAddon.getSetting('lolabits_pwd')
      try:
            link=abrir_url(MainURL)
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(link)[0]
            form_d = {'RedirectUrl':'','Redirect':'True','FileId':0,'Login':username_lb,'Password':pwd_lb,'RememberMe':'true','__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://lolabits.es', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://lolabits.es/','User-Agent':user_agent}
            endlogin=MainURL + 'action/login/login'
            try:
                  logintest= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')                  
            except: logintest='Erro'
      except:
            link='Erro'
            logintest='Erro'

      if re.search('003eA senha indicada n',logintest):
            #mensagemok('Lolabits.es','Contraseña incorrecta')
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Contraseña incorrecta", 3 , art_lola+'icon.png'))            
            entrarnovamente(1)
            return False
      elif re.search('existe. Certifica-te que indicaste o nome correcto.',logintest):
            #mensagemok('Lolabits.es','Nombre de usuario no válido')
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Nombre de usuario no válido", 3 , art_lola+'icon.png'))                        
            entrarnovamente(1)
            return False
      elif re.search(username_lb,logintest):
            #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Login correcto! Cookies guardadas", 3 , art_lola+'icon.png'))            
            net.save_cookies(cookies)
            return True
      
      elif re.search('Erro',logintest) or link=='Erro':
            #opcao= xbmcgui.Dialog().yesno('Lolabits @ Movie Ultra 7K', 'Sin conexión a Internet', "", "",'Reintentar', 'OK')
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Sin conexión a Internet", 3 , art_lola+'icon.png'))            
            return False
      else: return False
            

################################################### MENUS PLUGIN ######################################################

def menu_principal(params):
    plugintools.log('[%s %s] ---> Launching Lolabits... <--- ' % (addonName, addonVersion))
    datamovie={}    
          
    if login_lolabits():
        if status_lolabits == 'true': #addDir('Mi Lolabits',MainURL + username_lb,3, art_lola + 'pasta.png',2,True)
            datamovie["Plot"]='Acceder a mi cuenta en Lolabits. Asegúrate de haber configurado correctamente los datos de tu cuenta en la configuración de [B]Movie Ultra 7K[/B]'
            plugintools.add_item(action="pastas", title='[COLOR white]Mi Lolabits[/COLOR]', url=MainURL+username_lb, thumbnail=art_lola+'logo.png', fanart=fanart, info_labels=datamovie, extra="2", folder=True, isPlayable=False)
            datamovie["Plot"]='Accede a la cuenta Lolabits de otros usuarios y navega en busca de vídeos.'
            plugintools.add_item(action="abelhasmaisrecentes", title='[COLOR white]Ir a Lolabits de otro usuario[/COLOR]', thumbnail=art_lola+'logo.png', info_labels=datamovie, fanart=fanart, extra="2", folder=True, isPlayable=False)
            datamovie["Plot"]='Mi lista de archivos de Lolabits favoritos.'
            plugintools.add_item(action="favoritos", title='[COLOR white]Amigos[/COLOR]', url=MainURL, thumbnail=art_lola+'logo.png', extra="2", fanart=fanart, folder=True, isPlayable=False)
            datamovie["Plot"]='Búsqueda de contenidos en los servidores de Lolabits (¡hay gigas infinitos!).'
            plugintools.add_item(action="pesquisa", title='[COLOR white]Buscar contenido[/COLOR]', thumbnail=art_lola+'v.png', fanart=fanart, extra="3", folder=True, isPlayable=False)
            datamovie["Plot"]='Configura tu cuenta Lolabits de [B]Movie Ultra 7K[/B]'
            plugintools.add_item(action="config_lola", title='[COLOR red]Configuración[/COLOR]', url=MainURL+username_lb, thumbnail=art_lola+'logo.png', fanart=fanart, info_labels=datamovie, extra="2", folder=False, isPlayable=False)            
            #addDir('Amigos',MainURL,9, art_lola + 'pasta.png',2,True)
            #addDir('Buscar contenido','pesquisa',7, art_lola + 'pasta.png',3,True)
    else:
        addDir('Reconectar Addon',MainURL,6,art_lola + 'pasta.png',1,True)
      


def entrarnovamente(opcoes):
      print 'entrarnovamente'
      
      if opcoes==1: selfAddon.openSettings()
      addDir('Entrar al addon',MainURL,None,art_lola + 'refresh.png',1,True)
      addDir('Cambiar ajustes',MainURL,8,art_lola + 'defs.png',1,False)

def topcolecionadores():
    if status_lolabits == 'true':
        conteudo=clean(abrir_url_cookie('http://lolabits.es/' + username_lb))
        users=re.compile('<li><div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span></span></a></div>.+?<i>(.+?)</i></li>').findall(conteudo)
        for urluser,nomeuser,thumbuser,nruser in users:
            #addDir('[B][COLOR gold]' + nruser + 'º Abelhas[/B][/COLOR] ' + nomeuser,MainURL + urluser,3,thumbuser,len(users),True)
            plugintools.add_item(action="pastas", title='[COLOR gold]' + nruser + 'º Abelhas[/COLOR] ' + nomeuser, url=MainURL + urluser, thumbnail=thumbuser, folder=True, isPlayable=False)                

    xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def abelhasmaisrecentes(params):
    url = params.get("url")
    if status_lolabits == 'true':
        conteudo=clean(abrir_url_cookie('http://lolabits.es/action/LastAccounts/MoreAccounts'))
        users=re.compile('<div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span>').findall(conteudo)
        for urluser,nomeuser,thumbuser in users:
            #addDir('[B][COLOR gold]' + nomeuser + '[/B][/COLOR]',MainURL + urluser,3,thumbuser,len(users),True)
            plugintools.add_item(action='pastas', title='[COLOR gold]' + nomeuser + '[/COLOR]', url=MainURL+urluser, thumbnail=thumbuser, folder=True, isPlayable=False)
    xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def pesquisa(params):
      conteudo=clean(abrir_url_cookie('http://lolabits.es/action/Help'))      
      opcoeslabel=re.compile('<option value=".+?">(.+?)</option>').findall(conteudo)
      opcoesvalue=re.compile('<option value="(.+?)">.+?</option>').findall(conteudo)
      index = xbmcgui.Dialog().select('Seleccione un filtro', opcoeslabel)
      if index > -1:
            caixadetexto('pesquisa',ftype=opcoesvalue[index])
      else:sys.exit(0)

def favoritos(params):
      url=params.get("url")
      name = 'Amigos'
      
      if status_lolabits == 'true':
         conteudo=abrir_url_cookie(MainURL + username_lb)
         chomikid=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
         token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]

         if name=='Amigos':pagina=1
         else: pagina=int(name.replace("[COLOR gold]Página ",'').replace(' >>>[/COLOR]',''))
         form_d = {'page':pagina,'chomikName':chomikid,'__RequestVerificationToken':token}
         ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
         endlogin=MainURL + 'action/Friends/ShowAllFriends'
         info= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
         info=info.replace('javascript:;','/javascript:;')
         users=re.compile('<div class="friend avatar".+?<a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" />').findall(info)
         for urluser,nomeuser,thumbuser in users:
            #addDir(nomeuser,MainURL + urluser,3,thumbuser,len(users),True)
            plugintools.add_item(action="pastas", title=nomeuser, url=MainURL+urluser, thumbnail=thumbuser, folder=True, isPlayable=False)
         paginas(info)      
      
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def proxpesquisa_ab():
    from t0mm0.common.addon import Addon
    addon=Addon(addon_id)
    print addon_id
    save_cookies = addon.save_data('temp.txt',form_d)
    if save_cookies:
        pass
        #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Cookies guardadas", 3 , art_lola+'icon.png'))
    else:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "No se han guardado cookies", 3 , art_lola+'icon.png')) 
    ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
    form_d['Page']= form_d['Page'] + 1
    endlogin=MainURL + 'action/SearchFiles/Results'
    net.set_cookies(cookies)
    conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
    print 'form_d',form_d
    addon.save_data('temp.txt',form_d)
    pastas(MainURL + 'action/nada','coco',conteudo=conteudo)

def atalhos(type=False):
      pastatracks = os.path.join(pastaperfil, "atalhos")
      if not os.path.exists(pastatracks):
            os.makedirs(pastatracks)
            savefile('ref.tmp','0',pastafinal=pastatracks)
      if type=='addfolder':
            ref=int(openfile('ref.tmp',pastafinal=pastatracks)) + 1
            builder='{"name":"""%s""","url":"""%s""","type":"folder"}' % (name,url)
            savefile('%s.txt' % ref,builder,pastafinal=pastatracks)
            savefile('ref.tmp',str(ref),pastafinal=pastatracks)
            xbmc.executebuiltin("XBMC.Notification(abelhas.pt,Atalho adicionado,'500000',"+iconpequeno.encode('utf-8')+")")
      elif type=='addfile':
            ref=int(openfile('ref.tmp',pastafinal=pastatracks)) + 1
            builder='{"name":"""%s""","url":"""%s""","type":"file"}' % (name,url)
            savefile('%s.txt' % ref,builder,pastafinal=pastatracks)
            savefile('ref.tmp',str(ref),pastafinal=pastatracks)
            xbmc.executebuiltin("XBMC.Notification(abelhas.pt,Atalho adicionado,'500000',"+iconpequeno.encode('utf-8')+")")
      elif type=='remove':
            try:os.remove(os.path.join(pastatracks,name))
            except:pass
            xbmc.executebuiltin("Container.Refresh")
            
      else:
            try:lista = os.listdir(pastatracks)
            except: lista=[]
            
            for atal in lista:
                  
                  content=openfile(atal,pastafinal=pastatracks)
                  
                  try:ftype=re.compile('"type":"(.+?)"').findall(content)[0]
                  except:ftype=''
                  try:fname=re.compile('"name":"""(.+?)"""').findall(content)[0]
                  except:fname=''
                  try:furl=re.compile('"url":"""(.+?)"""').findall(content)[0]
                  except:furl=''
                  path=urllib.unquote_plus('/'.join(''.join(furl.split(MainURL)).split('/')[:-1]).replace('*','%'))
                  if ftype=='file': addCont('%s (%s)' % (fname,path),furl,4,'',art_lola + 'file.png',len(lista),False,atalhos=atal)
                  elif ftype=='folder': addDir('%s (%s)' % (fname,path),furl,3,art_lola + 'pasta.png',len(lista),True,atalhos=atal)
                  
            
#def pastas(url,name,formcont={},conteudo='',past=False):
def pastas(params):
    plugintools.log("[%s %s] pastas %s" % (addonName, addonVersion, repr(params)))
    
    url=params.get("url")
    name=params.get("title")
    formcont=params.get("page")
    if formcont == "":
        formcont={}
    conteudo=''
    past=False

    sitebase=MainURL
    host='lolabits.es'
    color='gold'

    if re.search('action/SearchFiles',url):
        ref_data = {'Host': host, 'Connection': 'keep-alive', 'Referer': 'http://'+host+'/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://'+host+'/'}
        endlogin=sitebase + 'action/SearchFiles'
        conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
        if re.search('El fichero n&#227;o fue encontrado',conteudo):
              mensagemok(host,'Sin resultados.')
       
        try:
            filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            try: ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            except: ftype='All'

            pagina=1
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]

            form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token};print 'form_d',form_d
            from t0mm0.common.addon import Addon
            addon=Addon(addon_id)
            save_cookies = addon.save_data('temp.txt',form_d)
            if save_cookies:
                pass
                #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Cookies guardadas", 3 , art_lola+'icon.png'))
            else:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "No se han guardado cookies", 3 , art_lola+'icon.png')) 
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'http://'+host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=sitebase + 'action/SearchFiles/Results'
            conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        except: pass
        
    else:
        if conteudo=='':
              extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
              conteudo=clean(abrir_url_cookie(url + extra))

    if re.search('ProtectedFolderChomikLogin',conteudo):
        chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]

        passwordfolder=caixadetexto('password');print 'passwordfolder',passwordfolder
        form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
        ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'http://' + host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
        endlogin=sitebase + 'action/Files/LoginToFolder'
        teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        teste=urllib.unquote(teste)
        if re.search('IsSuccess":false',teste):
              xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Contraseña incorrecta", 3 , art_lola+'icon.png'))
              sys.exit(0)
        else:
              xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Contraseña correcta", 3 , art_lola+'icon.png'))
              pastas_ref(url)
              
    elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
        chomiktype=re.compile('<input id="ChomikType" name="ChomikType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        accname=re.compile('<input id="AccountName" name="AccountName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        
        passwordfolder=caixadetexto('password');print 'password',passwordfolder
        form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','IsAdult':isadult,'Sex':sex,'AccountName':accname,'AdultFilter':adultfilter,'ChomikType':chomiktype,'TargetChomikId':chomikid}
        ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'http://'+host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
        endlogin=sitebase + 'action/UserAccess/LoginToProtectedWindow'
        teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        teste=urllib.unquote(teste)
        if re.search('<span class="field-validation-error">A password introduzida est',teste):
              xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Contraseña incorrecta", 3 , art_lola+'icon.png'))            
        else:
              xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Contraseña correcta", 3 , art_lola+'icon.png'))
              pastas_ref(url)
    else:
        try:
            conta=re.compile('<div class="bigFileInfoRight">.+?<h3>(.+?)<span>(.+?)</span></h3>').findall(conteudo)[0]
            nomeconta=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #addLink('[COLOR blue][B]' + 'Cuenta de ' + nomeconta + '[/B][/COLOR]: ' + conta[0] + conta[1],'',art_lola + 'star2.png')
            plugintools.add_item(action="", title='[COLOR blue]Cuenta de ' + nomeconta + '[/COLOR]: ' + conta[0] + conta[1] , thumbnail=art_lola+'star2.png', folder=False, isPlayable=False)
        except: pass

        try:
            checker=url.split('/')[:-1]
            if len(checker) > 3 and not re.search('action/SearchFiles',url) and not re.search('/action/nada',url):
                urlbefore='/'.join(checker);print 'urlbefore',urlbefore
                #addDir('[COLOR blue][B]Carpeta superior[/B][/COLOR]',urlbefore,3,art_lola + 'seta.png',1,True)
                plugintools.add_item(action="pastas", title='[COLOR blue]Carpeta superior[/COLOR]', url=urlbefore, extra="1", thumbnail=art_lola+'seta.png', folder=True, isPlayable=False)
        except: pass

        try:
              pastas=re.compile('<div id="foldersList">(.+?)</table>.+?').findall(conteudo)
              seleccionados=re.compile('<a href="/(.+?)".+?title="(.+?)">(.+?)</a>').findall(pastas[0])
              for urlpasta,nomepasta,password in seleccionados:
                    
                    if re.search('<span class="pass">',password): displock=' (' + 'bloqueado'+')'
                    else:displock=''
                    #addDir('[B][COLOR white]' + nomepasta + '[/COLOR][/B]' + displock,sitebase + urlpasta,3,art_lola + 'pasta.png',len(seleccionados),True)
                    items=len(seleccionados)
                    plugintools.add_item(action="pastas", title='[COLOR white]' + nomepasta + '[/COLOR]'+displock, url=sitebase+urlpasta, thumbnail=art_lola+'pasta.png', extra=str(items), folder=True, isPlayable=False)
        except: pass
        #contributo mafarricos com alteracoes, ty
        items1=re.compile('<a class="expanderHeader downloadAction" href="(.+?)" title="(.+?)">.+?</span>(.+?)</a>.+?<li><span>(.+?)</span></li>.+?<span class="downloadsCounter">.+?<li>(.+?)</li>.+?rel="(.+?)">').findall(conteudo)
        for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro,fileid in items1:
              extensao=extensao.replace(' ','')
              tamanhoficheiro=tamanhoficheiro.replace(' ','')
              if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.7z' or extensao=='.7Z': thumb=art_lola + 'rar.png'
              elif extensao=='.mp3' or extensao=='.MP3' or extensao=='.ogg' or extensao=='.OGG' or extensao=='.aac' or extensao=='.AAC' or extensao=='.m4a' or extensao=='.M4A' or extensao == '.wma' or extensao=='.WMA' or extensao=='.ac3' or extensao=='.AC3' or extensao=='.flac' or extensao=='.FLAC' or extensao=='.m3u' or extensao=='.M3U': thumb=art_lola + 'musica.png'
              elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=art_lola + 'foto.png'
              elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.ogm' or extensao == '.OGM' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV' or extensao=='.mpg' or extensao=='.MPG': thumb=art_lola + 'video.png'
              else:thumb=art_lola + 'file.png'
              tamanhoparavariavel=' (' + tamanhoficheiro + ')'
              if past==False: modo=4
              else: modo=22
              #addCont('[B][COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR][/B]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]',sitebase + urlficheiro,modo,tamanhoparavariavel,thumb,len(items1),past,False)
              plugintools.add_item(action="analyzer", title='[COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]', url=sitebase + urlficheiro, thumbnail=thumb, page=fileid ,extra=fileid, folder=False, isPlayable=False)
        #contributo mafarricos com alteracoes, ty
        items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>.+?rel="(.+?)">').findall(conteudo)
        for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro,fileid in items2:
              extensao=extensao.replace(' ','')
              if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.7z' or extensao=='.7Z': thumb=art_lola + 'rar.png'
              elif extensao=='.mp3' or extensao=='.MP3' or extensao=='.ogg' or extensao=='.OGG' or extensao=='.aac' or extensao=='.AAC' or extensao=='.m4a' or extensao=='.M4A' or extensao == '.wma' or extensao=='.WMA' or extensao=='.ac3' or extensao=='.AC3' or extensao=='.flac' or extensao=='.FLAC' or extensao=='.m3u' or extensao=='.M3U': thumb=art_lola + 'musica.png'
              elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=art_lola + 'foto.png'
              elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.ogm' or extensao == '.OGM' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV' or extensao=='.mpg' or extensao=='.MPG': thumb=art_lola + 'video.png'
              else:thumb=art_lola + 'file.png'
              tamanhoparavariavel=' (' + tamanhoficheiro + ')'
              if past==False: modo=4
              else: modo=22
              #addCont('[B][COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR][/B]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]',sitebase + urlficheiro,modo,tamanhoparavariavel,thumb,len(items2),past,False)
              plugintools.add_item(action="analyzer", title='[COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]', url=sitebase + urlficheiro, thumbnail=thumb, page=fileid, extra=fileid, folder=False, isPlayable=False)
        if not items1:
              if not items2:
                    conteudo=clean(conteudo)
                    #isto ta feio
                    items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                    for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                          tamanhoficheiro=tamanhoficheiro.replace(' ','')
                          extensao=extensao.replace(' ','')
                          tituloficheiro=tituloficheiro.replace(str(extensao),'')
                          thumb=art_lola + 'file.png'
                          tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                          if past==False: modo=4
                          else: modo=22
                          #addCont('[B][COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR][/B]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]',sitebase + urlficheiro,modo,tamanhoparavariavel,thumb,len(items2),past,False)
                          plugintools.add_item(action="analyzer", title='[COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]', url=sitebase+urlficheiro,thumbnail=thumb,folder=False,isPlayable=False)
                          
        paginas(conteudo)
    
def pastas_de_fora(url,name,formcont={},conteudo='',past=False):
    login_abelhas(True)
    source = xbmcgui.Dialog().select
    selectlist = []
    urllist = []
    formcont = {'submitSearchFiles': 'Procurar', 'FileType': 'video', 'IsGallery': 'False', 'FileName': name }
    if re.search('action/SearchFiles',url):
            ref_data = {'Host': 'lolabits.es', 'Connection': 'keep-alive', 'Referer': 'http://lolabits.es/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://lolabits.es/'}
            endlogin=MainURL + 'action/SearchFiles'
            conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
            if re.search('El fichero no fue encontrado',conteudo):
                    mensagemok('Lolabits.es','Sin resultados.')
                    sys.exit(0)
            try:
                    filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                    try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                    except: ftype='All'
                    pagina=1
                    token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]
                    form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token};print 'form_d',form_d
                    from t0mm0.common.addon import Addon
                    addon=Addon(addon_id)
                    save_cookies = addon.save_data('temp.txt',form_d)
                    if save_cookies:
                        pass
                        #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Cookies guardadas", 3 , art_lola+'icon.png'))
                    else:
                        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "No se han guardado cookies", 3 , art_lola+'icon.png')) 
                    ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                    endlogin=MainURL + 'action/SearchFiles/Results'
                    conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
    else:
            if conteudo=='':
                    extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                    conteudo=clean(abrir_url_cookie(url + extra))
    if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                    mensagemok('Lolabits.es','Contraseña incorrecta')
                    sys.exit(0)
            else:
                    pastas_ref(url)
    elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
            chomikid=re.compile('<input id="TargetChomikId" name="TargetChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            chomiktype=re.compile('<input id="ChomikType" name="ChomikType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            accname=re.compile('<input id="AccountName" name="AccountName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password');print 'passwordfolder',passwordfolder
            form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','IsAdult':isadult,'Sex':sex,'AccountName':accname,'AdultFilter':adultfilter,'ChomikType':chomiktype,'TargetChomikId':chomikid}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/UserAccess/LoginToProtectedWindow'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('<span class="field-validation-error">A password introduzida est',teste):
                    mensagemok('Lolabits.es','Contraseña incorrecta')
                    sys.exit(0)
            else:
                    pastas_ref(url)
    else:
            try:
                    conta=re.compile('<div class="bigFileInfoRight">.+?<h3>(.+?)<span>(.+?)</span></h3>').findall(conteudo)[0]
                    nomeconta=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                    addLink('[COLOR blue]' + 'Cuenta de' + nomeconta + '[/COLOR]: ' + conta[0] + conta[1],'',art_lola + 'star2.png')
            except: pass
            try:
                    checker=url.split('/')[:-1]
                    if len(checker) > 3 and not re.search('action/SearchFiles',url) and not re.search('lolabits.es/action/nada',url):
                            urlbefore='/'.join(checker)
                            #addDir('[COLOR blue][B]Carpeta superior[/B][/COLOR]',urlbefore,3,art_lola + 'seta.png',1,True)
                            plugintools.add_item(action="pastas", title='[COLOR blue]Carpeta superior[/COLOR]', url=urlbefore, thumbnail=art_lola+'seta.png',extra="1", folder=True, isPlayable=False)
            except: pass
            try:
                    pastas=re.compile('<div id="foldersList">(.+?)</table>').findall(conteudo)[0]
                    seleccionados=re.compile('<a href="/(.+?)".+?title="(.+?)">(.+?)</a>').findall(pastas)
                    for urlpasta,nomepasta,password in seleccionados:
                            if re.search('<span class="pass">',password): displock=' (' + 'bloqueado'+')'
                            else:displock=''
                            #addDir(nomepasta + displock,MainURL + urlpasta,3,art_lola + 'pasta.png',len(seleccionados),True)
                            plugintools.add_item(action="pastas", title=nomepasta+displock,url=MainURL+urlpasta, thumbnail=art_lola+'pasta.png',extra=len(seleccionados),folder=True, isPlayable=False)
            except: pass
            #contributo mafarricos com alteracoes, ty
            items1=re.compile('<li class="fileItemContainer">\s+<p class="filename">\s+<a class="downloadAction" href=".+?">    <span class="bold">.+?</span>(.+?)</a>\s+</p>\s+<div class="thumbnail">\s+<div class="thumbnailWrapper expType" rel="Image" style=".+?">\s+<a href="(.+?)" class="thumbImg" rel="highslide" style=".+?" title="(.+?)">\s+<img src=".+?" rel=".+?" alt=".+?" style=".+?"/>\s+</a>\s+</div>\s+</div>\s+<div class="smallTab">\s+<ul>\s+<li>\s+(.+?)</li>\s+<li><span class="date">(.+?)</span></li>').findall(conteudo)         
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1:
                    extensao=extensao.replace(' ','')
                    tamanhoficheiro=tamanhoficheiro.replace(' ','')
                    if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.7z' or extensao=='.7Z': thumb=art_lola + 'rar.png'
                    elif extensao=='.mp3' or extensao=='.MP3' or extensao=='.ogg' or extensao=='.OGG' or extensao=='.aac' or extensao=='.AAC' or extensao=='.m4a' or extensao=='.M4A' or extensao == '.wma' or extensao=='.WMA' or extensao=='.ac3' or extensao=='.AC3' or extensao=='.flac' or extensao=='.FLAC' or extensao=='.m3u' or extensao=='.M3U': thumb=art_lola + 'musica.png'
                    elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=art_lola + 'foto.png'
                    elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.ogm' or extensao == '.OGM' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV' or extensao=='.mpg' or extensao=='.MPG': thumb=art_lola + 'video.png'
                    else:thumb=art_lola + 'file.png'
                    tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                    if past==False: modo=4
                    else: modo=22
                    #addCont('[B]' + tituloficheiro + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,modo,tamanhoparavariavel,thumb,len(items1),past,False)
                    plugintools.add_item(action="analyzer", title='' + tituloficheiro + '' + tamanhoparavariavel,url=MainURL + urlficheiro, thumbnail=thumb,page=fileid,extra=fileid,folder=True, isPlayable=False)
            #contributo mafarricos com alteracoes, ty
            items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2:
                    extensao=extensao.replace(' ','')
                    if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.7z' or extensao=='.7Z': thumb=art_lola + 'rar.png'
                    elif extensao=='.mp3' or extensao=='.MP3' or extensao=='.ogg' or extensao=='.OGG' or extensao=='.aac' or extensao=='.AAC' or extensao=='.m4a' or extensao=='.M4A' or extensao == '.wma' or extensao=='.WMA' or extensao=='.ac3' or extensao=='.AC3' or extensao=='.flac' or extensao=='.FLAC' or extensao=='.m3u' or extensao=='.M3U': thumb=art_lola + 'musica.png'
                    elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=art_lola + 'foto.png'
                    elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.ogm' or extensao == '.OGM' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV' or extensao=='.mpg' or extensao=='.MPG': thumb=art_lola + 'video.png'
                    else:thumb=art_lola + 'file.png'
                    tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                    if past==False: modo=4
                    else: modo=22
                    #addCont('[B]' + tituloficheiro + extensao + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,modo,tamanhoparavariavel,thumb,len(items2),past,False)
                    if modo==4:
                            selectlist.append(tituloficheiro + extensao + ' '+tamanhoparavariavel)
                            urllist.append(MainURL + urlficheiro)
            if not items1:
                    if not items2:
                            conteudo=clean(conteudo)
                            #isto ta feio
                            items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                            for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                                    tamanhoficheiro=tamanhoficheiro.replace(' ','')
                                    thumb=art_lola + 'file.png'
                                    tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                                    if past==False: modo=4
                                    else: modo=22
                                    #addCont('[B]' + tituloficheiro + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,modo,tamanhoparavariavel,thumb,len(items2),past,False) 
                                    if modo == 4:
                                            selectlist.append(tituloficheiro + ' ' + tamanhoparavariavel)
                                            urllist.append(MainURL + urlficheiro)
                                            
            #paginas(conteudo)
    choose=source('Link a Abrir',selectlist)
    if choose > -1:	analyzer(urllist[choose])
    
def obterlistadeficheiros():
    string=[]
    nrdepaginas=71
    for i in xrange(1,int(nrdepaginas)+1):
          url='http://abelhas.pt/qqcoisa,%s' % i
          extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
          conteudo=clean(abrir_url_cookie(url + extra))
          items1=re.compile('<li class="fileItemContainer">\s+<p class="filename">\s+<a class="downloadAction" href=".+?">    <span class="bold">.+?</span>(.+?)</a>\s+</p>\s+<div class="thumbnail">\s+<div class="thumbnailWrapper expType" rel="Image" style=".+?">\s+<a href="(.+?)" class="thumbImg" rel="highslide" style=".+?" title="(.+?)">\s+<img src=".+?" rel=".+?" alt=".+?" style=".+?"/>\s+</a>\s+</div>\s+</div>\s+<div class="smallTab">\s+<ul>\s+<li>\s+(.+?)</li>\s+<li><span class="date">(.+?)</span></li>').findall(conteudo)         
          for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1:
                string.append(tituloficheiro)
          #contributo mafarricos com alteracoes, ty
          items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
          for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2:
                string.append(tituloficheiro)
          if not items1:
                if not items2:
                      conteudo=clean(conteudo)
                      #isto ta feio
                      items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                      for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                            string.append(tituloficheiro)

def criarplaylist(url,name,formcont={},conteudo=''):
   if re.search('minhateca.com.br',url):
      mensagemprogresso.create('Minhateca.com.br', 'Lista de reproducción creada')
      playlist = xbmc.PlayList(1)
      playlist.clear()
      if re.search('action/SearchFiles',url):
            ref_data = {'Host': 'minhateca.com.br', 'Connection': 'keep-alive', 'Referer': 'http://minhateca.com.br/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://minhateca.com.br/'}
            endlogin=MinhaMainURL + 'action/SearchFiles'
            conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
            if re.search('O ficheiro n.+?o foi encontrado',conteudo):
                  mensagemok('Minhateca.com.br','Sem resultados.')
                  sys.exit(0)
            try:
                filename=re.compile('<input name="FileName" type="hidden" value="(.+?)">').findall(conteudo)[0]
                try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)">').findall(conteudo)[0]
                except: ftype='All'
                pagina=1
                token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]
                form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token};print 'form_d',form_d
                from t0mm0.common.addon import Addon
                addon=Addon(addon_id)
                save_cookies = addon.save_data('temp.txt',form_d)
                if save_cookies:
                    pass
                    #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Cookies guardadas", 3 , art_lola+'icon.png'))
                else:
                    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "No se han guardado cookies", 3 , art_lola+'icon.png'))
                ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'minhateca.com.br','Origin':'http://minhateca.com.br','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                endlogin=MinhaMainURL + 'action/SearchFiles/Results'
                conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
      else:
            if conteudo=='':
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))
      if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'minhateca.com.br','Origin':'http://minhateca.com.br','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MinhaMainURL + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                  mensagemok('Minhateca.com.br','Contraseña incorrecta')
                  sys.exit(0)
            else: pastas_ref(url)
      elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
            chomikid=re.compile('<input id="TargetChomikId" name="TargetChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            chomiktype=re.compile('<input id="Mode" name="Mode" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            accname=re.compile('<input id="__accno" name="__accno" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','AccountName':accname,'ChomikType':chomiktype,'TargetChomikId':chomikid}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'minhateca.com.br','Origin':'http://minhateca.com.br','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MinhaMainURL + 'action/UserAccess/LoginToProtectedWindow'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('<span class="field-validation-error">A password introduzida est',teste):
                  mensagemok('Minhateca.com.br','Contraseña incorrecta')
                  sys.exit(0)
            else: pastas_ref(url)
      else:
            items1=re.compile('<a class="expanderHeader downloadAction" href="(.+?)" title="(.+?)">.+?</span>(.+?)</a>.+?<li><span>(.+?)</span></li>.+?<span class="downloadsCounter">.+?<li>(.+?)</li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1: analyzer(MinhaMainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2: analyzer(MinhaMainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            if not items1:
                  if not items2:
                        conteudo=clean(conteudo)
                        #isto ta feio
                        items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                        for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                              tamanhoficheiro=tamanhoficheiro.replace(' ','')
                              analyzer(MinhaMainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
   else:
      mensagemprogresso.create('Abelhas.pt', 'Lista de reproducción creada')
      playlist = xbmc.PlayList(1)
      playlist.clear()
      if re.search('action/SearchFiles',url):
            ref_data = {'Host': 'lolabits.es', 'Connection': 'keep-alive', 'Referer': 'http://lolabits.es/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}
            endlogin=MainURL + 'action/SearchFiles'
            conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
            if re.search('O ficheiro n.+?o foi encontrado',conteudo):
                  mensagemok('Lolabits.es','Sem resultados.')
                  sys.exit(0)
            try:
                filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                except: ftype='All'
                pagina=1
                token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]
                form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token};print 'form_d',form_d
                from t0mm0.common.addon import Addon
                addon=Addon(addon_id)
                save_cookies = addon.save_data('temp.txt',form_d)
                if save_cookies:
                    pass
                    #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Cookies guardadas", 3 , art_lola+'icon.png'))
                else:
                    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "No se han guardado cookies", 3 , art_lola+'icon.png')) 
                ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                endlogin= MainURL+ 'action/SearchFiles/Results'
                conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
      else:
            if conteudo=='':
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))
      if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                  mensagemok('Lolabits.es','Contraseña incorrecta')
                  sys.exit(0)
            else: pastas_ref(url)
      elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
            chomikid=re.compile('<input id="TargetChomikId" name="TargetChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            chomiktype=re.compile('<input id="Mode" name="Mode" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            accname=re.compile('<input id="__accno" name="__accno" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','AccountName':accname,'ChomikType':chomiktype,'TargetChomikId':chomikid}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/UserAccess/LoginToProtectedWindow'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('<span class="field-validation-error">A password introduzida est',teste):
                  mensagemok('Lolabits.es','Contraseña incorrecta')
                  sys.exit(0)
            else: pastas_ref(url)
      else:
            items1=re.compile('<a class="expanderHeader downloadAction" href="(.+?)" title="(.+?)">.+?</span>(.+?)</a>.+?<li><span>(.+?)</span></li>.+?<span class="downloadsCounter">.+?<li>(.+?)</li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1: analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2: analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            if not items1:
                  if not items2:
                        conteudo=clean(conteudo)
                        #isto ta feio
                        items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                        for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                              tamanhoficheiro=tamanhoficheiro.replace(' ','')
                              analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
      mensagemprogresso.close()
      xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
      xbmcPlayer.play(playlist)


def pastas_ref(url):      
      plugintools.log("pastas_ref(params) "+url)
      params=plugintools.get_params()
      pastas(params)

def paginas(link):
      sitebase=MainURL
      nextname='Lolabits'
      color='gold'
      mode=12

      try:
            #idmode=3
            idmode='pastas'
      
            try:
                  conteudo=re.compile('<div id="listView".+?>(.+?)<div class="filerow fileItemContainer">').findall(link)[0]
                  
            except:
                  try:conteudo=re.compile('<div class="paginator clear searchListPage">(.+?)<div class="clear">').findall(link)[0]
                  except:
                        conteudo=re.compile('<div class="paginator clear friendspager">(.+?)<div class="clear">').findall(link)[0]
                        #idmode=9
                        idmode='favoritos'
            try:
                  pagina=re.compile('anterior.+?<a href="/(.+?)" class="right" rel="(.+?)"').findall(conteudo)[0]
                  urlpag=pagina[0]
                  urlpag=urlpag.replace(' ','+')
                  #addDir('[COLOR '+color+']Página ' + pagina[1] + ' ' + nextname + ' >>>[/COLOR]',sitebase + urlpag,idmode,art_lola + 'seta.png',1,True)
                  plugintools.add_item(action=idmode, title='[COLOR '+color+']Página '+pagina[1]+' '+nextname+' >>>[/COLOR]', url=sitebase + urlpag, thumbnail=art_lola+'seta.png', extra="1", folder=True, isPlayable=False)
            except:
                  nrpagina=re.compile('type="hidden" value="([^"]+?)" /><input type="submit" value="p.+?gina seguinte.+?" /></form>').findall(link)[0]
                  #addDir('[COLOR '+color+']Página ' + nrpagina + ' ' + nextname + ' >>>[/COLOR]',sitebase,mode,art_lola + 'seta.png',1,True)
                  plugintools.add_item(action=idmode, title='[COLOR '+color+']Página ' + nrpagina + ' ' + nextname + ' >>>[/COLOR]', url=sitebase + urlpag, thumbnail=art_lola+'seta.png', extra="1", folder=True, isPlayable=False)
                  #pass
                  
      
            
      except:
            pass


########################################################### PLAYER ################################################

#def analyzer(url,subtitles='',playterm=False,playlistTitle=''):
def analyzer(params):
    plugintools.log('[%s %s] Analyzer %s ' % (addonName, addonVersion, repr(params)))
    
    name=params.get("title")
    url=params.get("url")
    subtitles=params.get("extra")
    params["thumbnail"]=art_lola+'logo.png'
    if subtitles=='sim': conteudo=abrir_url_cookie(url)
    else:conteudo=abrir_url_cookie(url,erro=False)
    playterm=False
    playlistTitle=''
        
    sitebase=MainURL
    host='lolabits.es'
    sitename='Lolabits.es'
    fileid = params.get("page");print 'fileid',fileid
      
    if playlistTitle == '': mensagemprogresso.create(sitename, 'Cargando...')
    linkfinal=''
    if subtitles=='sim': conteudo=abrir_url_cookie(url)
    else: conteudo=abrir_url_cookie(url)    

    # Error en datos de la cuenta
    if re.search('Pode acontecer que a mensagem de confirma',conteudo):
        mensagemok(sitename,'Debes activar tu cuenta en '+sitename+'.')
        return

    # Error en contraseña de carpeta
    if re.search('ProtectedFolderChomikLogin',conteudo):
        #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Error en contraseña de carpeta ", 2 , art_lola+'icon.png'))    
        plugintools.log("Carpeta protegida. Enviamos contraseña para: " + url)
        # 00:42:49 T:2800  NOTICE: Carpeta protegida. Enviamos contraseÃ±a para: http://lolabits.es//ARENAmas/ArenaTeam/CINE/Am*c3*a9lie,30221138.mkv(video)

        # 00:43:25 T:5588  NOTICE: Carpeta protegida. Enviamos contraseÃ±a para: http://lolabits.es/ARENAmas/ArenaTeam/CINE/Am*c3*a9lie,30221138.mkv(video)

        chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        passwordfolder=caixadetexto('password');print 'passwordfolder',passwordfolder
        form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
        ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'http://' + host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
        endlogin=sitebase + 'action/Files/LoginToFolder'
        teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        teste=urllib.unquote(teste)
        print 'teste',teste

    try:
        try: fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"/>').findall(conteudo)[0]
        except: fileid=params.get("extra")
        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        form_d = {'fileId':fileid,'__RequestVerificationToken':token}
        ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://' + host, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://'+host+'/','User-Agent':user_agent}
        endlogin=sitebase + 'action/License/Download'
        final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        final=final.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','');print 'final-1',final
    except: pass    
    try:
        if re.search('action/License/acceptLargeTransfer',final):
            try: fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"').findall(final)[0]
            except: fileid = params.get("page")
            orgfile=re.compile('<input type="hidden" name="orgFile" value="(.+?)"').findall(final)[0]
            userselection=re.compile('<input type="hidden" name="userSelection" value="(.+?)"').findall(final)[0]
            form_d = {'fileId':fileid,'orgFile':orgfile,'userSelection':userselection,'__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://' + sitebase, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://'+sitebase+'/','User-Agent':user_agent}
            endlogin=sitebase + 'action/License/acceptLargeTransfer'
            final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore');print 'final-2',final
    except: pass
    try:
        if re.search('causar problemas com o uso de aceleradores de download',final):linkfinal=re.compile('a href=\"(.+?)\"').findall(final)[0]
        else: linkfinal=re.compile('"redirectUrl":"(.+?)"').findall(final)[0];print 'linkfinal1',linkfinal
        comecarvideo(name,linkfinal,playterm=playterm)
    except: pass


def legendas(moviefileid,url):
      print 'legendas'
      url=url.replace(','+moviefileid,'').replace('.mkv','.srt').replace('.mp4','.srt').replace('.avi','.srt').replace('.wmv','.srt')[:-7]
      #legendas=analyzer(url,subtitles='sim')
      params=plugintools.get_params();params["url"]=url;params["extra"]='sim'
      legendas=analyzer(params)
      return legendas

def comecarvideo(name,url,playterm,legendas=None):
        print 'comecarvideo'
        sitename='Lolabits - '+name      
        playeractivo = xbmc.getCondVisibility('Player.HasMedia')
        if playterm=='download':
              fazerdownload(name,url)
              return
        thumbnail=''
        playlist = xbmc.PlayList(1)
        if not playterm and playeractivo==0: playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        #listitem.setInfo("Video", {"Title":"Balas & Bolinhos","year":2001})
        title='%s' % (name.split('[/B]')[0].replace('[B]',''))

        listitem.setInfo("Video", {"Title":title})
        listitem.setInfo("Music", {"Title":title})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        listitem.setThumbnailImage(art_lola+'logo.png')
        if playterm <> 'playlist':
              dialogWait = xbmcgui.DialogProgress()
              dialogWait.create('Video', 'Cargando')
        playlist.add(url, listitem)
        if playterm <> 'playlist':		
              dialogWait.close()
              del dialogWait
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        if not playterm and playeractivo==0:
              xbmcPlayer.play(playlist)
        if legendas!=None: xbmcPlayer.setSubtitles(legendas)
        else:
			if plugintools.get_setting("subtitles") == 'true': 
				try: totalTime = xbmc.Player().getTotalTime()
				except: totalTime = 0
				print '##totaltime',totalTime
				if totalTime >= int(plugintools.get_setting("minsize"))*60:
					print '#pesquisar legendas'
					from resources.lib import subtitles
					legendas = subtitles.getsubtitles(name,plugintools.get_setting("sublang1"),plugintools.get_setting("sublang2"))
					if legendas!=None: xbmcPlayer.setSubtitles(legendas)
        if playterm=='playlist': xbmc.executebuiltin("XBMC.Notification("+sitename+","+'Añadiendo a la lista de reproducción'+",'500000',"+iconpequeno.encode('utf-8')+")")

def limparplaylist():
        playlist = xbmc.PlayList(1)
        playlist.clear()
        xbmc.executebuiltin("XBMC.Notification(abelhas.pt,"+'Lista de reproducción vacía'+",'500000',"+iconpequeno.encode('utf-8')+")")

def comecarplaylist():
        playlist = xbmc.PlayList(1)
        if playlist:
              xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
              xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta,atalhos=False):
      contexto=[]
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      contexto.append(('Crear Lista', 'XBMC.RunPlugin(%s?mode=15&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append(('Limpiar lista de reproducción', 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append(('Ver Trailer', 'RunPlugin(%s?mode=17&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      if atalhos==False:contexto.append(('Adicionar atalho', 'RunPlugin(%s?mode=20&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      else:contexto.append(('Remover atalho', 'RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),atalhos)))
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%addonPath)
      liz.addContextMenuItems(contexto, replaceItems=False) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addCont(name,url,mode,tamanho,iconimage,total,pasta=False,atalhos=False):
      contexto=[]
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&tamanhof="+urllib.quote_plus(tamanho)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      contexto.append(('Agregar a la lista de reproducción', 'XBMC.RunPlugin(%s?mode=10&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append(('Comenzar lista de reproducción', 'XBMC.RunPlugin(%s?mode=13&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append(('Limpiar lista de reproducción', 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append(('Ver Trailer', 'RunPlugin(%s?mode=17&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      if atalhos==False: contexto.append(('Adicionar atalho', 'RunPlugin(%s?mode=19&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      else: contexto.append(('Remover atalho', 'RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),atalhos)))
      contexto.append(('Transferir fichero', 'XBMC.RunPlugin(%s?mode=11&url=%s&name=%s&tamanhof=%s)' % (sys.argv[0], urllib.quote_plus(url),name,tamanho)))
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%addonPath)
      liz.addContextMenuItems(contexto, replaceItems=True) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
           
######################################################## DOWNLOAD ###############################################
### THANKS ELDORADO (ICEFILMS) ###
def fazerdownload(name,url,tipo="outros"):
      vidname=name.replace('[B]','').replace('[/B]','').replace('\\','').replace(str(tamanhoparavariavel),'')
      vidname = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  vidname)
      dialog = xbmcgui.Dialog()
      if tipo=="fotos":
            mypath=os.path.join(pastaperfil, vidname)
      else:
            downloadPath = dialog.browse(int(3), 'Descargar carpeta','myprograms')
            if os.path.exists(downloadPath):
                  mypath=os.path.join(downloadPath,vidname)
            else: return

      if os.path.isfile(mypath) is True:
            ok = mensagemok('Abelhas.pt','Este archivo ya existe en el disco','','')
            return False
      else:              
            try:
                  dp = xbmcgui.DialogProgress()
                  dp.create('Abelhas.pt - ' + 'Transferir', '', name)
                  start_time = time.time()
                  try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
                  except:
                        while os.path.exists(mypath): 
                              try: os.remove(mypath); break 
                              except: pass 
                        if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): return False 
                        else: raise 
                        return False
                  return True
            except: ok=mensagemok('Lolabits.es','Descarga fallida'); print 'download failed'; return False

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total) 
            #e = 'Velocidade: (%.0f Kb/s) ' % kbps_speed
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = 'Tiempo restante' + ': %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
            #if percent=xbmc.executebuiltin("XBMC.Notification(Abelhas.pt,"+ mbs + e + ",'500000',"+iconpequeno+")")
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)

######################################################## OUTRAS FUNCOES ###############################################

def caixadetexto(url,ftype=''):
    ultpes=''
    save=False
    folderpwd = plugintools.get_setting("lolabits_folderpwd")
      
    if url=='password':  # Control para devolver contraseña de carpeta
        if folderpwd != "": return folderpwd
        
    if url=='pastas' and re.search('Abelha',name): title="Ir a - Lolabits"
    elif url=='pastas' and re.search('Minhateca',name): title="Ir para - Minhateca"
    elif url=='password': title="Contraseña - Lolabits.es"
    elif url=='pesquisa':
        title='Búsqueda'
        ultpes=plugintools.get_setting('ultima-pesquisa')
        save=True
    else: title="Lolabits.es"
    keyb = xbmc.Keyboard(ultpes, title)
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        if search=='': sys.exit(0)
        encode=urllib.quote_plus(search)
        if save==True: plugintools.set_setting('ultima-pesquisa', search)
        if url=='pastas' and re.search('Abelha',name): pastas(MainURL + search,name)
        elif url=='pastas' and re.search('Minhateca',name): pastas(MinhaMainURL + search,name) 
        elif url=='password': return search            
        elif url=='pesquisa':
              if status_lolabits == 'true':
                    form_d = {'FileName':encode,'submitSearchFiles':'Procurar','FileType':ftype,'IsGallery':'False'}
                    params=plugintools.get_params()
                    params["url"]=MainURL+'action/SearchFiles'
                    params["page"]=form_d
                    #pastas(MainURL + 'action/SearchFiles',name,formcont=form_d,past=True)
                    pastas(params)
            
    else: sys.exit(0)
            
def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def savefile(filename, contents,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal,filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou os temporarios de: %s" % filename

def openfile(filename,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu os temporarios de: %s" % filename
        return None


def abrir_url_cookie(url,erro=True):
      net.set_cookies(cookies)
      if net.set_cookies(cookies):
          #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Cargando cookies...", 3 , art_lola+'icon.png'))
          pass
      try:
          if status_lolabits == 'true':
              ref_data = {'Host': 'lolabits.es', 'Connection': 'keep-alive', 'Referer': 'http://lolabits.es/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}
              link=net.http_POST(url,ref_data).content.encode('latin-1','ignore')
              return link
      except urllib2.HTTPError, e:
          if erro==True: mensagemok('Lolabits.es',str(urllib2.HTTPError(e.url, e.code, 'Error en página', e.hdrs, e.fp)),'Error en página')
          sys.exit(0)
      except urllib2.URLError, e:
          if erro==True: mensagemok('Lolabits.es','Error en página'+'Inténtelo de nuevo')
          sys.exit(0)

def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.abelhas/addon.xml')
            match=re.compile('name="Lolabits.es"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('Lolabits.es','Movie Ultra 7K no consigue conectar con el servidor','de actualización. Verifique su instalación','')
            match='Error. Verificar el origen del error'
      return match

def redirect(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      gurl=response.geturl()
      return gurl

def get_params2():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&amp;':'&','&ntilde;':'ñ','&#39;':'\'','&#170;':'ª','&#178;':'²','&#179;':'³','&#192;':'À','&#193;':'Á','&#194;':'Â','&#195;':'Ã','&#199;':'Ç','&#201;':'É','&#202;':'Ê','&#205;':'Í','&#211;':'Ó','&#212;':'Ó','&#213;':'Õ','&#217;':'Ù','&#218;':'Ú','&#224;':'à','&#225;':'á','&#226;':'â','&#227;':'ã','&#231;':'ç','&#232;':'è','&#233;':'é','&#234;':'ê','&#237;':'í','&#243;':'ó','&#244;':'ô','&#245;':'õ','&#249;':'ù','&#250;':'ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

#trailer,sn
def trailer(name, url):
    print name,url
    url = trailer2().run2(name, url)
    if url == None: return
    item = xbmcgui.ListItem(path=url)
    item.setProperty("IsPlayable", "true")
    xbmc.Player().play(url, item)

class trailer2:
    def __init__(self):
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_query = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def run2(self, name, url):
        try:
            if url.startswith(self.youtube_base):
                url = self.youtube(url)
                if url == None: raise Exception()
                return url
            elif not url.startswith('http://'):
                url = self.youtube_watch % url
                url = self.youtube(url)
                if url == None: raise Exception()
                return url
            else:
                raise Exception()
        except:
            url = self.youtube_query + name + ' trailer'
            url = self.youtube_search(url)
            if url == None: return
            return url

    def youtube_search(self, url):
        try:
            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url= url.split('[/B]')[0].replace('[B]','')
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url, timeout='10').result
            result = parseDOM(result, "entry")
            result = parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]	
                url = self.youtube_watch % url
                url = self.youtube(url)
                if not url == None: return url
        except: return

    def youtube(self, url):
        print '#youtube'
        try:
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(self.youtube_info % id, timeout='10').result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(self.youtube_watch % id, timeout='10').result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return


def config_lola(self):  #Open addon settings
    plugintools.open_settings_dialog()
    

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='5'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result        


def parseDOM(html, name=u"", attrs={}, ret=False):
    if isinstance(name, str): # Should be handled
        try:  name = name #.decode("utf-8")
        except: pass

    if isinstance(html, str):
        try: html = [html.decode("utf-8")] # Replace with chardet thingy
        except: html = [html]
    elif isinstance(html, unicode): html = [html]
    elif not isinstance(html, list): return u""

    if not name.strip(): return u""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item: item = item.replace(match, match.replace("\n", " "))

        lst = _getDOMElements(item, name, attrs)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                lst2 += _getDOMAttributes(match, name, ret)
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                temp = _getDOMContent(item, name, match, ret).strip()
                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    return ret_lst

def _getDOMContent(html, name, match, ret):  # Cleanup

    endstr = u"</" + name  # + ">"

    start = html.find(match)
    end = html.find(endstr, start)
    pos = html.find("<" + name, start + 1 )

    while pos < end and pos != -1:  # Ignore too early </endstr> return
        tend = html.find(endstr, end + len(endstr))
        if tend != -1:
            end = tend
        pos = html.find("<" + name, pos + 1)

    if start == -1 and end == -1:
        result = u""
    elif start > -1 and end > -1:
        result = html[start + len(match):end]
    elif end > -1:
        result = html[:end]
    elif start > -1:
        result = html[start + len(match):]

    if ret:
        endstr = html[end:html.find(">", html.find(endstr)) + 1]
        result = match + result + endstr

    return result

def _getDOMAttributes(match, name, ret):
    lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
    if len(lst) == 0:
        lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
    ret = []
    for tmp in lst:
        cont_char = tmp[0]
        if cont_char in "'\"":

            # Limit down to next variable.
            if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

            # Limit to the last quotation mark
            if tmp.rfind(cont_char, 1) > -1:
                tmp = tmp[1:tmp.rfind(cont_char)]
        else:
            if tmp.find(" ") > 0:
                tmp = tmp[:tmp.find(" ")]
            elif tmp.find("/") > 0:
                tmp = tmp[:tmp.find("/")]
            elif tmp.find(">") > 0:
                tmp = tmp[:tmp.find(">")]

        ret.append(tmp.strip())

    return ret

def _getDOMElements(item, name, attrs):
    lst = []
    for key in attrs:
        lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
        if len(lst2) == 0 and attrs[key].find(" ") == -1:  # Try matching without quotation marks
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

        if len(lst) == 0:
            lst = lst2
            lst2 = []
        else:
            test = range(len(lst))
            test.reverse()
            for i in test:  # Delete anything missing from the next list.
                if not lst[i] in lst2:
                    del(lst[i])

    if len(lst) == 0 and attrs == {}:
        lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
        if len(lst) == 0:
            lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

    return lst


def lb_regex(params):
    plugintools.log('[%s %s] ---> Launching Lolabits regex... %s<--- ' % (addonName, addonVersion,repr(params)))

    fanart = 'https://lh3.googleusercontent.com/-UhgrYZCeNSY/Ul1dAlICQYI/AAAAAAAABe8/cXXLKfWG3Fc/s928-fcrop64=1,00310000ffcdffa6/lolabits_google_profileimage_1.jpg'    
    sitename='Lolabits.es'
    host='lolabits.es'
    sitebase = 'http://lolabits.es/'
    name=params.get("title")
    multiparser = 0
    fileid = ''
    
    vidname=params.get("title").replace("[B]", "").replace("[/B]", "").replace("[I]", "").replace("[/I]", "").replace("[Multiparser]", "").replace("[COLOR lightyellow]", "").replace("[COLOR white]", "").replace("[/COLOR]", "").strip()
    url = params.get("url");url_fixed=url.replace("(video)", "");print 'url_fixed',url_fixed

    # Comprobamos extensión del archivo y la ID del vídeo
    if url_fixed.endswith("mkv") == True:
        fname=vidname+'.mkv'
        url_fixed = url_fixed.replace(".mkv", "")
        fileid=url_fixed.split(",")
        fileid=fileid[1];print 'fileid',fileid
    if url_fixed.endswith("mp4") == True:
        fname=vidname+'.mp4'
        url_fixed = url_fixed.replace(".mp4", "")
        fileid=url_fixed.split(",")
        fileid=fileid[1];print 'fileid',fileid
    if url_fixed.endswith("avi") == True:
        fname=vidname+'.avi'
        url_fixed = url_fixed.replace(".avi", "")
        fileid=url_fixed.split(",")
        fileid=fileid[1];print 'fileid',fileid    
    if url_fixed.endswith("mov") == True:
        fname=vidname+'.mov'
        url_fixed = url_fixed.replace(".mov", "")
        fileid=url_fixed.split(",")
        fileid=fileid[1];print 'fileid',fileid     
    if url_fixed.endswith("mpg") == True:
        fname=vidname+'.mpg'
        url_fixed = url_fixed.replace(".mpg", "")
        fileid=url_fixed.split(",")
        fileid=fileid[1];print 'fileid',fileid 
        
    if url.startswith("multiparser"):
        url = url.replace("multiparser", "").strip()
        multiparser = 1
    progreso = xbmcgui.DialogProgressBG()
    progreso.create(sitename, 'Accediendo a Lolabits...')
    
    if login_lolabits():
        progreso.update(50, sitename, 'Negociando enlace... ')
        conteudo=abrir_url_cookie(url,erro=False)
        print conteudo
        
        # Error en datos de la cuenta
        if re.search('Pode acontecer que a mensagem de confirma',conteudo):
            mensagemprogresso.close()
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Por favor, revisa la configuración de Lolabits", 2 , art_lola+'icon.png'))
            return
    else:        
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Error al iniciar sesión en Lolabits ", 2 , art_lola+'icon.png'))
        sys.exit(0)

    # Error en contraseña de carpeta
    if re.search('ProtectedFolderChomikLogin',conteudo):
        #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Error en contraseña de carpeta ", 2 , art_lola+'icon.png'))    
        plugintools.log("Carpeta protegida. Enviamos contraseña para: " + url)
        chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
        passwordfolder=caixadetexto('password');print 'passwordfolder',passwordfolder
        form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
        ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'http://' + host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
        endlogin=sitebase + 'action/Files/LoginToFolder'
        teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        teste=urllib.unquote(teste)
        print 'teste',teste
        if re.search('IsSuccess":false',teste):
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Contraseña incorrecta", 3 , art_lola+'icon.png'))
            sys.exit(0)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Lolabits @ Movie Ultra 7K', "Contraseña correcta", 3 , art_lola+'icon.png'))
            
    try:
        #try: fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"/>').findall(conteudo)[0];print 'fileid',fileid
        print 'fileID',fileid
        token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0];print 'token',token
        form_d = {'fileId':fileid,'__RequestVerificationToken':token}
        ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://' + host, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://'+host+'/','User-Agent':user_agent}
        endlogin=sitebase + 'action/License/Download'
        final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
        final=final.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','');print 'final-1',final
    except: pass    
    try:
        if re.search('action/License/acceptLargeTransfer',final):
            try: fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"').findall(final)[0]
            except: fileid = params.get("page")
            orgfile=re.compile('<input type="hidden" name="orgFile" value="(.+?)"').findall(final)[0]
            userselection=re.compile('<input type="hidden" name="userSelection" value="(.+?)"').findall(final)[0]
            form_d = {'fileId':fileid,'orgFile':orgfile,'userSelection':userselection,'__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://' + sitebase, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://'+sitebase+'/','User-Agent':user_agent}
            endlogin=sitebase + 'action/License/acceptLargeTransfer'
            final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore');print 'final-2',final
    except: pass
    try:
        if re.search('causar problemas com o uso de aceleradores de download',final):linkfinal=re.compile('a href=\"(.+?)\"').findall(final)[0]
        else: linkfinal=re.compile('"redirectUrl":"(.+?)"').findall(final)[0];print 'linkfinal1',linkfinal
        #comecarvideo(name,linkfinal,playterm=playterm)
    except: pass
        
    url_final=plugintools.find_single_match(final, '<a href="([^"]+)')
    if url_final == "":
        url_final=plugintools.find_single_match(final, 'redirectUrl":"([^"]+)')
    print 'url_final',url_final
        
    if multiparser == 1:
        datamovie = {}
        # Info película
        infopeli=plugintools.find_single_match(conteudo, '<div class="fileInfo"(.*?)</div>')
        fdls=plugintools.find_single_match(infopeli, '<p class="downloadsCounter">(.*?)</p>')
        length=plugintools.find_single_match(infopeli, 'class="bold">(.*?)</span>')
        fsize=plugintools.find_single_match(infopeli, '<div class="fileSize">(.*?)</p>')
        #sinopsis=params.get("title").replace(" [COLOR lightyellow][Multiparser][/COLOR]","").replace("[COLOR white]", "").strip();print sinopsis
        if fsize == "":
            sinopsis = params.get("title")+"\n"+'[CR][COLOR white]Archivo protegido con contraseña[/COLOR]'
        else:
            sinopsis = params.get("title")+"\n"+'[COLOR white]Tamaño: '+fsize+' '+'Duración: '+length+' Descargas: '+fdls+'[/COLOR]'
        datamovie["Plot"]=sinopsis
        plugintools.add_item(action="lolaplay", title='Reproducir...', url=url_final, thumbnail=params.get("thumbnail"), info_labels=datamovie, fanart=fanart , folder=False, isPlayable=True)
        plugintools.add_item(action="loladownload", title='Descargar...', url=url_final, thumbnail=params.get("thumbnail"), info_labels=datamovie, fanart=fanart , extra=fname, folder=False, isPlayable=False)
        
    else: plugintools.play_resolved_url(url_final)


def lolaplay(params):
    url=params.get("url")
    plugintools.play_resolved_url(url)

def loladownload(params):
    vidname=params.get("title").replace("[B]", "").replace("[/B]", "").replace("[I]", "").replace("[/I]", "").replace("[Multiparser]", "").replace("[COLOR lightyellow]", "").replace("[COLOR white]", "").replace("[/COLOR]", "").strip()
    url=params.get("url")
    params=plugintools.get_params();print params
    filename=params.get("extra");print 'filename',filename

    dialog = xbmcgui.Dialog()
    downloadPath = dialog.browse(int(3), 'Descargar carpeta','myprograms')
    if os.path.exists(downloadPath):
        mypath=os.path.join(downloadPath,vidname)
        if os.path.isfile(mypath) is True:
            ok = mensagemok('Movie Ultra 7K','Este archivo ya existe en el disco','','')
            return False
        else:              
            try:
                  dp = xbmcgui.DialogProgress()
                  msgdp='Iniciando descarga de '+filename
                  dp.create(filename, '', msgdp)
                  start_time = time.time()
                  try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
                  except:
                        while os.path.exists(mypath): 
                              try: os.remove(mypath); break 
                              except: pass 
                        if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): return False 
                        else: raise 
                        return False
                  return True
            except: ok=mensagemok('Lolabits.es','Descarga fallida'); print 'download failed'; return False 
    
