# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de PlayLists de CopiaPop, Diskokosmiko, Youtube y DailyMotion by DarioMO
# Version 0.0.1 (12.10.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
# Gracias a las librerías resolvers y media_analyzer de JuarroX (Grupo PalcoTV http://arena.pe.hu/forums/index.php y http://palcotv.blogspot.com.es/)
# Gracias a los Regex de KabCasa

import os
import xbmcplugin
import xbmc, xbmcgui
import urllib

import sys
import urllib
import urllib2
import re

import xbmcaddon

import plugintools
import requests

from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


buscar=""
link_kosmipop = "plugin://plugin.video.live.streamspro/?url=%24doregex%5Burl%5D%7Cuser-agent%3DMozilla%2F5.0+%28Windows+NT+6.1%3B+rv%3A14.0%29+Gecko%2F20100101+Firefox%2F14.0.1&mode=17&regexs=%7Bu%27url%27%3A%20%7B%27cookiejar%27%3A%20%27%27%2C%20%27name%27%3A%20u%27url%27%2C%20%27expres%27%3A%20u%27Url%22%3A%22%28.%2A%3F%29%22%27%2C%20%27referer%27%3A%20u%27MI_REF/%27%2C%20%27page%27%3A%20u%27MI_REF/action/DownloadFile%3Flocation%3Dfi%26f%3D%24doregex%5Bid%5D%27%2C%20%27rawpost%27%3A%20u%27fileId%3D%24doregex%5Bid%5D%26__RequestVerificationToken%3D%24doregex%5Btok%5D%27%7D%2C%20u%27tok%27%3A%20%7B%27expres%27%3A%20u%27Token.%2A%3Fvalue%3D%22%28.%2A%3F%29%22%27%2C%20%27referer%27%3A%20u%27MI_REF/%27%2C%20%27name%27%3A%20u%27tok%27%2C%20%27page%27%3A%20u%27MI_URL%27%7D%2C%20u%27id%27%3A%20%7B%27expres%27%3A%20u%27fileId%3D%28.%2A%3F%29%22%27%2C%20%27referer%27%3A%20u%27MI_REF/%27%2C%20%27name%27%3A%20u%27id%27%2C%20%27page%27%3A%20u%27MI_URL%27%7D%7D"
link_daily = "plugin://plugin.video.live.streamspro/?url=%24doregex%5Bfinal-url%5D&mode=17&regexs=%7Bu%27url%27%3A%20%7B%27expres%27%3A%20u%22%24pyFunction%3A%27%24doregex%5Bget-url%5D%27.replace%28%27%5C%5C/%27%2C%27/%27%29%22%2C%20%27name%27%3A%20u%27url%27%2C%20%27page%27%3A%20None%7D%2C%20u%27final-url%27%3A%20%7B%27expres%27%3A%20u%27%28.%2A%29%23%27%2C%20%27name%27%3A%20u%27final-url%27%2C%20%27page%27%3A%20u%27%24doregex%5Burl%5D%26redirect%3D0%27%7D%2C%20u%27get-url%27%3A%20%7B%27expres%27%3A%20u%27mpegURL.%2A%22%28http.%2Aauth.%2A%3F%29%22%27%2C%20%27referer%27%3A%20u%27MI_REF%27%2C%20%27name%27%3A%20u%27get-url%27%2C%20%27page%27%3A%20u%27MI_URL%27%7D%7D"

mis_listas = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.palcotv/listmaker.xml'))
parser = "     [COLOR blue][B]ListMaker v0.0.1      [COLOR red]····[COLOR yellow]by DarioMO[COLOR red]····[/B][I][COLOR skyblue]   (Dedicado al rey de las Listas: [COLOR blue]Sebas[COLOR skyblue])[/I][/COLOR]"
logo="http://i.imgur.com/4rkycMX.png"
fondo = "http://i.imgur.com/V5vTrFR.png"

