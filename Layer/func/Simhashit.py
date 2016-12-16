# coding:utf-8

import re
import simhash


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def sim(text):
    return simhash.Simhash(get_features(text))


def distance(sim1, sim2):
    return sim1.distance(sim2)