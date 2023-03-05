import whois
def whoisurl(url):
    result = whois.whois(url)
    return result
