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

import Simhashit as Sim
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


def send_http(method, url, headers={}, payload={}, timeout=config.timeout):
    fake_headers = config.fake_headers.copy()
    fake_headers.update(headers)
    func = getattr(requests, method, 'head')
    if method == 'get' or method == 'head':
        return func(url, headers=fake_headers, timeout=timeout, verify=False)
    elif method == 'post':
        return func(url, headers=fake_headers, data=payload, timeout=timeout, verify=False)
    return None


def CheckExtensiveDomain(domain):
    isExtensiveDomain = False

    count = 0
    for i in xrange(3):
        checkdns = DnsResolver(randomStr(8) + '.' + domain, timeout=config.timeout)
        if checkdns.isSuccess:
            count += 1
    if count == 3:
        logging.warning("%s has extensive domain name analysis" % domain)
        isExtensiveDomain = True

    if isExtensiveDomain:
        if config.simhash:
            try:
                text = send_http('get', 'http://' +randomStr(8) + '.' + domain).text
                globals.itemSampleSim = Sim.sim(text)
            except:
                pass
        for _dnsServer in config.dnsServerList:
            dns = DnsResolver(randomStr(8) + '.' + domain, _dnsServer, config.timeout)
            if dns.isSuccess:
                for item in dns.Records:
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
        req = send_http('head', url)
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
    if config.slow:
        time.sleep(random.random())
    dns = DnsResolver(domain, dnsServer=_dnsServer, timeout=config.timeout)
    if not dns.isSuccess:
        return  # 解析失败

    if globals.curr_mode == globals.BRUTE_MODE: # 爆破模式才检查泛解析IP, 默认信任抓取回来的domain
        _white_ip = None
        for ip in dns.Records:
            if ip not in globals.blackIp:
                _white_ip = ip
                break
        if not _white_ip:
            if config.simhash and globals.itemSampleSim is not None:
                try:
                    text = send_http('get', 'http://'+domain).text
                    if Sim.distance(globals.itemSampleSim, Sim.sim(text)) < 3:
                        logging.debug("Simhash say %s is extensive result" % domain)
                        return # 文本相似
                except Exception, e:
                    logging.error("Simhash Error on %s: %s" % (domain, str(e)))
                    return
            else:
                logging.debug("BlackIp say %s is extensive result" % domain)
                return  # 全部命中黑名单(泛解析)

    _domain_data = globals.DomainData(domain)
    _domain_data.A_Records = dns.Records

    if config.checkPorts and not innerIp(_white_ip):
        openPorts = ScanPort(_white_ip, config.ports)
        _domain_data.ports = openPorts

    if config.checkServer and not innerIp(_white_ip):
        if 80 in _domain_data.ports:
            _domain_data.server = CheckWeb("http://" + domain)
        elif 443 in _domain_data.ports:
            _domain_data.server = CheckWeb("https://" + domain)

    globals.domainList.insert(_domain_data)