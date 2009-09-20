import os.path

import sys
import optparse
import scafile
import math
import os
import herman_dict

p = optparse.OptionParser()
p.add_option("-i","--infile",dest='filename',metavar="[*.hat]",help="input file")
p.add_option("-s","--scafile",dest="scafile",metavar="[*.sca]",help="scafile for cell params")

if len(sys.argv) <= 1 :
	p.print_help()
	exit()
(options,spillover) = p.parse_args()

def isatomline(line):
	import re
	headvars = ["TITL","CELL","LATT","SYMM","SFAC","UNIT","HKLF","END"]
	lineanal = line.split()
	if lineanal[0] in headvars:
		return False
	else:
		return True


filename = None
try:
	filename = open(options.filename,"r")
except IOError,e:
	print e
except TypeError, et:
	print p.print_help()
atomcount = 0
atomdict = {}
namedict = {}
negatomdict = {}
posatomdict = {}
for line in filename:
	if isatomline(line):
		atomcount = atomcount +1
		atominfo = line.split()[2:7]
		atomdict[atomcount] = atominfo
                namedict[atomcount] = line.split()[0]
		if float(atominfo[3]) > 0:
			posatomdict[atomcount] = atominfo
		if float(atominfo[3]) < 0:
			negatomdict[atomcount] = atominfo
print "Total Atoms :%d" % atomcount
print "Positive Occupancy:%d" % len(posatomdict.keys())
print "negative Occupancy:%d" % len(negatomdict.keys())
print namedict
cell = None
spg = None

a,b,c,oap,obt,ogm = 0,0,0,0,0,0
m = {}

if not options.scafile:
    a,b,c,oap,obt,ogm = raw_input("Input a,b,c,alpha,beta,gamma:")
else:
    myscafile = scafile.Scafile(options.scafile)
    print myscafile.cell
    [a,b,c,oap,obt,ogm] = map(float ,myscafile.cell.split(","))
    spg  = myscafile.spg
ap =  oap*math.pi/180.0
bt = obt*math.pi/180.0
gm = ogm*math.pi/180
Volume =  a * b * c * (1 - math.cos(ap)**2 - math.cos(bt)**2 - math.cos(gm)**2 + 2 * math.cos(ap)*math.cos(bt)*math.cos(gm))**0.5
m[0] = [a,b*math.cos(gm),c*math.cos(bt)]
m[1] = [0,b*math.sin(gm),c*(math.cos(ap)-math.cos(bt)*math.cos(gm))/math.sin(gm)]
m[2] = [0,0,Volume/(a*b*math.sin(gm))]
orthogdict = {}

for k in atomdict.keys():
    xfrac,yfrac,zfrac = float(atomdict[k][0]),float(atomdict[k][1]),float(atomdict[k][2])
    xorthog = m[0][0]*xfrac + m[0][1]*yfrac + m[0][2]*zfrac
    yorthog = m[1][0]*xfrac + m[1][1]*yfrac + m[1][2]*zfrac
    zorthog = m[2][0]*xfrac + m[2][1]*yfrac + m[2][2]*zfrac
    orthogdict[k] = [xorthog,yorthog,zorthog]
root,tail = os.path.splitext(r'%s' % options.filename)
outfilename = root + ".pdb"
outfile = open(outfilename , "wb")
print "CRYST1",a,b,c,oap,obt,ogm,spg,0,0
outfile.write("%6s%9.3f%9.3f%9.3f%7.2f%7.2f%7.2f %-11s\n" % ("CRYST1",a,b,c,oap,obt,ogm,herman_dict.hm[spg.strip()]))
for k in orthogdict.keys():
    print orthogdict[k]
    print namedict[k]
    print atomdict[k]
    print k,namedict[k][0:2],namedict[k][2:],orthogdict[k][0],orthogdict[k][1],orthogdict[k][2],atomdict[k][3],atomdict[k][4]
    print "numargs" , len((k,namedict[k][0:2],int(namedict[k][2:]),orthogdict[k][0],orthogdict[k][1],orthogdict[k][2],atomdict[k][3],atomdict[k][4]))
    outfile.write("ATOM  %5d %4sHOH Z%3d %8.3f%8.3f%8.3f%6.2f%6.2f\n" % (k,namedict[k][0:2],int(namedict[k][2:]),orthogdict[k][0],orthogdict[k][1],orthogdict[k][2],\
    float(atomdict[k][3]),float(atomdict[k][4])))

outfile.close()