# -*- coding: utf-8 -*-

from utils import Utils
from trpc.log import logger


class PTree():
    def __init__(self, tree: {}, dmap: {}):
        self.ttree = tree
        self.dmap = dmap

    def match_slots(self, q):
        q = '<' + q + '>'
        ret = []
        while len(q) > 0:
            rsearch = [[i[0], i[1].l_names] for i in self.ttree.search(q)]
            if not rsearch:
                q = q[1:]
            else:
                rsearch = sorted(rsearch, key=lambda k: len(k[0]))[-1]
                ret.append(rsearch)
                q = q[len(rsearch[0]):]
        ret = [[i.lstrip('<').rstrip('>'),j] for i,j in ret]
        return ret

    def match_domain(self, slots):
        ''' interpret return of dmtree
            Return:
                domain: str
                intent: str
                slots: 
        '''
        tdomain, tintent, tslots = '', '', []
        # domain
        cdomain = [sum([self.dmap[s] for s in ss[1] if s in self.dmap], [])
                   for ss in slots]
        cdomain = Utils.intersect(cdomain)
        # TODO if len(cdomain)>1 -> multi-round
        tdomain = cdomain[0] if len(cdomain) == 1 else ''
        # intent
        cintent = [i for i in sum([ss[1] for ss in slots], [])
                   if 'intent' in i]
        if len(set(cintent)) != 1:
            logger.warning('Mapping data no intent or not only')
        else:
            tintent = cintent[0].split('.', 1)[1]
        # slots
        for aslot in slots:
            if len(aslot[1]) == 1:
                sname = aslot[1][0]
            elif len(aslot[1]) > 1 and tdomain:
                tslot = [s for s in aslot[1] if s in self.dmap
                         and self.dmap[s] == tdomain]
                if not tslot:
                    continue
                sname = tslot[0]
            else:
                continue
            if 'intent' in sname:
                continue
            tslots.append([sname, aslot[0]])
        return tdomain, tintent, tslots


        
