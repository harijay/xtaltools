# To change this template, choose Tools | Templates
# and open the template in the editor.

from optparse import OptionParser
import sys
import re
import os

def cleanup(infile):
    myinfile = None
    loopcount = 0
    param_order = []
    reflections = {}
    correctorder = {0: "_refln.crystal_id",
1 :"_refln.wavelength_id",
2 : "_refln.scale_group_code",
3 : "_refln.status",
4 : "_refln.index_h",
5:"_refln.index_k",
6:"_refln.index_l",
7:"_refln.F_meas_au",
8:"_refln.F_meas_sigma_au"}
    orderinfile = {}
    try :
        myinfile = open(infile , "read")
        outfile = open(os.path.splitext(myinfile.name)[0] + "_out.txt" , "w")
        reffile = open(os.path.splitext(myinfile.name)[0] + "_ref.txt" , "w")
    except IOError:
        print "Input file not found"


    for line in myinfile:
        # Once you find the loop for symmetry
        if "loop_" in line:
            outfile.write(line)
            line = myinfile.next()
            while "loop_" not in line:
                outfile.write(line)
                line = myinfile.next()
            # Now we find next loop and get out
            # We write that loop declaration
            outfile.write(line)
            line = myinfile.next()
            i = 0
            while "1 1 1" not in line:
                param_order.append(line.strip())
                orderinfile[i] = line.strip()
                i = i + 1
                line = myinfile.next()
            for index in range(len(correctorder.keys())):
                outfile.write(correctorder[index] + "\n")
            while "#END OF REFLECTIONS" not in line:
                reffile.write(line)
                linevals = line.split()
                outstr = []
                for elem in range(len(param_order)):
                    outstr.append(linevals[param_order.index(correctorder[elem])])
                modline =  " ".join(outstr)
                outfile.write(modline + "\n")
                line = myinfile.next()

            outfile.write(line)
        else:
            outfile.write(line)
    outfile.close()
    reffile.close()




        
if __name__=="__main__":
    try:
        p = OptionParser()
        p.add_option("-i", "--ciffile" ,dest="ciffile", help="screwed up cif file" )
        options,args = p.parse_args()
        cleanup(options.ciffile)
    except Exception , e:
        print e
        p.print_help()

    
