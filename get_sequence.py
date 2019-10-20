"""Usage: get_sequence.py  <uniprot_id> [<start-stop>]"""

from cmd import Cmd
import urllib.request, urllib.error, urllib.parse
import ssl
import tempfile
from tempfile import NamedTemporaryFile
import Bio
from urllib.error import HTTPError

from docopt import docopt

class GetSequence(Cmd):

    def __init__(self,uniprot_id,start_stop,*args,**kwds):
        Cmd.__init__(self,*args,**kwds)
        context = ssl._create_unverified_context()
        self.seq_fileobj = urllib.request.urlopen("https://www.uniprot.org/uniprot/{}.fasta".format(uniprot_id),context=context)
        self.seq_header = next(self.seq_fileobj)
        print("Read in sequence information for {}.".format(self.seq_header.rstrip()))
        self.sequence = [char for a_line in self.seq_fileobj for char in a_line.decode().rstrip('\n')]
        print("Sequence:{}\n".format("".join(self.sequence)))
        self.prompt = "Sequence[{start}-{stop}]:".format(start = 1, stop = len(self.sequence))
        self.start_stop = start_stop

    def preloop(self):
        start_stop = self.start_stop
        if self.start_stop:
            self.default(start_stop)

    def default(self,start_stop):
        try:
            start,stop = start_stop.split("-")
        except ValueError:
            start = start_stop
            stop = start_stop
        print("Sequence[{}-{}]:".format(start,stop),"".join(self.sequence[int(start)-1:int(stop)]))

    def do_EOF(self, line):
        return True

if __name__ == "__main__":
    arguments = docopt(__doc__,version="0.1")
    try:
        GetSequence(uniprot_id=arguments["<uniprot_id>"],start_stop=arguments["<start-stop>"]).cmdloop()
    except HTTPError:
        print("Sequence for {uniprot_id} not found. Check the id".format(uniprot_id=arguments["<uniprot_id>"]))
    except KeyboardInterrupt:
        print("Thank you for using {}".format(__file__))