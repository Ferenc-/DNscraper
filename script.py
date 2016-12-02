#!/usr/bin/env python3

import argparse
import requests
from lxml import html
# from bs4 import BeautifulSoup
# from bs4 import UnicodeDammit

# https://kazuar.github.io/scraping-tutorial/
# https://stackoverflow.com/questions/15622027/parsing-xml-file-gets-unicodeencodeerror-elementtree-valueerror-lxml#15622069
LOGIN_URL = 'https://www.dijnet.hu/ekonto/control/login'
URL = 'https://www.dijnet.hu/ekonto/login/login_check_password'


def do_scraping(username, password):
    session_requests = requests.session()
    # Get login authenticity token
    result = session_requests.get(LOGIN_URL)
    result.encoding = 'ISO-8859-2'
    result.raw.decode_content = True
    tree = html.fromstring(result.content)
    # xml_tree = etree.parse(result.raw)
    authenticity_token = list(
            set(tree.xpath("//input[@name='vfw_form']/@value")))[0]
    print("Authenticity_token:", authenticity_token)
    # Create payload
    payload = {
            'vfw_form': authenticity_token,
            'username': username,
            'password': password
            }
    # Perform login
    result = session_requests.post(
            LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))
    # Scrape url
    result = session_requests.get(URL, headers=dict(referer=URL))
    result.raw.decode_content = True
    result.encoding = 'ISO-8859-2'
    parser = html.HTMLParser(encoding='ISO-8859-2')

    tree = html.document_fromstring(result.content, parser=parser)
    print(tree.xpath("//input[@name='vfw_form']/@value"))
    for e in tree.iter():
        print("%s - %s" % (e.tag, e.text))
    # print(login_info)


def main():
    parser = argparse.ArgumentParser(description='DNScraper')
    parser.add_argument('-p', '--password')
    parser.add_argument('-u', '--username')
    args = parser.parse_args()

    do_scraping(args.username, args.password)


if __name__ == '__main__':
    main()
