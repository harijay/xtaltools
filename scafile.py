#!/usr/bin/python
import sys
class Scafile(object):

	def __init__(self,filename):
		self.filename = filename
		self.spg = None
		self.cell = None
		try:
			self.file = open(self.filename)
		except IOError, e:
			print e
			raise
		self.file.readline()
		self.file.readline()
		cellline = self.file.readline().split()
		self.cell = ",".join(cellline[:-1])
		self.spg = cellline[-1]


if __name__=="__main__":
    import optparse
    p = optparse.OptionParser()
    p.add_option("-s","--scafile",dest="scafile",metavar="[*.sca]",help="input scafile")
    if len(sys.argv) <= 1:
        p.print_help(),
        exit()
    (options,spillover) = p.parse_args()
    # Scafile object
    mysca = None
    try:
        mysca = Scafile(options.scafile)
    except TypeError, e:
        mysca = Scafile(spillover[0])
    print "CELL:%s" % mysca.cell
    print "SPAG:%s" % mysca.spg