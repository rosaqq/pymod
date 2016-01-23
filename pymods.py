import requests
from lxml import html


def py_ping():
    return 'pong'


def py_haiku():
    page = requests.get('http://www.randomhaiku.com/')
    tree = html.fromstring(page.content)
    verso = tree.xpath('//div[@class="line"]/text()')
    return '```' + verso[0] + '\n' + verso[1] + '\n' + verso[2] + '\n' + '```'


def py_xkcd():
    page = requests.get('http://c.xkcd.com/random/comic/')
    tree = html.fromstring(page.content)
    img_link = 'http:' + str(tree.xpath('//img')[1].get('src'))
    return img_link
