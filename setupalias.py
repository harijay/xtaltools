#!/usr/bin/env python
import os
projdict = {}

class proj(object):
	def __init__(self,num):
		self.num = num
		self.name = None
		self.path = None
		
def createdict():
	try:
		dirfile = open(os.environ.get("HOME") + "/.CCP4/unix/directories.def")
	except IOError:
		pass
	import re
	projdir = re.compile("PROJECT_PATH\,([\d]+)\s+_dir\s+(.*)") 
	projname = re.compile("PROJECT_ALIAS,([\d]+)\s+_text\s+(.*)")	
	for i in dirfile:
		if projname.match(i):
			num = projname.match(i).group(1)
			p = proj(num)
			p.name = projname.match(i).group(2).replace("-","_")
			projdict[projname.match(i).group(1)] = p
		if projdir.match(i):
			projdict[projdir.match(i).group(1)].path = projdir.match(i).group(2)
		
def printprojs():
	for key in projdict.keys():
		print key ,projdict[key].name, projdict[key].path

def makealias():
	aliasfile = open(os.environ.get("HOME") + "/.CCP4/unix/aliases.sh", "write")
	aliasfile.write("#!/usr/bin/bash\n")	
	for key in projdict.keys():
		com = "export " + os.environ.get("USER") + "job%s=" % (projdict[key].name) + "%s\n"  % projdict[key].path
		aliasfile.write(com)
					
if __name__=="__main__":
	createdict()
#	printprojs()
	makealias()
