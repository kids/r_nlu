# -*- coding: utf-8 -*-

from ttree import Node
import re

class Utils():
    def __init__(self):
        pass

    @staticmethod
    def build_tree(f: str):
        tree = Node('')
        with open(f) as cf:
            for line in cf:
                if ',' not in line or line.startswith('#'):
                    continue
                slottype, name = line.strip().replace(' ','').split(',')[:2]
                tree.add(name.lower(), slottype)
        print(len(tree))
        return tree

    @staticmethod
    def build_reg(f: str) -> {str: (str, [])}:
        regmap = {}
        with open(f) as cf:
            for line in cf:
                if ';' not in line or line.startswith('#'):
                    continue
                regkey, regexp, domain, slots = line.strip().replace(' ','').split(';')
                regmap[re.compile(regexp)] = (domain, slots.split(','))
        return regmap

    @staticmethod
    def dmapping(f: str) -> {}:
        # slot->domain config with weight
        dmap = {}
        with open(f) as cf:
            for line in cf:
                if ';' not in line or line.startswith('#'):
                    continue
                slotname, domains = line.replace(' ', '').strip().split(';')
                domains = domains.split(',')
                dmap[slotname] = domains
        return dmap

    @staticmethod
    def smapping(f :str) -> {}:
        # slot->slot output
        smap = {}
        with open(f) as cf:
            for line in cf:
                if ';' not in line or line.startswith('#'):
                    continue
                slotname, condition, oslot = line.replace(' ', '').strip().split(';')
                if slotname not in smap:
                    smap[slotname] = {}
                smap[slotname][condition] = oslot
        return smap

    @staticmethod
    def intersect(ll):
        '''extract non-empty intersections from list of lists'''
        # ll = [l for l in ll if l]
        ret = ll[0] if ll else []
        for l in ll:
            if not ret:
                break
            ret = [i for i in ret if i in l]
        return ret

    @staticmethod
    def qstrip(s):
        for w in ['请','麻烦','请你','帮我','替我','你好']:
            s = s.lstrip(w)
        for w in ['呢','呀','吧']:
            s = s.rstrip(w)
        s = s.lower().replace(' ','')
        return s

    @staticmethod
    def encode(rsp):
        rsp.domain = rsp.domain.encode('utf-8')
        rsp.intent = rsp.intent.encode('utf-8')
        for s in rsp.slots:
            s.sname = s.sname.encode('utf-8')
            s.stext = s.stext.encode('utf-8')
        return rsp
        

if __name__ == '__main__':
    import os
    mreg = Utils.build_reg(os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'rmap.txt')))
    for reg in mreg:
        print(reg)
        print(reg.match('查一下导航去王府井，顺路去公司需要多长时间').groups())
