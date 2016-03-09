"""
scrapes compliments from http://emergencycompliment.com/

special thanks to Nate Beatty for taking time to give me some tips and help me scrap compliments
from the above mentioned website, where he "codes and does fancy internet stuff to everything"

This module is mostly code he provided to me, with a few changes, just to make it fit inside
the pymod program and python conventions ;)

http://natebeatty.com/
"""

import json
import requests
from random import randint


def reduce(asd):
    return asd["gsx$compliments"]["$t"]


def get_compliment_list(url):
    response = requests.get(url)
    json_data = json.loads(response.text)
    return list(map(reduce, json_data["feed"]["entry"]))


class CompMod:
    rank = 0
    help_dict = {'py_comp': 'chats a random compliment'}
    url = 'https://spreadsheets.google.com/feeds/list/1eEa2ra2yHBXVZ' \
          '_ctH4J15tFSGEu-VTSunsrvaCAV598/od6/public/values?alt=json'

    def __init__(self, client, message):
        self.client = client
        self.message = message

    async def py_comp(self):
        complist = get_compliment_list(CompMod.url)
        num = randint(0, len(complist))
        await self.client.send_message(self.message.channel, complist[num])