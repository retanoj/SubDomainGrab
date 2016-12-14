# 子域名挖掘机Python版

努力还原Seay牛C#版的《Layer子域名挖掘机》，再改进:)



### 备注

---

1. 原字典太大了。添加了个小字典，取自subDomainsBrute。
2. 程序采用multiprocessing.dummy的多线程方式。考虑过用gevent，综合来看都差不多 ( 太快了都会跑死DNS :(
3. 还原版放在分支original



### Todo.

---

1. DNS列表随机模式（缓解DNS限速
2. 输出报告

