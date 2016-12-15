# coding:utf-8

import dns.resolver
import dns.name
import logging

class DnsResolver(object):
    def __init__(self, domain, dnsServer="119.29.29.29", timeout=2):
        self.Domain     = domain
        self.DnsServer  = dnsServer if isinstance(dnsServer, list) else [dnsServer]
        self.TimeOut    = timeout
        self.Records    = []
        self.isSuccess  = False

        self.Dig()

    def Dig(self):

        dnsClient = dns.resolver.Resolver()
        # dnsClient.domain = dns.name.from_text('.')
        dnsClient.nameservers = self.DnsServer
        dnsClient.timeout     = self.TimeOut
        dnsClient.lifetime    = self.TimeOut

        try:
            dnsMessage = dnsClient.query(self.Domain)
            for dnsRecord in dnsMessage.response.answer:
                for item in dnsRecord.items:
                    if item.rdtype == dns.rdatatype.from_text('A'):
                        self.isSuccess = True
                        self.Records.append(item.address)
        except dns.resolver.Timeout:
            dnsClient.nameservers = ["119.29.29.29"]
            try:
                dnsMessage = dnsClient.query(self.Domain)
                for dnsRecord in dnsMessage.response.answer:
                    for item in dnsRecord.items:
                        if item.rdtype == dns.rdatatype.from_text('A'):
                            self.isSuccess = True
                            self.Records.append(item.address)
            except Exception, e:
                logging.error("DnsResolver %s on %s: %s" % (dnsClient.nameservers[0], self.Domain, str(e)) )
                self.isSuccess = False
        except Exception, e:
            logging.error("DnsResolver %s on %s: %s" % (dnsClient.nameservers[0], self.Domain, str(e)) )
            self.isSuccess = False