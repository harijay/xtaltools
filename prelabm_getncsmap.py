#!/usr/bin/python
import os
import sys
import re
# Take in pdb chain
# Read pdb chain and make sure all the chains are kosher
# Calculate the symmetry matrices for A to B and  C and D
# Do the tansform
# Recapitulate the built pdb
# Display the pdb in pymol

pdb = open(sys.argv[1] , "read")
pdb_pfx = os.path.splitext(pdb.name)[0]
pdb_sfx =  os.path.splitext(pdb.name)[1]
max_atomnum = 0
fixedpdb = []

def cleanup_pdb(filename , chainid): 
 pdb_dirty = open(filename,"read")
 file_root = os.path.splitext(pdb_dirty.name)[0]
 new_file = file_root + "_mod.pdb"
 pdbout = open(new_file , "write")
 chain_id = chainid
 global max_atomnum
# Atom counter
 def change_segid_chaind(atom_array,new):
  atom_array[7] = new
  atom_array[-3] = new + (4-len(new))*' '
  atom_array[1] = "%5d" % (max_atomnum)
  return atom_array

 for eachline in pdb_dirty:
  pdbout.flush()
  # If Line is not a ATOM line leave it alone and pass it on
  atom = "^ATOM"
  if (re.search(atom,eachline)):
   max_atomnum  = max_atomnum + 1 ;
   myline = []
   myline.extend([eachline[0:6],eachline[6:11]," ",eachline[12:16],eachline[16],eachline[17:20]," ",eachline[21],eachline[22:26],eachline[26],3*" ",eachline[30:38],eachline[38:46],eachline[46:54],eachline[54:60],eachline[60:66],6*" ",eachline[72:76],eachline[76:78],eachline[78:80]])
   myline = change_segid_chaind(myline,chain_id)
   s = ""
   for j in range(len(myline)):
    s = s + str(myline[j])
   pdbout.write(s + "\n")
   pdbout.flush()
  else:
   pdbout.write(eachline)
 if(os.path.exists(pdbout.name)):
  os.system("mv %s %s" % (pdbout.name,pdb_dirty.name))
  print "Cleaned up file %s and wrote file %s with segid and chainid %s" % (pdb_dirty.name,pdbout.name, chainid) 
 pdbout.close()
 
			   
def select_chain_writepdb(chainid):
 outfile_name = pdb_pfx + "_%s" % chainid + pdb_sfx
 logfile_name = pdb_pfx + "_%s" % chainid + "_chainextract.log"
# logfile = open(logfile_name , "write")
 exec_str = '''pdbset XYZIN %s  XYZOUT %s<<eof >%s\n
 remark pdbset for extracting mol %s\n
 select chain -
 %s
 end
 eof''' % (pdb.name ,outfile_name,logfile_name,chainid,chainid)
 os.system(exec_str)
 if(os.path.exists(outfile_name)):
  print "Done extracting chain %s" % chainid 
  file_array = [outfile_name , logfile_name]
  return file_array
 else:
  print "Problem in command %s see log file %s " % (exec_str, logfile_name) 


def run_lsqkab(moving , fixed, idA , idB ,start_similarity_residue_number , end_similarity_residue_number):
 outfile_name = os.path.splitext(moving)[0] + "_%s_%s_lsq1" % (idA,idB) +  os.path.splitext(moving)[1]
 logfile_name =  os.path.splitext(moving)[0] + "_%s_%s_lsqkab.log" % (idA,idB)
# logfile = open(logfile_name , "write")
 exec_str='''lsqkab XYZIN2 %s  XYZIN1 %s  XYZOUT %s<<eof>%s\n
 title test superpose for python script
 fit res CA %d to %d -
 chain %s
 match %d to %d -
 chain %s
 output -
 xyz
 end
 eof''' % ( moving,fixed,outfile_name, logfile_name,start_similarity_residue_number , end_similarity_residue_number,idA, start_similarity_residue_number , end_similarity_residue_number,idB)
 os.system(exec_str)
 if(os.path.exists(outfile_name)):
  print "Lsqkab sucess transformed %s chain onto %s chain" % (moving , fixed)
  file_array = [outfile_name , logfile_name]
  return file_array
 else:
  print "Problem in command %s see log file %s " % (exec_str, logfile_name)

def analyse_ncs_log(logfile_name):
 parse_result = []
#order for parse_result = cen_working , cen_reference , rot_mat 1 , rot_mat 2 , rot_mat 3 , trans vect 
# lines to capture 
#      CENTROID OF "WORKING" MOLECULE  :
#     CENTROID OF "REFERENCE" MOLECULE  :
#       ROTATION MATRIX:
#  TRANSLATION VECTOR IN AS   22.72297  44.87856  44.77779
 file = open(logfile_name,"read")
 for eachline in file:
  centroid_working = re.search("CENTROID OF \"WORKING\" MOLECULE\s+:\s+(.*)",eachline)
  centroid_fixed = re.search("CENTROID OF \"REFERENCE\" MOLECULE:\s+(.*)",eachline)
  rotation_matrix = re.search("ROTATION MATRIX:",eachline)
  if (rotation_matrix != None):
   parse_result.append(file.next().strip())
   parse_result.append(file.next().strip())
   parse_result.append(file.next().strip())
   tran = re.search("TRANSLATION VECTOR IN AS\s+(.*)",file.next())
   if (tran != None):
    parse_result.append(tran.group(1).strip())
   else:
    pass
  elif(centroid_working != None):
   parse_result.append( centroid_working.group(1).strip())
  elif(centroid_fixed != None):
   parse_result.append( centroid_fixed.group(1).strip())
  else:
   pass
 return parse_result

