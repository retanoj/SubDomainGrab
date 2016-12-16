# 子域名挖掘机Python版

努力还原Seay牛C#版的《Layer子域名挖掘机》，再改进:)



### 备注

---

1. 还原版放在分支original
2. 程序采用multiprocessing.dummy的多线程方式。考虑过用gevent，综合来看都差不多 ( 太快了都会跑死DNS :(
3. 原字典太大了。添加了个小字典，取自subDomainsBrute
4. 改进版添加随机挑选DNS Server解析模式
5. 改进版添加了文本相似度判断（很慢！），用以应对泛解析和虚拟主机同在的问题


### Todo.

---

