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
#pysam.view("-H",args.bam)

test=subprocess.check_output("samtools view  -H %s >headers.txt" % args.bam,
                            shell=True)


with open(args.list, 'r') as f:
    unitigs = [line.rstrip(u'\n') for line in f]
'''
text=''
with open("headers.txt", 'r') as f:
    #unitigs = [line.rstrip(u'\n') for line in f]
    for line in f: 
        try:
            if str(re.sub("SN:","", line.split('\t')[1])) in unitigs or line.split('\t')[0]!="@SQ":
                text=text+line
        except:
            pass

print(text)'''
#obam = pysam.AlignmentFile(args.o, "w",text=text)
obam=pysam.AlignmentFile(args.o, "w",template=bam)



def subset_bam():
    for unitig in unitigs:
        for b in bam.fetch(unitig,until_eof=True):
            #try:
            obam.write(b)
            #except:
                #pass
                #print(unitig)
                #exit()
    bam.close()
    obam.close()
    pysam.sort("-o", args.o, args.o)


subset_bam()

