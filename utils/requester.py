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
import httpx
from utils import utils
import time

warnings.filterwarnings("ignore")    # ignor any warning in teminal


async def Main(Url, Semaphore, H=None, Data=None, Headers=None,
               Cookie=None, Type=None, Method=None, Proxy=None):  
    
    U = ""
    if 'Content-Length' in Headers:
        del Headers['Content-Length']
    try:
        async with Semaphore:  # Limit concurrent 
            start_time = time.time()
            async with httpx.AsyncClient(proxies=Proxy, headers=Headers, verify=False, follow_redirects=False) as client:
                for attempt in range(1):  # Retry up to 1 times
                    try:
                        req = await client.request(method=Method, url=Url, data=Data)
                        end_time = time.time()
                        response_time = end_time - start_time
                        resp = req.text
                        soup = BeautifulSoup(resp, 'html.parser')
                        respheaders = req.headers
                        status_code = req.status_code

                        #count
                        response_length = len(utils.make_Clean(resp))
                        header_length = len(Counter(respheaders.keys()))  
                        count = response_length + header_length                        

                    except (httpx.ConnectTimeout, httpx.ReadTimeout):
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff on timeout
                        continue  # Retry after waiting if a timeout occurred
    except Exception as e:
        #pass
        print(f"An unexpected error occurred for {Url}: {e}")

    finally:
        # Ensure client is closed properly
        await client.aclose()
        pass
        
    await asyncio.sleep(0.005) 
    return U.strip()
