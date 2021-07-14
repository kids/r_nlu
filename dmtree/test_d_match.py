# -*- coding: utf-8 -*-

import unittest
import logging
import os
import sys

# add the stub to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "stub")))  # noqa


test_logger = logging.getLogger(__name__)
test_logger.setLevel(level=logging.DEBUG)

from d_match import UService

class TestDMatchServicer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDMatchServicer, self).__init__(*args, **kwargs)
        self.runner = UService()

    def test_intergrate_match(self):
        cases = [
            #("查一下导航去王府井，顺路去公司需要多长时间", ('domain.op.geonavi.navi','qa.route',[['slot.object.geoloc.poi.destination', '王府井'], ['slot.object.geoloc.poi.bypass', '公司']])),
            #("2d车头向上", ('domain.op.service.app.page','',[['slot.object.app.apppage', '2d车头向上']])),
            #('我们想顺路去5公里内的地铁站', ('domain.dialog.search.realtime.lbs', '', [['slot.number.withunit', '5公里'], ['slot.object.geoloc.public', '地铁站']])),
            #('打开音乐打开音乐', ('domain.op.service.app', 'move.open', [['slot.object.app.appname', '音乐'], ['slot.object.app.appname', '音乐']])),
            #('放一首五月天的王者无敌', ('domain.op.media.music', 'op.play', [['slot.object.person.singer', '五月天'], ['slot.object.ipname.song', '王者无敌']])),
            #('三里屯在哪里呢', ('domain.dialog.search.realtime.lbs', 'qa.nearby', [['slot.object.geoloc.poi', '三里屯']])),
            #('不去加油站了', ('domain.dialog.search.realtime.lbs', 'move.stop', [['slot.object.geoloc.public', '加油站']])),
            #('不想看全览了', ('domain.op.service.app.page', 'move.stop', [['slot.object.app.apppage', '全览']])),
            #('不要走高速啊', ('domain.dialog.search.realtime.lbs', '', [['slot.property', '不要走高速']])),
            #('变更目的地为天安门附近的地铁站', ('domain.multiple', 'move.switch', [['slot.object.other', '目的'], ['slot.object.other', '天安门附近的地铁站']])),
            #('当前限速', ('domain.op.geonavi.navi', 'qa.speedlimit', [])),
            #('周末限行吗', ('domain.op.geonavi.navi', 'qa.accesslimit', [['slot.number.datetime', '周末']])),
            #('地图缩小三倍', ('domain.op.geonavi.navi', 'op.setting.zoomin', [])),
            #('导航到合作化北路与清溪路交口', ('domain.op.geonavi.navi', '', [['slot.object.geoloc.poi.destination', '合作化北路与清溪路交口']])),
            #('导航到北青公路9665号', ('domain.op.geonavi.navi', '', [['slot.object.geoloc.poi.destination', '北青公路9665号']])),
            #('导航条为黑夜模式', ('domain.op.service.app.page', '', [['slot.object.app.apppage', '黑夜模式']])),
            #('带我去保定市长城南大街1485号世纪汽车城院内', ('domain.op.geonavi.navi', 'op.navi', [['slot.object.geoloc.poi.destination', '保定市长城南大街1485号世纪汽车城院内']])),
            #('开始继续导航', ('domain.op.service.app', 'move.back', [])),
            #('收藏一下这个位置', ('domain.op.geonavi.navi', 'op.save', [['slot.object.geoloc.poi', '这']])),
            #('请为我避开限行', ('domain.dialog.search.realtime.lbs', '', [['slot.property', '避开限行']])),
            #('路上有几个服务区啊', ('domain.dialog.search.realtime.lbs', 'qa.count', [['slot.object.geoloc.public', '服务区']])),
            #('饭店在哪里', ('domain.dialog.search.realtime.lbs', 'qa.nearby', [['slot.object.geoloc.public', '饭店']])),
            ('导航去公司避开限行', ()),
            ('帮忙导航导航', ()),
            ('删除第一个途经点', ()),
            ('北岸中心广场设置为家', ()),
            ('取消中途的加油站', ()),
            ('导航途经佳世客', ()),
            ('换个别的路', ()),
            ('中途路过加油站', ()),
            ('取消途经地点', ()),
            ('这次导航回去的路上看看有没有吃好吃的', ()),
            ('导航至桃村', ()),
            ('导航先暂停', ()),
            ('返回起点', ()),
            ('经过岱黄高速', ()),
            ('导航去公主岭不走高速', ()),
            ('重新规划路线选择高速', ()),
            ('导航去那个东河高速路口', ()),
            ('输入目的地丹马小区', ()),
            ('导航到茂县走最近的路', ()),
            ('计算一下途经淑吕村的路程', ()),
            ('请放大一些', ()),
            ('', ()),
            ('', ()),
        ]
        for case, expected in cases:
            result = self.runner(case)
            test_logger.debug(f'======case:{case}')
            test_logger.debug(f'======result:{result}')
            test_logger.debug(f'======case:{expected}')
            #self.assertEqual(result, expected)

    def test_reg_match(self):
        pass

    def test_trie_match(self):
        pass

    def test_mdl_match(self):
        pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        runner = UService()
        test_logger.debug(runner(sys.argv[1]))
    else:
        unittest.main()
