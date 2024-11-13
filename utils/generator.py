#!/usr/bin/python3
# -*- coding: utf-8 -*-

import warnings
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, quote, urlencode
from collections import Counter
import sys
import re
import asyncio
import copy
import time


warnings.filterwarnings("ignore")    # ignor any warning in teminal


#Colors 
class Colors:
    BOLD = '\033[1m'
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

#Vectors
delimiter = []
OOff = [
    "%00", "%01", "%02", "%03", "%04", "%05", "%06", "%07", "%08", "%09", "%0a", "%0b", "%0c", "%0d", "%0e", "%0f",
    "%10", "%11", "%12", "%13", "%14", "%15", "%16", "%17", "%18", "%19", "%1a", "%1b", "%1c", "%1d", "%1e", "%1f",
    "%20", "%21", "%22", "%23", "%24", "%25", "%26", "%27", "%28", "%29", "%2a", "%2b", "%2c", "%2d", "%2e", "%2f",
    "%30", "%31", "%32", "%33", "%34", "%35", "%36", "%37", "%38", "%39", "%3a", "%3b", "%3c", "%3d", "%3e", "%3f",
    "%40", "%41", "%42", "%43", "%44", "%45", "%46", "%47", "%48", "%49", "%4a", "%4b", "%4c", "%4d", "%4e", "%4f",
    "%50", "%51", "%52", "%53", "%54", "%55", "%56", "%57", "%58", "%59", "%5a", "%5b", "%5c", "%5d", "%5e", "%5f",
    "%60", "%61", "%62", "%63", "%64", "%65", "%66", "%67", "%68", "%69", "%6a", "%6b", "%6c", "%6d", "%6e", "%6f",
    "%70", "%71", "%72", "%73", "%74", "%75", "%76", "%77", "%78", "%79", "%7a", "%7b", "%7c", "%7d", "%7e", "%7f",
    "%80", "%81", "%82", "%83", "%84", "%85", "%86", "%87", "%88", "%89", "%8a", "%8b", "%8c", "%8d", "%8e", "%8f",
    "%90", "%91", "%92", "%93", "%94", "%95", "%96", "%97", "%98", "%99", "%9a", "%9b", "%9c", "%9d", "%9e", "%9f",
    "%a0", "%a1", "%a2", "%a3", "%a4", "%a5", "%a6", "%a7", "%a8", "%a9", "%aa", "%ab", "%ac", "%ad", "%ae", "%af",
    "%b0", "%b1", "%b2", "%b3", "%b4", "%b5", "%b6", "%b7", "%b8", "%b9", "%ba", "%bb", "%bc", "%bd", "%be", "%bf",
    "%c0", "%c1", "%c2", "%c3", "%c4", "%c5", "%c6", "%c7", "%c8", "%c9", "%ca", "%cb", "%cc", "%cd", "%ce", "%cf",
    "%d0", "%d1", "%d2", "%d3", "%d4", "%d5", "%d6", "%d7", "%d8", "%d9", "%da", "%db", "%dc", "%dd", "%de", "%df",
    "%e0", "%e1", "%e2", "%e3", "%e4", "%e5", "%e6", "%e7", "%e8", "%e9", "%ea", "%eb", "%ec", "%ed", "%ee", "%ef",
    "%f0", "%f1", "%f2", "%f3", "%f4", "%f5", "%f6", "%f7", "%f8", "%f9", "%fa", "%fb", "%fc", "%fd", "%fe", "%ff",
    "%00", "%0", ]
Crlf = ["%E2%A0%80%0A%E2%A0%80", "%0a%0a%0a%0a%0a",
        "嘍嘊", "%E5%98%8D%E5%98%8A", "%3f%0d", 
        "%2f%2e%2e%0d%0a", "%25%32%65"]
Tab = ["%5Ct", "%5Cn", "%5Cx0b%5Cx0c"]
Extra = ["%B0%B0%B0", "%2e%2e", "%5c%75%64%66%66%66%0a", "&",
         "%2f%2f.", "%3a%2f%2f", "°", "%ff%ff", "%0b%0b", 
         "%00%00", "%0a%0a", "%0d%0d", "%252e", "%E2%80%AE",
         "%00000000000000", "@%23!@%25$%5e&%25%5e%5e%25", "[]", "{}"]
