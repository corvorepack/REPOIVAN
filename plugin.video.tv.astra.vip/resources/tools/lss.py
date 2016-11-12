# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  TV Ultra 7K
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
#  cipromario(at)gmail(dot)com
# Version 0.0.4 (29.11.2014)
#   !!! Intentar NO compartir este archivo !!!
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------
from __main__ import *
burl='http://www.livesportstreams.tv/';lang='en';lang='es';#www.livesportstreams.tv/en/events/-/1/-/

def lsstv(params):
 try:
  thumbnail=params['thumbnail'];fanart=params.get("fanart");data=plugintools.read(burl+"sidebar.php?top=1&type=1&l="+lang);
  grups='<span\sid="span_link_sidebar"\sonClick="updateDivContentIconR\(\d{1,2},\s\'([^\']+).*?\'(\/.*?\d{1,2}[^\']+).*?>([^<]+)';
  grups=plugintools.find_multiple_matches(data,grups);grups=list(set(grups));grup=[]
  for i in range(0,len(grups)):
   try:r='-\s(.*)';nrmeci=plugintools.find_single_match(grups[i][2],r);nrmeci=' ('+nrmeci+')'
   except:pass
   if nrmeci==' ()':nrmeci=''
   tit=grups[i][0].replace('Ver ahora',' [COLORred]DIRECTOS ahora[/COLOR]').replace('en Directo',' [COLORgreen]Todos los deportes[/COLOR]')
   grup.append([tit+nrmeci,str(grups[i][1])])
   #plugintools.add_item(action="lsstv1",title=tit+nrmeci,url=str(grups[i][1]),thumbnail=thumbnail,isPlayable=False,folder=True);
 except: pass
 for i in sorted(grup):plugintools.add_item(action="lsstv1",title=i[0],url=i[1],thumbnail=thumbnail,isPlayable=False,folder=True);
def lsstv1(params):
 if 'Todos los deportes' in params['title']:lsstv3(params);return;#seleccion por idiomas
 a=burl+params['url'];data=plugintools.read(a);r='(<table.*?<\/table>)';language_list=[];prms={};jprms={};match='';
 m=plugintools.find_single_match(data,r).replace('&quot;','"');r='<tr.*?onc?C?lick(.*?<tr.*?onc?C?lick.*?)<\/tr>';
 m=plugintools.find_multiple_matches(m,r);repl=params['title'][:-4];#53522,59999,53912,59990,5001
 for i in m:
  r='<img\salt=[\'"]([^\'"]+).*?>(\d{1,2}:\d{1,2})<.*?font-size:13px;.*?>([^<]+).*?<td.*?>(.*?)<\/td>.*?id=[\'"]img_event_([^\'"]+)';
  pars=plugintools.find_multiple_matches(i,r);hhq='';p='<span.*?>([^<]+)<\/span>(.*)';
  try:hq=plugintools.find_multiple_matches(pars[0][3],p);lg=hq[0][1];hq='('+hq[0][0].replace('&nbsp;','')+')';
  except:hq='';lg=pars[0][3];pass
  ling=' [COLORwhite]'+lg.lower()+'[COLORred]'+hq+'[/COLOR]' if hq else ' [COLORwhite]'+pars[0][3].lower()+'[/COLOR]'
  url='http://www.livesportstreams.tv/'+lang+'/links/'+str(pars[0][4])+'/1';meci=pars[0][2];ora=pars[0][1]
  title="[COLORgreen]"+ora+"[COLORyellow] "+pars[0][2].upper()+" [COLOR=red][CR]"+pars[0][0].replace(repl,'').lower()+ling;
  if meci==match:language_list.append((lg,hq,str(pars[0][4])));prms[meci].update({'lg':language_list})
  else:language_list=[(lg,hq,str(pars[0][4]))];prms.update({meci:{'ora':pars[0][1],'comp':pars[0][0].replace(repl,'').lower(),'lg':language_list}})
  match=meci;
  plugintools.add_item(action="lsstv2",title=title,url=url,page=a,thumbnail=params['thumbnail'],isPlayable=True,folder=False);
 #PROXIMA ACTUALIZACION:un solo enlace para los partidos con selector de idioma
 '''
 for k,v in prms.iteritems():
  title="[COLORgreen]"+v['ora']+"[COLORyellow] "+k.upper()+" [COLOR=red][CR]"+v['comp'].replace(repl,'').lower();
  for i in v['lg']:lg=i[0]+i[1];link=i[2]
  plugintools.add_item(action="lsstv2",title=title,url='',page=a,thumbnail=params['thumbnail'],isPlayable=True,folder=False);
 '''
