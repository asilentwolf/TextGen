#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
import asyncio
from urllib.parse import urlparse
import aiofiles
import re
from utils import generator

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
    parser.add_argument('-vt', '--vt', help="Vector Type")
    parser.add_argument('-text', '--text', help="To text for Gen")
    parser.add_argument('-o', '--out', help="For file OUTPUT")
    parser.add_argument('-a', '--a', help='Attackr identifier, Vectors and Others')
    parser.add_argument('-v', '--v', help='Victim identifier, Vectors and Others')
    parser.add_argument('-ad', '--ad', help='Attacker Doamin tld or other things')
    parser.add_argument('-type', '--type', help='rff To FUZZ Regex')
    parser.add_argument('-peram', '--peram', help='Peram Name To Work')


    args = parser.parse_args()
    
    #VType
    if args.vt is not None:
        vtype = args.vt
    else:
        vtype = 'all'
    
    #A,V and AD args
    if args.a:
        Attacker = args.a
    else:
        Attacker = None
    if args.v:
        Victim = args.v
    else:
        Victim = None
    if args.ad:
        AttackerD = args.ad
    else:
        AttackerD = None
    
    if args.type:
        Type = args.type
    else:
        Type = None
    
    if args.text:
        Text = args.text
    else:
        Text = None

    Gen = generator.Main(text=Text, AD=AttackerD, A=Attacker, V=Victim, VT=vtype)
    await Gen.run(Type=Type)    
        
if __name__ == "__main__":
    print(logo)
    asyncio.run(argparser())