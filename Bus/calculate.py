import argparse
import pickle
from datetime import timedelta
import heapq
import json

def parse():
   parser = argparse.ArgumentParser(description='all pair shortest problem')
   parser.add_argument('inputs', type=str, help='input directory')
   parser.add_argument('target', type=str, help='input directory')
   parser.add_argument('outputs', type=str, help='input directory')
   return parser.parse_args()


def main():
   args = parse()
   with open(args.inputs, 'rb') as f:
      maps = pickle.load(f)

   reverse_edge_map = {}
   for edge, diff in maps['edge'].items():
      src, dst = edge
      if dst not in reverse_edge_map:
         reverse_edge_map[dst] = {}
      reverse_edge_map[dst][src] = diff

   visited_nodes = {}
   heap = []
   heapq.heappush(heap, (timedelta(0), args.target))
   while len(heap) > 0:
      times, node = heapq.heappop(heap)
      if node in visited_nodes:
         continue
      visited_nodes[node] = times

      if node in reverse_edge_map:
         for src, diff in reverse_edge_map[node].items():
            heapq.heappush(heap, (times + diff, src))

   visited_list = []
   for node, times in visited_nodes.items():
      node_map = {}
      node_map['id'] = node
      node_map['times'] = times.total_seconds()
      node_map['longitude'] = maps['node'][node]['longitude']
      node_map['latitude'] = maps['node'][node]['latitude']
      visited_list.append(node_map)

   output_map = {
      'target': args.target,
      'longitude': maps['node'][args.target]['longitude'],
      'latitude': maps['node'][args.target]['latitude'],
      'nodes':visited_list
   }
   import ipdb; ipdb.set_trace()
   with open(args.outputs, 'w') as out:
      out.write(json.dumps(output_map))


if __name__=='__main__':
   main()
