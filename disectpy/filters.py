

import packets
import binascii
import contextlib




SHOW = 0x1
# continue dissection of underlying layers
STOP = 0x10
# abort current packet parsing
CONTINUE = 0x100
# do nothing
FILTERS = []
DIG = 0x1000

class AbortDissection(Exception):
    pass

def filter_decorator(f):
    """Wrap filter execution, and translate it's return value
    to exceptions"""
    global FILTERS

    def wrap(p, *args, **kwargs):
        ret = f(p, *args, **kwargs)
        if not ret or not isinstance(ret, int):
            return
        if ret & SHOW:
            p.pprint()
        elif ret & CONTINUE:
            pass
        elif ret & STOP:
            raise AbortDissection
    FILTERS.append(wrap)
    return wrap

@contextlib.contextmanager
def filter_ctx():
    """Wrap packet-parsing code execution,
    in order to allow predicates function to stop execution"""
    try:
        yield
    except AbortDissection:
        pass
    finally:
        pass
#
# filters - precision helpers
#
def on_layer(LayerType):
    def wrap_decorator(f):
        def wrap(p, *args, **kwargs):
            if isinstance(p, LayerType):
                ret = f(p, *args, **kwargs)
                return ret
            return None
        return wrap
    return wrap_decorator
#
# filters
#

@filter_decorator
@on_layer(packets.UDPLayer)
def sampleFilter(p):
    #if isinstance(p, packets.UDPLayer):
    #    return SHOW ^ STOP
    #if isinstance(p, packets.TCPLayer):
    #    return SHOW ^ STOP
    return SHOW ^ STOP

@filter_decorator
def all_packets(p):
    """Let all pass"""
    return CONTINUE

FILTERS = [all_packets]



