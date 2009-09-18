#!/usr/bin/python
import sys

infile = sys.argv[1]
resfile = open(infile,"read")

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


