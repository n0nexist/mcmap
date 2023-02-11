#!/usr/bin/env python
# MCMAP made by github.com/n0nexist
# www.n0nexist.gq
import os
import modules.python.ping
import modules.python.logger
import threading


# clear screen & print logo
os.system("clear")
print("""\033[36m                                                                        
.sSSSsSS SSsSSSSS .sSSSSs.    .sSSSsSS SSsSSSSS .sSSSSs.    .sSSSSs.    
S SSS  SSS  SSSSS S SSSSSSSs. S SSS  SSS  SSSSS S SSSSSSSs. S SSSSSSSs. 
S  SS   S   SSSSS S  SS SSSS' S  SS   S   SSSSS S  SS SSSSS S  SS SSSSS 
S..SS       SSSSS S..SS       S..SS       SSSSS S..SSsSSSSS S..SS SSSSS 
S:::S       SSSSS S:::S SSSSS S:::S       SSSSS S:::S SSSSS S:::SsSSSSS 
S;;;S       SSSSS S;;;S SSSSS S;;;S       SSSSS S;;;S SSSSS S;;;S       
S%%%S       SSSSS S%%%S SSSSS S%%%S       SSSSS S%%%S SSSSS S%%%S       
SSSSS       SSSSS SSSSSsSSSSS SSSSS       SSSSS SSSSS SSSSS SSSSS     

                \033[33m[\033[0ma script made by \033[36mwww.n0nexist.gq\033[33m]
                       [\033[0mgithub.com/n0nexist\033[33m]
\033[0m""")

import sys

# try to import nmap
try:
    import nmap
except ImportError:
    print("\033[31m[\033[0m-\033[31m]\033[33m ERROR\033[36m =>\033[31m RUN 'pip3 install python-nmap' ON YOUR SYSTEM AND RESTART THE SCRIPT\033[0m")
    exit(1)

# parse arguments
myhost = ""
myports = ""
try:
    myhost = sys.argv[1]
    myports = sys.argv[2]
except:
    print(f"\033[31m[\033[0m-\033[31m]\033[33m ERROR\033[36m =>\033[31m {sys.argv[0]} (host/range) (portstart-portend)\033[0m")
    exit(2)
    
print("* initializing scanner...")

# initialize the nmap scanner
nm = nmap.PortScanner()

# start logging
modules.python.logger.startlogging(myhost, myports)

# scan the specified hosts and ports
# with the specified arguments
nm.scan(hosts=myhost, arguments=f'-p {myports}')

print("* pinging and checking...")

# iterate through each host
for host in nm.all_hosts():
    # iterate through each open port
    # for the specific host
    for port in nm[host].all_tcp():
        if nm[host]['tcp'][port]['state'] == 'open':
            threading.Thread(target=modules.python.ping.pinghost,args=(host,port,)).start()