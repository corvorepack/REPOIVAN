# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  Movie Ultra 7K
# (http://forum.rojadirecta.es/
# (http://xbmcspain.com/foro/
#  cipromario(at)gmail(dot)com
# Version 0.0.4 (29.11.2014)
#   !!! Intentar NO compartir este archivo !!!
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

from __main__ import *
from datetime import datetime
thumb="http://beba.tv/css/images/stream/logo.15c9f708.png"
fan="http://beba.tv/css/images/stream/logo.15c9f708.png"
baseurl='http://beba.tv/';ch='';ref=''
messs='plugintools.message("ERROR","[COLOR=yellow]Cambios en la web[/COLOR]","[COLOR=red](avisar en el foro)[/COLOR]")'
nolink='plugintools.message("ATENCION","[COLOR=yellow]Canal sin emicion[/COLOR]","[COLOR=red](no hay enlaces)[/COLOR]")'
pxmess='plugintools.message("ATENCION","[COLOR=yellow]Necesita proxy RDS!!![/COLOR]","[COLOR=red](se intenta abrir)[/COLOR]")'

def bebatv0(params):
 plugintools.add_item(action="bebatv10",title="[COLOR=blue]Programacion[/COLOR]",url=baseurl,thumbnail=thumb,fanart=fan,isPlayable=False,folder=True)
 plugintools.add_item(action="bebatv11",title="[COLOR=blue]Deportes[/COLOR]",url=baseurl,thumbnail=thumb,fanart=fan,isPlayable=False,folder=True)

def bebatv11(params):
  xbmcgui.Dialog().notification('ESPERE','buscando canales...',icon,1000);body,jar=cookie_frame01(baseurl,baseurl,'','')
  r='<div class="menu  container"(.*?)<\/a>\s+<\/div>';q=plugintools.find_single_match(body,r);r='(href|title|class)=[\'|"]([^\'"]+)'
  q=plugintools.find_multiple_matches(q,r);
  for i in xrange(0,len(q),5):m=q[i+3][1];plugintools.add_item(action='bebatv12',title=q[i+1][1],url=baseurl[:-1]+q[i][1],thumbnail=thumb,fanart=fan,isPlayable=False,folder=True);

def bebatv12(params):
  xbmcgui.Dialog().notification('ESPERE','buscando canales...',icon,1000);print params['url']
  body,jar=cookie_frame01(params['url'],baseurl,'','')
  try: r='class="arrow glyphicon glyphicon-triangle-right">.*?>.*?>(.*?)<div style';w=plugintools.find_single_match(body,r).strip();
  except: w='';pass
  if w:tit='[COLOR=blue]'+w+'[/COLOR]';plugintools.add_item(action='',title=tit,thumbnail=thumb,fanart=fan,folder=False);
  else:eval(messs);sys.exit()
  r='<div class="menu  container"(.*?)<\/a>\s+<\/div>';q=plugintools.find_single_match(body,r);body=body.replace(q,'')
  #print q
  try:
   r='<div class="menu"(.*?)<div class="col-sm-3 sideBar">';w=plugintools.find_single_match(body,r);
   r='href=[\'|"]([^\'"]+)[\'|"]\s?>watch\sevent';q=plugintools.find_single_match(w,r);
   r='original_time.*?>([^<]+).*?head(.*?)<\/div>\s+<\/div>.*?body(.*?)<\/div>\s+<\/div>';w=plugintools.find_multiple_matches(w,r);
   for j in w:
	thum=plugintools.find_single_match(j[1],'img\ssrc="([^"]+)');meci=plugintools.find_single_match(j[1],'subject.*?>([^<]+)');
	ora=datetime.fromtimestamp(int(j[0])).strftime('%H:%M')
	links=plugintools.find_multiple_matches(j[2],'float:left;line-height:40px(.*?)<\/div>');lin=''
	if links:
	 for i in links:
	  link=plugintools.find_multiple_matches(i,'<a>\s?([^:<]+).*?openLink\(\'([^\']+)');lin+='@'+'@'.join(link[0])
	title="[COLOR=green]"+ora+ "[COLOR=yellow] "+meci.upper()+"[/COLOR]";
	plugintools.add_item(action='bebatv1',title=title,url=lin,page=q,thumbnail=thum,fanart=fan,isPlayable=True,folder=False);
  except: exec(messs);pass

