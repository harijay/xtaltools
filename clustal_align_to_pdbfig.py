#!/usr/bin/env python
# Useage clustal_align_to_pdbfig -a culstal.txt -i cy.pdb 
# Program to map an alignment to the pdb bfactor column


from optparse import OptionParser
import pdbfile
import pprint
import re
import atom
import os 

clustaldict = {}
seqtop = ""
seqbot = ""
alin = ""

class AlignmentParseException(Exception):
	def __init__(self,message):
		self.message = message
	def __str__(self):
		return repr(self.message)

def read_clustal_make_dict(file):
	global seqtop,seqbot,alin
	blankline = re.compile("^\s+$")
	clustalline = re.compile("^CLUSTAL*")
	startstop = None
	try:
		clustalfile = open(file,"read")	
		for line in clustalfile:
			if not (blankline.match(line) or clustalline.match(line)):
				seqtop = seqtop + line.split()[1]
				botseqline = clustalfile.next()
				seqbot = seqbot + botseqline.split()[1]
				thirdline = clustalfile.next()
				#Hack to get the first meaningful entry of the conservation symbol i.e "*" or ":" or " "
				topstartindex = line.index(line.split()[1][0])
				botstartindex = botseqline.index(botseqline.split()[1][0])
				if startstop == None:
					startstop = max(topstartindex,botstartindex)
					
				alin = alin + thirdline[startstop:-1]
				
		if not (len(seqtop) == len(seqbot) == len(alin)):
			raise AlignmentParseException("Sequences not same length : Check")
		for item in (seqtop,seqbot,alin):
			pprint.pprint(item)
	except IOError:
		print "alignment file not found"
		
def get_property_by_resn():
	myindex = {}
	resnumber = 1
	for poscount,entry in enumerate(seqbot):
		if entry != "-" and entry != " ":
			myindex[resnumber] = alin[poscount]
			resnumber = resnumber + 1
	pprint.pprint(myindex)
	return myindex
bfacdict = {":" :" 50.00" ,"*":"100.00"," ": " 00.00" ,"." : " 25.00"}

def counts():
	myindex =  get_property_by_resn()
	full = []
	quart = []
	empty = []
	half = []
	binner = {":" : half , "." : quart , "*" : full , " " : empty }
	pprint.pprint(myindex)
	for i in myindex.keys():
		binner[myindex[i]].append(i)
	for key in binner.keys():
		print key , len(binner[key])
		
def setbfac_property_clustal(pdbfile):
	pdbfile.seek(0)
	isatom = re.compile("^ATOM")
	oldatom = None
	curatom = None
	myindex = get_property_by_resn()
	oldfile_name = os.path.splitext(pdbfile.name)[0] + "-unchanged.pdb"
	newfile_name = os.path.splitext(pdbfile.name)[0] + "-bfacmapped.pdb"
	oldfile = open(oldfile_name,"wb")
	newfile = open(newfile_name,"wb")
	for line in pdbfile:
		if isatom.match(line):
			curatom = atom.Atom(line)
			oldfile.write(curatom.write_line())
			curatom.bfac = bfacdict[myindex[int(curatom.resseq.strip())]]
			newfile.write(curatom.write_line())
		else :
			oldfile.write(line)
			newfile.write(line)
		newfile.flush()
		oldfile.flush()
	counts()
	newfile.close()
	oldfile.close()
						
if __name__=="__main__":
	try:
		p = OptionParser()
		p.add_option("--infile","-i",dest="pdbfile",metavar="*.pdb")
		p.add_option("--alignment" ,"-a",dest="alnfile",metavar="*.txt with alignment")
		opttuple,spillover = p.parse_args()
		pdb = pdbfile.pdbfile(opttuple.pdbfile)
		ad = pdb.make_atom_dict()
		read_clustal_make_dict(opttuple.alnfile)
		dictunme = get_property_by_resn()
		setbfac_property_clustal(open(opttuple.pdbfile))
		
	except IOError:
		p.print_help()
	except TypeError:
		p.print_help()