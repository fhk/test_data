"""
Given a set of results for each solution we want to extract the time
data into a table so that we can visualize the results.

Runtime
Method,500,1000,5000,10000
sp_1,X,X,X,X
sp_2...
sp_3...
pmed,X,X,X,X
...
pcst,X,X,X,X
...
nfmp,X,X,X,X
...
spamp,X,X,X,X
...

Footprint
Method,500,1000,5000,10000
sp_1,X,X,X,X
sp_2...
sp_3...
pmed,X,X,X,X
...
...
pcst,X,X,X,X
...
nfmp,X,X,X,X
...
spamp,X,X,X,X
...

# Solve Functions - check value cumtime
"link/link/solve/pmed.py:9(solve)"
"link/link/solve/nfmp.py:12(solve)"
"link/link/solve/pcst.py:10(solve)"
"link/link/solve/spamp.py:13(solve)"
# Util Functions - check value cumtime
"link/link/solve/util.py:108(make_assi_graph)"
"""

import csv
import os
import time
import copy

import geopandas as gpd

AREAS = ["500", "1000", "5000", "10000"]
METHOD = ["sp", "pmed", "pcst", "nfmp", "spamp"]

SOL_FUNC = {
    "sp": "link/link/solve/pmed.py:9(solve)",
    "pmed": "link/link/solve/pmed.py:9(solve)",
    "nfmp": "link/link/solve/nfmp.py:12(solve)",
    "pcst": "link/link/solve/pcst.py:10(solve)",
    "spamp": "link/link/solve/spamp.py:13(solve)"
}

CALC_FUNC = {
    "sp": "link/link/solve/util.py:108(make_assi_graph)",
    "pmed": "link/link/solve/util.py:108(make_assi_graph)",
    "spamp": "link/link/solve/util.py:108(make_assi_graph)"
}

def main():

    files = [(x[0], time.ctime(x[1].st_ctime)) for x in sorted([(fn, os.stat(fn)) for fn in os.listdir(".")], key = lambda x: x[1].st_ctime)]
    output = [
        ["Method", "500", "1000", "5000", "10000"],
        ["sp_1"],
        ["sp_2"],
        ["sp_3"],
        ["pmed_1"],
        ["pmed_2"],
        ["pmed_3"],
        ["pcst_1"],
        ["pcst_2"],
        ["pcst_3"],
        ["nfmp_1"],
        ["nfmp_2"],
        ["nfmp_3"],
        ["spamp_1"],
        ["spamp_2"],
        ["spamp_3"]
    ]

    l_output = copy.deepcopy(output)
    t_output = copy.deepcopy(output)
    index_loc = 0
    for a in AREAS:
        for m in METHOD:
            solve_file_name = f"{a}.{m}."
            solve_solution_dir = f"./{a}_{m}"
            solution_output = f"output"
            s_files = [s[0] for s in files if solve_file_name in s[0]]
            sol_files = [(x[0], time.ctime(x[1].st_ctime)) for x in sorted([(fn, os.stat(f"./{a}_{m}/" + fn)) for fn in os.listdir(f"./{a}_{m}")], key = lambda x: x[1].st_ctime)]
            solution_files = [s for s in sol_files if s[0].split('.')[-1] == 'geojson']
            for i in range(0, 3): # the number of trials
                index_loc += 1
                with open(s_files[i], 'r') as s_file:
                    for l in s_file.readlines():
                        if SOL_FUNC[m] in l:
                            output[index_loc].append(l.split(' ')[-2])
                        elif CALC_FUNC.get(m, 'NOTINHERE') in l:
                            t_output[index_loc].append(l.split(' ')[-2])
                gdf = gpd.read_file(f"./{a}_{m}/" + solution_files[i][0])
                p_gdf= gdf.to_crs(epsg=26943)
                t_length = sum(p_gdf.geometry.length)
                l_output[index_loc].append(t_length)
        index_loc = 0

    with open("time_summary.csv", "w") as t_sum:
        writer = csv.writer(t_sum)
        writer.writerows(output)

    with open("geom_summary.csv", "w") as g_sum:
        writer = csv.writer(g_sum)
        writer.writerows(l_output)

    with open("pre_summary.csv", "w") as p_sum:
        writer = csv.writer(p_sum)
        writer.writerows(t_output)

if __name__ == "__main__":
    main()

