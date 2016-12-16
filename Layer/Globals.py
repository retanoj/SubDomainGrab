# coding:utf-8

import json

# 泛解析黑名单IP
blackIp = []
itemSampleSim = None

# 枚举字典
domainPrefix = []

# 爆破一次任务集的步长
STEP = 10000

# 模式
CRAWL_MODE = 0
BRUTE_MODE = 1
curr_mode = CRAWL_MODE


# 数据结构Domain
class DomainData(object):
    domain = ""
    A_Records = []
    ports = []
    server = ""

    def __init__(self, domain, records=[], ports=[], server=""):
        self.domain = domain
        self.A_Records = records
        self.ports = ports
        self.server = server

    def __str__(self):
        return "Domain: {}, A: [{}], Ports: [{}], Server: '{}'".format(
            self.domain,
            ','.join(self.A_Records),
            '|'.join(map(lambda _:str(_), self.ports)),
            self.server
        )

    def to_json(self):
        return json.dumps({
            "Domain": self.domain,
            "A": self.A_Records,
            "Ports": self.ports,
            "Server": self.server
        })

class DomainList(object):
    domain_list = []

    def insert(self, item):
        if not isinstance(item, DomainData):
            return
        self.domain_list.append(item)

    def __len__(self):
        return self.domain_list.__len__()


class DomainCache(object):
    domain_cache = set()

    def __contains__(self, item):
        return hash(item) in self.domain_cache

    def insert(self, item):
        self.domain_cache.add(hash(item))

# 缓存
domainCache = DomainCache()

# 获取到的域名
domainList = DomainList()