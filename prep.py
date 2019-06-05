"""
This script creates the input data required by the link module
"""
import os
import argparse
import json
import fiona
import numpy as np
import scipy.spatial as spatial
from osgeo import ogr, osr
import math

INPUT = {"type": "FeatureCollection", "features": []}
STREETS = "streets.shp"
DEMAND = "demand.shp"

def _distance(a, b):
    # approximate radius of earth in km
    lat1, lon1 = a
    lat2, lon2 = b
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d * 1000


def split_line_multiple(line, length=None):
    """ Splits a ogr wkbLineString into multiple sub-strings, either of
    a specified <<length>> or a specified <<n_pieces>>.

    line should be an ogr LineString Geometry
    Length should be a float or int.
    n_pieces should be an int.
    Either length or n_pieces should be specified.

    Returns a list of ogr wkbLineString Geometries.

    """
    out_lines = []
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromEPSG(3857)

    transform = osr.CoordinateTransformation(source, target)
    transform_out = osr.CoordinateTransformation(target, source)

    line.Transform(transform)
    line.Segmentize(length)
    points = line.GetPoints()

    for i in range(len(points) - 1):
        points[i]
        points[i + 1]
        cut_line = ogr.Geometry(ogr.wkbLineString)

        cut_line.AddPoint(*points[i])
        cut_line.AddPoint(*points[i + 1])

        cut_line.Transform(transform_out)

        out_lines.append(cut_line)

    return out_lines


def create_parser():
    """
    Read in the cmd line arguments 'data' arg is the data set
    which shall be used.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("data")
    args = parser.parse_args()

    return args


def read_process_streets(args):
    new_lines = []
    for f in fiona.open(os.path.join(args.data, STREETS)):
        coords = f["geometry"]
        ogr_line = ogr.CreateGeometryFromJson(json.dumps(coords))
        new_lines += split_line_multiple(ogr_line, 30)

    return [l.ExportToJson() for l in new_lines]


def extract_nodes(lines):
    nodes = []
    for feature in lines:

        coords = list(eval(feature)["coordinates"])
        for i in range(len(coords) - 1):
            s_node = coords[i][:2]
            e_node = coords[i + 1][:2]

            INPUT["features"].append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            s_node, e_node]},
                    "properties":
                        {"length": _distance(s_node, e_node)}
                }
            )

            nodes.append(s_node)
            nodes.append(e_node)

    return nodes


def snap_demand(nodes, args):
    demand = fiona.open(os.path.join(args.data, DEMAND))
    points = np.array(nodes)
    point_tree = spatial.cKDTree(points)
    count = 0

    for i, feature in enumerate(demand):

        coords = feature["geometry"]["coordinates"]

        idx = point_tree.query(coords, k=1)

        nearest = points[idx[1]]

        INPUT['features'].append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": coords},
                "properties":
                    {
                        "demand": 1
                        }
            }
        )
        INPUT["features"].append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        coords, nearest.tolist()]},
                "properties":
                    {"length": _distance(coords, nearest.tolist())}
            })


        INPUT['features'].append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": nearest.tolist()},
                "properties":
                {
                    "candidate": 0,
                    "capacity": 0
                }
            }
        )
        count += 1


def main():
    args = create_parser()
    lines = read_process_streets(args)
    nodes = extract_nodes(lines)
    snap_demand(nodes, args)

    with open(os.path.join(args.data, "input.geojson"), 'w') as output:
        json.dump(INPUT, output)


if __name__ == "__main__":
    main()

