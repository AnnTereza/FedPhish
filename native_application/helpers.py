import re
from urllib.parse import urlparse
from datetime import datetime



def standardize(url):
    # Converts the given URL into standard format
    if re.match(r"www.",url) is not None:
        url = url.replace("www.","")
    if not re.match(r"^https?", url):
        url = "http://" + url
    return url


def haveAtSign(url):
    # Check if @ is present
    match = re.search(r'@', url)
    if match is None:
        return 0, url
    else:
        return 1, url[match.start()+1:]


def lenCategory(url):
    url_len = len(url)
    if url_len < 54:
        len_cat = 0
    elif url_len >= 54 and url_len <= 75:
        len_cat = 1
    else:
        len_cat = 2
    return len_cat


def havingIP(url):
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', url)
    if match is None:
        return 0
    else:
        return 1


def haveDoubleSlash(url):
    pos=url.rfind("//")
    if pos>7:
        have_double_slash = 1
    else:
        have_double_slash = 0
    
    return have_double_slash


def haveDash(domain_name):
    if '-' not in domain_name:
        have_dash = 0
    else:
        have_dash = 1

    return have_dash


def haveHTTPS(url):
    if 'https://' in url:
        return 0
    else:
        return 1


def haveMultiSubDomains(url):
    dots=len(re.findall('\.', urlparse(url).netloc))
    dots-=1
    if dots > 2:
        dots = 2
    return dots


def getRegLen(domain):
    creation_date = domain.creation_date
    expiration_date = domain.expiration_date
    if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
        try:
            creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        return 1
    else:
        reg_len = abs((expiration_date - creation_date).days)
        if (reg_len < 366):
            age = 1
        else:
            age = 0
    return age


def genuineFavicon(soup, domain):
    if soup == -999:
        return 1
    favicon = soup.find("link", rel="icon")
    if  favicon is  None:
        return 1
    else:
        favicon_domain = urlparse(favicon['href']).netloc
        if favicon_domain == '':
            return 0
        elif domain in favicon_domain:
            return 0
        else:
            return 1


def externalLoading(soup, url, domain):
    i = 0
    success = 0
    if soup == -999:
        return 1
    else:
        for img in soup.find_all('img', src= True):
            dots= [x.start(0) for x in re.finditer('\.', img['src'])]
            if url in img['src'] or domain in img['src'] or len(dots)==1:
                success = success + 1
            i=i+1

        for audio in soup.find_all('audio', src= True):
            dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
            if url in audio['src'] or domain in audio['src'] or len(dots)==1:
                success = success + 1
            i=i+1

        for embed in soup.find_all('embed', src= True):
            dots=[x.start(0) for x in re.finditer('\.',embed['src'])]
            if url in embed['src'] or domain in embed['src'] or len(dots)==1:
                success = success + 1
            i=i+1

        for iframe in soup.find_all('iframe', src= True):
            dots=[x.start(0) for x in re.finditer('\.',iframe['src'])]
            if url in iframe['src'] or domain in iframe['src'] or len(dots)==1:
                success = success + 1
            i=i+1

        try:
            percentage = success/float(i) * 100
            if percentage < 22.0 :
                return 0
            elif((percentage >= 22.0) and (percentage < 61.0)) :
                return 1
            else :
                return 2
        except:
            return 2


def anchorURLs(soup, url, domain):
    percentage = 0
    i = 0
    unsafe=0
    if soup == -999:
        return 2
    else:
        for a in soup.find_all('a', href=True):
        # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
        # there in the actual a['href']
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1

        try:
            percentage = unsafe / float(i) * 100
        except:
            return 2

        if percentage < 31.0:
            return 0
        elif ((percentage >= 31.0) and (percentage < 67.0)):
            return 1
        else:
            return 2


def linksInTags(soup, url, domain):
    i=0
    success =0
    if soup == -999:
        return 2
    else:
        for link in soup.find_all('link', href= True):
           dots=[x.start(0) for x in re.finditer('\.',link['href'])]
           if url in link['href'] or domain in link['href'] or len(dots)==1:
              success = success + 1
           i=i+1

        for script in soup.find_all('script', src= True):
           dots=[x.start(0) for x in re.finditer('\.',script['src'])]
           if url in script['src'] or domain in script['src'] or len(dots)==1 :
              success = success + 1
           i=i+1
        try:
            percentage = success / float(i) * 100
        except:
            return 2

        if percentage < 17.0 :
           return 0
        elif((percentage >= 17.0) and (percentage < 81.0)) :
           return 1
        else :
           return 2


def SFH(soup, url, domain):
    if soup == -999:
        return 2
    for form in soup.find_all('form', action= True):
        if form['action'] =="" or form['action'] == "about:blank" :
            return 2
        elif url not in form['action'] and domain not in form['action']:
            return 1
        else:
            return 0
    return 0


def submittingToEmail(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[mail\(\)|mailto:?]", response.text):
            return 1
        else:
            return 0


def redirectCount(response):
    if response == "":
        return 2
    else:
        if len(response.history) <= 1:
            return 0
        elif len(response.history) <= 4:
            return 1
        else:
            return 2


def onMouseOver(response):
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0


def rightClick(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 1
        else:
            return 0


def popUp(response):
    if response == "":
        return 1
    else:
        if re.findall(r"alert\(", response.text):
            return 1
        else:
            return 0


def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 1
        else:
            return 0


