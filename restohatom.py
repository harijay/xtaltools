#!/usr/bin/python
import sys
import optparse
useage = "usage: %prog [options] arg1 arg2"
input_parser = optparse.OptionParser(usage=useage,version="%prog 0.1")
input_parser.add_option("--infile","-i",dest="filename",help="input res file from Shelx",metavar="*.res")
(myoptions,args) = input_parser.parse_args()

infile =None

infile = myoptions.filename

try:
    resfile = open(infile,"r")
except TypeError,IOError:
    input_parser.print_help()
    exit()

for i in range(7):
	resfile.readline()
import re
space = re.compile("\s+")
def hatomize(line):
	elems = space.split(line)
	outline ="ATOM   Se  %s  %s  %s\n" % (elems[2],elems[3],elems[4])
	return outline
import os
outfile= os.path.splitext(infile)[0] + ".hatom"
hatomfile = open(outfile,"write")

atom = re.compile("SE.*")
resfile.seek(0)
for line in resfile:
	print line
	if atom.match(line):
		myline = hatomize(line)
		print myline
		hatomfile.write(myline)