def lsstv2(params):
 #print params['url'],params['page'];exit()
 b,j=cookie_frame01(params['url'],params['page'],'','');r='window\.open\([\'|"]([^\'"]+)';m=plugintools.find_multiple_matches(b,r);
 y=[m[x] for x in xrange(len(m))];w=['Fuente :'+str(x+1) for x in xrange(len(m))];
 if len(y)==0:eval(nolink);sys.exit()
 try:
  link=w;index=0;ch=0;tit=plugintools.find_multiple_matches(params['title'],'\]([^\[]+)');tit=' '.join(tit)
  index=plugintools.selector(link,title='[COLORyellow]'+tit[:30]+'[/COLOR]');
  ch=y[index];
  if ch:
   if index > -1:
	url='plugin://plugin.video.ArenaDevil/?mode=1&amp;item=catcher%3dstreams%26url='+ch+'%26referer='+params['url'];print url
	plugintools.play_resolved_url(url)
 except KeyboardInterrupt: pass;
 except IndexError: raise
def lsstv3(params):
 plugintools.add_item(action="lsstv1",title='[COLORred]Cualquier idioma[/COLOR]',url=params['url'],thumbnail=params['thumbnail'],isPlayable=False,folder=True);
 a=burl+params['url'];data=plugintools.read(a);r='(<table.*?<\/table>)';language_list=[];
 m=plugintools.find_single_match(data,r).replace('&quot;','"');r='<tr.*?onc?C?lick(.*?<tr.*?onc?C?lick.*?)<\/tr>';
 m=plugintools.find_multiple_matches(m,r);repl=params['title'][:-4];#53522,59999,53912,59990,5001
 for i in m:
  r='<img\salt=[\'"]([^\'"]+).*?>(\d{1,2}:\d{1,2})<.*?font-size:13px;.*?>([^<]+).*?<td.*?>(.*?)<\/td>.*?id=[\'"]img_event_([^\'"]+)';
  pars=plugintools.find_multiple_matches(i,r);p='<span.*?>([^<]+)<\/span>(.*)';
  try:hq=plugintools.find_multiple_matches(pars[0][3],p);lg=hq[0][1];hq='('+hq[0][0].replace('&nbsp;','')+')';
  except:hq='';lg=pars[0][3];pass
  if lg.lower() not in language_list:language_list.append(lg.lower())
 for i in language_list:plugintools.add_item(action="lsstv4",title=i.upper(),url=params['url'],page=i.encode('base64'),thumbnail=params['thumbnail'],isPlayable=False,folder=True);
def lsstv4(params):
 a=burl+params['url'];data=plugintools.read(a);r='(<table.*?<\/table>)';language_list=[];prms={};jprms={};match='';
 m=plugintools.find_single_match(data,r).replace('&quot;','"');r='<tr.*?onc?C?lick(.*?<tr.*?onc?C?lick.*?)<\/tr>';
 m=plugintools.find_multiple_matches(m,r);repl=params['title'][:-4];dif=params['page'];
 for i in m:
  r='<img\salt=[\'"]([^\'"]+).*?>(\d{1,2}:\d{1,2})<.*?font-size:13px;.*?>([^<]+).*?<td.*?>(.*?)<\/td>.*?id=[\'"]img_event_([^\'"]+)';
  pars=plugintools.find_multiple_matches(i,r);hhq='';p='<span.*?>([^<]+)<\/span>(.*)';
  try:hq=plugintools.find_multiple_matches(pars[0][3],p);lg=hq[0][1];hq='('+hq[0][0].replace('&nbsp;','')+')';
  except:hq='';lg=pars[0][3];pass
  ling=' [COLORwhite]'+hq if hq else ''
  url='http://www.livesportstreams.tv/'+lang+'/links/'+str(pars[0][4])+'/1';meci=pars[0][2];ora=pars[0][1]
  title="[COLORgreen]"+ora+"[COLORyellow] "+pars[0][2].upper()+" [COLOR=red][CR]"+pars[0][0].replace(repl,'').lower()+ling+'[/COLOR]';
  if dif==lg.lower().encode('base64'):plugintools.add_item(action="lsstv2",title=title,url=url,page=a,thumbnail=params['thumbnail'],isPlayable=True,folder=False);
