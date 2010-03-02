#!/usr/bin/env python
import subprocess
import os.path
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hari"
__date__ ="$Jun 29, 2009 10:09:03 AM$"

import os,sys,argparse
class Converter(object):
    program = None
    # Mask convert maskconvert -i input mask -o outputformat
    def __init__(self,toformat=None ,infilepath=None):
        self.toformat = toformat
        self.infilepath = infilepath
        if "linux" in sys.platform:
            gotprog = self.__checkformapman("lx_mapman")
            if gotprog:
                Converter.program  = gotprog
                print "Using %s for mask conversion" % self.program

            elif self.__checkformapman("mapman"):
                gotprog = self.__checkformapman("mapman")
                Converter.program  = gotprog
                print "Using %s for mask conversion" % self.program
      
        elif "darwin" in sys.platform:
            gotprog = self.__checkformapman("osx_mapman")
            if gotprog:
                Converter.program  = gotprog
                print "Using %s for mask conversion" % self.program

            elif __checkformapman("mapman"):
                gotprog = __checkformapman("mapman")
                Converter.program  = gotprog
                print "Using %s for mask conversion" % self.program
        else:
            print "Exiting no mapman in path"
            raise

    def __checkformapman(self,myprogram):
        def is_exe(tested_program):
            return os.path.exists(tested_program) and os.access(tested_program, os.X_OK)

        fpath, fname = os.path.split(myprogram)

        if fpath:
            if is_exe(os.path.join(fpath,fname)):
                program = os.path.join(fpath, fname)
                return program

        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, myprogram)
                if is_exe(exe_file):
                    program = exe_file
                    return program
        return None

    def convertto(self,format,informat="CCP4"):
        print "Converting  format to %s using %s " % ( format , self.program)
        base,name = os.path.split(self.infilepath)
        name_root = os.path.splitext(name)[0]
        outfile = os.path.join(base,"".join([name_root,".",format.lower()]))
        print os.path.join(base, outfile)
        if os.path.lexists(self.infilepath):
            mapman_scr = """re m1 %s %s\nwr m1 %s %s\nquit\n""" % (self.infilepath,informat,outfile,format)
            tmp = open("tmp.scr","w")
            tmp.write(mapman_scr)
            tmp.close()
            a = os.system(self.program + " < tmp.scr ")
            

        
 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i" , dest="infile" ,required=True)
    parser.add_argument("-d" , dest="output_format", required=True, choices=["CCP4", "X-PLOR","CNS","OMAP"])
    parser.add_argument("-s",dest="input_format",choices=["CCP4", "X-PLOR","CNS","OMAP"])
    cli = parser.parse_args()
    c = Converter(infilepath=cli.infile)
    if cli.input_format:
        c.convertto(cli.output_format,cli.input_format)
    else:
        c.convertto(cli.output_format)
   
