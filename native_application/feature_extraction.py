import re
import requests
import whois
import time

from helpers import *



def extract_features(url):
    '''
        Extract features from the given url
    '''
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    url = standardize(url)

    url_len = lenCategory(url)
    have_dash = haveDash(url)
    have_multi_subdomains = haveMultiSubDomains(url)
    have_double_slash = haveDoubleSlash(url)
    have_at, url = haveAtSign(url)

    url = standardize(url)
    domain = urlparse(url)
    dns_record = 0
    try:
        who_is = whois.whois(domain.netloc)
    except:
        dns_record = 1
    
    try:
        response = requests.get(url, headers=headers)
        if response.text:
            ssl_final_state = 0
    except Exception as e:
        ssl_final_state = 2
        response = ""

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        soup = -999
    
    have_ip = havingIP(url)
    have_https = haveHTTPS(url)

    if dns_record == 1:
        reg_len = 1
    else:
        reg_len = getRegLen(who_is)
    
    favicon = genuineFavicon(soup, domain)
    external_loading = externalLoading(soup, url, domain)
    anchor_urls = anchorURLs(soup, url, domain)
    links_in_tags = linksInTags(soup, url, domain)
    sfh = SFH(soup, url, domain)
    submitting_to_email = submittingToEmail(response)
    redirect_count = redirectCount(response)
    on_mouse_over = onMouseOver(response)
    right_click = rightClick(response)
    popup_present = popUp(response)
    iframe_present = iframe(response)

    features = [
        have_ip, url_len, have_at, have_double_slash, have_dash,
        have_multi_subdomains, ssl_final_state, reg_len, favicon,
        have_https, external_loading, anchor_urls, links_in_tags, 
        sfh, submitting_to_email, redirect_count, on_mouse_over,
        right_click, popup_present, iframe_present, dns_record

    ]

    return features

start_time = time.time()
url_checklist = [
    #'https://freecodecamp.org',
    #'https://linkedin.com', 
    #'https://sphnere-finance.com/dashboard/extensions/=nkbihrfbeogaeaoehlefnkodbefgpgknn/metamask.html',
    'http://xavier-net.gq/?login=do'
]

for url in url_checklist:
    print(extract_features(url))
print("--- %s seconds ---" % (time.time() - start_time))