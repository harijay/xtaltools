#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
import parser

__author__="hari"
__date__ ="$Mar 27, 2009 8:52:03 AM$"

def main():
    import sys
    import os
    h = 6.6260689633e-34
    c = 299792458
    electron  = 1.60217653141e-19

    def toenergy(wave):
        energy = (h*c)/(float(wave)*1e-10*electron)
        return energy

    def towave(energy):
        wave = (h*c)/(float(energy)*electron)
        return wave

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--energy","-e",dest="energy",metavar="energy ev",help="Energy in ev")
    parser.add_option("--wave","-w",dest="wave",metavar="wave A",help="wavelenbth in Angstrom")
    (options,spillover) = parser.parse_args()


    if options.energy is not None:
        energy = options.energy
        wave = towave(energy)
        print "The input %s energy in ev corresponds to %s wavelength" % ( energy , wave)


    elif options.wave is not None:
        wave = sys.argv[2]
        energy = toenergy(wave)
        print "The input %s wavelength corressponds to %s ev " % (wave,energy)
    else:
        parser.print_help()
        exit()

if __name__ == "__main__":
    main()
