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

   for node in loc:
      nid = str(node['Id'])
      lon = float(node['longitude'])
      lat = float(node['latitude'])

      if len(merged_map) < 1:
         cand_id = str(len(merged_map) + 1)
         merged_map[cand_id] = {
            'longitude': lon,
            'latitude': lat
         }
         index_map[nid] = cand_id

      else:
         add_new_node = True
         min_dis = 1e9
         for cand_id, _ in merged_map.items():
            dis = math.sqrt(
               pow(merged_map[cand_id]['longitude'] - lon, 2) + \
               pow(merged_map[cand_id]['latitude'] - lat, 2)
            )
            if dis < 0.003:
               add_new_node = False
               if dis < min_dis:
                  min_dis = dis
                  new_id = cand_id

         if add_new_node:
            cand_id = str(len(merged_map) + 1)
            merged_map[cand_id] = {
               'longitude': lon,
               'latitude': lat
            }
            index_map[nid] = cand_id
         else:
            index_map[nid] = new_id
            merged_map[new_id]['longitude'] += lon
            merged_map[new_id]['latitude'] += lat
            merged_map[new_id]['longitude'] /= 2
            merged_map[new_id]['latitude'] /= 2


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

   merged = {'node': merged_map, 'edge': merged_graph}

   with open(args.outputs + '_graph', 'wb') as out:
      pickle.dump(merged, out)

   with open(args.outputs + '_index', 'wb') as out:
      pickle.dump(index_map, out)

if __name__=='__main__':
   main()
