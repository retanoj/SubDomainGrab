# coding:utf-8

import argparse
from Layer.Layer import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="子域名挖掘机Python版")
    parser.add_argument("-d", "--domain",
                        metavar="", help="Target domain.")
    parser.add_argument("-t", "--timeout", type=int,
                        metavar="", help="Global timeout.")
    parser.add_argument("-p", "--ports",
                        metavar="", help="Ports to scan, default:[80,443].")
    parser.add_argument("--dict", dest="dicPath",
                        metavar="", help="Dictionary path.")
    parser.add_argument("--checkport", dest="checkPorts", action="store_true", default=False,
                        help="Check ports.")
    parser.add_argument("--checkserver", dest="checkServer", action="store_true", default=False,
                        help="Check server type.")
    parser.add_argument("--no-crawl", dest="noCrawlMode", action="store_true", default=False,
                        help="Close crawl mode.")
    parser.add_argument("--no-brute", dest="noBruteMode", action="store_true", default=False,
                        help="Close brute mode.")
    parser.add_argument("--slow", action="store_true", default=False,
                        help="Enable slow scan mode.")
    parser.add_argument("--simhash", action="store_true", default=False,
                        help="Enable Simhash.(It's Slow!!)")
    args = parser.parse_args()
    main(args)