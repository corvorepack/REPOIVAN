# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movie Ultra 7K Updater v0.2 (21.10.2014)
# Version 0.3.0 (18.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import time
import datetime
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools

from dateutil.parser import parse

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


home = xbmcaddon.Addon().getAddonInfo('path')+'/'
playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))
art = xbmc.translatePath(os.path.join(addonPath,'art/'))


# Comprobamos qué versión es la más reciente
def check_update(params):
    plugintools.log("[movie.ultra.7k-0.3.0].check_update "+repr(params))

    data = plugintools.read( params.get("url") )
    datamovie = {}
    #plugintools.log("data= "+data)
    title = params.get("title")
    name_channel = parser_title(title)
    # name_channel = parser_title(name_channel)
    data_update = plugintools.find_single_match(data, '<name>'+name_channel+'(.*?)</channel>')
    subchannel = plugintools.find_multiple_matches(data_update, '<subchannel>(.*?)</subchannel>')
    datamovie["Plot"]='Módulo de actualizaciones para [B]Movie Ultra 7K[/B]'
    plugintools.add_item(action = "", title = '[COLOR gold]Updater Movie Ultra 7K[/COLOR]', url = "" , info_labels=datamovie, thumbnail = params.get("thumbnail") , fanart = params.get("fanart") , folder = False , isPlayable = False)    
    i = 0
    for entry in subchannel:
        plugintools.log("entry= "+entry)        
        title = plugintools.find_single_match(entry, '<name>(.*?)</name>')
        url = plugintools.find_single_match(entry, '<url>([^<]+)</url>')
        thumbnail = plugintools.find_single_match(entry, '<thumbnail>([^<]+)</thumbnail>')
        version = plugintools.find_single_match(entry, '<version>([^<]+)</version>')
        author = plugintools.find_single_match(entry, '<author>([^<]+)</author>')
        size_remote = plugintools.find_single_match(entry, '<filesize>([^<]+)</filesize>')
        ts_remote = plugintools.find_single_match(entry, '<update>([^<]+)</update>')
        path = plugintools.find_single_match(entry, '<path>([^<]+)</path>')
        fanart = plugintools.find_single_match(entry, '<fanart>([^<]+)')
        datamovie["Plot"] = '[COLOR white]'+plugintools.find_single_match(entry, '<changelog>(.*?)</changelog>')+'[/COLOR]'
        f = open(home+path, 'r')
        f.seek(0,2)
        size_local = f.tell()
        size_local = str(size_local)
        last_modified = time.ctime(os.path.getmtime(home+path))
        print 'last_modified',str(last_modified)  # Última modificación del archivo
        print 'ts_remote',ts_remote
        dt = parse(last_modified)
        ts_local = time.mktime(dt.timetuple())
        ts = parse(ts_remote)
        ts_remote = time.mktime(ts.timetuple())
        print 'ts_local',ts_local  # Última modificación del archivo local
        print 'ts_remote',ts_remote  # Última modificación del archivo remoto
        if int(ts_remote) <= int(ts_local) :
            plugintools.log("[%s %s] No es necesario actualizar el módulo= %s " % (addonName, addonVersion, path))
        else:
            # Hay que actualizar, así que mostramos la entrada
            plugintools.addShow(action = "update_file", title = '[COLOR white]'+title+'[/COLOR][COLOR lightblue][I] [' + author + '][/I][/COLOR][COLOR lightgreen][I] [' + version + '][/I][/COLOR]', url = url , info_labels=datamovie, thumbnail = thumbnail , extra = home+path , fanart = fanart , folder = False , isPlayable = False)
            i = i + 1
                
    if i == 0:
        datamovie["Plot"]='¡Felicidades! Tu copia de [B]Movie Ultra 7K[/B] tiene todos los módulos actualizados ;)[CR][CR][COLOR red]NOTA:[/COLOR] Bugs o sugerencias a [B]juarrox@gmail.com[/B]'
        plugintools.addShow(action = "", title = '[COLOR white]No hay actualizaciones pendientes[/COLOR]', url = "" , info_labels=datamovie, thumbnail = 'http://www.clker.com/cliparts/U/b/3/E/T/z/ok-icon-hi.png' , fanart = params.get("fanart") , folder = False , isPlayable = False)
        

