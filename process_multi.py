#!/usr/bin/python
# -*- coding: latin-1 -*-
# Class that takes in a file name and other optional inputs and converts the scafile to an mtz file

from optparse import OptionParser
import aurigaerrors
import os
import sys
import subprocess
from Queue import Queue
from threading import Thread,Lock
from mrdict import modeldict
import shlex
import tempfile
import time

# Global output directory root prefix

auriga_output_directory_root = None


# Check and see if the global output directory is defined

if os.environ.get("AURIGA_OUTPUT_ROOT"):
    auriga_output_directory_root=os.environ.get("AURIGA_OUTPUT_ROOT")
else:
    # print "Setting directory for all output to %s" % os.path.abspath(os.curdir)
    auriga_output_directory_root=os.path.abspath(os.curdir)


# Class to carry out Scalepack to mtz file conversion

class scalatomtz(object):
    """Class that accepts filename, (optional) spacegroup,cell_dimensions, wavelength and number of residues in the ASU as imput. Runs truncate and outputs the mtz file.
    """
    
    def __init__(self,filename,spag=None,cell_dimensions_tuple=None,wavelength=None,number_of_residues_in_asu=130 ):
        """Assume only filename and infer cell dimensions and spacegroup
        """
        self.filename = filename.strip()
        self.file = open(self.filename.strip(),"r")
        self.spag = self.extract_spag()
        self.cell_dimensions_string = self.extract_cell_dimensions_string()
        self.wavelength = wavelength
        self.number_of_residues_in_asu = number_of_residues_in_asu
        self.title = os.path.splitext(os.path.split(self.filename)[1])[0] + "_autoproc"
        self.proj_name =  os.path.splitext(os.path.split(self.filename)[1])[0].upper()
        self.scalepack2mtz_dict = dict(title = self.title ,spag = self.spag , cell = self.cell_dimensions_string , wavelength = self.wavelength , proj_name = self.proj_name)
        self.outputdir = os.path.join(auriga_output_directory_root,self.proj_name) 
        if not os.path.exists(self.outputdir):
            os.mkdir(self.outputdir)
            
    def extract_cell_dimensions_string(self):
        """
        Arguments:
        - `self`:
        """
        self.file.seek(0)
        self.file.readline()
        self.file.readline()
        cell_dimensions_string = ",".join(self.file.readline().split()[:-1])
       # print "CELL DIM STR" , cell_dimensions_string
        return cell_dimensions_string
    
    def extract_spag(self):
        self.file.seek(0)
        self.file.readline()
        self.file.readline()
        cell_line =  self.file.readline().split()
     #   print "CELL LINE" , cell_line
        return cell_line[-1]
    
    def describe(self):
        description = """Scalepack file:{self.filename},{self.spag},{self.cell_dimensions_string}""".format(self=self)
       # print description
        
    def mtzoutpath(self):
        return  os.path.join(self.outputdir,"{self.proj_name}_trnfreeR.mtz".format(self=self))
    
    def create_and_return_runscript_file(self):
        scrfile1 = open(os.path.join(self.outputdir,"%s_1.sh" % self.proj_name),"w")
        scrfile2 = open(os.path.join(self.outputdir,"%s_2.sh" % self.proj_name),"w")
        scrfile3 = open(os.path.join(self.outputdir,"%s_3.sh" % self.proj_name),"w")
        scrfile4 = open(os.path.join(self.outputdir,"%s_4.sh" % self.proj_name),"w")
        outfile_prefix  = os.path.join(self.outputdir,self.proj_name)
      #  print "PROJ_NAME_OUTPREFIX set to ", outfile_prefix ,"DIRECTORY"
        
        scr1 =  """#!/bin/sh 
#set -e
# bug # 3192 - run-all examples produce harvest files - well to counteract
# this here set HARVESTHOME to somewhere in $CCP4_SCR

HARVESTHOME=${self.outputdir}
export HARVESTHOME

#   from /home/hari/official_ccp4/ccp4-6.1.3/examples/unix/runnable
#   SCALEPACK2MTZ
#
#  h k l I+ SigI+ I- SigI-   were extracted from aucn.na4
#  (acentric data only), and put into scalepack format. 
#  This is simply to illustrate the procedure for getting 
#  scalepack data into CCP4. I don't really know if it
#  is a good example.
#
#  (You can use the same procedure whether or not you have 
#  anomalous data.)

scalepack2mtz hklin {self.filename}  hklout {outfile_prefix}_junk1.mtz <<eof
name project {self.proj_name} crystal {self.proj_name} dataset {self.proj_name}
symm {self.spag}
end
eof
""".format(self = self,outfile_prefix=outfile_prefix)
        
        scr2 = """#!/bin/sh
# convert Is to Fs and Ds.

truncate hklin {outfile_prefix}_junk1.mtz hklout {outfile_prefix}_junk2.mtz <<eof
title {self.proj_name} data 
truncate yes
nresidue {self.number_of_residues_in_asu}
labout  F=FP_{self.proj_name} SIGF=SIGFP_{self.proj_name}
end
eof
""".format(self = self,outfile_prefix=outfile_prefix)
        
        scr4 = """#!/bin/sh
# Add free r to reflections
freerflag hklin  {outfile_prefix}_trn.mtz hklout  {outfile_prefix}_trnfreeR.mtz <<eof
FREERFRAC 0.05
END
eof""".format(self=self, outfile_prefix = outfile_prefix)

        scr3 = """#!/bin/sh
# get correct sort order and asymmetric unit

cad hklin1 {outfile_prefix}_junk2.mtz hklout {outfile_prefix}_trn.mtz <<eof
labi file 1 ALL
sort H K L
end
eof
#""".format(self = self,outfile_prefix=outfile_prefix)
        scrfile1.write(scr1)
        scrfile2.write(scr2)
        scrfile3.write(scr3)
        scrfile4.write(scr4)
        scrfile1.close()
        scrfile2.close()
        scrfile3.close()
        scrfile4.close()
        os.chmod(scrfile1.name,0755)
        os.chmod(scrfile2.name,0755)
        os.chmod(scrfile3.name,0755)
        os.chmod(scrfile4.name,0755)
        return (scrfile1.name,scrfile2.name,scrfile3.name,scrfile4.name)
    