def bebatv10(params):
  xbmcgui.Dialog().notification('ESPERE','buscando canales...',icon,1000)
  body,jar=cookie_frame01(baseurl,baseurl,'','')
  try: r='class="arrow glyphicon glyphicon-triangle-right">.*?>.*?>(.*?)<div style';w=plugintools.find_single_match(body,r).strip();
  except: w='';pass
  if w:tit='[COLOR=blue]'+w+'[/COLOR]';plugintools.add_item(action='',title=tit,thumbnail=thumb,fanart=fan,folder=False);
  else:eval(messs);sys.exit()
  r='<div class="menu  container"(.*?)<\/a>\s+<\/div>';q=plugintools.find_single_match(body,r);body=body.replace(q,'')
  #print q
  try:
   r='<div class="menu"(.*?)<div class="col-sm-3 sideBar">';w=plugintools.find_single_match(body,r);
   r='href=[\'|"]([^\'"]+)[\'|"]\s?>watch\sevent';q=plugintools.find_single_match(w,r);
   r='original_time.*?>([^<]+).*?head(.*?)<\/div>\s+<\/div>.*?body(.*?)<\/div>\s+<\/div>';w=plugintools.find_multiple_matches(w,r);
   for j in w:
	thum=plugintools.find_single_match(j[1],'img\ssrc="([^"]+)');meci=plugintools.find_single_match(j[1],'subject.*?>([^<]+)');
	ora=datetime.fromtimestamp(int(j[0])).strftime('%H:%M')
	links=plugintools.find_multiple_matches(j[2],'float:left;line-height:40px(.*?)<\/div>');lin=''
	if links:
	 for i in links:
	  link=plugintools.find_multiple_matches(i,'<a>\s?([^:<]+).*?openLink\(\'([^\']+)');lin+='@'+'@'.join(link[0])
	title="[COLOR=green]"+ora+ "[COLOR=yellow] "+meci.upper()+"[/COLOR]";
	plugintools.add_item(action='bebatv1',title=title,url=lin,page=q,thumbnail=thum,fanart=fan,isPlayable=True,folder=False);
  except: exec(messs);pass

def bebatv1(params):
 if params['url']=='':eval(nolink);sys.exit()
 url=params['url'].split('@')[1:];w=[url[x] for x in xrange(0,len(url),2)];y=[url[x] for x in xrange(1,len(url),2)];
 try:
  link=w;index=0;ch=0;tit=plugintools.find_multiple_matches(params['title'],'\]([^\[]+)');tit=' '.join(tit)
  index=plugintools.selector(link,title='[COLORyellow]'+tit[:30]+'[/COLOR]');
  ch=y[index];
  if ch:
   if index > -1:
	params.update({'url':ch,'page':baseurl+params['page'],'server':w[index]});#q=eval(params['server'].lower())(params);print q
	url='plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+baseurl+ch+'%26referer='+baseurl+params['page'];print url
	xbmc.executebuiltin('XBMC.RunPlugin('+url+')');
	#play(url)
	#plugintools.play_resolved_url(q)
 except KeyboardInterrupt: pass;
 except IndexError: raise;

