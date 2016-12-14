# coding:utf-8

import logging
import requests
import re
from multiprocessing.dummy import Pool

import Layer.Config as config
from Layer.func.Tools import analysisDomain

class domainCrawl(object):
    def __init__(self,  domain):
        self.domain = domain

    def start(self):
        domains = []

        _ilinks = self.__ilinks()
        if len(_ilinks) > 0:
            domains.extend(_ilinks)
            domains = list(set(domains))

        pool = Pool(config.poolNum)
        pool.map_async(analysisDomain, domains)
        pool.close()
        pool.join()

    def __ilinks(self):
        url = "http://i.links.cn/subdomain/"
        domain_re = r"id=domain\d+\s+value=\"http://(.*)\"><input"
        fake_headers = config.fake_headers.copy()
        _fake_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "http://i.links.cn/subdomain/"
        }
        fake_headers.update(_fake_headers)

        data = {"domain": self.domain, "b2": 1, "b3": 1, "b4": 1}

        result = []
        try:
            req = requests.post(url, headers=fake_headers, data=data, timeout=config.timeout)
            req.encoding = 'GBK'
            content = req.text
            _domain = re.findall(domain_re, content)
            result = filter(lambda x: x.endswith('.' + self.domain), _domain)
            logging.info("Crawl %d links from ilinks" % len(result))
        except Exception, e:
            logging.error("Enumerate Subdomain Error: %s" % str(e))

        return result

