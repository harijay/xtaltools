#!/usr/bin/env python
import optparse
import sys
import re

def decrunch_alignment(file):
	isheader = re.compile("^\>.*")
	for line in file:
		if isheader.match(line):
			print line,
			out = ""
			line = file.next()
			while not isheader.match(line):
				try:
					out = out + line.replace(".","")
					out = out.replace("\n","")
					line = file.next()
				except StopIteration as e:
					break
			print out
			
if __name__ == '__main__':
	try:
		p = optparse.OptionParser(" %prog [options]. \nThis program de-aligns Fasta formatted multiple sequence alignments for input into another alignment program")
		p.add_option("-i", "--infile", dest="infile",metavar="[*.txt infile]")
		options,args = p.parse_args()
		decrunch_alignment(open(options.infile))
	except IndexError as e:
		p.print_help()
	except TypeError as e:
		p.print_help()
	except NameError as e:
		p.print_help()
		
		