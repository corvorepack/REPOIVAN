# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  Movie Ultra 7K
# (http://forum.rojadirecta.es/
# (http://xbmcspain.com/foro/
# Version 0.0.5 (05.02.2015)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

from __main__ import *
baseurl='http://u-stream.me/'
burl='http://u-peak.me/'

def ustreamme0(params):
 #plugintools.add_item(action="ustreamme11",title="[COLOR=orange]Programacion[/COLOR]",isPlayable=False,folder=True)
 plugintools.add_item(action="ustreamme1",title="[COLOR=orange]Canales[/COLOR]",isPlayable=False,folder=True)

def ustreamme1(params):
 try: y=plugintools.read(baseurl);
 except: exec(messs);sys.exit();
 r='<div\sid="nav\d{2}d".*?href="([^"]+).*?src="([^"]+)';w=plugintools.find_multiple_matches(y,r);y=[];
 for x in w:
  tit=x[0].replace(baseurl,'').replace('.html','').title();fan=baseurl+x[1].replace(' ','%20')
  plugintools.add_item(action="ustreamme2",title=tit,url=baseurl+x[0],fanart=fan,thumbnail=fan,isPlayable=True,folder=False );
 
def ustreamme2(params):
 try: y=plugintools.read(params['url']);params['page']=params['url'];#use this to send referer in params!!!
 except: exec(messs);sys.exit();
 try:
  try: r='<script type=.*?width=([^,]+),\sheight=([^,]+),\schannel=\'([^\']+).*?src=\'(.*?mips[^\']+)';params['url']=plugintools.find_single_match(y,r);q='http://www.mipsplayer.com/embedplayer/'+q[2]+'/1/'+q[0]+'/'+q[1];st='MIPS';ustreamme3(params);
  except: pass
  try: r='src=\'?"?(http:\/\/www\.iguide\.to[^\'"]+)';params['url']=plugintools.find_single_match(y,r);st='IGUIDE';ustreamme4(params);
  except: pass
  print st;
 except: exec(messs);sys.exit();

def ustreamme4(params):
 request_headers=[];request_headers.append(["Referer",params['page']]);url=params['url'].split('/')[4].split('&');
 url='http://www.iguide.to/embedplayer_new.php?'+url[1]+'&'+url[2]+'&channel='+url[0]+'&'+url[3];
 body,response_headers = plugintools.read_body_and_headers(url,headers=request_headers);
 try: r='getJSON\("([^"]+).*?streamer\':\s\'([^\']+).*?file\':\s\'([^\.]+).*?flash\',\ssrc:\s\'([^\']+)';w=plugintools.find_multiple_matches(body,r)
 except: exec(nolink);sys.exit();
 body,response_headers = plugintools.read_body_and_headers(w[0][0],headers=request_headers);
 params['url']=w[0][1]+' playpath='+w[0][2]+' swfUrl='+w[0][3]+' token='+body.split('"')[3]+' pageUrl='+params['url'];
 play_resolved_url(params['url']);sys.exit();
 
def ustreamme3(params):
 request_headers=[];request_headers.append(["Referer",params['page']])
 body,response_headers = plugintools.read_body_and_headers(params['url'],headers=request_headers);
 try: r='SWFObject\("([^"]+).*?FlashVars\',\s\'([^\']+)';w=plugintools.find_multiple_matches(body,r)
 except: exec(nolink);sys.exit();
 host=urlparse.urlparse(params['url']).netloc;p=plugintools.find_single_match(w[0][1],'s=([^\&]+)');
 id=plugintools.find_single_match(w[0][1],'?id=([^\&]+)');lb=plugintools.find_single_match(plugintools.read('http://'+host+':1935/loadbalancer?'+id),'=(.*)')
 params['url']='rtmp://'+lb+'/live playpath='+p+'id='+id+' swfUrl='+host+w[0][0]+' pageUrl='+params['url']+' live=1 conn=S:OK';#' -K "gaolVanusPob';
 play(params['url']);sys.exit();