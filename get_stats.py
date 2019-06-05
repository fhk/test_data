import os
from time import gmtime, strftime
from io import StringIO
import cProfile, pstats
from collections import namedtuple

from solve import main as runner

AREAS = ["500", "1000", "5000", "10000"]
METHOD = ["pmed", "sp", "pcst", "pamp", "nfmp"]


fakeArgs = namedtuple('fakeArgs', ['data', 'method'])


def main():
    for area in AREAS:
        for method in METHOD:
            pr = cProfile.Profile()
            pr.enable()
            fake_arg = fakeArgs(area, method)
            pr.enable()
            runner(fake_arg)
            pr.disable()
            s = StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            t_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            with open(f"{area}.{method}.{t_stamp}.txt", "w") as t_out:
                t_out.write(s.getvalue())


if __name__ == "__main__":
    main()
