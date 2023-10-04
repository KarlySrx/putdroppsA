import os
import re
import random
import time
import asyncio
import requests

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InputMediaAnimation, Message
from defs import getUrl, getcards

# Lista de URLs de GIFs
gif_urls = [
    "https://media.tenor.com/pbN7I_yikUwAAAAC/vanitas-no-carte-anime.gif",
    "https://www.icegif.com/wp-content/uploads/2022/04/icegif-1217.gif",
    # Agrega más URLs de GIFs aquí
]

class Scraper:
    def __init__(self, id, hash, chat, chats):
        self.id = id
        self.hash = hash
        self.chat = chat
        self.chats = chats
        self.ccs = []

        with open('cards.txt', 'r') as r:
            temp_cards = r.read().splitlines()

        for x in temp_cards:
            car = getcards(x)
            if car:
                self.ccs.append(car[0])

    async def get_bin_info(self, cc):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://bins-su-api.danielsaumett2093.workers.dev/api/{cc[:6]}') as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return data

    async def handle_message(self, client, message):
        text = message.text
        cards = getcards(text)
        if not cards:
            return
        cc, mes, ano, cvv = cards
        if cc in self.ccs:
            return
        self.ccs.append(cc)

        bin_info = await self.get_bin_info(cc)
        if not bin_info:
            return

        brand = bin_info["data"]["vendor"]
        types = bin_info["data"]["type"]
        level = bin_info.get("data", {}).get("level", "N/A")
        bank = bin_info.get("data", {}).get("bank", "N/A")
        country = bin_info["data"]["country"]
        flag = bin_info["data"]["countryInfo"]["emoji"]
        
        # Selección aleatoria de una URL de GIF
        gif = random.choice(gif_urls)

        extra = cc[0:0 + 12]
        crd = f"{cc}|{mes}|{ano}|{cvv}"
        text = f""" 

[ϟ] New Cards Found ⛈
[ϟ] Card: <code> {cc}|{mes}|{ano}|{cvv} </code>
     ϟ 
[ϟ] Bin Information: 
    ϟ Type:  {types}
    ϟ Level: {level}
    ϟ Bank:  {bank}
      ϟ  {brand}
    ϟ Country: {country}({flag})
      ϟ @TeamSirux[FreeDB] 
 
"""

        print(f'Card => {cc}|{mes}|{ano}|{cvv}  {country} - ({flag}    ')
        with open('cards.txt', 'a') as w:
            w.write(crd + '\n')

        await client.send_media_group(
            self.chat,
            [
                InputMediaAnimation(gif, caption=text)
            ]
        )

    def run(self):
        app = Client("session", api_id=self.id, api_hash=self.hash)

        @app.on_message(filters.chat(self.chats) & filters.text)
        async def my_event_handler(client, message):
            await self.handle_message(client, message)

        app.run()

if __name__ == "__main__":
    id = 27681377
    hash = '43f342537ee796353a06c6b7b6931c57'
    chat = '@dbSiruxCcs'
    chats = [
        '@scrapperlala', '@ritagroupOfc', '@OficialScorpionsGrupo','@JohnnySinsChat','@freeusersdev','@alterchkchat','@BINEROS_CCS2'
    ]
    scraper = Scraper(id, hash, chat, chats)
    scraper.run()
