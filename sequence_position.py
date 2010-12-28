#!/usr/bin/env python
import urllib
import optparse
import sys
from private import proteinname_uniprot_fasta_url_map

# pdict is a file with a python dictionary of protein names mapped to their uniprot fasta pages
# for eg proteinname_uniprot_fasta_url_map = {"cy":"http://www.uniprot.org/uniprot/P73745.fasta","eric":"http://www.uniprot.org/uniprot/P37019.fasta"}

def print_sequence(seqname):
	f = urllib.urlopen(proteinname_uniprot_fasta_url_map[seqname])
	f.readline()
	seq = ""
	for line in f:
		seq = seq + line.replace("\n","")
	print " I read in sequence %s of %s residues " % (seq , len(seq))
	while True:
		input = raw_input("Sequence for:")
		start = input.split("-")
		try:
			print seq[int(start[0])-1:int(start[1])]
		except IndexError:
			print seq[int(start[0])-1]
		
		  

if __name__=="__main__":
	p = optparse.OptionParser()
	p.add_option("-p" ,"--protein", metavar=["Protein Name in lower case"], dest="protein")
	options,args = p.parse_args()
	try:
		sys.argv[1] 
	except IndexError:
		p.print_help()
		exit()
	print_sequence(options.protein)
	
	
