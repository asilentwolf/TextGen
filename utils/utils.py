#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import re
from urllib.parse import urlparse, quote
import os
from random import choice
import warnings
import tempfile
import urllib.parse
import random
import html

warnings.filterwarnings("ignore")    # ignor any warning in teminal
stdinX = ""     #None value will provide an error

if sys.stdin.isatty():
    pass
else:
   stdinX = sys.stdin.read().strip()

words = None
Worker = None   #Threads
proxy = None
Concurrency = None
TargetHost = None
rawff = None
url = None
pathx = None
header = None
host = None
body = None
datax = None
query = None
frag = None
netloc = None
scheme = None
METHODS = None
reqtype = None

#regex...
POST = re.match(r"(POST)\s+([^ ]+)", stdinX)
GET = re.match(r"(GET)\s+([^ ]+)", stdinX)
PUT = re.match(r"(PUT)\s+([^ ]+)", stdinX)
http = re.compile(r'^http')
GETx = re.compile(r"(GET)\s+([^ ]+)")
POSTx = re.compile(r"(?i)(POST|PUT)\s+([^\s]+)(?:\s+HTTP/\d\.\d)?")
Jsonx = re.compile(r'(\{(?:[^{}]|\{.*?\})*\}|\[(?:[^\[\]]|\[.*?\])*\])(,?\s*)', re.DOTALL)

try:
    if sys.stdin.isatty():
        pass

    elif http.search(stdinX):
        reqtype = 'get'
        url = stdinX
        rawff = stdinX
        parsed_url = urlparse(url)
        pathx = parsed_url.path
        host = parsed_url.hostname
        query = parsed_url.query
        fullpathx = f"{pathx}?{query}"
        frag = parsed_url.fragment
        netloc = parsed_url.netloc
        scheme = parsed_url.scheme

    elif GETx.search(stdinX) and not http.search(stdinX):
        #Do Not include space in last at req.txt
        reqtype = 'get'
        rawff = stdinX
        raw_requests = rawff.split('\n\n')
        for raw in raw_requests:
            exclude_key = 'Host'
            rawx = raw.strip().split('\n')
            firstline = rawx[0]
            d = raw_requests[-1]
            datax = None
            match = re.match(r"(GET)\s+([^ ]+)", firstline)
            if match:
                fullpathx = match.group(2)
                pathx = '?'.join(fullpathx.split('?')[:1])
                parsed_url = urlparse(url)
                query = parsed_url.query
                if query:
                    query = query
                else:
                    query = None
                dictx = dict(line.split(": ", 1) for line in rawx[1:])
                host = dictx.get('Host', '')
                url = f"https://{host}{fullpathx}"
                if exclude_key in dictx:
                    del dictx[exclude_key]
                    header = dictx
                else:
                    pass

    elif POSTx.match(stdinX) and not Jsonx.findall(stdinX):
        reqtype = 'post'
        rawff = stdinX
        raw_requests = rawff.split('\n\n')
        for raw in raw_requests:
            exclude_key = 'Host'
            rawx = raw.strip().split('\n')
            firstline = rawx[0]
            d = raw_requests[-1]
            datax = d
            query = datax
            match = re.match(r"(POST|PUT)\s+([^ ]+)", firstline)
            if match:
                pathx = match.group(2)
                fullpathx = pathx
                dictx = dict(line.split(": ", 1) for line in rawx[1:])
                host = dictx.get('Host', '')
                url = f"https://{host}{pathx}"
                if exclude_key in dictx:
                    del dictx[exclude_key]
                    header = dictx

    elif Jsonx.findall(stdinX):
        try:
            jsondict = {}
            reqtype = 'json'
            rawff = stdinX
            raw_requests = rawff.split('\n\n')
            for raw in raw_requests:
                exclude_key = 'Host'
                rawx = raw.strip().split('\n')
                firstline = rawx[0]
                d = raw_requests[-1]
                datax = d
                query = datax
                jsondict.update(json.loads(datax))
                match = re.match(r"(POST|PUT)\s+([^ ]+)", firstline)
                if match:
                    fullpathx = match.group(2)
                    pathx = match.group(2)
                    dictx = dict(line.split(": ", 1) for line in rawx[1:])
                    host = dictx.get('Host', '')
                    url = f"https://{host}{pathx}"
                    if exclude_key in dictx:
                        del dictx[exclude_key]
                        header = dictx
                else:
                    pass
        except Exception as e:
            print(f"JSON Errors: {e}")
    else:
        pass

    if POST:
        METHODS = 'POST'
    elif GET:
        METHODS = 'GET'
    elif PUT:
        METHODS = 'PUT'
    else:
        METHODS = 'GET'

except NameError as e:
    print(f"An error occurred: {e}")

#db
currentdirectory = os.path.dirname(os.path.realpath(__file__))
os.chdir(currentdirectory)
agenttext = os.path.join(currentdirectory, '..', 'db/HTTP/User-Agents.txt')
profilefile = os.path.join(currentdirectory, '..', 'db/HTTP/Profiles.txt')
Methodsf = os.path.join(currentdirectory, '..', 'db/HTTP/Methods.txt')


chunksize = 30
with open(agenttext, "r") as file:
    user_agents = [line.strip() for line in file]
    UserAgent = choice(user_agents)

with open(profilefile, "r") as pfile:
    P = [line.strip() for line in pfile]
    ProfilesX = choice(P)


#Usefull func...
def make_Clean(html):
    url_pattern = re.compile(
        r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?' +    # Matches Base64 strings (minimum length of 20 for practical use)
        r'|[^\s]{20,}' +                                                       # Matches non-whitespace characters (including long sequences)
        r'|(\?[^\s]*=X(?:&[^\s]*=[^\s]*)*)?' +                                 # Matches optional query parameters
        r'|"[^"]+"\s*:\s*"[^"]*X"'                                             # Matches JSON key-value pairs with values ending in 'X'
    )
    
    text = re.sub(url_pattern, '', html)
    return text.strip()

def deduplicate(text):
  input_lines = set(text.split("\n"))
  return "\n".join(input_lines)

def wordsfromresp(url):
    from utils import WordsGen
    import requests as r
    headers = {
        "User-Agent": ProfilesX,
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i"

    }
    if header:
        headers.update(header)
    else:
        pass
    if datax:
        data = datax
    else:
        data = None
    try:
        req = r.get(url=url, data=data, proxies=proxy, headers=headers, allow_redirects=False, verify=False, timeout=10)
        resp = str(req.text)
        keys = WordsGen.main(resp)
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".txt") as tempwords:
            for x in keys:
                w = x
                tempwords.write(w + "\n")
            return tempwords.name
    except:
        pass

def Domaintoip(domain):
    import socket
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        print(f"Error: {e}")
        return None