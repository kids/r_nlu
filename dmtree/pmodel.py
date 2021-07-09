# -*- coding: utf-8 -*-

import json
import requests
from trpc.log import logger

class PModel():
    '''parse by model'''
    def __init__(self, mdlurl, len_cut):
        self.mdlurl = mdlurl
        self.len_cut = len_cut

    def _mdl_req(self, q):
        '''making http request to model server'''
        try:
            a = requests.get(self.mdlurl + q).text
            b, c = a.split(' = ')
            b, c = b.split(':'), json.loads(c.replace("'", '"'))
            # logger.debug(a, b, c)
            cc = []
            # combine continous non-repeating slots
            for i in range(len(c)):
                if i > 0 and c[i][0] == c[i - 1][0] and c[i - 1][1] != c[i][1] \
                        and c[i - 1][1] + c[i][1] in q:
                    cc[-1] = [cc[-1][0], cc[-1][1] + c[i][1],
                              min(cc[-1][2], c[i][2])]
                else:
                    cc.append(c[i])
            # domain:str, [[slot_type:str, slot_text:str, slot_score:float]]
            return b, cc
        except Exception as e:
            logger.warning(e)
            return str(e)

    def mdl_parse(self, q: str) -> (str, []):
        rq = []
        tdomain = ''
        if len(q) > self.len_cut:
            for qs in q.split('。'):
                if len(qs) <= self.len_cut:
                    rq.append(self._mdl_req(qs))
        else:
            rq.append(self._mdl_req(q))
        tdomain = [i[0] for i in rq if not isinstance(i, str) and i[0][0] != 'domain.non']
        if len(tdomain) >= 1:
            tdomain = sorted(tdomain, key=lambda k: float(k[1]))[-1][0]
        else:
            tdomain = 'domain.non'
        # [[slot_type:str, slot_text:str, slot_score:float]]
        tslots = sum([i[1] for i in rq if not isinstance(i, str)], [])
        return tdomain, tslots
