# Network Test Suite

The test data which was used for the paper "Optimization for physical network design problems: Creating benchmarks". This research explores network design problems with applications in physical infrastructure engineering.

## Summary
This repo contains the input data, clipped test areas of size:

- 500
- 1000
- 5000
- 10000

These are used to benchmark Prize Collecting Steiner Tree (PCST) solution approaches. These can be used to solve network infrastructure design problems.

When selecting an approach it can be challenging to determine which or which combination is best suited. This research seeks to establish metrics for the quantitative and qualitative aspects of two approaches.

This includes items like run time, software complexity (lines of code), open source v. closed source, as well as more quantifiable metrics like optimality gap, and total solution distance.

It is also noted that in order to produce the best possible results, for example in a commercial setting the input data would typically be extensively cleaned. For further information regarding this refer to:

1. https://www.esri.com/news/arcuser/0401/topo.html
2. http://resources.arcgis.com/en/help/main/10.2/01mm/pdf/topology_rules_poster.pdf
3. https://csun.uic.edu/codes.html

## Abstract

#### Benchmarking tree approaches on street data

Keywords: Telecommunications, Graphs and Networks, Network flows

By examining the use of algorithms to solve the Prize Collecting Steiner Tree (PCST) problem we consider the facets which determine effectiveness. Specifically, by measuring a number of solution approaches and comparing them based on metrics. In order to understand the solution approach we must asses why it is useful. Our goal is to determine the effectiveness of Mixed Integer Programming (MIP) and heuristic methods. Utilizing freely available street and address data a base graph representation is created and then computed on. Such that a tree connects every address utilizing the minimum total length of edges from the street network. This is the basis of many approaches used to solve infrastructure problems including telecommunications network design and costing. The analysis is conducted on methods developed by Hegde et al. 2015, Ljubić et al. 2006, and Teitz et al. 1963. We present a data processing architecture, as well as a concise set of results and a framework for assessing the facets and trade-offs for a given approach. In this case the heuristic approaches are proven to have advantages in the simplistic case but fail when more complex requirements are added. This is where the MIP approach is able to capitalize, whilst detrimentally limiting the flexibility due to the strictness and specificity in modelling.

## TODO

- [X] Source test data
- [X] Cut up data
- [X] Create runner module
- [X] Create test run time data structure
- [X] Run test cases

## Outcomes/Results

TBC

## HOWTO

1. Install the "link" environment from [here](https://github.com/fhk/link_src)
2. Source input data from open address and open street map and place it in the "basedata" folder
3. Create a new folder that can be run through the pipeline
4. Run "conda create -n test python=3.6"
5. Run "conda install fiona scipy"
5. Run "python prep.py {area}" - this will create the input geoJSON required as input for the link solution methods. The input data line data is cut up into segements. Each address point is then connected to the nearest line vertex. This is done such that a fully connected graph can be created.
6. Run "python get_stats.py". This will run the areas and methods specified in the file
7. Run "python analysis.py". This will analyze the results and output the reports

# Reference this and the link framework research

DOI 10.17605/OSF.IO/3PZJ8

