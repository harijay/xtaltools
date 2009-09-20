import sys
import re
from numpy import *
file = open(sys.argv[1] , "rb")
assert file , " No file please use python makesymm.py [filename]"

class atom():
  recname = None
  serial = None
  name = None
  altloc = None
  resname = None
  chainid = None
  resseq = None
  icode = None
  x = None
  y = None
  z = None
  occupancy = None
  tempfactor = None
  segid = None
  element = None
  charge = None
  
  def __init__(self,line):
   self.recname = line[0:6]
   self.serial = line[6:11]
   self.blank1 = " "
   self.name = line[12:16]
   self.altloc = line[16]
   self.resname = line[17:20]
   self.blank2 = " "
   self.chainid = line[21]
   self.resseq = line[22:26]
   self.icode = line[26]
   self.blank3 = "   "
   self.x = line[30:38]
   self.y = line[38:46]
   self.z = line[46:54]
   self.occupancy = line[54:60]
   self.tempfactor_raw = line[60:66]
   self.tempfactor = "%6.2f" % float(self.tempfactor_raw )
   self.deprecated = line[66:72]
   if self.deprecated == None:
    self.deprecated = "     "
   self.segid_raw = line[72:76]
   if self.segid_raw == None or self.segid_raw == "   ":
    self.segid_raw = self.chainid
   self.segid = "%-4s" % self.segid_raw
   self.element_raw = line[77:78]
   if self.element_raw == None or self.element_raw ==" ":
    self.element_raw = " "
   self.element = "%+2s" % self.element_raw
   self.charge = line[79:80]
   if self.charge == None or self.charge == " ":
    self.charge = " "

def do_op(x,y,z):
 import numpy
 xfrac =  0.004889*float(x) +  0.002823*float(y) +  0.000000*float(z)
 yfrac =  -0.000000*float(x) +  0.005645*float(y) +  0.000000*float(z)
 zfrac =   0.000000*float(x) - 0.000000*float(y) +  0.010080*float(z)
# print xfrac , yfrac , zfrac
 xnewfrac = yfrac
 ynewfrac = xfrac
 znewfrac = -1 * zfrac
 a = 204.546 
 b = 204.546 
 c = 99.204
 ap = (90 * math.pi)/180
 bt = (90 * math.pi)/180
 gm =  (120 *math.pi)/180
 Volume =  a * b * c * (1 - math.cos(ap)**2 - math.cos(bt)**2 - math.cos(gm)**2 + 2 * math.cos(ap)*math.cos(bt)*math.cos(gm))**0.5
 m1 = numpy.matrix(((a,b*math.cos(gm),c*math.cos(bt)),(0,b*math.sin(gm),c*(math.cos(ap)-math.cos(bt)*math.cos(gm))/math.sin(gm)),(0,0,Volume/(a*b*math.sin(gm)))))
# print m1
 m2 = numpy.array((xnewfrac,ynewfrac,znewfrac))
 coord = m1*m2
 xnew = coord.item(0)
 ynew = coord.item(1)
 znew = coord.item(2)
 return [xnew , ynew , znew]

def parse_atom(eachline):
    myatom = atom(eachline)

    x = myatom.x
    y = myatom.y
    z = myatom.z
    [xnew_raw, ynew_raw , znew_raw ] = do_op(x,y,z)
    # make sure everything is the right size 
    xnew  = "%8.3f" % float(xnew_raw)
    ynew = "%8.3f" % float(ynew_raw)
    znew = "%8.3f" % float(znew_raw)

    line = myatom.recname + myatom.serial + myatom.blank1 + myatom.name + myatom.altloc + myatom.resname + myatom.blank2 + myatom.chainid +myatom.resseq + myatom.icode + myatom.blank3 +xnew + ynew + znew + myatom.occupancy + myatom.tempfactor + myatom.deprecated + myatom.segid + myatom.element + myatom.charge + "\n"
#    print  myatom.recname,myatom.serial,myatom.blank1,myatom.name, myatom.altloc , myatom.resname, myatom.blank2 ,myatom.chainid ,myatom.resseq , myatom.icode , myatom.blank3,xnew ,ynew ,znew ,myatom.occupancy,myatom.tempfactor,myatom.segid ,myatom.element ,myatom.charge
#    print line
    return line

def read_pdb_and_convert():
 outfile = open("outnewer.pdb","wb")
 for line in file:
  if re.search("^ATOM" , line):
   pline = parse_atom(line)
   outfile.write(pline)
   outfile.flush()
  else:
   pass
 outfile.close()


read_pdb_and_convert()