def update_file(params):
    plugintools.log("[movie.ultra.7k-0.3.0].Update_now "+repr(params))

    nobackup = 0
    title = params.get("title").replace("[COLOR white]", "").split("[")[0]
    runUpdate = xbmcgui.Dialog().yesno('Movie Ultra 7K', '¿Desea actualizar el módulo [B]'+title+'[/B]?')
    
    if(runUpdate):
        local_file = params.get("extra")
        local_filename = local_file.split("/")[-1]
        remote_file = params.get("url")
        runBackup = xbmcgui.Dialog().yesno('Movie Ultra 7K', '¿Desea crear una copia de seguridad de [B]'+title+'[/B]?')
        if(runBackup):
            plugintools.log("Iniciando backup del módulo local...") 
            backup = local_filename.split(".py")[0];backup=backup+'-BAK.py'
            local_filebak = local_file.replace(local_filename, backup)
            try:
                shutil.copyfile(local_file, local_filebak)
            except:
                nobackup = -1
                pass
                    
    if(runUpdate):
        if nobackup == -1:
            runUpdateWithBackup = xbmcgui.Dialog().yesno('Movie Ultra 7K', 'Error al crear [B]'+backup+'[/B]', '¿Desea continuar con la actualización?')
        if nobackup != -1 or runUpdateWithBackup:            
            progreso = xbmcgui.DialogProgressBG()
            progreso.create("Iniciando actualización... " , local_filename )
            yesno = 0
            plugintools.log("remote= "+remote_file)        
            r = urllib2.urlopen(remote_file)
            f = open(temp + local_filename, "wb")
            f.write(r.read())
            f.close()
            
            try:
                progreso.update(50, "Copiando archivo... " , local_filename)
                shutil.copyfile(temp + local_filename, local_file)        
                progreso.update(100, "Actualización completada! " , local_filename)
                progreso.close()
            except:
                progreso.update(0, "Error al sobreescribir! " , local_filename)
                pass       
                
            try:
                os.remove(temp + local_filename)
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Actualización completada!", 3 , art+'icon.png'))
            except:
                pass
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Actualización cancelada!", 3 , art+'icon.png'))

    xbmc.executebuiltin("Container.Refresh")


def update_palco(params):
    plugintools.log("[movie.ultra.7k-0.3.0].update_palco "+repr(params))
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Espere...", 3 , art+'icon.png'))

    local_filename = params.get("extra")
    remote_filename = params.get("url")
    plugintools.log("local= "+local_file)
    plugintools.log("remote= "+remote_file)
    #try:
    r = urllib2.urlopen(remote_file)
    f = open(temp + local_file, "wb")
    f.write(r.read())
    f.close()
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Actualización completada", 3 , art+'icon.png'))
 
    '''
    except IOError:
        pass
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Error en la descarga", 3 , art+'icon.png'))
    '''

    unzipper = ziptools()
    unzipper.extract(temp + local_file, remote_file, params)
    
    '''except IOError:
        pass
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Movie Ultra 7K', "Actualización fallida", 3 , art+'icon.png'))
        '''
    os.remove(temp + local_file)
    




class ziptools:

    def extract(self, file, dir, params):
        plugintools.log("file=%s" % file)
        #dir = addons
        
        if not dir.endswith(':') and not os.path.exists(dir):
            os.mkdir(dir)

        zf = zipfile.ZipFile(file)
        self._createstructure(file, dir)
        num_files = len(zf.namelist())

        for name in zf.namelist():
            plugintools.log("name=%s" % name)
            if not name.endswith('/'):
                plugintools.log("no es un directorio")
                plugintools.log("dst_folder= "+dir)                                
                try:
                    (path,file) = os.path.split(os.path.join(dir, name))
                    plugintools.log("path=%s" % path)
                    plugintools.log("name=%s" % name)
                    os.makedirs( path )
                except:
                    pass
                outfilename = os.path.join(dir, name)
                plugintools.log("outfilename=%s" % outfilename)
                try:
                    outfile = open(outfilename, 'wb')
                    outfile.write(zf.read(name))
                except:
                    plugintools.log("Error en fichero "+name)

    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)

    def create_necessary_paths(filename):
        try:
            (path,name) = os.path.split(filename)
            os.makedirs( path)
        except:
            pass

    def _makedirs(self, directories, basedir):
        for dir in directories:
            curdir = os.path.join(addons, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs(self, file):
        zf = zipfile.ZipFile(file)
        dirs = []
        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)

        dirs.sort()
        return dirs
    
 

      
def parser_title(title):
    plugintools.log("[movie.ultra.7k-0.3.0].parser_title " + title)

    cyd = title

    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR green]", "")
    cyd = cyd.replace("[COLOR red]", "")
    cyd = cyd.replace("[COLOR blue]", "")    
    cyd = cyd.replace("[COLOR royalblue]", "")
    cyd = cyd.replace("[COLOR white]", "")
    cyd = cyd.replace("[COLOR pink]", "")
    cyd = cyd.replace("[COLOR cyan]", "")
    cyd = cyd.replace("[COLOR steelblue]", "")
    cyd = cyd.replace("[COLOR forestgreen]", "")
    cyd = cyd.replace("[COLOR olive]", "")
    cyd = cyd.replace("[COLOR khaki]", "")
    cyd = cyd.replace("[COLOR lightsalmon]", "")
    cyd = cyd.replace("[COLOR orange]", "")
    cyd = cyd.replace("[COLOR lightgreen]", "")
    cyd = cyd.replace("[COLOR lightblue]", "")
    cyd = cyd.replace("[COLOR lightpink]", "")
    cyd = cyd.replace("[COLOR skyblue]", "")
    cyd = cyd.replace("[COLOR darkorange]", "")    
    cyd = cyd.replace("[COLOR greenyellow]", "")
    cyd = cyd.replace("[COLOR yellow]", "")
    cyd = cyd.replace("[COLOR yellowgreen]", "")
    cyd = cyd.replace("[COLOR orangered]", "")
    cyd = cyd.replace("[COLOR grey]", "")
    cyd = cyd.replace("[COLOR gold]", "")
    cyd = cyd.replace("[COLOR=FF00FF00]", "")  
                
    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")

    title = cyd
    title = title.strip()
    plugintools.log("title_parsed= "+title)
    return title

