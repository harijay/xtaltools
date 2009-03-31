import os.path
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hari"
__date__ ="$Mar 26, 2009 4:21:37 PM$"

from optparse import OptionParser
parser = OptionParser()
import os
parser.add_option("-o",dest="mtzfile",help="output mtz file",metavar="*.phs")
parser.add_option("-i","--phs",help="Input phases file from shelx",dest="phs",metavar="*.phs")
parser.add_option("--sca","-s",dest="scafile",help="scafile for cell parameters",metavar="*.sca")
parser.add_option("-c","--cell",dest="cell",help="cell parameters a b c alpha beta gamma",metavar="CELL")
parser.add_option("--sym",dest="symm",help="symmetry / space group",metavar="P1")
(options,spillover) = parser.parse_args()

def getcellparams(scafile):
    myfile = None
    if os.path.lexists(scafile):
        myfile = open(scafile,"read")
    else:
        print "File not found %s: Please give cell parameters" % scafile
        exit()
    myfile.readline()
    myfile.readline()
    cellline = myfile.readline().split()
    cell = " ".join(cellline[:-1])
    spg = cellline[-1]
    return (cell,spg)


def main():
    try:
        sys.argv[1]
    except BaseException :
        parser.print_help()
        exit()
  
    cellparams,symm_from_sca = (None,None)
    if options.scafile != None:
        (cellparams,symm_from_sca) = getcellparams(options.scafile)
    if options.symm == None:
        options.symm = symm_from_sca
    script =  """SYMM %s
    CELL %s
    skipline
    LABOUT H K L FP FOM PHIS X
    CTYPOUT H H H F W P R
    FORMAT '(3f4.0,f11.2,f8.2,f8.1,f8.2)'
    END
    eof""" %(options.symm,cellparams)
    import subprocess
    f2mtzargs = ["f2mtz hklin %s hklout %s " % (options.phs,options.mtzfile),"<<eof"]
    a = subprocess.Popen(f2mtzargs,stdin=subprocess.PIPE,shell=True)
    a.communicate(input=script)
    #print script
    
        
if __name__ == "__main__":
    main()
