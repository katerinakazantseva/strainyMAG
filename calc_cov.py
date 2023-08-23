import subprocess
import os
import re
files = os.listdir("output/bams")



def calc_cov():
    for i in files:
        if re.match('.*bai', i)==None:
            bin=re.sub('\.bam','',i)
            cov=subprocess.check_output("samtools depth  -a output/bams/%s.bam  | awk '{sum+=$3} END {print sum/NR}'" % bin,shell=True)
            cov=cov.decode("utf-8")
            cov=cov.replace("\n", "")
            print(bin+","+str(cov))

calc_cov()

