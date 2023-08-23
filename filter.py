import re
import subprocess

def cov_filtered(list):
    print("Filter_coverage")
    res=[]
    try:
        with open(list, 'r') as f:
               lines = [line.rstrip('\n') for line in f]
               for line in lines:
                   if int(line.split(',')[1].split(".")[0])>10:
                       bin=line.split(',')[0]
                       res.append("output/transformed_bins/%s.fa" % bin)
    except: pass
    print(res)
    return(res)

def get_best():
        res=[]
        print("Filter by MAG quality")
        test="""awk '$2>=80 && $3<=11 {{ print $1}}' output/qa_bins/quality_report.tsv """
        proc = subprocess.Popen(test,  shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
        stdout=re.sub('\'','',re.sub('b', '',str(stdout_value),1))
        for item in stdout.split('\\n'):
                if item!='':
                    res.append("output/bams/%s.bam" % item)
                    res.append("output/bams/%s.bam.bai" % item)
        print(res)
        return res
#cov_filtered("output/coverage_list.lst")
