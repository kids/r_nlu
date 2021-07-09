# -*- coding: utf-8 -*-
"""
test client
"""
import logging
import os
import sys

# add the stub to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "stub")))  # noqa



from trpc import context
from trpc.client.options import *
from trpc.codec.serialization import SerializationType

from trpc_wecar_roi_s_app_wecar_roi_dmtree import rpc as rpc, dmtree_pb2 as pb

test_logger = logging.getLogger()
test_logger.setLevel(level=logging.DEBUG)


def test_DMatch_MatchStr():
    proxy = rpc.DMatchClientProxyImpl()
    req = pb.ReqBody()
    options = [
        with_target('ip://127.0.0.1:8000'),
        with_protocol('trpc'),
        with_serialization_type(SerializationType.PB),
        with_network('tcp')
    ]
    ctx = context.Context()
    try:
        ret = proxy.MatchStr(ctx, req, options)
        print(ret)
        assert ret is not None
    except Exception as exc:
        test_logger.exception(exc)
        assert 0
    

