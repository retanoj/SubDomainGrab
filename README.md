# 子域名挖掘机Python版

努力还原Seay牛C#版的《Layer子域名挖掘机》，再改进:)



### 备注

---

1. 原字典太大了。添加了个小字典，取自subDomainsBrute
2. 程序采用multiprocessing.dummy的多线程方式。考虑过用gevent，综合来看都差不多 ( 太快了都会跑死DNS :(
3. 还原版放在分支original
4. 改进版添加了DNS列表，每次解析随机挑选一个DNS Server
5. 改进版添加了两个网页抓取域名记录，取自wydomain ( 还是感觉wydomain好用一点


### Todo.

---

1. 输出报告

