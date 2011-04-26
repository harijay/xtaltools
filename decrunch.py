#!/usr/bin/env python
import optparse
import sys
import re
isheader = re.compile("^\>.*")
found_sequence = "No"

def decrunch_alignment(afile):
    out = ""
    while 1 :
        try:
            line = afile.next()
            if isheader.match(line):
                if out != "":
                    print out
                print line,
                found_sequence="Yes"
                out = ""
            if ">" not in line and found_sequence=="Yes":
                out = out + line.replace(".","")
                out = out.replace("-","")
                out = out.replace("\n","")
        except StopIteration as e:
            print out
            break
			
			
if __name__ == '__main__':
    p = optparse.OptionParser(" %prog [options]. \nThis program de-aligns Fasta formatted multiple sequence alignments for input into another alignment program")
    p.add_option("-i", "--infile", dest="infile",metavar="[*.txt infile]")
    options,args = p.parse_args()
    decrunch_alignment(open(options.infile))
	
		
		
