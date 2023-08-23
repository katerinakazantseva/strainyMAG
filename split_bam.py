from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import pysam
import re
import os
import subprocess
try:
    os.mkdir("output/bams")
except:
    pass
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument("-bam", help="bam file", required=True)
requiredNamed.add_argument("-list", help="list file", required=True)
requiredNamed.add_argument("-o", help="output file", required=True)
args = parser.parse_args()

bam = pysam.AlignmentFile(args.bam)
obam=pysam.AlignmentFile(args.o, "w",template=bam)

with open(args.list, 'r') as f:
    unitigs = [line.rstrip(u'\n') for line in f]


def subset_bam():
    for unitig in unitigs:
        for b in bam.fetch(unitig,until_eof=True):
            obam.write(b)
    bam.close()
    obam.close()
    pysam.sort("-o", args.o, args.o)


subset_bam()
