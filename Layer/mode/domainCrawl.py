# coding:utf-8

import logging
import re
from multiprocessing.dummy import Pool

import Layer.Config as config
from Layer.func.Tools import analysisDomain, is_domain, send_http


class domainCrawl(object):
    def __init__(self,  domain):
        self.domain = domain

    def start(self):
        domains = []

        _ilinks = self.__ilinks()
        if len(_ilinks) > 0:
            domains.extend(_ilinks)
            domains = list(set(domains))

        _chinaz = self.__chinaz()
        if len(_chinaz) > 0:
            domains.extend(_chinaz)
            domains = list(set(domains))

        pool = Pool(config.poolNum)
        pool.map_async(analysisDomain, domains)
        pool.close()
        pool.join()

    def __ilinks(self):
        url = "http://i.links.cn/subdomain/"
        domain_re = r"id=domain\d+\s+value=\"http://(.*)\"><input"
        _fake_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "http://i.links.cn/subdomain/"
        }

        data = {"domain": self.domain, "b2": 1, "b3": 1, "b4": 1}

        result = []
        try:
            req = send_http('post', url, headers=_fake_headers, payload=data, timeout=config.timeout * 2)
            req.encoding = 'GBK'
            content = req.text
            _domain = re.findall(domain_re, content)
            result = filter(lambda x: x.endswith('.' + self.domain), _domain)
            logging.info("Crawl %d links from ilinks" % len(result))
        except Exception, e:
            logging.error("Enumerate Subdomain Error: %s" % str(e))

        return result

    def __chinaz(self):
        url = 'http://alexa.chinaz.com/?domain={0}'.format(self.domain)

        result = []
        try:
            r = send_http('get', url, timeout=config.timeout * 2).content
            subs = re.compile(r'(?<="\>\r\n<li>).*?(?=</li>)')
            _domain = subs.findall(r)
            for sub in _domain:
                if is_domain(sub):
                    result.append(sub)
            logging.info("Crawl %d links from chinaz" % len(result))
        except Exception, e:
            logging.error("Enumerate Subdomain Error: %s" % str(e))
        return result