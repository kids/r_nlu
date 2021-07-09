# -*- coding: utf-8 -*-
# Code generated by trpc-go/trpc-go-cmdline. DO NOT EDIT.
# source: dmtree.proto


from typing import List

from trpc import client
from trpc import codec
from trpc import context
from trpc import server

from . import dmtree_pb2 as pb


# DMatchService defines service
class DMatchServicer(object):
    async def MatchStr(self, request: pb.ReqBody, ctx: context.Context) -> pb.RepBody:
        raise NotImplementedError('Method not implemented!')
    

def register_DMatchServicer_server(svr: server.Server, servicer: DMatchServicer):
    desc = server.ServiceDesc("/trpc.wecar_roi_s_app.wecar_roi_dmtree.DMatch",
        [
            server.Method(
                "/trpc.wecar_roi_s_app.wecar_roi_dmtree.DMatch/MatchStr",
                pb.ReqBody,
                pb.RepBody,
                servicer.MatchStr,
                )]
        )

    svr.register(desc)


# client definition
class DMatchClientProxy:
    def MatchStr(self, ctx: context.Context, request: pb.ReqBody, options: List) -> pb.RepBody:
        pass

    async def asyncMatchStr(self, ctx: context.Context, request: pb.ReqBody, options: List) -> pb.RepBody:
        pass

    

class DMatchClientProxyImpl(DMatchClientProxy):
    def __init__(self):
        self.client = client.get_client()
        self.options = {}
    def MatchStr(self, ctx: context.Context, request: pb.ReqBody, options: List=[]) -> pb.RepBody:
        rsp_cls = pb.RepBody
        ctx, msg = codec.clone_client_message(ctx)
        msg.set_client_rpc_name('/trpc.wecar_roi_s_app.wecar_roi_dmtree.DMatch/MatchStr')
        msg.set_callee_service_name('trpc.wecar_roi_s_app.wecar_roi_dmtree.DMatch')
        msg.set_callee_method('MatchStr')
        return self.client.invoke_sync(ctx, request, rsp_cls, options)

    async def asyncMatchStr(self, ctx: context.Context, request: pb.ReqBody, options: List=[]) -> pb.RepBody:
        rsp_cls = pb.RepBody
        ctx, msg = codec.clone_client_message(ctx)
        msg.set_client_rpc_name('/trpc.wecar_roi_s_app.wecar_roi_dmtree.DMatch/MatchStr')
        msg.set_callee_service_name('trpc.wecar_roi_s_app.wecar_roi_dmtree.DMatch')
        msg.set_callee_method('MatchStr')
        rsp = await self.client.invoke(ctx, request, rsp_cls, options)
        return rsp

    