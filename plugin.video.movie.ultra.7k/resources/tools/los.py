#!/usr/bin/env python
# -*- coding: 850 -*-
# -*- coding: utf-8 -*-
from __main__ import *
baseurl='http://liveonsat.com/quickindex.html';#http://gg.gg/cipqwpw http://i.imgur.com/MRquG2Z.gif
thumb='http://liveonsat.com/images/LJ_banner_main_FLAG.jpg';burl='http://liveonsat.com/'
btitle="[COLOR=cyan][B]Live[/B][COLOR=grey]On[COLOR=cyan][B]Sat[/B][/COLOR]";tz='1'
def los0(params):
 plugintools.add_item(title=btitle,fanart=thumb,thumbnail=thumb,folder=False)
 plugintools.add_item(action='los1',title='[COLORgold]Programacion por Fecha[/COLOR]',thumbnail=thumb,fanart=thumb,folder=True)
 plugintools.add_item(action='los2',title='[COLORgold]Competiciones Top[/COLOR]',thumbnail=thumb,fanart=thumb,folder=True)
 plugintools.add_item(action='los3',title='[COLORgold]Otros Paises/Deportes[/COLOR]',thumbnail=thumb,fanart=thumb,folder=True)
def los1(params):
 plugintools.add_item(title=btitle+' : '+params['title'],fanart=thumb,thumbnail=thumb,folder=False)
 for i in range(-1,10):
  timestp=int(time.time())+i*24*60*60;td=datetime.fromtimestamp(timestp).strftime('%d/%m/%Y').split('/');
  if i==-1: fecha='[COLOR=grey]Ayer,'+'-'.join(td)+'[/COLOR]';
  elif i==0: fecha='Hoy,'+'-'.join(td);
  elif i==1: fecha='[COLOR=grey]Manana,'+'-'.join(td)+'[/COLOR]';
  else: fecha='[COLOR=grey]'+'-'.join(td)+'[/COLOR]';
  url='http://liveonsat.com/daily.php?start_dd='+td[0]+'&start_mm='+td[1]+'&start_yyyy='+td[2]+'&end_dd='+td[0]+'&end_mm='+td[1]+'&end_yyyy='+td[2];
  plugintools.add_item(action='los4',title='[COLORgold]'+fecha+'[/COLOR]',url=url,thumbnail=thumb,fanart=thumb,folder=True)
def los2(params):
 plugintools.add_item(title=btitle+' : '+params['title'],fanart=thumb,thumbnail=thumb,folder=False)
 ref=baseurl;body='';jar='';body,jar=cric2(baseurl,ref,body,jar);
 r='<map\sname="(.*?)<\/map>';w=plugintools.find_single_match(body,r);
 r='href="([^"]+)';w=plugintools.find_multiple_matches(w,r);
 for x in w:
  tit=plugintools.find_single_match(x,'los_soc_\w{1,3}_([^_]+)');
  plugintools.add_item(action='los4',title='[COLORgold]'+tit.title()+'[/COLOR]',url=burl+x,fanart=thumb,thumbnail=thumb,folder=True)
def los3(params):
 plugintools.add_item(title=btitle+' : '+params['title'],fanart=thumb,thumbnail=thumb,folder=False)
 ref=baseurl;body='';jar='';body,jar=cric2(baseurl,ref,body,jar);
 r='<table.*?id="AutoNumber3">(.*?)<\/table>';w=plugintools.find_single_match(body,r);
 r='<a href="([^"]+).*?>([^<]+)';w=plugintools.find_multiple_matches(w,r);k={};
 for x,y in w: k.update({x:y});
 try: from collections import OrderedDict;k=OrderedDict(sorted(k.items()));#print "Value : %s" %  titnew
 except: k=dict(sorted(k.items()));#possible solution for spmc?!?
 for x,y in k.iteritems(): plugintools.add_item(action='los4',title='[COLORgold]'+y.title()+'[/COLOR]',url=burl+x,fanart=thumb,thumbnail=thumb,folder=True)
