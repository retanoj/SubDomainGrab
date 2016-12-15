# coding:utf-8

import logging
import Colorer
import sys

import Config
import Globals
from func.Tools import *
from mode.domainCrawl import domainCrawl
from mode.domainBrute import domainBrute


def main(args):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%d %b %H:%M:%S')

    domain = getattr(args, 'domain', None)
    if not is_domain(domain):
        logging.error("Please input a valid domain.")
        sys.exit(-1)

    if getattr(args, 'timeout', None):
        Config.timeout = args.timeout
    if getattr(args, 'ports', None):
        ports = map(lambda _:int(_), args.ports.strip('[]').split(','))
        Config.ports = ports
    if getattr(args, 'dicPath', None):
        Config.dicPath = args.dicPath
    if getattr(args, 'checkPorts', False):
        Config.checkPorts = args.checkPorts
    if getattr(args, 'checkServer', False):
        Config.checkServer = args.checkServer
    if getattr(args, 'slow', False):
        Config.slow = args.slow

    if not os.path.exists(Config.dicPath):
        logging.error("%s not exist!" % Config.dicPath)
        sys.exit(-1)

    logging.info("Checking %s has extensive analysis or not" % domain)
    CheckExtensiveDomain(domain)

    if not getattr(args, 'noCrawlMode', False):
        globals.curr_mode = globals.CRAWL_MODE
        domainCrawl(domain).start()

    if not getattr(args, 'noBruteMode', False):
        with open(Config.dicPath, 'rb') as inf:
            for l in inf:
                Globals.domainPrefix.append(l.strip())

        globals.curr_mode = globals.BRUTE_MODE
        domainBrute(domain).start()

    del globals.DomainCache

    report()


def report():
    logging.info("Total got %d" % len(globals.domainList))
    for _domain in globals.domainList.domain_list:
        print _domain.to_json()
