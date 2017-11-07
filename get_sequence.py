"""Usage: get_sequence.py  <uniprot_id> [<start-stop>]"""

from cmd import Cmd
import urllib2
import pprint

from docopt import docopt

class GetSequence(Cmd):
	
	def __init__(self,uniprot_id,start_stop,*args,**kwds):
		Cmd.__init__(self,*args,**kwds)
		self.seq_fileobj = urllib2.urlopen("http://www.uniprot.org/uniprot/{}.fasta".format(uniprot_id))
		self.seq_header = self.seq_fileobj.next()
		print "Read in sequence information for {}.".format(self.seq_header[:-1])
		self.sequence = [achar for a_line in self.seq_fileobj for achar in a_line if achar != "\n"]
		print "Sequence:{}\n".format("".join(self.sequence))		
		self.prompt = "Sequence[start-stop]:"
		self.start_stop = start_stop
		
	def preloop(self):
		start_stop = self.start_stop
		if self.start_stop:
			self.default(start_stop)
		
	def default(self,start_stop):
		start,stop = start_stop.split("-")
		print "Sequence[{}-{}]:".format(start,stop),"".join(self.sequence[int(start)-1:int(stop)])
	
	def do_EOF(self, line):
		return True
		
if __name__ == "__main__":
	arguments = docopt(__doc__,version="0.1")
	GetSequence(uniprot_id=arguments["<uniprot_id>"],start_stop=arguments["<start-stop>"]).cmdloop()
