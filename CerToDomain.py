# coding=utf-8
'''
    Created on 2019年04月01日
    @info: 主域名扫描器
    @author: heartS
    @version: 1.0
'''
import socket
import requests
import ssl
import re
import sys;
import time;
import os;

flags = """
----------------------------------------------------------------------
    ____ _____ ____ _____ ___  ____   ___  __  __    _    ___ _   _  
   / ___| ____|  _ \_   _/ _ \|  _ \ / _ \|  \/  |  / \  |_ _| \ | | 
  | |   |  _| | |_) || || | | | | | | | | | |\/| | / _ \  | ||  \| | 
  | |___| |___|  _ < | || |_| | |_| | |_| | |  | |/ ___ \ | || |\  | 
   \____|_____|_| \_\|_| \___/|____/ \___/|_|  |_/_/   \_\___|_| \_|                                                                                                                                   
              Coded By heartS (V1.0 RELEASE) email:chyheartS@163.com 
----------------------------------------------------------------------
"""

def getIp(domain):
    ip = ""
    try:
        myaddr = socket.getaddrinfo(domain,'http')
        ip = myaddr[0][4][0]
    except:
        pass;
    return ip;
    
    
def getDomain(ip):
    #ip = getIp('xiaojukeji.com');
    l = list();
    header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding' : 'gzip, deflate',
        'Connection' : 'close',
        'Upgrade-Insecure-Requests' : '1'
        }
    try:
        response = requests.get("https://"+str(ip),headers=header, verify=True,timeout=3);
    except requests.exceptions.SSLError as x:
        #print(str(x));
        l = re.findall("(?:[^\"\'\,\s]|\\.)*(?:[^\"\'\,\s]|\\.)",str(x))
        #print(l)
    except:
        pass;
        
    return l;

if __name__ == '__main__':
    print(flags)
    ips = [];
    domains = [];
    domain = sys.argv[1];
    #domain = "xiaojukeji.com"
    count = 0;
    domains.append(domain);
    outPutFilePath = os.getcwd() + "\\" + str(domain+".txt");
    outPutFile = open(outPutFilePath,'a+')
    outPutFile.write(str(domain)+"\n")
    
    while True:
        #print(count)
        #print(len(domains))
        ip = getIp(domains[count])
        #print("发现一个IP"+str(ip));
        if len(ip) != 0:
            if ip not in ips:
                ips.append(ip);
                
                domainTemp = getDomain(ip);
                if len(domainTemp) != 0:
                    for i in range(7,len(domainTemp),1):
                        #print(domainTemp[i])
                        t = domainTemp[i].replace("*.","");
                        if t not in domains:
                            domains.append(t);
                            print("[+] Found domain："+str(t));
                            outPutFile.write(str(t)+"\n")
        count += 1;
        
        if count >= len(domains):
            break;
        #time.sleep(1);
        ips.append(ip);
        
    outPutFile.close()
