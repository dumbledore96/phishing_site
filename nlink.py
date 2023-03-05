from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re

# 回傳網站資料
def nlink(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    domain = urlparse(url).scheme+"://"+urlparse(url).netloc
    internalLinks = getInternalLinks(soup,domain)
    externalLinks = getExternalLinks(soup,domain)
    result = {'inter': internalLinks,
              'inlen': len(internalLinks),
              'exter': externalLinks,
              'exlen': len(externalLinks),
              'type':resp.headers.get('content-type'),
              'last_modified':resp.headers.get('last-modified'),
              'server': resp.headers.get('server'),
            }
    return result

# 內部連結
def getInternalLinks(soup, includeUrl):
    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []
    #找出所有以'/'開頭的連結
    for link in soup.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

# 外部連結
def getExternalLinks(soup, excludeUrl):
    externalLinks = []
    #找出所有以"http"或者"www"開頭且不包含當前URL的連結
    for link in soup.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks