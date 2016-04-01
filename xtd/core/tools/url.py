# -*- coding: utf-8
#------------------------------------------------------------------#

__author__    = "Xavier MARCELET <xavier@marcelet.com>"

#------------------------------------------------------------------#

import urllib
import urllib.parse

#------------------------------------------------------------------#

def parse_unix(p_url):
  l_unix  = None
  l_parse = urllib.parse.urlparse(p_url)
  l_items = list(l_parse)
  if l_items[0].startswith("unix+"):
    l_unix     = urllib.parse.unquote_plus(l_items[1])
    l_items[0] = l_items[0][5:]
    l_items[1] = "localhost"
  elif l_items[0].startswith("unix"):
    l_unix     = l_items[2]
    l_items[0] = "http"
    l_items[1] = "localhost"
    l_items[2] = ""
  return l_items, l_unix

def unparse_unix(p_parsed, p_unix):
  p_parsed = list(p_parsed)
  if p_unix:
    p_parsed[0] = "unix+%s" % p_parsed[0]
    p_parsed[1] = urllib.parse.quote_plus(p_unix)
  return urllib.parse.urlunparse(p_parsed)
