# coding:utf-8

import logging
import requests
import re
from multiprocessing.dummy import Pool

import Layer.Config as config
from Layer.func.Tools import analysisDomain, is_domain

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

        _alexa_cn = self.__alexa_cn()
        if len(_alexa_cn) > 0:
            domains.extend(_alexa_cn)
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
            req = requests.post(url, headers=fake_headers, data=data, timeout=config.timeout * 2)
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
            r = requests.get(url, headers=config.fake_headers, timeout=config.timeout * 2).content
            subs = re.compile(r'(?<="\>\r\n<li>).*?(?=</li>)')
            _domain = subs.findall(r)
            for sub in _domain:
                if is_domain(sub):
                    result.append(sub)
            logging.info("Crawl %d links from chinaz" % len(result))
        except Exception, e:
            logging.error("Enumerate Subdomain Error: %s" % str(e))
        return result

    def __alexa_cn(self):
        def get_sign_alexa_cn():
            url = 'http://www.alexa.cn/index.php?url={0}'.format(self.domain)
            r = requests.get(url, headers=config.fake_headers, timeout=config.timeout * 2).text
            sign = re.compile(r'(?<=showHint\(\').*?(?=\'\);)').findall(r)
            if len(sign) >= 1:
                return sign[0].split(',')
            else:
                return None

        sign = get_sign_alexa_cn()
        if sign is None:
            logging.error("Sign Fetch Failed on alexa_cn")
            return []
        else:
            (domain,sig,keyt) = sign

        pre_domain = self.domain.split('.')[0]

        url = 'http://www.alexa.cn/api_150710.php'
        payload = {
            'url': domain,
            'sig': sig,
            'keyt': keyt,
            }

        result = []
        try:
            r = requests.get(url, headers=config.fake_headers, data=payload, timeout=config.timeout * 2).text

            for sub in r.split('*')[-1:][0].split('__'):
                if sub.split(':')[0:1][0] == 'OTHER':
                    break
                else:
                    sub_name = sub.split(':')[0:1][0]
                    sub_name = ''.join((sub_name.split(pre_domain)[0], domain))
                    if is_domain(sub_name):
                        result.append(sub_name)
            logging.info("Crawl %d links from __alexa_cn" % len(result))
        except Exception, e:
            logging.error("Enumerate Subdomain Error: %s" % str(e))

        return result

