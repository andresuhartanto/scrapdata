import requests
import json
import urllib.parse
from lxml import html

g_API = 'https://f2e-test.herokuapp.com'
g_session = requests.Session()

def Authenticate():
    page = requests.get(g_API)
    tree = html.fromstring(page.content)
    csrf = tree.xpath("string(//input[@name='csrf']/@value)")

    url = urllib.parse.urljoin(g_API, 'api/auth')
    payload = {
        'username': 'f2e-candidate',
        'password': 'P@ssw0rd',
        'csrf': csrf
    }

    # Authenticating to get cookies
    g_session.post(url, data=payload)

def ScrapData(offset, limit):
    Authenticate()

    params = {'offset': offset, 'limit': limit}
    url = urllib.parse.urljoin(g_API, 'api/products') + '?' + urllib.parse.urlencode(params)

    content = g_session.get(url).text
    data = json.loads(content)

    with open('data.json', 'w') as outfile:
        json.dump(data['data'], outfile)

ScrapData(0, 1000)