EmailPays = ["@", "|", "||","|||", "%0Acc:", "&", "%", "#", "%", "%0Abcc:", "%5Cr%5Cn%20%5Cncc"]
HPP = ["&", ";", ":", "[]", "{}", "|", "||", "#", "@"]

class Main:
    def __init__(self, text=None, AD=None, A=None, V=None, VT=None):        
        self.text = text
        self.AD = AD
        self.A = A
        self.V = V
        self.VT = VT
    
    async def Payed(self, type=None):
        Payed = []
        unicode = ["\\udfff", "\\x00"]
        forUnicode = ["%20","%00", "%09", "%0d", "%0", "%01", "%bf", "%2f", "%0f",
           "%0b", "%0c", "%1c", "%1d", "%1e", "%1f", "%2A", 
           "%25", "%27", "%0d","%0a", "%40", "%23", "%ff", "%3b"]
        
        if type == "all":
            for x in forUnicode:   #Unicode
                unicode.append(f"\\u00{x.replace('%', '')}")
            for u in unicode:
                Payed.append(u)
            for c in Crlf:   #Crlf
                Payed.append(c)
            for t in Tab:   #Tab
                Payed.append(t)
            for e in Extra:     #Extra
                Payed.append(e)
            for p in OOff:  #00-FF
                Payed.append(p)
        elif type == "u":
            for x in forUnicode: 
                unicode.append(f"\\u00{x.replace('%', '')}")
            for u in unicode:
                Payed.append(quote(u))
        elif type == "crlf":
            for c in Crlf:  
                Payed.append(c)
        elif type == "tab":
            for t in Tab:   
                Payed.append(t)
        elif type == "extra":
            for e in Extra:   
                Payed.append(e)
        elif type == "ff":
            for p in OOff:  
                Payed.append(p)
        elif type == "wff": 
            for x in forUnicode:   
                unicode.append(f"\\u00{x.replace('%', '')}")
            for u in unicode:
                Payed.append(u)
            for c in Crlf:   
                Payed.append(c)
            for t in Tab:   
                Payed.append(t)
            for e in Extra:     
                Payed.append(e)
        elif type == "hpp":
            for h in HPP:     
                Payed.append(h)
        elif type == "dff": #To fuzz 2 Bytes
            print("SOON")
        
        return list(set(Payed))

    async def regexfuzzing(self, text, VT):
        import string
        import re
        async def TextGen(ch):
            Payed = []
            pay = await self.Payed(type=VT) 
            if ch in text:
                parts = text.split(ch)
                for x in range(len(parts) - 1):
                    before_separator = ch.join(parts[:x + 1])
                    after_separator = ch.join(parts[x + 1:])
                    
                    # Generating variations using each element from `pay`
                    for y in sorted(list(set(pay))):
                        Payed.append(before_separator + y + ch + after_separator)
                        Payed.append(f"{y}{text}")
                        Payed.append(f"{text}{y}")
                    for i in set(await self.abnormalizer(text=text)):
                        Payed.append(i)
            return Payed

        async def Main():
            final = set() 
            for ch in string.punctuation:
                generated_texts = await TextGen(ch=ch)
                final.update(generated_texts)  
            return sorted(final) 

        return await Main()

    async def abnormalizer(self, text):
        from utils import abnormalizer
        return abnormalizer.main(text=text)
    

    async def Email_Pay(self, A, V, AD, Type=None):
        Genarated = []
        Pay_char = await self.Payed(type=self.VT)
        for xx in sorted(set(Pay_char)):
            #victim@mail.com@attackr@mail.com
            Genarated.append(f"{A}{xx}{V}")
            #name@Victim.com&attacker.com
            Genarated.append(f"{V}{xx}{AD}")
            #Array of emails
            Genarated.append(f"[{V}{xx}{A}]") 
        return Genarated 
    
    async def HPP(self, Type=None):
        print("HPP")

    async def run(self, Type=None):
        if Type == "email":
            result = await self.Email_Pay(A=self.A, V=self.V, AD=self.AD)
            if result:
                for x in result:
                    print(x)
        elif Type == "rff":
            result = await self.regexfuzzing(text=self.text, VT=self.VT)
            if result:
                for x in result:
                    print(x)
