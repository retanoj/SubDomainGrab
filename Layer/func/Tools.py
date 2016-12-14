# coding:utf-8

import collections
import logging
import os
import re
import requests
import random
import socket
import time
import traceback
from struct import unpack

import Layer.Globals as globals
import Layer.Config as config
from DnsResolver import DnsResolver

PortCache = collections.defaultdict(list)  # {host:[ports]}

def randomStr(n=5):
    return ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(16)))[:n]


def ip2long(ip_addr):
    return unpack("!L", socket.inet_aton(ip_addr))[0]


def innerIp(ip):
    ip = ip2long(ip)
    return ip2long('127.0.0.0') >> 24 == ip >> 24 or \
            ip2long('10.0.0.0') >> 24 == ip >> 24 or \
            ip2long('172.16.0.0') >> 20 == ip >> 20 or \
            ip2long('192.168.0.0') >> 16 == ip >> 16


def is_domain(domain):
        domain_regex = re.compile(
            r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z',
            re.IGNORECASE)
        return True if domain and domain_regex.match(domain) else False


def CheckExtensiveDomain(domain):
    isExtensiveDomain = False
    for i in xrange(3):
        checkdns = DnsResolver(randomStr(8) + '.' + domain, config.dnsServer, config.timeout)
        if checkdns.isSuccess:
            isExtensiveDomain = True
            for item in checkdns.Records:
                globals.blackIp.append(item)

    globals.blackIp = list(set(globals.blackIp))
    return isExtensiveDomain


def ScanPort(host, ports):
    if host in PortCache:
        return PortCache.get(host)

    logging.debug("ScanPort on %s" % host)
    openPorts = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(config.timeout)
            s.connect((host, int(port)))
            s.close()
            del s

            openPorts.append(port)
        except Exception, e:
            pass

    if len(openPorts) > 0:
        if host not in PortCache:
            PortCache[host] = openPorts
    logging.debug("Port open on %s: [%s]" % (host, '|'.join(map(lambda _:str(_),openPorts))) )
    return openPorts


def CheckWeb(url):
    try:
        logging.debug("CheckWeb on %s" % url)
        req = requests.head(url, headers=config.fake_headers, timeout=config.timeout, verify=False)
        return req.headers.get("Server", "")
    except Exception, e:
        logging.error("CheckWeb on %s: %s" % (url, str(e)) )

    return ""


def analysisDomain(domain):
    if domain in globals.domainCache: return  # 查过的domain
    if globals.curr_mode != globals.BRUTE_MODE: # 爆破模式字典已去重, 不插入缓存。
        globals.domainCache.insert(domain)

    logging.info("analysis domain %s" % domain)
    _dnsServer = random.choice(config.dnsServerList)
    dns = DnsResolver(domain, dnsServer=_dnsServer, timeout=config.timeout)
    if not dns.isSuccess:
        return  # 解析失败
    _domain_data = globals.DomainData(domain)
    _domain_data.A_Records = dns.Records

    _white_ip = None
    for ip in dns.Records:
        if ip not in globals.blackIp and not innerIp(ip):
            _white_ip = ip
            break
    if not _white_ip:
        globals.domainList.insert(_domain_data)
        return  # 全部命中黑名单(泛解析, 内网IP)

    if config.checkPorts:
        openPorts = ScanPort(_white_ip, config.ports)
        _domain_data.ports = openPorts

    if config.checkServer:
        if 80 in _domain_data.ports:
            _domain_data.server = CheckWeb("http://" + domain)
        elif 443 in _domain_data.ports:
            _domain_data.server = CheckWeb("https://" + domain)

    globals.domainList.insert(_domain_data)