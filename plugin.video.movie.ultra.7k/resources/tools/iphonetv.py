# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  Movie Ultra 7K
# (http://forum.rojadirecta.es
# (http://xbmcspain.com/foro
# Version 0.0.1 (26.10.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------
# Thanks DerbyCrash

from __main__ import *
burl='http://en.firstonetv.com/index'
'''
 plugintools.add_item(action="iph0",title="[COLORwhite][B]FIRST[COLORgreen]1[COLORwhite].TV[/B][/COLOR]",fanart='http://en.firstonetv.com/images/sliders/revolution/siphone.png',thumbnail='http://en.firstonetv.com/images/logo.png',folder=True)
'''

def iph0(params):
 mssg='buscando programas...';timp=1000;exec(dlg);
 plugintools.add_item(title=params['title'],thumbnail=params['thumbnail'],fanart=params['thumbnail'],isPlayable=False,folder=False);
 body,jar=plugintools.read_body_and_headers(burl);r='<li><a\shref="(channels[^"]+)">([^<]+)';w=plugintools.find_multiple_matches(body,r);
 for x in w:
  th='http://img.freeflagicons.com/thumb/round_icon/'+x[1].lower().replace(' ','_')+'/'+x[1].lower().replace(' ','_')+'_640.png'
  th=th.replace('italia','italy').replace('u.s.a','united_states_of_america')
  plugintools.add_item(title=x[1],action='iph1',url=x[0],thumbnail=th,fanart=th,isPlayable=False,folder=True); 
 
def iph1(params):
 mssg='buscando enlaces...';timp=1000;exec(dlg);curl=burl.replace('index','');url=curl+params['url'];body,jar=plugintools.read_body_and_headers(url);
 r='<a\shref="(stream[^"]+).*?img\ssrc="([^"]+).*?alt="([^"]+)';w=plugintools.find_multiple_matches(body,r);f=params['thumbnail']
 for x in w:
  plugintools.add_item(title=x[2],action='iph2',url=curl+x[0],thumbnail=curl+x[1].replace('&amp;','&'),fanart=f,isPlayable=True,folder=False);
		
def iph2(params):
 body,jar=plugintools.read_body_and_headers(params['url']);r='iframe\ssrc="(http:\/\/api\.firstonetv\.com[^"]+)';
 try:w=plugintools.find_single_match(body.replace('&quot;','"'),r);
 except:pass
 if not w:eval(nolink);sys.exit()
 body,jar=plugintools.read_body_and_headers(w);r='eval\(decodeURIComponent\(atob\("([^"]+)'
 w=plugintools.find_single_match(body,r);w=urllib.unquote_plus(b64_error(w).decode('base64'));x=w
 while 'decodeURIComponent' in x:w=urllib.unquote_plus(x);w=plugintools.find_single_match(w,r);w=b64_error(w).decode('base64');x=w
 if '(p,a,c,k,e,d)' in urllib.unquote_plus(x):w=iph_unpack(urllib.unquote_plus(x));
 r='="([^"]+)';w=plugintools.find_single_match(w,r);
 if w:plugintools.play_resolved_url(w);
 
def iph_unpack(x):
 pars=x.split("return p}('");p,a,c,k,e,d=('','0','0','','','')
 ss="p,a,c,k=('"+pars[1].split(".spli")[0]+')';exec(ss);k=k.split('|');pars=pars[1].split("))'");
 while(c>=1):
  c=c-1
  if (k[c]):aa=str(iph_itoa(c,a));p=re.sub('\\b' +aa+'\\b',k[c],p)
 return p
  
def iph_itoa(cc,a):
 aa="" if cc<a else iph_itoa(int(cc/a),a)
 cc=(cc%a)
 bb=chr(cc+29) if cc>35 else str(iph_itoa2(cc,36))
 return aa+bb
 
def iph_itoa2(num,radix):
 result=""
 if num==0:return '0'
 while num>0:result="0123456789abcdefghijklmnopqrstuvwxyz"[num%radix]+result;num/=radix
 return result

def b64_error(b64_str):
 missing_padding=4-len(b64_str)%4
 if missing_padding: b64_str+=b'='*missing_padding;return b64_str