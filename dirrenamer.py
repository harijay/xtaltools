import os
import shutil

source_directory="/Users/hari/OneDriveBusiness/OneDrive - EDITASMED/DropboxMigration/constellation_wrapup/constellation_wrapup/Hari-refinements/G_NLE9-B-Norleucine-peptide/coot-backup"
template_sample="_Users_hari_constellation_wrapup_Hari-refinements_G_MET9-SAH-A_Nle_8.1.pdb_Mon_Jan__4_06/53/56_2016_modification_32.pdb.gz"

for root,dirs,files in os.walk(source_directory):
	for a_file in files:
		a_file_mod = a_file.replace("/","_").replace("_","uscore").replace(":","colon")
		print(os.path.join(root,a_file_mod))
		try:
			shutil.move(os.path.join(root,a_file),os.path.join(root,a_file_mod))
		except OSError:
			print("Error handling %s\n" % os.path.join(root,a_file_mod))
