# coding:utf-8
import os

LayerPath = os.path.split(os.path.realpath(__file__))[0]

fake_headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
}

# 全局超时时间
timeout = 3

# 线程池大小
poolNum = 100

# DNS服务器
dnsServer = "119.29.29.29"

# 待扫描服务器端口
ports = [80, 443]

# 扫描端口开关
checkPorts = False

# 扫描服务器类型开关
checkServer = False

dicPath = os.path.join(LayerPath, 'dic', 'subnames.txt')
