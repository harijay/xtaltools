import re
import sys 
import atom
import os
from optparse import OptionParser

class pdbfile(object):
	non_atom_record = []
	atom_record = []
	linedict = {}
	atomdict = {}
	
	
	def __init__(self,file):
		self.file = open(file,"read")	
		self.isatom = re.compile("^ATOM")
		i = 0
		for line in file:
			self.linedict[i] = line
			if self.isatom.match(line):
				myatom = atom.Atom(line)
				atomkey = (myatom.serial,myatom.name,myatom.chainid)
				self.atomdict[atomkey] = myatom
			i = i + 1
			
	
	def make_chainid_segid_same(self):
		outfile_name = os.path.splitext(self.file.name)[0] + "-mod-chain-segsame.pdb"
		outfile = None
		try:
			outfile = open(outfile_name,"write")
		except IOError:
			print "Cannot open file for writing"	
		atomarray = []
		self.file.seek(0)
		for line in self.file:
			if self.isatom.match(line):
				if line[21:22] != line[72:73]:
					newline = line[0:72] + line[21:22] + line[73:]
					outfile.write(newline)
					outfile.flush()
				else:
					outfile.write(line)
					outfile.flush()
			else:
				outfile.write(line)
				outfile.flush()
		outfile.flush()
		outfile.close()


if __name__=="__main__":
	try:
		p = OptionParser()
		p.add_option("-i","--infile" , dest="pdbfile",metavar="*.pdb")
		opttuple,spillover = p.parse_args()
		file = opttuple.pdbfile
		p = pdbfile(file)
		p.make_chainid_segid_same()
		
	except IOError:
		p.print_help()
	except TypeError:
		p.print_help()
			
		
				
		