def listmaker0(params):

	if not os.path.exists(mis_listas):
		file_listas=open(mis_listas, "w+")
		file_listas.close()

	plugintools.add_item(action="",url="",title=parser,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

	plugintools.add_item(action="todas_mis_listas",url="",title="- [COLOR blue][B]Mis Listas[/COLOR][/B]",thumbnail="http://i.imgur.com/fn1GrXU.png", fanart="http://4.bp.blogspot.com/-JdFkDlR_Ho4/UE3f5XZegQI/AAAAAAAAAVE/vHVZZgm7xyk/s1600/Collage+movies.jpg", folder=True, isPlayable=False)
	plugintools.add_item(action="agrega_lista",url="",title="[COLOR white]- Agregar Lista[/COLOR]",thumbnail="http://imgur.com/puMgxxm.png", fanart="http://4.bp.blogspot.com/-JdFkDlR_Ho4/UE3f5XZegQI/AAAAAAAAAVE/vHVZZgm7xyk/s1600/Collage+movies.jpg", folder=True, isPlayable=False)
	plugintools.add_item(action="modif_lista",url="",title="[COLOR white]- Modificar Lista[/COLOR]",thumbnail="http://imgur.com/dNp0f86.png", fanart="http://4.bp.blogspot.com/-JdFkDlR_Ho4/UE3f5XZegQI/AAAAAAAAAVE/vHVZZgm7xyk/s1600/Collage+movies.jpg", folder=True, isPlayable=False)
	plugintools.add_item(action="borra_lista",url="",title="[COLOR white]- Eliminar Lista[/COLOR]",thumbnail="http://imgur.com/OQdg4mI.png", fanart="http://4.bp.blogspot.com/-JdFkDlR_Ho4/UE3f5XZegQI/AAAAAAAAAVE/vHVZZgm7xyk/s1600/Collage+movies.jpg", folder=True, isPlayable=False)
	

	
def todas_mis_listas(params):

	parser2 = parser.replace("(Dedicado al rey de las Listas: [COLOR blue]Sebas[COLOR skyblue])" , "*** Mis Listas ***")

	file_listas=open(mis_listas, "r")
	mis_lists = file_listas.read()
	file_listas.close()

	plugintools.add_item(action="",url="",title=parser2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

	
	cada_lista = plugintools.find_multiple_matches(mis_lists,'<Lista>(.*?)<Fin Lista>')
	
	for item in cada_lista:
		nombre = plugintools.find_single_match(item,'<Nombre>(.*?)<<')
		url = plugintools.find_single_match(item,'<Url>(.*?)<<')
		logo1 = plugintools.find_single_match(item,'<Logo>(.*?)<<')
		fondo1 = plugintools.find_single_match(item,'<Fondo>(.*?)<<')

		plugintools.add_item(action="kosmipop_linker",url=url,title="[COLOR white]- "+nombre.title()+"[/COLOR]",thumbnail=logo1, fanart=fondo1, folder=True, isPlayable=False)

		

		
def agrega_lista(params):

	parser2 = parser.replace("(Dedicado al rey de las Listas: [COLOR blue]Sebas[COLOR skyblue])" , "*** Agregar Lista ***")

	#plugintools.add_item(action="",url="",title=parser2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
	
	titulo = plugintools.keyboard_input('', 'Introduzca [COLOR red]Nombre[/COLOR] de la Lista')
	url = plugintools.keyboard_input('', 'Introduzca [COLOR red]URL[/COLOR] de la Lista')
	logo1 = plugintools.keyboard_input('', 'Introduzca [COLOR red]Url del Logo[/COLOR] de la Lista')
	fondo1 = plugintools.keyboard_input('', 'Introduzca [COLOR red]Url del Fondo[/COLOR] de la Lista')

	file_listas=open(mis_listas, "a+")
	file_listas.write("<Lista>\n")
	file_listas.write("<Nombre>"+titulo+"<<\n")
	file_listas.write("<Url>"+url+"<<\n")
	file_listas.write("<Logo>"+logo1+"<<\n")
	file_listas.write("<Fondo>"+fondo1+"<<\n")
	file_listas.write("<Fin Lista>\n")

	file_listas.close()
	
	return
	



def modif_lista(params):

	parser2 = parser.replace("(Dedicado al rey de las Listas: [COLOR blue]Sebas[COLOR skyblue])" , "*** Modificar Lista ***")

	file_listas=open(mis_listas, "r")
	mis_lists = file_listas.read()
	file_listas.close()

	plugintools.add_item(action="",url="",title=parser2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

	
	cada_lista = plugintools.find_multiple_matches(mis_lists,'<Lista>(.*?)<Fin Lista>')
	
	for item in cada_lista:
		nombre = plugintools.find_single_match(item,'<Nombre>(.*?)<<')
		url = plugintools.find_single_match(item,'<Url>(.*?)<<')
		logo1 = plugintools.find_single_match(item,'<Logo>(.*?)<<')
		fondo1 = plugintools.find_single_match(item,'<Fondo>(.*?)<<')

		plugintools.add_item(action="modif_lista2",url=url,title="[COLOR white]- "+nombre.title()+"[/COLOR]",thumbnail=logo1, fanart=fondo1, folder=True, isPlayable=False)

		

	
def modif_lista2(params):
	url1 = params.get("url")
	nombre1 = params.get("title").replace("- " , "")
	logo1 = params.get("thumbnail")
	fondo1 = params.get("fanart")

	parser2 = parser.replace("(Dedicado al rey de las Listas: [COLOR blue]Sebas[COLOR skyblue])" , "*** Modificar Lista ***")

	file_listas=open(mis_listas, "r")
	mis_lists = file_listas.read()
	file_listas.close()

	plugintools.add_item(action="",url="",title=parser2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

	
	cada_lista = plugintools.find_multiple_matches(mis_lists,'<Lista>(.*?)<Fin Lista>')
	i = 0
	for item in cada_lista:
		nombre0 = plugintools.find_single_match(item,'<Nombre>(.*?)<<').title()
		url0 = plugintools.find_single_match(item,'<Url>(.*?)<<')
		logo0 = plugintools.find_single_match(item,'<Logo>(.*?)<<')
		fondo0 = plugintools.find_single_match(item,'<Fondo>(.*?)<<')
		
		if nombre0 == nombre1 and url0 == url1 and logo0 == logo1 and fondo0 == fondo1:

			nombre1 = plugintools.keyboard_input('', 'Introduzca [COLOR red]Nombre[/COLOR] de la Lista')
			url1 = plugintools.keyboard_input('', 'Introduzca [COLOR red]URL[/COLOR] de la Lista')
			logo1 = plugintools.keyboard_input('', 'Introduzca [COLOR red]Url del Logo[/COLOR] de la Lista')
			fondo1 = plugintools.keyboard_input('', 'Introduzca [COLOR red]Url del Fondo[/COLOR] de la Lista')
			
			cada_lista[i] = cada_lista[i].replace(nombre0 , nombre1)
			cada_lista[i] = cada_lista[i].replace(url0 , url1)
			cada_lista[i] = cada_lista[i].replace(logo0 , logo1)
			cada_lista[i] = cada_lista[i].replace(fondo0 , fondo1)
			
			break
			
		else:
			i = i + 1

	file_listas=open(mis_listas, "w+")
	for item in cada_lista:
		escribe = "<Lista>" + item + "<Fin Lista>\n"
		file_listas.write(escribe)

	file_listas.close()
	
	xbmcgui.Dialog().ok( "¡¡ATENCIÓN!!" , "La Modificación se ha Guardado Correctamente." )
	
	return
			





def borra_lista(params):

	parser2 = parser.replace("(Dedicado al rey de las Listas: [COLOR blue]Sebas[COLOR skyblue])" , "*** Borrar Lista ***")

	file_listas=open(mis_listas, "r")
	mis_lists = file_listas.read()
	file_listas.close()

	plugintools.add_item(action="",url="",title=parser2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

	
	cada_lista = plugintools.find_multiple_matches(mis_lists,'<Lista>(.*?)<Fin Lista>')
	
	for item in cada_lista:
		nombre = plugintools.find_single_match(item,'<Nombre>(.*?)<<')
		url = plugintools.find_single_match(item,'<Url>(.*?)<<')
		logo1 = plugintools.find_single_match(item,'<Logo>(.*?)<<')
		fondo1 = plugintools.find_single_match(item,'<Fondo>(.*?)<<')

		plugintools.add_item(action="borra_lista2",url=url,title="[COLOR white]- "+nombre.title()+"[/COLOR]",thumbnail=logo1, fanart=fondo1, folder=True, isPlayable=False)

		

	
def borra_lista2(params):
	url1 = params.get("url")
	nombre1 = params.get("title").replace("- " , "")
	logo1 = params.get("thumbnail")
	fondo1 = params.get("fanart")

	parser2 = parser.replace("(Dedicado al rey de las Listas: [COLOR blue]Sebas[COLOR skyblue])" , "*** Borrar Lista ***")

	file_listas=open(mis_listas, "r")
	mis_lists = file_listas.read()
	file_listas.close()

	plugintools.add_item(action="",url="",title=parser2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

	
	cada_lista = plugintools.find_multiple_matches(mis_lists,'<Lista>(.*?)<Fin Lista>')
	i = 0
	eliminar = False
	for item in cada_lista:
		nombre0 = plugintools.find_single_match(item,'<Nombre>(.*?)<<').title()
		url0 = plugintools.find_single_match(item,'<Url>(.*?)<<')
		logo0 = plugintools.find_single_match(item,'<Logo>(.*?)<<')
		fondo0 = plugintools.find_single_match(item,'<Fondo>(.*?)<<')
		
		if nombre0 == nombre1 and url0 == url1 and logo0 == logo1 and fondo0 == fondo1:

			eliminar = xbmcgui.Dialog().yesno("¡¡Atención!!", "Se va a eliminar la lista [COLOR red]"+nombre0+"[/COLOR]" , "       ¿Confirma el Borrado?" )
			if eliminar:
				del(cada_lista[i])
			
			break
			
		else:
			i = i + 1

	if eliminar:
		file_listas=open(mis_listas, "w+")
		for item in cada_lista:
			escribe = "<Lista>" + item + "<Fin Lista>\n"
			file_listas.write(escribe)

		file_listas.close()
		
		xbmcgui.Dialog().ok( "¡¡ATENCIÓN!!" , "La Modificación se ha Guardado Correctamente." )
	
	return
			









	


def kosmipop_linker(params):
	lista = params.get("url")

	r=requests.get(lista)
	data = r.content

	titu_lista = plugintools.find_single_match(data,'titu_lista=(.*?)</Line>')
	logo_lista = plugintools.find_single_match(data,'logo_lista=(.*?)</Line>')
	autor = plugintools.find_single_match(data,'autor=(.*?)</Line>')
	fondo_lista = plugintools.find_single_match(data,'fondo_lista=(.*?)</Line>')
	thumbnail=logo_lista
	fanart=fondo_lista

	plugintools.add_item(action="",url="",title="[COLOR skyblue][B]       "+titu_lista+"[/B]     [I][COLOR yellow]    **** "+autor+" ****[/I][/COLOR]",thumbnail=logo_lista,fanart=fondo_lista,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=logo_lista, fanart=fondo_lista, folder=False, isPlayable=False)

	if "<Coment" in data:
		comentarios = plugintools.find_multiple_matches(data,'<Coment(.*?)/Coment>')
		for item in comentarios:
			comentario = plugintools.find_single_match(item,'>(.*?)<').strip().title()
			if len(comentario) > 0:
				plugintools.add_item(action="",url="",title="[COLOR yellow]"+comentario+"[/COLOR]",thumbnail=logo_lista, fanart=fondo_lista, folder=False, isPlayable=False)
		
	
	listas = plugintools.find_multiple_matches(data,'<Line>(.*?)</Line>')
	
	#Las ordeno y pongo identificativo de cambio de letra
	#para que no exista desorden entre mayusculas y minusculas... pongo titulo en formato Title()
	listas_orden=[]
	for item in listas:
		titu = plugintools.find_single_match(item,'titu=(.*?)url=').strip()
		if len(titu) <> 0:
			listas_orden.append(item.replace(titu, titu.title()))
		
	listas_orden.sort()
	
	letra = ""
	HaySinopsis = False
	for item in listas_orden:
		titu = plugintools.find_single_match(item,'titu=(.*?)url=').strip()
		url = plugintools.find_single_match(item,'url=(.*?)logo=').strip()
		logo = plugintools.find_single_match(item,'logo=(.*?)fondo=').strip()
		fondo = plugintools.find_single_match(item,'fondo=(.*?)sinop=').strip()
		sinop = plugintools.find_single_match(item,'sinop=(.*)').strip()

		if len(logo) == 0:
			logo = thumbnail
		if len(fondo) == 0:
			fondo = fanart
		if len(sinop) <> 0:
			HaySinopsis = True
		
		if titu[:1] <> letra:
			letra = titu[:1]
			
			plugintools.add_item(action="",url=url,title="[COLOR blue][I]**"+letra+"**[/I][/COLOR]",thumbnail=logo_lista, fanart=fondo_lista, extra=sinop, folder=False, isPlayable=False)
			
		datamovie = {}
		datamovie["Plot"]=sinop

		if url.startswith("http://copiapop.com/") == True:
			accion = "abrekosmipop_lista"
			titu = titu + "  [COLOR skyblue][I][CopiaPop][/I]"
		elif url.startswith("http://diskokosmiko.mx/") == True:
			accion = "abrekosmipop_lista"
			titu = titu + "  [COLOR yellow][I][DiskoKosmiko][/I]"
		elif url.startswith("http://www.dailymotion.com/") == True: 
			accion = "abredaily_lista"
			titu = titu + "  [COLOR orange][I][DailyMotion][/I]"
		elif url.startswith("https://vimeo.com/") == True: 
			accion = "abrevimeo_lista"
			titu = titu + "  [COLOR green][I][Vimeo][/I]"
		elif url.startswith("https://www.youtube.") == True: 
			accion = "abretube_lista"
			titu = titu + "  [COLOR red][I][YouTube][/I]"
			
		plugintools.add_item(action=accion,url=url,title='[COLOR white]' + titu + '[/COLOR]' ,thumbnail=logo, fanart=fondo, info_labels = datamovie, folder=True, isPlayable=False)

	if HaySinopsis:
		plugintools.set_view(plugintools.TV_SHOWS)
	else:
		plugintools.set_view(plugintools.LIST)



		
def abretube_lista(params):
	busqueda = params.get("url").replace("https://", "http://")
	fanart = params.get("fanart")
	titulo = params.get("title")
	thumbnail = params.get("thumbnail")

	
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": busqueda}
	r=requests.get(busqueda, headers=headers)
	data = r.content
	
	videos = plugintools.find_multiple_matches(data, '<tr class="pl-video yt-uix-tile(.*?)pl-video-edit-options')
	
	if len(videos) == 0:
		salir = True
		pagina = 1
	else:
		salir = False
		
	videos_ord = []
	for item in videos:
		video = plugintools.find_single_match(item, '//i.ytimg.com/vi/(.*?)/')
		titu_vid = plugintools.find_single_match(item, 'title="(.*?)"')
		logo_vid = plugintools.find_single_match(item, 'data-thumb="(.*?)"')
		duracion = plugintools.find_single_match(item, 'segundos">(.*?)<')

		url_montada = video  # Solo quiero el Id del video

		linea_ord = titu_vid.title() + ">>>>1" + url_montada + "2>>>>2" + logo_vid + "3>>>>3" + duracion
		videos_ord.append(linea_ord)

	videos_ord.sort()
	
	logo = thumbnail
			
	letra = ""

	for item in videos_ord:
		titu = plugintools.find_single_match(item,'(.*?)>>>>1').strip()
		url_montada = plugintools.find_single_match(item,'>>>>1(.*)2>>>>2').strip()
		logo = plugintools.find_single_match(item,'>>>>2(.*)3>>>>3').strip()
		duracion = plugintools.find_single_match(item,'>>>>3(.*)').strip()
		
		titu = titu + "     [I][COLOR yellow](" + duracion + ")[/I]"
		
		if titu[:1] <> letra:
			letra = titu[:1]
			
			plugintools.add_item(action="",url="",title="[COLOR blue][I]**"+letra+"**[/I][/COLOR]",thumbnail=logo, fanart=fanart, folder=False, isPlayable=False)
			
		datamovie = {}

		plugintools.add_item( action = "lanza_video_plug" , title = '[COLOR white]' + titu + '[/COLOR]', url = url_montada , extra = "youtube" , info_labels = datamovie, thumbnail = logo , fanart = fanart , folder = False , isPlayable = False )




def lanza_video_plug(params):		
	url = params.get("url")
	plugin = params.get("extra")

	if plugin == "vimeo":
		xbmc.executebuiltin('PlayMedia(plugin://plugin.video.vimeo/play/?video_id='+url+'&amp;sf_options=winID%3D10001%26_options_sf)')
	elif plugin == "youtube":
		xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+url+')')
	
	

	
	

def abrevimeo_lista(params):
	busqueda = params.get("url").replace("https://", "http://")
	fanart = params.get("fanart")
	titulo = params.get("title")
	thumbnail = params.get("thumbnail")

	
	busqueda0 = busqueda
	busqueda = busqueda + "/page:1"
	pagina = 1
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": busqueda}
	r = requests.get(busqueda,headers=headers)
	data = r.content
	
	videos = plugintools.find_multiple_matches(data, 'data-position=(.*?)class="thumbnail')

	videos_ord = []
	
	paginacion = plugintools.find_single_match(data,'<div id="pagination"(.*?)<li class="pagination_next">')
	if paginacion:
		n_pag = plugintools.find_multiple_matches(paginacion,'data-page="([0-9])"')
		for item in n_pag:
			url = busqueda + "/page:" + str(item)+"/sort:preset/format:thumbnail"
			headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": busqueda}
			r=requests.get(url, headers=headers)
			data = r.content
			videos = plugintools.find_multiple_matches(data, 'data-position=(.*?)class="thumbnail')
			plugintools.log("********************Videos: "+str(len(videos))+"***********************")
			for item in videos:
				video = plugintools.find_single_match(item, 'href="(.*?)"')
				titu_vid = plugintools.find_single_match(item, 'title="(.*?)"')
				logo_vid = plugintools.find_single_match(item, 'src="(.*?)"')
				divide = video.split("/")
				url_montada = divide[-1]  # Solo quiero el Id del video
				linea_ord = titu_vid + ">>>>1" + url_montada + "2>>>>2" + logo_vid + "3>>>>3"
				videos_ord.append(linea_ord)
				plugintools.log("********************item: "+item+"***********************")	
				plugintools.log("********************linea: "+linea_ord+"***********************")	
				plugintools.log("********************regex: "+video+"***********************")
	else:
		videos = plugintools.find_multiple_matches(data, 'data-position=(.*?)class="thumbnail')
		plugintools.log("********************Videos: "+str(len(videos))+"***********************")
		for item in videos:
			video = plugintools.find_single_match(item, 'href="(.*?)"')
			titu_vid = plugintools.find_single_match(item, 'title="(.*?)"')
			logo_vid = plugintools.find_single_match(item, 'src="(.*?)"')
			divide = video.split("/")
			url_montada = divide[-1]  # Solo quiero el Id del video
			linea_ord = titu_vid + ">>>>1" + url_montada + "2>>>>2" + logo_vid + "3>>>>3"
			videos_ord.append(linea_ord)
			plugintools.log("********************item: "+item+"***********************")	
			plugintools.log("********************linea: "+linea_ord+"***********************")	
			plugintools.log("********************regex: "+video+"***********************")	
				
		
	videos_ord.sort()
	plugintools.log("********************VideosOrd: "+str(len(videos_ord))+"***********************")	
	
	logo = thumbnail
			
	letra = ""
	for item in videos_ord:
		titu = plugintools.find_single_match(item,'(.*?)>>>>1').strip()
		url_montada = plugintools.find_single_match(item,'>>>>1(.*)2>>>>2').strip()
		logo = plugintools.find_single_match(item,'>>>>2(.*)3>>>>3').strip()
		duracion = plugintools.find_single_match(item,'>>>>3(.*)').strip()
		
		titu = titu + "     [I][COLOR red](" + duracion + ")[/I]"
		
		if titu[:1] <> letra:
			letra = titu[:1]
			
			plugintools.add_item(action="",url="",title="[COLOR blue][I]**"+letra+"**[/I][/COLOR]",thumbnail=logo, fanart=fanart, folder=False, isPlayable=False)
			
		plugintools.log("*******************URL MONTADA: "+url_montada+"***********************")	
		datamovie = {}

		plugintools.add_item( action = "lanza_video_plug" , title = '[COLOR white]' + titu + '[/COLOR]', url = url_montada , extra = "vimeo" , info_labels = datamovie, thumbnail = logo , fanart = fanart , folder = False , isPlayable = False )





	

def abredaily_lista(params):
	busqueda = params.get("url")
	fanart = params.get("fanart")
	titulo = params.get("title")
	thumbnail = params.get("thumbnail")

	mi_ref = "http://" + plugintools.find_single_match(busqueda, "http://(.*?)/")

	busqueda0 = busqueda
	busqueda = busqueda + "/1"
	pagina = 1
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": busqueda}
	r=requests.get(busqueda, headers=headers)
	data = r.content
	
	videos = plugintools.find_multiple_matches(data, 'class="preview(.*?)/div><img')
	
	if len(videos) == 0:
		salir = True
		pagina = 1
	else:
		salir = False
		
	videos_ord = []
	while salir == False:  # Usa múltiples páginas
		for item in videos:
			video = mi_ref + plugintools.find_single_match(item, 'href="(.*?)"')
			titu_vid = plugintools.find_single_match(item, 'title="(.*?)"')
			logo_vid = plugintools.find_single_match(item, 'data-src="(.*?)"').strip()
			duracion = plugintools.find_single_match(item, 'duration">(.*?)<').strip()
			url_montada = link_daily.replace("MI_URL", video).replace("MI_REF", mi_ref)

			linea_ord = titu_vid.title() + ">>>>1" + url_montada + "2>>>>2" + logo_vid + "3>>>>3" + duracion
			videos_ord.append(linea_ord)

		pagina = pagina + 1
		busqueda = busqueda0 + "/" + str(pagina)
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": busqueda}
		r=requests.get(busqueda, headers=headers)
		data = r.content

		videos = plugintools.find_multiple_matches(data, 'class="preview(.*?)/div><img')
			
		if len(videos) == 0:
			salir = True
			pagina = 1
		else:
			salir = False
		
	videos_ord.sort()
	
	logo = thumbnail
			
	letra = ""
	for item in videos_ord:
		titu = plugintools.find_single_match(item,'(.*?)>>>>1').strip()
		url_montada = plugintools.find_single_match(item,'>>>>1(.*)2>>>>2').strip()
		logo = plugintools.find_single_match(item,'>>>>2(.*)3>>>>3').strip()
		duracion = plugintools.find_single_match(item,'>>>>3(.*)').strip()
		
		titu = titu + "     [I][COLOR red](" + duracion + ")[/I]"
		
		if titu[:1] <> letra:
			letra = titu[:1]
			
			plugintools.add_item(action="",url="",title="[COLOR blue][I]**"+letra+"**[/I][/COLOR]",thumbnail=logo, fanart=fanart, folder=False, isPlayable=False)
			
		datamovie = {}
		plugintools.runAddon( action = "runPlugin" , title = '[COLOR white]' + titu + '[/COLOR]', url = url_montada , info_labels = datamovie, thumbnail = logo , fanart = fanart , folder = False , isPlayable = False )




def abrekosmipop_lista(params):
	busqueda = params.get("url")
	fanart = params.get("fanart")
	titulo = params.get("title")
	thumbnail = params.get("thumbnail")

	mi_ref = "http://" + plugintools.find_single_match(busqueda, "http://(.*?)/")

	if busqueda.find("gallery") < 0:
		if busqueda.find("/list,") >= 0:
			lista = busqueda.replace("/list,", "/gallery,")
		else:	
			lista = busqueda.strip() +"/gallery,1,1"
	else:
		lista = busqueda.strip()
	#Me aseguro empezar x la 1ª
	lista = "http" + plugintools.find_single_match(lista, 'http(.*?)gallery,') + "gallery,1,1"

	num_pag = 1

	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": lista}
	r=requests.get(lista, headers=headers)
	data = r.content
	
	logo = thumbnail
	
	
	videos = plugintools.find_multiple_matches(data,'<li data-file-id(.*?)>')
	num_vid1 = len(videos)
	pag_sig = "http://" + plugintools.find_single_match(lista, 'http://(.*?)gallery,') + "gallery,1," + str(num_pag+1)

	plugintools.add_item(action="",url="",title="[COLOR yellow][I]              ····[COLOR skyblue]"+titulo+"[COLOR yellow]····[/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

	titulo_list = titulo
	
	salir = False
	#Voy a comprobar el nº de pag. q tiene, pues cada 1 tiene mas que la anterior, exepto la q ya "no existe", que tiene el mismo nº q la última
	while salir == False:

		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": pag_sig}
		r=requests.get(pag_sig, headers=headers)
		data = r.content
		
		videos = plugintools.find_multiple_matches(data, '<li data-file-id(.*?)>')
		num_vid2 = len(videos)
		
		if num_vid2 > num_vid1:  #Es una pag. siguiente real
			num_pag = num_pag + 1
			pag_sig = "http://" + plugintools.find_single_match(lista, 'http://(.*?)gallery,') + "gallery,1," + str(num_pag+1)
			salir = False
			num_vid1 = num_vid2
		else:
			salir = True

	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": pag_sig}
	r=requests.get(pag_sig, headers=headers)
	data = r.content
	
	videos = plugintools.find_multiple_matches(data, '<li data-file-id=(.*?)/a></h2>')
	
	videos_ord = []
	for item in videos:
		video = mi_ref + plugintools.find_single_match(item, 'href="(.*?)"')
		titu_vid = plugintools.find_single_match(item, 'preview">(.*?)<')
		url_montada = link_kosmipop.replace("MI_URL", video).replace("MI_REF", mi_ref)

		linea_ord = titu_vid.title() + ">>>>" + url_montada
		videos_ord.append(linea_ord)

	
		##Así no me funciona
		##plugintools.add_item(action="runPlugin",url=link_kosmipop.replace("MI_URL", video).replace("MI_REF", mi_ref),title="[COLOR white]"+titu_vid+"[/COLOR]",thumbnail=logo,fanart=fanart,folder=False,isPlayable=True)
		#plugintools.add_item(action="lanza_cosmipop",url=url_montada, title="[COLOR white]"+titu_vid+"[/COLOR]",thumbnail=logo,fanart=fanart,folder=False,isPlayable=True)

		
	videos_ord.sort()
	
	letra = ""
	for item in videos_ord:
		titu = plugintools.find_single_match(item,'(.*?)>>>>').strip()
		url_montada = plugintools.find_single_match(item,'>>>>(.*)').strip()
		
		if titu[:1] <> letra:
			letra = titu[:1]
			
			plugintools.add_item(action="",url="",title="[COLOR blue][I]**"+letra+"**[/I][/COLOR]",thumbnail=logo, fanart=fanart, folder=False, isPlayable=False)
			
		datamovie = {}
		plugintools.runAddon( action = "runPlugin" , title = '[COLOR white]' + titu + '[/COLOR]', url = url_montada , info_labels = datamovie, thumbnail = logo , fanart = fanart , folder = False , isPlayable = False )
		


		
def lanza_kosmipop(url):

	mi_ref = "http://" + plugintools.find_single_match(url, "http://(.*?)/")
	url_montada = link_kosmipop.replace("MI_URL", url).replace("MI_REF", mi_ref)
	
	return url_montada
	#xbmc.executebuiltin('PlayMedia('+url_montada+')')
	
	

	
	
	
	