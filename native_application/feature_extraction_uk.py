import re
import requests
from bs4 import BeautifulSoup as soup

from urllib.parse import urlparse,urlencode

import ssl, socket
from datetime import datetime

def extract_features(url):
    '''
        Extract features from the given url
    '''
    features = []
    print(url)

# 1. URL based extractions
# 1.1 Check if the URL has IP Address
    
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', url)
    if match == None:
        print('ip is not present')
    else:
        print(match)
        print("ip is  present")
    
 # 1.2. checking the URL length
    match = len(url)
    if match < 54:
        print("legitimate", match)
    elif match >= 54 and match <= 75:
        print("suspiuos", match)
    else:
        print("phishing", match)


# 1.3. Check if the site uses URL Shortening
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

    match=re.search(shortening_services,url)
    if match:
        print("Shortening service used")
    else:
        print("Shortening service not used")


# 1.4 Check if there's @ symbol in URL
    match = re.search(r'@', url)
    if re.search(r'@', url) == None:
        print("@  not found")
    else:
        print(match)
        print("@ found")

# 1.5 Check if there's redirect using // in url
    pos=url.rfind('//')
    if pos > 6:
        if pos > 7:
            print ("// Redirect used")
    else:
        print("// Redirect not used")

# 1.6 Check for prefix or suffix in domain part of URL
    if '-' in urlparse(url).netloc:
        print("- is found")
    else:
        print("- is not found")
    

# 1.7 Check the amount of subdomains
    domain=urlparse(url).netloc
    print(domain)
    match=domain.count(".")
    print(match)
    if match == 1:
        print ("no subdomain")
    elif match == 2:
        print("1 subdomain")
    else:
        print("3 or more subdomain")


# 1.8 Check if it has HTTPS 
    if 'https://' in url:
        print("HTTPS present")
    else:
         print("HTTPS not present")

# 1.9 Check the issuer of SSL Certificate
    ctx=ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
        s.connect((domain, 443))
        cert = s.getpeercert()

    subject = dict(x[0] for x in cert['subject'])
    issued_to = subject['commonName']
    issuer = dict(x[0] for x in cert['issuer'])
    issued_by = issuer['commonName']
    print ("Certified by :",issued_by)
    print ("Certified to :",issued_to)


# 1.10  Checking the age of the website
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
        try:
            creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            print("SIte is phishing")
    if ((expiration_date is None) or (creation_date is None)):
        print("SIte is phishing")
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        print("SIte is phishing")
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        if ((ageofdomain/30) < 6):
            print("SIte is phishing")
        else:
            print("SIte is Legitimate")


# 1.11 Checking expiry date
    expiration_date = domain_name.expiration_date
    if isinstance(expiration_date,str):
        try:
          expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            print("SIte is phishing")
    if (expiration_date is None):
        print("SIte is phishing")
    elif (type(expiration_date) is list):
        rprint("SIte is phishing")
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        if ((end/30) < 6):
        print("SIte is Legitimate")
        else:
        print("SIte is phishing")

# 2. HTML and Javascript based features
# 2.1 IFrame Detection
    if re.findall(r"[<iframe>|<frameBorder>]", response.text):
        print("no iframe")
    else:
        print("has iframe")


# 2.2 Status Bar Customization
    if re.findall("<script>.+onmouseover.+</script>", response.text):
        print("has statusbar customization")
    else:
        print("has no statusbar customization")

# 2.3 Disabling RIght Click
    if re.findall(r"event.button ?== ?2", response.text):
        print("no right click lock")
        else:
        print("has right click lock")

# 2.4 Website forwarding
    if len(response.history) <= 2:
      print("no forwarding")
    else:
      print("has forwaring")


    return features

url_checklist = [
    'www.google.com',
    'amazon.com@google.com',
    'https://192.168.1.100/home/',
    'bit.ly/xKbsY',
    'https://bananapeel.com/surprise//phishing.html',
]

for url in url_checklist:
    print(extract_features(url))
