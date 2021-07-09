# -*- coding: utf-8 -*-

import logging
import os
import sys

# add the stub to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "stub")))  # noqa
if __name__ != '__main__':  # noqa
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # noqa

import trpc

try:
    # import sdk and plugins
    import tconf
    import tjg_opentracing
    import trpc_log_atta
    import trpc_metrics_m007
    import trpc_metrics_runtime
    import trpc_naming_polaris
    import trpc_opentracing_tjg

except ImportError as e:
    logging.exception("fail to import plugins")
    # raise e

from trpc_wecar_roi_s_app_wecar_roi_dmtree import rpc

from d_match import DMatchServicer



def serve(conf_path):
    svr = trpc.new(conf_path)

    rpc.register_DMatchServicer_server(svr, DMatchServicer())

    svr.serve()


def main():
    config = os.path.abspath(os.path.join(os.path.dirname(__file__), "trpc_python.yaml"))
    logging.info("load config %s", config)
    serve(config)


if __name__ == '__main__':
    sys.exit(main())
