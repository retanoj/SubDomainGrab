# coding:utf-8

from multiprocessing.dummy import Pool
from Layer.func.Tools import *


class domainBrute(object):
    def __init__(self, domain):
        self.domain = domain

    def start(self):
        pool = Pool(config.poolNum)
        for _prefix in globals.domainPrefix:
            pool.apply_async(analysisDomain, args=(_prefix + '.' +self.domain,))
        pool.close()
        pool.join()