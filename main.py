#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
import asyncio
from urllib.parse import urlparse
import aiofiles
import re
from utils import generator
from utils import utils

#Colors...
class Colors:
    BOLD = '\033[1m'
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'


#Text to display
logo = f"""
        ↗↗
    ↗       ↗
 ↗             ↗
 ---------------------->
 |      {Colors.BOLD}{Colors.CYAN}TextGenV.1 {Colors.RESET}
 | A Vector text generator!
 ---------------------->
 ↖             ↖
    ↖       ↖
        ↖↖
        {Colors.YELLOW}BY @asilentwolf{Colors.RESET}
"""

async def argparser():
    parser = argparse.ArgumentParser()
    # Global arguments
    parser.add_argument('--file', help='File to be processed')
    parser.add_argument('-p', '--proxy', help='Proxy if any (default: None)')
    parser.add_argument('-w', '--worker', type=int, help='Number of Workers (default: 5)')
    parser.add_argument('-c', '--concurrency', type=int, help='Number of concurrency Workers[Use it for multiple Hosts]')
    parser.add_argument('-m', '--method', type=str, help="To Use Method")
    parser.add_argument('-vt', '--vt', help="Vector Type")
    parser.add_argument('-text', '--text', help="To text for Gen")
    parser.add_argument('-o', '--out', help="For file OUTPUT")
    parser.add_argument('-a', '--a', help='Attackr identifier, Vectors and Others')
    parser.add_argument('-v', '--v', help='Victim identifier, Vectors and Others')
    parser.add_argument('-ad', '--ad', help='Attacker Doamin tld or other things')
    parser.add_argument('-type', '--type', help='rff To FUZZ Regex')
    parser.add_argument('-name', '--name', help='Peram Name To Work')
    parser.add_argument('-pay', '--pay', help='Payload Text')
    parser.add_argument('-po', '--printonly', action="store_true", help='Only Print')


    args = parser.parse_args()
    
    #args
    vtype = args.vt if args.vt is not None else 'all'
    Attacker = getattr(args, 'a', None)
    Victim = getattr(args, 'v', None)
    AttackerD = getattr(args, 'ad', None)
    Type = getattr(args, 'type', None)
    Text = getattr(args, 'text', None)
    Name = getattr(args, 'name', None)
    PAY = getattr(args, 'pay', None)
    Data = getattr(utils, 'datax', None)

    if args.printonly:
        Print = True
    else:
        Print = None
    if args.worker is not None:
        utils.Worker = args.worker
    else:
        utils.Worker = 1
    if args.proxy is not None:
        utils.proxy = args.proxy
    else:
        utils.proxy = None
    if args.concurrency is not None:
        utils.Concurrency = args.concurrency
    else:
        utils.Concurrency = 1
    if args.method is not None:
        method = args.method
    else:
        method = utils.METHODS
    if utils.url:
        url = utils.url
    else:
        url = None
    
    if utils.header:
        Headers = utils.header
    else:
        Headers = {
            "User-Agent": utils.UserAgent,
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
    


    Gen = generator.Main(text=Text, Data=Data, AD=AttackerD, Print=Print, Method=method, Headers=Headers,
                         A=Attacker, V=Victim, VT=vtype, Name=Name, PAY=PAY, Proxy=utils.proxy, Url=url)
    await Gen.run(Type=Type)    
        
if __name__ == "__main__":
    print(logo)
    asyncio.run(argparser())