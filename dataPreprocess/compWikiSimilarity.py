#!/usr/bin/env python
#encoding=utf8

import urllib2
import urllib

from globalSetting import WEB_SERVICE_COMPARE

def test():
    word1 = "kiwi"
    word2 = "takahe"

    term1 = "?term1=" + word1
    term2 = "&term2=" + word2

    url = WEB_SERVICE_COMPARE+term1+term2
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'name':'anthonylife', 'location':'Beijing', 'language':'Python'}
    headers = {'User-Agent': user_agent}

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)
    content = urllib2.urlopen(req).read()

    print content

if __name__ == "__main__":
    test()
