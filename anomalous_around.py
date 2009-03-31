#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hari"
__date__ ="$Mar 27, 2009 9:32:07 AM$"

import urllib

class AtomDict(object):

    def __init__(self,name):
        self.name = name
        self.dict_url = "http://skuld.bmsc.washington.edu/scatter/data/%s.dat" % self.name
        self.dict = {}
        self.vals = []
        import urllib
        self.data = urllib.urlopen(self.dict_url)
        self.make_dict()

    def print_data(self):
        print "%-14s%-14s%-14s" % ("Energy", "Fprime" , "Fdprime")
        for i in self.data:
            print "%-14s%-14s%-14s" % (i.split()[0],i.split()[1],i.split()[2])

    def make_dict(self):
        for i in self.data:
            vals = i.strip().split()
            self.dict[vals[0]] = (vals[1],vals[2])
            self.vals.append(vals[0])

    def closest_vals(self,energy):
        for entry in self.vals:
            if float(energy) > float(entry):
                pass
            else:
                current_index = self.vals.index(entry)
                print "Indexed values for Value:%s," % energy,self.vals[ current_index - 1],self.dict[self.vals[current_index - 1]],entry,self.dict[entry],self.vals[current_index + 1], self.dict[self.vals[current_index + 1]]
                exit()

    def print_energy_intervals(self):
        for index,entry in enumerate(self.vals):
            first = entry
            try:
                print float(a.vals[index + 1]) - float(entry)
            except IndexError:
                pass

def main():
    from optparse import OptionParser
    p = OptionParser()
    p.add_option("--atom" , "-a", dest="atom",help="Atom id for eg. Se " , metavar="Se")
    p.add_option("--energy" ,"-e", dest="energy",help="Energy in ev ",metavar="[Energy ev]")
    p.add_option("--wave","-w", dest="wave",help="Wavelength in A",metavar="[wavelength]")
    try:
        sys.argv[1]
    except BaseException :
        p.print_help()
        exit()
    options,spillover = p.parse_args()

    if (options.wave is not None) and (options.energy is None) :
        h = 6.6260689633e-34
        c = 299792458
        electron  = 1.60217653141e-19
        options.energy = (h*c)/(float(options.wave)*1e-10*electron)
    a = AtomDict(options.atom)
    a.closest_vals(options.energy)

if __name__ == "__main__":
  main()
  
