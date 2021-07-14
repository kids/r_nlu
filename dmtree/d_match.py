# -*- coding: utf-8 -*-

import os
import base64
from trpc import context
from trpc.log import logger
from trpc_wecar_roi_s_app_wecar_roi_dmtree import rpc, dmtree_pb2 as pb
from utils import Utils
from pregex import PReg
from pmodel import PModel
from ptrie import PTree


class UService():
    def __init__(self):
        rpath = os.path.dirname(__file__)
        self.reg = Utils.build_reg(os.path.abspath(
            os.path.join(rpath, 'rmap.txt')))
        self.tree = Utils.build_tree(os.path.abspath(
            os.path.join(rpath, 'ocslots.txt')))
        self.dmap = Utils.dmapping(os.path.abspath(
            os.path.join(rpath, 'dmap.txt')))
        self.smap = Utils.smapping(os.path.abspath(
            os.path.join(rpath, 'smap.txt')))
        self.mslot = PTree(self.tree, self.dmap)
        self.mreg = PReg(self.reg)
        # TODO put on rainbow and Polaris
        mdlurl = base64.b64decode(
            b'aHR0cDovLzEwOS4yNDQuMjU1LjE0OjgwODAvZG0/c3RyPQ==').decode()
        sentence_cut_len = 29
        self.mmdl = PModel(mdlurl, sentence_cut_len)
        self.sentence_max_len = 128

    def __call__(self, qtext):
        # preprocessing
        qtext = Utils.qstrip(qtext)
        segs = self.mslot.match_slots(qtext)
        logger.info('trie matched {}'.format(segs))

        # trie match
        tdomain, tintent, tslots = self.mslot.match_domain(segs)
        logger.info('domain matched with {}, {} and {}'.format(
            tdomain, tintent, tslots))

        # reg match
        rdomain, rslots = self.mreg(qtext)
        logger.info('regex matched with {} and {}'.format(
            rdomain, rslots))
        if rdomain:
            return rdomain, tintent, rslots

        # mdl match
        if len(qtext) < self.sentence_max_len:
            if not tdomain or not tslots:
                tdomain, mslots = self.mmdl.mdl_parse(qtext)
                logger.info('model parsed with {} and {}'.format(
                    tdomain, mslots))
                if len(mslots):
                    tslots = mslots

        # post processing
        tdomain, tslots = self.reformat(qtext, tdomain, tslots, segs)
        logger.info('reformated to {} and {}'.format(
            tdomain, tslots))
        return tdomain, tintent, tslots

    def reformat(self, text, domain, slots, segs):
        tdomain = domain if domain not in self.dmap else self.dmap[domain][0]
        tslots = []
        for s in slots:
            text = text.replace(s[1], s[1].join(['|', '|']))
        text = [i for i in text.split('|') if i]

        d_text_type = {i[1]: i[0] for i in slots}
        logger.debug(f'd_text_type:{d_text_type}')
        logger.debug(f'text:{text}')

        for i, w in enumerate(text):
            if w not in d_text_type:
                sw = [[s[1][0], s[0]] for s in segs
                     if s[0] in w and len(s[1])==1 and 'intent' not in s[1][0]]
                logger.info(f'seg sw:{sw}')
                for s in sw:
                    tslots.append(s)
                continue

            sw = [s for s in segs if s[0] == w] # s: [stext: [stype]]
            logger.info(f'sw:{sw}')
            if sw:
                s_retro_type = [s_type for s_type in sw[0][1]
                     if d_text_type[w] in s_type]
                if s_retro_type:
                    logger.info('s_retro_type:{}'.format(s_retro_type))
                    if len(s_retro_type) != 1:
                        logger.error('multiple retro slot type matched: {}'.format(
                            s_retro_type))
                    tslots.append([s_retro_type[0], w])
                    continue

            w_type = d_text_type[w]
            if w_type not in self.smap:
                tslots.append([w_type, w])
                continue

            logger.info(f'{w} relative smap:{self.smap[w_type]}')
            cname = []
            for rule in self.smap[w_type]:
                if rule.startswith('equal'):
                    if w == rule.split('.')[-1] and \
                        self.smap[w_type][rule] == 'slot.toremove':
                        cname = []
                        break
                if rule.startswith('unequal'):
                    tomatch = rule.split('.')[-1]
                    if len(w) == len(tomatch) and w != tomatch and \
                        self.smap[w_type][rule] == 'slot.toremove':
                        cname = []
                        break
                if rule.startswith('startswith') and 'slot.removeit' == self.smap[w_type][rule]:
                    if w.startswith(rule.split('.')[-1]):
                        w = w.lstrip(rule.split('.')[-1])
                if rule.startswith('with.slot') and 'slot.removeit' == self.smap[w_type][rule]:
                    sw = [[s[1][0], s[0]] for s in segs
                        if s[0] in w and len(s[1])==1 and rule.split('.', 1)[1] == s[1][0]]
                    if sw and w.endswith(sw[0][1]):
                        tslots.append(sw[0])
                        w = w.rstrip(sw[0][1])
                if rule.startswith('left.with'):
                    if i > 0 and rule.split('.')[-1] in text[i - 1]:
                        cname.append(self.smap[w_type][rule])
                if rule.startswith('left.equal'):
                    if i > 0 and rule.split('.')[-1] == text[i - 1]:
                        cname.append(self.smap[w_type][rule])
                if rule.startswith('right.with'):
                    if i < len(text) - 1 and rule.split('.')[-1] in text[i + 1]:
                        cname.append(self.smap[w_type][rule])
                if rule.startswith('right.equal'):
                    if i < len(text) - 1 and rule.split('.')[-1] == text[i + 1]:
                        cname.append(self.smap[w_type][rule])
                if rule.startswith('domain'):
                    if rule == domain:
                        cname.append(self.smap[w_type][rule])
                if rule == '':
                    cname.append(self.smap[w_type][rule])
            if len(cname) > 0:
                # TODO a ranking dict
                cname = sorted(cname, key=lambda k: k.count('.'))[-1]
                tslots.append([cname, w])

        return tdomain, tslots



class DMatchServicer(rpc.DMatchServicer):
    """Provides methods that implement functionality of nlu servicer."""

    def __init__(self):
        self.runner = UService()

    async def MatchStr(self, ctx: context.Context, request: pb.ReqBody) -> pb.RepBody:
        logger.info(request, request.msg)
        tdomain, tintent, tslots = self.runner(request.msg)

        rsp = pb.RepBody()
        rsp.domain = tdomain
        rsp.intent = tintent
        rsp.status = 0
        rsp.errmsg = ''
        for aslot in tslots:
            oneslot = pb.Slot()
            oneslot.sname = aslot[0]
            oneslot.stext = aslot[1]
            rsp.slots.extend([oneslot])
        return rsp


if __name__ == '__main__':
    dms = DMatchServicer()
