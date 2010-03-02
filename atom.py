#!/usr/bin/python
import aadict 

class Atom():
	atomtoken = None
 	serial = None
 	name = None
 	altloc = Noneresn = None
	chainid = None
	resseq = None
	inscode = None
	x = None
	y = None
	z = None
	occ = None
	bfac = None
	fnote = None
	def __init__(self,line):
		 self.atomtoken = line [0:6]
		 self.serial = line[6:11]
		 self.space1 = " "
		 self.name = line[12:16]
		 self.altloc = line[16:17]
		 self.resn = line [17:20]
		 self.space2 = " "
		 self.chainid = line[21:22]
		 self.resseq = line[22:26]
		 self.inscode = line[26:27]
		 self.space3 = "   "
		 self.x = line[30:38]
		 self.y = line[38:46]
		 self.z = line[46:54]
		 self.occ = line[54:60]
		 self.bfac = line[60:66]
		 self.fnote = line[67:70]
		 self.resid = line[72:73]
		 self.elemcode = line[77:78]
		 self.remainder = line[78:]
		
	def write_line(self):
		outstr = ""
		for i in [self.atomtoken,self.serial,self.space1,self.name,self.altloc,self.resn,self.space2,self.chainid,self.resseq,self.inscode,self.space3,self.x,self.y,self.z,self.occ,self.bfac," ",self.fnote,"  ",self.resid,"    ",self.elemcode,self.remainder]:
			outstr = outstr + str(i)
		return outstr
	def aa_code(self):
  		resn = self.resn.strip()
		return aadict.aadict[resn]

  
