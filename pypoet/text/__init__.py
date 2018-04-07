import os
import sys

# for each text file in this directory, load it and add it to 
# TODO: if it takes too long to load, do it on demand.
# for 
_absdirname = os.path.dirname(os.path.abspath(__file__))
for filename in os.listdir(_absdirname):
    name, ext = os.path.splitext(os.path.basename(filename))
    if ext == ".txt":
        with open(os.path.join(_absdirname, filename)) as open_file:
            globals()[name] = open_file.read()