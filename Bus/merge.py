import argparse
import pickle
from datetime import timedelta
import json
import math


def parse():
   parser = argparse.ArgumentParser(description='all pair shortest problem')
   parser.add_argument('inputs', type=str, help='input graph')
   parser.add_argument('location', type=str, help='location')
   parser.add_argument('outputs', type=str, help='output graph')
   return parser.parse_args()


def main():
   args = parse()
   with open(args.inputs, 'rb') as f:
      maps = pickle.load(f)

   with open(args.location, 'r') as f:
      loc = json.loads(f.read())['BusInfo']

   index_map = {}
   merged_map = {}

   cand_id = None

   for node in loc:
      nid = str(node['Id'])
      lon = float(node['longitude'])
      lat = float(node['latitude'])

      if (cand_id is None):
         cand_id = str(len(merged_map) + 1)
         merged_map[cand_id] = {
            'longitude': lon,
            'latitude': lat
         }
         index_map[nid] = cand_id

      else:
         dis = math.sqrt(
            pow(merged_map[cand_id]['longitude'] - lon, 2) + \
            pow(merged_map[cand_id]['latitude'] - lat, 2)
         )
         if dis < 0.01:
            index_map[nid] = cand_id
            merged_map[cand_id]['longitude'] += lon
            merged_map[cand_id]['latitude'] += lat
            merged_map[cand_id]['longitude'] /= 2
            merged_map[cand_id]['latitude'] /= 2
         else:
            cand_id = str(len(merged_map) + 1)
            merged_map[cand_id] = {
               'longitude': lon,
               'latitude': lat
            }
            index_map[nid] = cand_id

   merged_graph = {}
   merged_times = {}

   for key, value in maps['edge'].items():
      a, b = key
      if a not in index_map or b not in index_map:
         continue
      edge = (index_map[a], index_map[b])
      if edge in merged_graph:
         merged_graph[edge] += value
         merged_times[edge] += 1
      else:
         merged_graph[edge] = value
         merged_times[edge] = 1

   for key, value in merged_graph.items():
      merged_graph[key] /= merged_times[key]

   import ipdb; ipdb.set_trace()
   with open(args.outputs + '_graph', 'wb') as out:
      pickle.dump(merged_graph, out)

   with open(args.outputs + '_index', 'wb') as out:
      pickle.dump(index_map, out)

   with open(args.outputs + '_node', 'wb') as out:
      pickle.dump(merged_map, out)

if __name__=='__main__':
   main()
