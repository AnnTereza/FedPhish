import re
import requests


def extract_features(url):
    '''
        Extract features from the given url
    '''
    features = []
    print(url)

    # URL Features
    # Check if ip address is present
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', url)
    if match == None:
        print('ip is not present')
    else:
        print(match)
        print("ip is  present")
    
    # url length
    match = len(url)
    if match < 54:
        print("legitimate", match)
    elif match >= 54 and match <= 75:
        print("suspiuos", match)
    else:
        print("phishing", match)

    # Check if @ is present
    match = re.search(r'@', url)
    if re.search(r'@', url) == None:
        print("@  not found")
    else:
        print(match)
        print("@ found")

    # html based features
    response = requests.get(url)

    match = re.search(r'iframe', response.text)
    if match == None:
        print("No match")
    else:
        print("Match found")
    
    return features

url_checklist = [
    'http://www.google.com',
    'http://amazon.com@google.com',
    'https://192.168.1.100/home/',
]

for url in url_checklist:
    print(extract_features(url))