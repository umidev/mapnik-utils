# $Id: Hello World 2008-04-29 dane $

Mapnik Hello World Tutorial
---------------------------

This directory contains sample data and scripts to generate basic png images of the world in standard geographic coordinates.

The use of the Mapnik python bindings are highlighted in two ways to create an identical map.

The 'pure_python' folder contains a script that shows how to use pure python syntax to construct the list of styles and rules to properly symbolize the map as well as set the datasource, extents, and output file.

The 'xml_config' folder contains a basic python script to initiate the map style, rules, datasource, and projection from an XML document. In this case the extents and output file are still set using python syntax.

Pure python scripting has the advantage (when used with more complicated map creation) to allow dynamic and conditional map construction.

XML configuration provides advantages for storing and maintaining complicated styles in a separate, potentially more manageable format.


Note: Paths are relative in these scripts. Therefore these scripts are meant to be run from the shell like:

$ python world_map.py

If you wish to paste the python code into a python interpreter, be sure to either edit your path names to be absolute or initiate your interpreter session from the proper working directory (which contains the python script).