import gfapy
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import pickle
import io


parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument("-g", help="gfa file", required=True)
requiredNamed.add_argument("-list", help="list file", required=True)
requiredNamed.add_argument("-outfile", help="output file file", required=True)
args = parser.parse_args()
initial_graph = gfapy.Gfa.from_file(args.g,vlevel=0)

#with open(args.list, 'rb') as f:
    #unitigs = pickle.load(f)


with open(args.list, 'r') as f:
    unitigs = [line.rstrip(u'\n') for line in f]

def subset_graph():
    cur_unitigs=unitigs
    for ed in initial_graph.segments:
        if ed.name not in cur_unitigs:
            initial_graph.rm(ed)
    for link in initial_graph.dovetails:
        if link.to_segment not in cur_unitigs or link.from_segment not in cur_unitigs:
            initial_graph.rm(link)
    gfapy.Gfa.to_file(initial_graph, args.outfile)



subset_graph()