def los4(params):
 ref=baseurl;body='';jar='';body,jar=cric2(params['url'],ref,body,jar);#print body,jar
 timestp=int(time.time())+int(tz)*60*60;#print 'TimeZone=GMT'+tz,timestp;
 ahora=datetime.now();td=datetime.fromtimestamp(timestp).strftime('%H:%M');
 #tr='01:50';tr=time.strptime(tr,'%H:%M');tk=time.strptime(ahora,'%H:%M');print params['title'],timestp,ahora,td,tr,tk;#trei dif ore pt meci
 r='<span\sclass\s?=\s?"?comp_head\s?"?>(.*?)<\/span>.*?<div\sclass\s?=\s?"?blockfix\s?"?>(.*?)<\!-- block 1 ENDS-->';
 try: w=plugintools.find_multiple_matches(body,r);#print w,len(w)
 except: exec(noevent);sys.exit();
 if len(w)>0: plugintools.add_item(title=params['title'],fanart=thumb,thumbnail=thumb,folder=False)
 else: exec(notf);sys.exit();
 for x,y in w:
  r='(<div class\s?=\s?"?fix_text\s?"?>.*?<div class\s?=\s?"?fLeft\s?"?>)';q=plugintools.find_single_match(y,r);y=y.replace(q,'');
  r='<img\ssrc="([^"]+)';imgmatch=plugintools.find_multiple_matches(q,r);
  r='(<div\sclass\s?=\s?"?fLeft_time_live\s?"?>.*?<\/div>)';q=plugintools.find_single_match(y,r);y=y.replace(q,'');
  r='[ST:]+?\s?(\d{1,2}:\d{2})';horamatch=plugintools.find_single_match(q,r);#print horamatch;
  r='([^\:]+)(.*)';hrep=plugintools.find_multiple_matches(horamatch,r);horamatch=str(int(tz)+int(hrep[0][0]))+str(hrep[0][1])
  '''
  if int(hrep[0][0][0])>1 and int(hrep[0][0][1])>3: hrepx='0'+str(int(hrep[0][0])-24);horamatch=str(int(tz)+int(hrepx))+str(hrep[0][1])
  elif int(hrep[0][0])<0: hrepx=str(23+int(hrep[0][0]));horamatch=str(int(tz)+int(hrepx))+str(hrep[0][1])
  else: horamatch=str(int(tz)+int(hrep[0][0]))+str(hrep[0][1])
  '''
  r=';">(.*?)<\/a>';tv=plugintools.find_multiple_matches(y,r);tv='@'.join(tv);#print tv
  tit='[COLORgreen]'+horamatch+' [COLORwhite]'+x+'[/COLOR]'
  plugintools.add_item(action='los5',title=tit,url=tv,fanart=burl+imgmatch[1],thumbnail=burl+imgmatch[1],folder=False)
def ocr2text(params):
 img_local=art+'ocrtest.png';url='http://api.ocrapiservice.com/1.0/rest/ocr';post='image='+img_local+'&language=en&apikey=Atvq9Py6VN'
 heads=[];heads.append(["User-Agent","Chrome/26.0.1410.65 Safari/537.31"]);body,heads=plugintools.read_body_and_headers(url,headers=heads,post=post);
 return body,heads
def los5(params):
 g=params['url'].split('@');q=[];
 for i in g:
  cor='white';
  if i.find('HD')>0: cor='green';
  if i.find('PPV')>0: cor='red';
  if i.find('online')>0: cor='yellow';
  i='[COLOR'+cor+']'+i+'[/COLOR]';q.append(i);
 if len(q)==0: exec(nolink);sys.exit();
 try:
  index=0;ch=0;
  index=plugintools.selector(q,title=params['title']);
  ch=q[index];
  if ch:
   if index > -1: exec(nocode);sys.exit();
 except KeyboardInterrupt: pass;
 except IndexError: raise;