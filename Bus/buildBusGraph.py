import re
import os
import argparse
from datetime import datetime
from joblib import Parallel, delayed
import pickle

def parse():
   parser = argparse.ArgumentParser(description='bus data to csv')
   parser.add_argument('inputs', type=str, help='input directory')
   parser.add_argument('outputs', type=str, help='output csv file')
   parser.add_argument('start_time', type=str, help='start time')
   parser.add_argument('end_time', type=str, help='end time')
   return parser.parse_args()


def build_edge_map(dirs, inputs, s_time, e_time):
   edge_maps = {}
   node_maps = {}
   edge_times = {}

   for d in dirs:
      dir_path = os.path.join(inputs, d)
      if not os.path.isdir(dir_path):
         continue
      dir_dir = os.listdir(dir_path)
      path = os.path.join(dir_path, dir_dir[0])
      with open(path, 'r', errors='ignore') as f:
         f.readline()
         start = None
         start_time = None
         next_start = None
         next_start_time = None
         for line in f:
            line = re.sub('.*\t', '', line.strip())
            if line[0:2]!='A2':
               continue
            tokens = line.split(',')
            status = tokens[3]
            stop = tokens[7]
            leave = tokens[8]
            record_time = datetime.strptime(tokens[-1], '%y%m%d%H%M%S')

            if (status!='1' or record_time < s_time):
               continue
            elif (record_time > e_time):
               break

            if stop not in node_maps:
               node_maps[stop] = 1

            if leave=='1' and start is None:
               start = stop
               start_time = record_time
            elif leave=='1':
               next_start = stop
               next_start_time = record_time
            elif leave=='0' and start is not None and start != stop:
               edge = (start, stop)
               diff = record_time - start_time
               if edge not in edge_maps:
                  edge_maps[edge] = diff
                  edge_times[edge] = 1
               else:
                  edge_maps[edge] += diff
                  edge_times[edge] += 1
               start = next_start
               start_time = next_start_time

   for key, values in edge_maps.items():
      edge_maps[key] /= edge_times[key]
   return (node_maps, edge_maps)

def chunks(l, n):
   for i in range(0, len(l), n):
      yield l[i:i + n]

def main():
   args = parse()
   dirs = os.listdir(args.inputs)
   s_time = datetime.strptime(args.start_time, '%y%m%d%H%M%S')
   e_time = datetime.strptime(args.end_time, '%y%m%d%H%M%S')

   chunk_size = len(dirs) // 4 + 1
   edge_collections = Parallel(n_jobs=4, verbose=5)(
      delayed(build_edge_map)(
         d,
         args.inputs,
         s_time,
         e_time
      ) for d in chunks(dirs, chunk_size)
   )

   node_map = {}
   edge_map = {}

   for nodes, edges in edge_collections:
      for node, _ in nodes.items():
         node_map[node] = 1
      for edge, diff in edges.items():
         if edge not in edge_map:
            edge_map[edge] = diff
         else:
            edge_map[edge] += diff
            edge_map[edge] /= 2

   maps = {"node": node_map, "edge": edge_map}
   with open(args.outputs, 'wb') as out:
      pickle.dump(maps, out)

if __name__=='__main__':
   main()
