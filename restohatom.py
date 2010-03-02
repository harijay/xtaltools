#!/usr/bin/python
import sys
from optparse import OptionParser
p = OptionParser()
p.add_option("--resfile" , "-r" , metavar="[*.res or *.hat file]", dest="resfile")
p.add_option("--atomtype","-a",metavar="SE",dest="atomtype")
options,args = p.parse_args()

if len(sys.argv) <= 1 :
 p.print_help()
 exit()

infile = options.resfile

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
inputatom = options.atomtype.upper()

atom = re.compile("%s.*" % inputatom)
resfile.seek(0)
for line in resfile:
	print line
	if atom.match(line):
		myline = hatomize(line)
		print myline
		hatomfile.write(myline)


