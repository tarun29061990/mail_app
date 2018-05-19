import cProfile
import contextlib
import pstats
import logging

from io import StringIO


@contextlib.contextmanager
def profiled():
    pass
    # pr = cProfile.Profile()
    # pr.enable()
    # yield
    # pr.disable()
    # s = StringIO()
    # ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    # ps.print_stats()
    # # uncomment this to see who's calling what
    # # ps.print_callers()
    # logging.info(s.getvalue())
