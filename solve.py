"""
The script to run the solution methods and time them.
Usage:
    cd ./test_data
    python3 -m cProfile -o profile_output run.py > ""
"""
import os
import argparse
import json
import random
from datetime import datetime

from link.solve.main import (
    run_pcst,
    run_pmed,
    run_pamp,
    run_nfmp,
    run_spamp
)

def create_parser():
    """
    Read in the cmd line arguments.the 'data' arg is the data set
    which shall be used. the 'method' refers to the solution approach
    and 'output_dir' is where the solution file is written.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("data")
    parser.add_argument("method")

    args = parser.parse_args()

    return args


def add_one_candidate(input_data):
    # we want to add one candidate
    input_data["features"][-1]["properties"]["candidate"] = 10000
    input_data["features"][-1]["properties"]["capacity"] = 10000


def add_candidates(input_data):
    # we want to create some random potential candidates
    num_points = sum(1 for f in input_data["features"] if f["geometry"]["type"] == "Point" and not f["properties"].get("demand", 0))
    locations = [random.randrange(0, num_points) for _ in range(100)]
    count = 0
    for f in input_data["features"]:
        if not f["properties"].get("demand", 0) and f["geometry"]["type"] == "Point":
            if count in locations:
                f["properties"]["candidate"] = 10000
                f["properties"]["capacity"] = 10000
            count += 1


def main(args=None):
    if args is None:
        args = create_parser()

    with open(os.path.join(args.data, "input.geojson")) as input_geojson:
        input_data = json.load(input_geojson)
        if args.method == "sp":
            add_one_candidate(input_data)
            result = run_pmed(input_data)

        if args.method == "pcst":
            result = run_pcst(input_data)

        if args.method == "nfmp":
            add_one_candidate(input_data)
            result = run_nfmp(input_data)

        if args.method == "pmed":
            add_candidates(input_data)
            result = run_pmed(input_data)

        if args.method == "pamp":
            add_candidates(input_data)
            result = run_pamp(input_data)

        if args.method == "spamp":
            add_candidates(input_data)
            result = run_spamp(input_data)

    the_time = datetime.now()

    with open(os.path.join(args.data + "_" + args.method, f"output.{the_time}.geojson"), "w") as output_geojson:
        json.dump(result, output_geojson)

if __name__ == "__main__":
    main()