def sawlive(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');
 r='swidth=[\'|"]([^\'"]+).*?sheight=[\'|"]([^\'"]+).*?src=[\'|"](.*?sawlive[^\'"]+)';w=plugintools.find_multiple_matches(b,r);q=w[0][2]
 b,j=cookie_frame01(q,baseurl+params['url'],'',j);w=urllib.unquote_plus(tamzar(unpack(b)));r='src="([^\'"]+)';z=plugintools.find_single_match(w,r);
 b,j=cookie_frame01(z,q,'',j);r='SWFObject\(\'([^\']+).*?file\',\s?\'([^\']+).*?streamer\',\s?\'([^\']+)';w=plugintools.find_multiple_matches(b,r);print w
 try:
  url=w[0][2]+' playpath='+w[0][1]+' swfUrl='+w[0][0]+' token=‪#‎yw‬%tt#w@kku conn=S:OK timeout=15 live=1 pageUrl='+z;return url
 except: exec(nolink);pass
def hdcast(params):
 r='fid=[\'|"]([^;\'"]+).*?v_width=[\'|"]?([^;]+).*?v_height=[\'|"]?([^;]+).*?src=[\'|"](.*?hdcast[^\'"]+)';
 b,j=cookie_frame01(baseurl+params['url'],params['page'],'','');w=plugintools.find_multiple_matches(b,r);
 q='http://www.hdcast.org/embedlive.php?u='+w[0][0]+'&vw='+w[0][1]+'&vh='+w[0][2]+'&domain=beba.tv';
 #http://mamahd.com/watch-bundesliga-konferenz-simulcast-live-stream-free-online-1.html
 b,j=cookie_frame01(q,baseurl+params['url'],'',j);print b,q,params['page'];exit()
 r='file:[\'|"]([^\'"]+)';url=plugintools.find_single_match(b,r);
 r='src="([^"]+)';w=plugintools.find_single_match(w,r);
 return url
def bbstream(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='document\.write\(unescape\("([^"]+)';w=urllib.unquote_plus(plugintools.find_single_match(b,r));
 r='src="([^"]+)';w=plugintools.find_single_match(w,r);
 b,j=cookie_frame01(w,baseurl+params['url'],'',j);r='file:[\'|"]([^\'"]+)';url=plugintools.find_single_match(b,r);
 return url
def cstream(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='document\.write\(unescape\("([^"]+)';w=urllib.unquote_plus(plugintools.find_single_match(b,r));
 r='src="([^"]+)';w=plugintools.find_single_match(w,r);
 b,j=cookie_frame01(w,baseurl+params['url'],'',j);r='file:[\'|"]([^\'"]+)';url=plugintools.find_single_match(b,r);
 return url
 print w;sys.exit();
def hqstream(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='<iframe.*?src=[\'|"]?(.*?hqstream[^\'"]+)';w=plugintools.find_single_match(b,r);
 b,j=cookie_frame01(w,baseurl+params['url'],'',j);r='.*var a =\s*([^;]+).*var b =\s*([^;]+).*var c =\s*([^;]+).*var d =\s*([^;]+).*var f =\s*([^;]+).*var v_part =\s*\'([^\']+).*';y=plugintools.find_multiple_matches(b,r);
 url='rtmp://'+str(int(y[0][0])/int(y[0][4]))+'.'+str(int(y[0][1])/int(y[0][4]))+'.'+str(int(y[0][2])/int(y[0][4]))+'.'+str(int(y[0][3])/int(y[0][4]))+y[0][5]+' swfUrl=http://filo.hqstream.tv/jwp6/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl='+w
 return url
def mybeststream(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='<iframe.*?src=[\'|"]?(.*?mybeststream[^\'"]+)';q=plugintools.find_single_match(b,r)
 try:
  b,j=cookie_frame01(q,'http://footdirect24.com/c.php?channel=2','',j);r='(eval\(function\(w,i,s,e\).*?<\/script>)';w=plugintools.find_single_match(b,r);
  w=unwise_process(w);r='(hestia|securetoken):[\'|"]([^\'"]+)';w=plugintools.find_multiple_matches(w,r);
  #rd='rtmpdump -r "rtmpe://l.mybeststream.xyz/r/" -a "r/" -f "WIN 18,0,0,209" -W "http://mybeststream.xyz/YmRlYjE3ZWUzZTQxNWRjNWRjYzljMTBkMzVhMmE0NjY4NGU5Y2/jwplayer.flash.swf" -p "http://mybeststream.xyz/gen_br.php?id=29321&width=100%&height=100%" -y "fod2156" -o- | ace_player -'
  #os.system(rd);raw_input(rd);sys.exit();print w;exit();
  url='rtmpe://l.mybeststream.xyz/r app=r swfUrl=http://mybeststream.xyz/YmRlYjE3ZWUzZTQxNWRjNWRjYzljMTBkMzVhMmE0NjY4NGU5Y2/jwplayer.flash.swf token='+w[1][1]+' live=true timeout=15 swfVfy=1 playpath='+w[0][1]+' pageUrl='+q;return url
 except:exec(nolink);pass
def mybest2(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='document\.write\(unescape\("([^"]+)';w=urllib.unquote_plus(plugintools.find_single_match(b,r));
 r='src="([^"]+)';w=plugintools.find_single_match(w,r);
 b,j=cookie_frame01(w,baseurl+params['url'],'',j);r='file:[\'|"]([^\'"]+)';url=plugintools.find_single_match(b,r);
 print b;exit()
 return url
def tvshare(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='document\.write\(unescape\("([^"]+)';w=urllib.unquote_plus(plugintools.find_single_match(b,r));
 r='src="([^"]+)';w=plugintools.find_single_match(w,r);
 b,j=cookie_frame01(w,baseurl+params['url'],'',j);
 try:r='file:[\'|"]([^\'"]+)';url=plugintools.find_single_match(b,r);
 except:pass
 try:
  r='<iframe.*?src=[\'|"]([^\'"]+)';q=plugintools.find_single_match(b,r);b,j=cookie_frame01(q,w,'',j);p='unescape\([\'|"]([^\'"]+)';
  q=urllib.unquote_plus(plugintools.find_single_match(b,p));b,j=cookie_frame01(q,w,'',j);w=plugintools.find_single_match(b,r);b,j=cookie_frame01(w,q,'',j);
  r='top\.location\s?=\s?[\'|"]([^\'"]+)';q=plugintools.find_single_match(b,r);b,j=cookie_frame01(w,q,'',j);r='window\.location\s?=\s?[\'|"]([^\'"]+)';
  w=plugintools.find_single_match(b,r);b,j=cookie_frame01(q,w,'',j);
  print b,q,j,w;
  url='';return url
 except:pass
def flash(params):
 try:#1,livestream
  b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='<iframe.*?src="([^"]+)';w=plugintools.find_single_match(b,r).replace('accounts','api/accounts');
  r='(player.*)';q=plugintools.find_single_match(w,r);w=w.replace(q,'feed.json?&filter=video');b,j=cookie_frame01(w,baseurl+params['url'],'',j);#b=json.loads(b);
  try:r='(progressive_url_hd|secure_progressive_url_hd|progressive_url|secure_progressive_url|m3u8_url|secure_m3u8_url|smil_url|secure_smil_url|f4m_url|secure_f4m_url)[\'|"]:[\'|"]([^\'""]+)';w=plugintools.find_multiple_matches(b,r)
  except:pass
  q=[x[0].replace('_url','').replace('_',' ') for x in w];y=[x[1] for x in w];
  try:
   link=q;index=0;ch=0;tit=plugintools.find_multiple_matches(params['title'],'\]([^\[]+)');tit=' '.join(tit)
   index=plugintools.selector(link,title='[COLORyellow]'+tit[:30]+'[/COLOR]');
   ch=y[index];
   if ch:
    if index > -1: params.update({'url':ch,'server':q[index]});return ch
  except KeyboardInterrupt: pass;
  except IndexError: raise;
 except:pass
 try:#2,p3g.tv
  b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='<iframe.*?src="([^"]+)';q=plugintools.find_single_match(b,r);
  b,j=cookie_frame01(q,baseurl+params['url'],'',j);r='<script\stype=[\'|"]text\/javascript[\'|"]>\s?width=[\'|"]?(\d{3}).*?height=[\'|"]?([^,]+).*?channel=[\'|"]?([^\'"]+).*?g=[\'|"]?([^\'"]+).*?src=[\'|"]?(.*?p3g[^\'"]+)';
  w=plugintools.find_multiple_matches(b,r);w='http://www.p3g.tv/membedplayer/'+w[0][2]+'/'+w[0][3]+'/'+w[0][0]+'/'+w[0][1]
  b,j=cookie_frame01(w,q,'',j);r='source\.setAttribute\([\'|"]src[\'|"],\s[\'|"]([^\)]+)';p='\$\.ajax\(\{url:\s?[\'|"]([^\'"]+)';
  w=plugintools.find_single_match(b,r).split('"');q=plugintools.find_single_match(b,p);q=plugintools.read(q).split('=')[1];url=w[0]+q+w[2];
  b,j=cookie_frame01(url,q,'',j);r='(http.*)';url=plugintools.find_single_match(b,r);
  return url
 except:pass
 try:#3,laola
  b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='<iframe.*?src=[\'|"]?(.*?laola[^\'"]+)';q=plugintools.find_single_match(b,r);
  b,j=cookie_frame01(q,baseurl+params['url'],'',j);q='plugin://plugin.video.cipqtv/?url=http%3A%2F%2Fwww.laola1.tv%2Fen-int%2Flive%2Fcev-satellite-timisoara-court-2%2F368161.html&mode=10&name=Today%2C+14.08.2015%2C+NOW+LIVE+-+CEV+Satellite%2C+Timisoara+-+Court+2'
  #xbmc.executebuiltin('XBMC.RunPlugin('+q+')');
  q='http://www.laola1.tv/en-int/live/cev-satellite-timisoara-court-2/368161.html';name='Today, 14.08.2015, NOW LIVE - CEV Satellite, Timisoara - Court 2'
  PLAY(q,name);out=xbmc.translatePath(os.path.join('special://home/addons/'+addon.getAddonInfo('id')+'/playlists/tmp.m3u8'));
  f=open(out,'r');q=f.read();f.close();r='(http.*)';url=plugintools.find_single_match(q,r);
  return url
 except:pass
def leton(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='<iframe.*?src="(.*?leton[^"]+)';w=plugintools.find_single_match(b,r);
 b,j=cookie_frame01(w,baseurl+params['url'],'',j);r='.*var a =\s*([^;]+).*var b =\s*([^;]+).*var c =\s*([^;]+).*var d =\s*([^;]+).*var f =\s*([^;]+).*var v_part =\s*\'([^\']+).*';y=plugintools.find_multiple_matches(b,r);
 url='rtmp://'+str(int(y[0][0])/int(y[0][4]))+'.'+str(int(y[0][1])/int(y[0][4]))+'.'+str(int(y[0][2])/int(y[0][4]))+'.'+str(int(y[0][3])/int(y[0][4]))+y[0][5]+' swfUrl=http://files.leton.tv/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl='+w
 return url
def jjcast(params):
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');r='<script\stype="text\/javascript"\ssrc="(.*?jjcast[^"]+)';w=plugintools.find_single_match(b,r);
 b,j=cookie_frame01(w,baseurl+params['url'],'',j);r='src=[\'|"]([^\'"]+)';y=plugintools.find_single_match(b,r);
 try:
  b,j=cookie_frame01(y,w,'',j);r='eval\(function\(p,a,c,k,e,d\)(.*?)<\/script>';w=unpack(plugintools.find_single_match(b,r));
  r='.*var myRtk(.*).*?file.*';q=plugintools.find_single_match(w,r).replace("myScrT.push('",'').replace("myRtk.push('",'').replace("');",'');
  q=urllib.quote_plus(q).replace('%2527','');q=urllib.unquote_plus(urllib.unquote_plus(urllib.unquote_plus(q)));r='.*(rtmp.*)jwplayer';
  rtmp=plugintools.find_single_match(q,r);r='.*Array\(\);(.*)rtmp';pp=plugintools.find_single_match(q,r);
  r='.*flashplayer\':"([^"]+)';swf=plugintools.find_single_match(q,r);
  url=rtmp+' playpath='+pp+' swfUrl=http://jjcast.com/'+swf+' live=1 timeout=10 swfVfy=1 pageUrl='+y
  return url
 except:pass
def bebatv2(params):
 print params;sys.exit()
 b,j=cookie_frame01(baseurl+params['url'],baseurl,'','');
 if params['server'].lower()=='jjcast':print 'jjcast'
 else:print 'unknown'
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
