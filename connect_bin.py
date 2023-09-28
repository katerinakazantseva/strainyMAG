import sys
import os

import gfapy
from tqdm import tqdm

MAX_DEPTH = 8

def make_bin_connected(graph, bin, unavailable_unitigs):
    for unitig in tqdm(bin):
        L_connected, R_connected = check_unitig_connectedness(graph, unitig, bin)
        
        if not L_connected:
            BFS(graph, bin, unitig, 'L', unavailable_unitigs)

        if not R_connected:
            BFS(graph, bin, unitig, 'R', unavailable_unitigs)
    return bin

        
def check_unitig_connectedness(graph, unitig, bin):
    dovetails_L = graph.try_get_segment(unitig).dovetails_L
    dovetails_R = graph.try_get_segment(unitig).dovetails_R

    L_connected = False
    R_connected = False
    for line in dovetails_L:
        if (line.to_name == unitig and line.from_name in bin or
            line.from_name == unitig and line.to_name in bin):
            L_connected = True
            break

    for line in dovetails_R:
        if (line.to_name == unitig and line.from_name in bin or
            line.from_name == unitig and line.to_name in bin):
            R_connected = True
            break

    return L_connected, R_connected


def BFS(graph, bin, start, direction, possessed_unitigs):
    # Visit unitigs that are in direction side and mark them visited
    # if they are in the bin:
        # backtrace to starting unitig, add unitigs in this path to bin, exit
    # for each node, visit neighbors of that node and mark them visited


    queue = []
    visited = [start+'+', start+'-']
    prev = {start+'+': -1, start+'-': -1}
    prev_direction = []
    depth = 0

    # initilize the queue with the nodes in the direction to be visited

    if direction == 'L':
        segments = graph.try_get_segment(start).dovetails_L
    if direction == 'R':
        segments = graph.try_get_segment(start).dovetails_R
    for s in segments:
        if s.from_name == start:
            unitig = s.to_name+s.to_orient
            queue.append(unitig) 
            visited.append(unitig)
            prev[unitig] = start + s.from_orient
            prev_direction.append('to')
        else:
            unitig = s.from_name+s.from_orient
            queue.append(unitig)
            visited.append(unitig) 
            prev[unitig] = start + s.to_orient
            prev_direction.append('from')


    connected = False
    while queue and not connected:
        depth += 1
        if depth > MAX_DEPTH:
            break
        
        curr_unitig = queue.pop(0)
        curr_unitig_name = curr_unitig[:-1]
        curr_unitig_orient = curr_unitig[-1]
        prev_unitig_dir = prev_direction.pop(0)

        # we can't use unitigs that belong to another bin
        if curr_unitig_name in possessed_unitigs:
            # print(f'{curr_unitig_name} is ignored because it belongs to another bin')
            continue

        segments = graph.try_get_segment(curr_unitig_name).dovetails

        for s in segments:
            """
            direction was the same as before:
                orient is also same -> NOT OK
                orient different -> OK
            direction was different than before:
                orient is same -> OK
                orient is different -> X
            """
            if s.to_name == curr_unitig_name:
                if prev_unitig_dir == 'to':
                    if s.to_orient == curr_unitig_orient:
                        continue
                    else:
                        neighbor = s.from_name + gfapy.invert(s.from_orient)
                        neighbor_direction = 'to'
                elif prev_unitig_dir == 'from':
                    if s.to_orient == curr_unitig_orient:
                        neighbor = s.from_name + s.from_orient
                        neighbor_direction = 'from'
                    else:
                        continue

            elif s.from_name == curr_unitig_name:
                if prev_unitig_dir == 'to':
                    if s.from_orient == curr_unitig_orient:
                        neighbor = s.to_name + s.to_orient
                        neighbor_direction = 'to'
                    else:
                        continue
                else:
                    if s.from_orient == curr_unitig_orient:
                        continue
                    else:
                        neighbor = s.to_name + gfapy.invert(s.to_orient)
                        neighbor_direction = 'from'

            if neighbor not in visited:
                queue.append(neighbor)
                visited.append(neighbor)

                neighbor_name = neighbor[:-1]
                prev[neighbor] = curr_unitig
                prev_direction.append(neighbor_direction)
                if neighbor_name in bin:
                    p = neighbor
                    connected = True
                    break

    if connected:
        while p != -1:
            if p[:-1] not in bin:
                bin.append(p[:-1])
            p = prev[p]
     

def read_unavailable_unitigs(bin_folder, bin_file):
    bin_files = [x for x in next(os.walk(bin_folder))[2]]
    unavailable_unitigs = set()
    for file in bin_files:
        if os.path.basename(bin_file) == file:
            # ignore the bin file if it is in this folder
            continue
        with open(os.path.join(bin_folder, file), 'r') as f:
            b = f.read().splitlines()
            for i in b:
                unavailable_unitigs.add(i)

    return unavailable_unitigs


def read_bin_contents(bin_file):
    with open( bin_file, 'r') as f:
        bin = f.read().splitlines()
    return bin


def print_bin_contents(bin):
    # prints comma separated unitig names, makes it easy to paste into Bandage
    for i in range(len(bin)):
        print(bin[i], end=', ')
        if i == len(bin) - 1:
            print(bin[i])


def save_bin_contents(bin, output_file):
    with open(output_file, 'w+') as f:
        f.write('\n'.join(bin))


def connect_unitigs_wrapper(bin_file, bin_folder, graph_path, output_file,
                            print=False):
    """
    bin_file: Full path to a file that conatins the \n separated unitig names of
            the bin you want to make more connected by adding new (available) unitigs
    bin_folder: Folder that conatins other bins in the bin_file format. Unitigs
            that belong to bins in this folder will not be added to the bin.
            If a file with the same basename as the bin file appears in this folder,
            it is ignored (contents are not marked unavailable).
    graph_path: path to the original assembly graph
    output_file: Save the updated bin to this location, following the same format
    print: Whether to print the unitigs of the updated bin to standard output
    """
    unavailable_unitigs = read_unavailable_unitigs(bin_folder, bin_file)
    bin = read_bin_contents(bin_file)
    graph = gfapy.Gfa.from_file(graph_path)

    bin = make_bin_connected(graph, bin, unavailable_unitigs)

    save_bin_contents(bin, output_file)

    if print:
        print_bin_contents(bin)

    
if __name__ == '__main__':
    bin_file = sys.argv[1]
    bin_folder = sys.argv[2]
    graph_path = sys.argv[3]
    output_file = sys.argv[4]

    connect_unitigs_wrapper(bin_file, bin_folder, graph_path, output_file, True)


    