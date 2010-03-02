#!/usr/bin/env python

from optparse import OptionParser
import sys
import re
import pprint

seqtop = ""
seqbot = ""
alin = ""
clustaldict = {}
top_dict = {}
bot_dict = {}

class AlignmentParseException(Exception):
	def __init__(self,message):
		self.message = message
	def __str__(self):
		return repr(self.message)

def parse_file_and_create_dicts(filename):
	global seqtop,seqbot,alin,clustaldict
	blankline = re.compile("^\s+$")
	clustalline = re.compile("^CLUSTAL*")
	startstop = None
	try:
		clustalfile = open(filename,"read")	
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
	# Expected output TopCHAIN : ID : 45 : Ala == BotCHAIN : ID : Cys == ANOT AS : "."
	#Now that the three are of the same length we can just zip them up
	#wE NEED THE SEQUENCE numbers
	seq_top_nogap = seqtop.replace("-","")
	seq_bot_nogap = seqbot.replace("-","")
	myindex = 0
	mygaps = []
	correction = 0
	if len(seq_top_nogap) != len(seq_bot_nogap):
		for index, elem in enumerate(seqtop):
			if elem == "-":
				mygaps.append(elem)
				clustaldict[index] = [elem,index,index-len(mygaps),seqbot[index],index-len(mygaps),alin[index]]
				print "BREAK IN SEQ ALN at posn", index
				continue
			else :
				clustaldict[index] = [elem,index,index-len(mygaps),seqbot[index],index-len(mygaps),alin[index]]
		
	else:
		for index , elem in enumerate(seqtop):
			clustaldict[index] = [elem, index , seqbot[index],index,alin[index]]
	pprint.pprint(clustaldict)
	return clustaldict

def get_mismatch_number(start, stop , one ,  other):
	for index , elem in enumerate(one):
		if elem != other[index]:
			return start + index 
			
def give_sequences():

	while True:
		start = raw_input("Give start:")
		stop = raw_input("Give  stop:")
		top = ""
		bottom = ""
		if int(start) == int(stop):
			stop = int(stop) + 1
		for i in range(int(start),int(stop) + 1,1):
			top = top + seqtop[i-1]
			bottom = bottom + seqbot[i-1]
		print top,"\n",bottom
		if top != bottom:
			indexmismatch = get_mismatch_number(int(start),int(stop) + 1 , top , bottom)
			print "Mismatch at:%s\n" % indexmismatch
if __name__=="__main__":
	try:
		p = OptionParser()
		p.add_option("-i" , "--infile",metavar="*.aln",dest="infile",help="alignment file from http://www.ebi.ac.uk/Tools/clustalw2/index.html")
		options,spillover = p.parse_args()	
		parse_file_and_create_dicts(options.infile)
		give_sequences()
		
	except Exception , e:
		print e
		p.print_help()