def print_for_resolve(parse_result):
 ncs = '''rota_matrix %s\nrota_matrix %s\nrota_matrix %s\ntran_orth %s\ncenter_orth %s\n''' % (parse_result[2],parse_result[3],parse_result[4],parse_result[5],parse_result[1])
 print ncs

def make_ncs():
 test_a = select_chain_writepdb("A")
 test_b = select_chain_writepdb("B")
 test_c = select_chain_writepdb("C")
 test_d = select_chain_writepdb("D")

 if (test_a != None) & (test_b != None) & ( test_c != None ) & (test_d != None):
  print "Successfully extracted Chain %s and Chain %s and Chain %s and Chain %s " % (test_a[0] , test_b[0] , test_c[0],test_d[0])
  lsq_run_ab = run_lsqkab(test_a[0],test_b[0],"A","B",45,415)
  lsq_run_ac = run_lsqkab(test_a[0],test_c[0],"A","C",45,415)
  lsq_run_ad = run_lsqkab(test_a[0],test_d[0],"A","D",45,415)
  parse_tf_ab = analyse_ncs_log(lsq_run_ab[1])
  parse_tf_ac = analyse_ncs_log(lsq_run_ac[1])
  parse_tf_ad = analyse_ncs_log(lsq_run_ad[1])
  print "rota_matrix 1 0 0 \nrota_matrix 0 1 0 \nrota_matrix 0 0 1 \ntran_orth 0 0 0 \ncenter_orth %s \n" % parse_tf_ab[0]
  print_for_resolve(parse_tf_ab)
  print_for_resolve(parse_tf_ac)
  print_for_resolve(parse_tf_ad)

def make_babies():
    # 
 test_a = select_chain_writepdb("A")
 test_b = select_chain_writepdb("B")
 test_c = select_chain_writepdb("C")
 test_d = select_chain_writepdb("D")
 parse_tf_ab , parse_tf_ac , parse_tf_ad = None , None , None
 if (test_a != None) & (test_b != None) & ( test_c != None ) & (test_d != None):
  print "Successfully extracted Chain %s and Chain %s and Chain %s and Chain %s " % (test_a[0] , test_b[0] , test_c[0],test_d[0])
  lsq_run_ab = run_lsqkab(test_a[0],test_b[0],"A","B",45,415)
  lsq_run_ac = run_lsqkab(test_a[0],test_c[0],"A","C",45,415)
  lsq_run_ad = run_lsqkab(test_a[0],test_d[0],"A","D",45,415)
  parse_tf_ab = analyse_ncs_log(lsq_run_ab[1])
  parse_tf_ac = analyse_ncs_log(lsq_run_ac[1])
  parse_tf_ad = analyse_ncs_log(lsq_run_ad[1])
  print "rota_matrix 1 0 0 \nrota_matrix 0 1 0 \nrota_matrix 0 0 1 \ntran_orth 0 0 0 \ncenter_orth %s \n" % parse_tf_ab[0]
  print_for_resolve(parse_tf_ab)
  print_for_resolve(parse_tf_ac)
  print_for_resolve(parse_tf_ad)
  def make_child(apdb,bpdb,chainid,tfarray):
   outfile_name = os.path.splitext(bpdb[0])[0] + "_tf.pdb"
   logfile_name = os.path.splitext(bpdb[0])[0] + "_tf_logfile.log"
   exec_str = '''pdbset XYZIN %s XYZOUT %s <<EOF>%s\n
remark [No title given]
rotate -
    %s -
    %s -
    %s
shift -
    %s
end
EOF''' %(apdb[0],outfile_name,logfile_name,tfarray[2],tfarray[3],tfarray[4],tfarray[5])
   print exec_str
   print outfile_name
   print logfile_name
   os.system(exec_str)
   cleanup_pdb(outfile_name,chainid)
   fixedpdb.append(outfile_name)

 make_child(test_a,test_b,"B",parse_tf_ab)
 make_child(test_a,test_c,"C",parse_tf_ac)
 make_child(test_a,test_d,"D",parse_tf_ad)
 
 
make_ncs() 
test_a = select_chain_writepdb("A")
cleanup_pdb(test_a[0],"A")
fixedpdb.append(test_a[0])
make_babies()

def make_final():
 import re
 file_out = pdb_pfx + "_reworked.pdb"
 final = open(file_out , "write")
 garbage = open(os.path.splitext(final.name)[0] + "garbage.txt" , "write")
 header = None
 for file in fixedpdb:
  readfile = open(file,"read")
  for line in readfile:
   if(header == None):
    final.write(line)
    final.flush()
    # when you find the file atom line
    if (re.search("^ATOM",line)):
      header = "got"
#      final.write(line)
   elif(re.search("^ATOM",line)):
    final.write(line)
    final.flush()
   else:
    garbage.write(line)
    garbage.flush()

    
  readfile.close()
  print "Closed %s \n after appending to %s" %(readfile.name , final.name)
 final.write("END\n")
 garbage.close()
 print "CLOSED final %s" % final.name

make_final()      
   