#        print scrfile.name
#        mutex.acquire()
#        subprocess.call([scrfile.name])
#        sys.stdout.flush()
#        mutex.release()

def report(message):
     mutex.acquire()
   #  print message
     sys.stdout.flush()
     mutex.release()

def safe_write_script(string,filehandle):
    mutex.acquire()
    filehandle.write(string)
    filehandle.close()
    mutex.release()

class ScaToMtzConvertor(Thread):
    def __init__(self, in_queue, out_queue):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
    def run(self):
        while True:
            path = self.in_queue.get()
            sys.stdout.flush()
            if path is None:
                self.out_queue.put(None)
                break
       #     print "GOTPATH" , path
            report("Converting %s" % path)
            myfile = scalatomtz(path)
            scrfiles = myfile.create_and_return_runscript_file()
            for index,file in enumerate(scrfiles):
                subprocess.call([file])
                #print "CALLED%s%s" % (index,file) *5
            #report(myfile.describe())
            report("Done %s" %  path)
            self.out_queue.put(myfile.mtzoutpath())

            
class PhaserRunOrchestrator(Thread):
    def __init__(self,in_queue,out_queue):
        Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
    def run(self):
        while True:
            mtzfile = self.in_queue.get()
            if mtzfile is None:
                self.out_queue.put(None)
                break
            runner = PhaserRun(mtzfile)
            runner.run()
            time.sleep(2)
            # This has the root of the output files
         #   print "PUTTING TO OUT PATH" , runner.outfilepath
            self.out_queue.put(runner.outfilepath)


    
class PhaserRun(object):
    """Class that runs automated molecular replacement using phaser
    """
    
    def __init__(self,inputmtzpath):
        """Class looks at input mtz , gets the right pdb and number of molecules from mrdict.mrdict and then launches a phaser run
        """
        self.mycomfile = None
        self.outfilepath = None
        self.proj_name = None
        try:
            self.data_tuple   = modeldict[os.path.splitext(os.path.split(inputmtzpath)[1])[0].split("_")[0].upper()]
            self.inputmtzpath = inputmtzpath
            self.pdb_path = self.data_tuple[0]
            self.num_copies = self.data_tuple[1]
            self.proj_name =  "_".join(os.path.splitext(os.path.split(self.inputmtzpath)[1])[0].split("_")[0:2]).upper()
            self.outfilepath = os.path.join(os.path.join(auriga_output_directory_root,self.proj_name),self.proj_name)
            self.mycomfile = """#!/bin/sh 
phaser <<eof
TITLE {self.proj_name} phaser run automatic
MODE MR_AUTO
HKLIn {self.inputmtzpath}
LABIn F=FP_{self.proj_name} SIGF=SIGFP_{self.proj_name}
ENSEmble 1    PDBfile {self.pdb_path} IDENtity 0.99
COMPosition PROTein MW 28853 NUM {self.num_copies} #beta
SEARch ENSEmble 1 NUM {self.num_copies}
ROOT {self.outfilepath} # not the default
eof""".format(self=self)
        except KeyError:
            pass
        
    def run(self):
        comfile = open(os.path.join(os.path.join(auriga_output_directory_root,self.proj_name),self.proj_name  + "_phaser_input.sh"),"w")
        safe_write_script(self.mycomfile,comfile)
        os.chmod(comfile.name,0755)
        subprocess.call([comfile.name])
   #     print "PHASER for {self.proj_name} DONE {self.inputmtzpath} Processed . Files written to {self.outfilepath}".format(self=self)
        
        
