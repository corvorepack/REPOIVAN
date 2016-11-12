# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  TV Ultra 7K
# (http://forum.rojadirecta.es/
# (http://xbmcspain.com/foro/
# Version 0.0.4 (29.11.2014)
#   !!! Intentar NO compartir este archivo !!!
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

from __main__ import *
thumb="http://i39.tinypic.com/3128vb9.png"
fan="http://666kb.com/i/c8imw30y35vh0e528.png"
baseurl='http://www.wiz1.net/lag10_home.php';
messs='plugintools.message("ERROR","[COLOR=yellow]Cambios en la web[/COLOR]","[COLOR=red](avisar en el foro)[/COLOR]")'
nolink='plugintools.message("ATENCION","[COLOR=yellow]Canal sin emicion[/COLOR]","[COLOR=red](no hay enlaces)[/COLOR]")'
pxmess='plugintools.message("ATENCION","[COLOR=yellow]Necesita proxy RDS!!![/COLOR]","[COLOR=red](se intenta abrir)[/COLOR]")'

def wiz0(params):
  xbmcgui.Dialog().notification('ESPERE','buscando canales...',icon,1000)
  body,jar=cookie_frame01(baseurl,baseurl,'','')
  try: r='(\d{2}\/\d{2}\/\d{4})';w=plugintools.find_single_match(body,r);
  except: w='';pass
  tit='[COLOR=blue]WIZ '+w+'[/COLOR]';plugintools.add_item(action='',title=tit,thumbnail=thumb,fanart=fan,folder=False);
  try:
   r='(\d{2}:\d{2}).*?<b>([^<]+).*?<\/font>([^<]+).*?href="([^"]+).*?>([^<]+)';w=plugintools.find_multiple_matches(body,r);
   for j in range(0,len(w)):
    title="[COLOR=green]"+str(w[j][0])+ "[COLOR=yellow] "+w[j][2].upper() + " [COLOR=red] ("+str(w[j][1]).lower()+') [COLOR=white]'+w[j][4]+"[/COLOR]";
    plugintools.add_item(action='wiz1',title=title,url=w[j][3],thumbnail=thumb,fanart=fan,isPlayable=True,folder=False)
  except: exec(messs);pass
  

def wiz1(params):
 fan=params.get('fanart');thumb=params.get('thumbnail');url=params.get('url');title=params.get('title')
 request_headers=[];body,jar=cookie_frame01(url,baseurl,'','');bod=body;ref=url;
 r='<iframe.*?src="([^"]+)';w=plugintools.find_multiple_matches(body,r);url=w[0]
 body,jar=cookie_frame01(url,ref,'','');ref=url;
 r='<script\stype="text\/javascript">\s?swidth="?\'?([^"\']+)"?\'?\s?,?;?\s?sheight="?\'?([^"\']+)"?\'?.*?src="?\'?([^\'"]+)';
 w=plugintools.find_multiple_matches(body,r);url=w[0][2];
 data,jar=cookie_frame01(url,ref,'','');ref=url;
 data=unpack(data);
 r='src="([^"]+)';w=plugintools.find_single_match(urllib.unquote_plus(tamzar(data)),r);
 data,jar=cookie_frame01(w,ref,'','');ref=url;url=w;
 r='SWFObject\(\'([^\']+).*?file\',\s?\'([^\']+).*?streamer\',\s?\'([^\']+)';w=plugintools.find_multiple_matches(data,r);print w
 try:
  url=w[0][2]+' playpath='+w[0][1]+' swfUrl='+w[0][0]+' token=‪#‎yw‬%tt#w@kku conn=S:OK timeout=15 live=1 pageUrl='+url;print url
  plugintools.play_resolved_url(url)
 except: exec(nolink);pass

def tamzar(data):
 r='Tamrzar\.push\(\'([^\']+)';w=plugintools.find_multiple_matches(data,r);data=''.join(w);
 return data

def unpack(sJavascript,iteration=1, totaliterations=1  ):
 aSplit = sJavascript.split("rn p}('")
 p1,a1,c1,k1=('','0','0','')
 ss="p1,a1,c1,k1=(\'"+aSplit[1].split(".spli")[0]+')';exec(ss)
 k1=k1.split('|')
 aSplit = aSplit[1].split("))'")
 e = '';d = ''
 sUnpacked1 = str(__unpack(p1, a1, c1, k1, e, d,iteration))
 if iteration>=totaliterations: return sUnpacked1
 else: return unpack(sUnpacked1,iteration+1)
def __unpack(p, a, c, k, e, d, iteration,v=1):
 while (c >= 1):
  c = c -1
  if (k[c]):
   aa=str(__itoaNew(c, a))
   p=re.sub('\\b' + aa +'\\b', k[c], p)
 return p
def __itoa(num, radix):
 result = ""
 if num==0: return '0'
 while num > 0: result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result;num /= radix
 return result
def __itoaNew(cc, a):
 aa="" if cc < a else __itoaNew(int(cc / a),a)
 cc = (cc % a)
 bb=chr(cc + 29) if cc> 35 else str(__itoa(cc,36))
 return aa+bb