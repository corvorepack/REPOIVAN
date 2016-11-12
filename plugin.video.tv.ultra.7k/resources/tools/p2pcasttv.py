# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  TV Ultra 7K
# (http://forum.rojadirecta.es
# (http://xbmcspain.com/foro
# Version 0.0.9 (08.01.2015)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

from __main__ import *
baseurl="http://p2pcast.tv/";fan='http://www.adslzone.net/app/uploads/2014/11/apertura-p2p.jpg';thum='http://imgur.com/PxhIUAv.png';
def p2pcast0(params):
 w,j=shsp100(baseurl,baseurl,'','');w=plugintools.find_single_match(w,'<ul.*?aria-labelledby="exploreMenu">(.*?)<\/ul>');
 w=plugintools.find_multiple_matches(w,'href="([^"]+).*?<i\sclass="([^"]+).*?<\/i>(\s?.*?)\n');j=0;
 for i in w:
  if j%2==0:
   plugintools.add_item(action="p2pcast1",title='[COLORcyan]'+i[2]+'[/COLOR]',url=baseurl+i[0],thumbnail=thum,fanart=fan,isPlayable=False,folder=True)
  else:
   plugintools.add_item(action="p2pcast1",title='[COLORwhite]'+i[2]+'[/COLOR]',url=baseurl+i[0],thumbnail=thum,fanart=fan,isPlayable=False,folder=True)
  j+=1
 
def p2pcast1(params):
 ref=baseurl;w,j=shsp100(params['url'],baseurl,'','');z=plugintools.find_single_match(w,'<div\sid="pager"(.*?)<\/div>');
 z=plugintools.find_multiple_matches(z,'<a\shref="([^"]+)');w=plugintools.find_single_match(w,'<div\sid="pagedContent"(.*?)<div\sid="pager"');
 w=plugintools.find_multiple_matches(w,'<a\shref="([^"]+).*?background-image:\surl\(\'([^\']+).*?<h4\sclass=[\'|"]title[\'|"]>([^<]+).*?<\/i>([^<]+)');q=[]
 plugintools.add_item(title=params['title'],thumbnail=thum,fanart=fan,isPlayable=False,folder=False)
 for i in z:
  m,n=shsp100(baseurl+i,params['url'],'',j);#m=plugintools.find_single_match(m,'<div\sid="pagedContent"(.*?)<div\sid="pager"');
  m=plugintools.find_multiple_matches(m,'<a\shref="([^"]+).*?background-image:\surl\(\'([^\']+).*?<h4\sclass=[\'|"]title[\'|"]>([^<]+).*?<\/i>([^<]+)');
  q.extend(m)
 q.extend(w);q=list(set(q))
 for i in q:plugintools.add_item(action='p2pcast11',title=i[2],url=baseurl+i[0],thumbnail=baseurl+i[1],fanart=fan,isPlayable=True,folder=False);

def p2pcast11(params):
 q,b=shsp100(params['url'],baseurl,'','');r='<iframe\sclass="embed-responsive-item".*?src=[\'|"]([^"]+)';w=plugintools.find_single_match(q,r);p=baseurl+w
 q,b=shsp100(p+'&live=0&stretching=uniform',params['url'],'',b);r='<iframe\ssrc=[\'|"]([^"]+).*?curl\s=\s[\'|"]([^\'"]+)';w=plugintools.find_multiple_matches(q,r);
 #print p,w[0][1].decode('base64');
 tok='http://p2pcast.tv/getToken.php';q,b=shsp100(tok,p,'',b);tok=plugintools.find_single_match(q,'"token":"([^"]+)');
 #plugintools.play_resolved_url(w[0][1].decode('base64')+tok+'|Referer=http://cdn.p2pcast.tv/jwplayer.flash.swf&User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36')
 plugintools.play_resolved_url(w[0][1].decode('base64')+'UkKQcKMHyjSSIRrAy43UJg|Referer=http://cdn.p2pcast.tv/jwplayer.flash.swf&User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36')