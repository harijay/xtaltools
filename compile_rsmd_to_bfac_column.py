#!/usr/bin/env python
# Useage compile_rmsd_to_bfac -i pdb -s screedump.txt

# U.I part
import  optparse
import pdbfile
import atom 
import re
import pprint
import os 
# funtion to parse screendump
match_dict = {}
reference_dict = {}

def reference_array_from_txt(txtfile):
	movrefdistline = re.compile("\s?Moving  Reference   Distance")
	blankline = re.compile("^\s+$")
	for line in txtfile:
		if movrefdistline.match(line):
			counter = 0
			try:
				while not (blankline.match(line)):
					match_dict[counter] = line.strip().split()
					try:
						reference_dict[int(line.strip().split()[4])] = line.strip().split()[6]
					except IndexError as e:
						pass
					line = txtfile.next()
					counter = counter + 1
				print "File Parsed and dictionary created"
			except StopIteration:
				print "File Parsed and dictionary created"	
				
def bfactor_implant(pdbfile):
	if reference_dict == {}:
		raise Exception("Reference dict empty")
	# pprint.pprint(reference_dict)
	pdbfile.seek(0)
	isatom = re.compile("^ATOM")
	oldatom = None
	curatom = None
	oldfile_name = os.path.splitext(pdbfile.name)[0] + "-unchanged_rmsd.pdb"
	newfile_name = os.path.splitext(pdbfile.name)[0] + "-rmsdmapped.pdb"
	oldfile = open(oldfile_name,"wb")
	newfile = open(newfile_name,"wb")
	for line in pdbfile:
		if isatom.match(line):
			curatom = atom.Atom(line)
			oldfile.write(curatom.write_line())
			try:
				curatom.bfac = "%6.2f" % (float(reference_dict[int(curatom.resseq.strip())].strip()) * 100.0)
				newfile.write(curatom.write_line())
				# print "I have%sthis" % curatom.bfac
			except KeyError as e:
				# print "KeyError setting to 0" , e
				curatom.bfac = "00.00"
				newfile.write(curatom.write_line())
				continue
			
		else :
			oldfile.write(line)
			newfile.write(line)
		newfile.flush()
		oldfile.flush()
	newfile.close()
	oldfile.close()
	print "rmsd mapped as B-factor in output file %s ( Unmodified file saved as %s ) " % (newfile.name,oldfile.name)
		
		
				
				
if __name__=="__main__":
	try:
		p = optparse.OptionParser()
		p.add_option("-i" , "--infile" , metavar="*.pdb",dest="pdbfile",help="input file to append bfactors to")
		p.add_option("-s" , "--screedump" , metavar="*.txt",dest="txtfile",help="input file with screen dump after SSM superpose")
		opttuple , spillover = p.parse_args()
		reference_array_from_txt(open(opttuple.txtfile))	
		bfactor_implant(open(opttuple.pdbfile))
	except TypeError as e:
		p.print_help()
		print e
	except IndexError as e:
		p.print_help() 
		print e
	
	
	