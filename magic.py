import requests
import random
import xml.etree.ElementTree as ET
from keeplow import *

cur_list = {"usd": ["R01235", "$"], "eur": ["R01239", "€"], "gbp": ["R01035", "£"], "uah": ["R01720", "₴"]}


def getrates(raw_qry):
    qry = raw_qry.split("_")
    try:
        url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={qry[1]}"
        gxml = requests.get(url, headers={'User-Agent': random.choice(user_agents),
                                          'cookie': '__ddg1_=eGPwfFU6NCZa9ErcJR6w'})
        try:
            parser = ET.XMLParser(encoding="windows-1251")
            structure = ET.fromstring(gxml.content, parser=parser)
        except ET.ParseError:
            return "parse error"
    except ConnectionError:
        return "connection error"

    try:
        return qry[0].upper() + ' = ' + structure.find(f"./*[@ID='{cur_list[qry[0]][0]}']/Value").text.replace(',', '.') + "₽"
    except AttributeError:
        return None