class Refmac5Runner():

    def __init__(self,phaseroutput_root):
        self.mtzfile = phaseroutput_root.strip() + ".1.mtz"
        self.pdbfile = phaseroutput_root.strip() + ".1.pdb"
        self.proj_name = os.path.split(phaseroutput_root)[-1]
        self.outputdir = os.path.join(auriga_output_directory_root,self.proj_name)
        if os.path.exists(self.mtzfile) and os.path.exists(self.pdbfile):
            pass
        else:
            pass
            #print "phaser_run files {self.mtzfile} , {self.pdbfile} not FOUND".format( self = self)

    def run(self):
        #print self.pdbfile
        self.comstring = """#!/bin/csh
#
#   Example of refinement by refmac
#
set inmtz={self.outputdir}/{self.proj_name}_trnfreeR.mtz
start:

set name = {self.proj_name}
set last = 1
set cycles = 1
set count = 0
while ($count != $cycles)
echo '*******************************************************************'
echo  $count
echo '*******************************************************************'
@ curr = $last + 1

#
# Refmac 
#
refmac:
refmac5 \
HKLIN   $inmtz \
HKLOUT   {self.outputdir}/{self.proj_name}.${{curr}}.mtz \
XYZIN   {self.outputdir}/{self.proj_name}.${{last}}.pdb \
XYZOUT  {self.outputdir}/{self.proj_name}.${{curr}}.pdb \
<< eor
#
#####Do not add hydrogens
#
MAKE_restraints HYDRogens No
#
#####Do not check correctness of all monomers. Rely on users naming
#####One should be careful in using this option.
#
MAKE CHECk 0
#
####Input mtz labels. 
#
LABIN FP=FP_{self.proj_name} SIGFP=SIGFP_{self.proj_name} FREE=FreeR_flag
#
####Output mtz labels
#
LABO FC=FC PHIC=PHIC    FWT=2FOFCWT PHWT=PH2FOFCWT -
                     DELFWT=FOFCWT  PHDELWT=PHFOFCWT
#
####Restrained refinement. Reflections between 20 1.5Å resolution will be used
#
REFI TYPE RESTrained RESOLUTION  20 1.10
#
####Use maximum likelihood residual
####Use maximum likelihood residual
#
REFI RESI MLKF
#
####Refine isotropic B values.
# 
REFI BREF ISOTropic  
#
####Use 0.35 as weighting between X-ray and geometry
# 
WEIGHT AUTO
#
####Scaling parameters. Use BULK solvent based on Babinet's principle.
####NB: Unless otherwise SOLVENT NO given contribution of bulk solvent
####based on constant value will be used. 
#
SCALe TYPE BULK   
#
####Fix Babinet's bulk solvent B value to 200.0
#
SCALe LSSCale FIXBulk 200.0
#
####number of refinement cycles
#
NCYC 2
#
####Monitor only overall statistics
# 
MONI MEDIUM
end
eor
if ($status) exit
#
@ last++
@ count++
end
""".format(self=self)
        self.mycomfile = open(os.path.join(self.outputdir,self.proj_name + "_refmac5_input.sh"),"w")
        safe_write_script(self.comstring,self.mycomfile)
        os.chmod(self.mycomfile.name,0755)
        subprocess.call([self.mycomfile.name])
    
    
class Refmac5RunOrchestrator(Thread):

    def __init__(self,in_queue,out_queue):
        Thread.__init__(self)
   #     print "REFMAC  Orchestrator"
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            my_mtz = self.in_queue.get()
            if my_mtz is None:
                break
            runner = Refmac5Runner(my_mtz)
            runner.run()
            time.sleep(2)
            self.out_queue.put(my_mtz)
            
scafile_in_queue = Queue()
phaser_in_queue = Queue()
mutex = Lock()

THREAD_COUNT = 1
worker_list = []

for i in range(THREAD_COUNT):
    worker = ScaToMtzConvertor(scafile_in_queue, phaser_in_queue)
    worker.start()
    worker_list.append(worker)

phaser_worker_list = []

refmac5_in_queue = Queue()

if __name__ == '__main__':
    sca_listfile  = "scafiles.txt"
    for i in open(sca_listfile,"r"):
        scafile_in_queue.put(i) 

for i in range(THREAD_COUNT):
    scafile_in_queue.put(None)      
    
for worker in worker_list:
    worker.join()  

for i in range(THREAD_COUNT):
    phaser_run = PhaserRunOrchestrator(phaser_in_queue,refmac5_in_queue)
    phaser_run.start()
    phaser_worker_list.append(phaser_run)
    
for phaserrunner in phaser_worker_list:
    phaserrunner.join()


refmac5_worker_list = []
refmac5_out_queue = Queue()

for i in range(THREAD_COUNT):
    refmac5_run = Refmac5RunOrchestrator(refmac5_in_queue,refmac5_out_queue)
  #  print "RUNNING REFMAC"
    refmac5_run.start()
    refmac5_worker_list.append(refmac5_run)

for refmac5_runner in refmac5_worker_list:
    refmac5_runner.join()
    

# with 4        
#real	1m17.021s
#user	1m2.530s
#sys	0m5.300s
#with 1
#real	1m19.310s
#user	1m4.490s
#sys	0m5.410s
#with 8 
#real	1m13.971s
#user	1m1.020s
#sys	0m5.070s
