# -*- coding: utf-8 -*-

import re
from trpc.log import logger


class PReg():
    def __init__(self, regmap):
        self.regmap = regmap

    def __call__(self, q):
        domain, slots = '', []
        for reg in self.regmap:
            r = reg.match(q)
            if r:
                slot_texts = r.groups()
                domain, slot_types = self.regmap[reg]
                if len(slot_texts) != len(slot_types):
                    logger.warning('slot matching len not match: \
                        slot_texts are {}, while slot_types are {}'.format(
                            slot_texts,slot_types))
                else:
                    for i,j in zip(slot_types, slot_texts):
                        slots.append([i,j])
                break
        return domain, slots
