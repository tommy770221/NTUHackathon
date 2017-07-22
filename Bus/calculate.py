import argparse
import pickle
from datetime import timedelta

def parse():
   parser = argparse.ArgumentParser(description='all pair shortest problem')
   parser.add_argument('inputs', type=str, help='input directory')
   parser.add_argument('outputs', type=str, help='input directory')
   return parser.parse_args()


def main():
   args = parse()
   with open(args.inputs, 'rb') as f:
      maps = pickle.load(f)

   distance_maps = maps['edge']

   for i, _ in maps['node'].items():
      for j, _ in maps['node'].items():
         edge = (i, j)
         if edge in distance_maps and i!=j:
            v = distance_maps[edge]
            if (i,i) in distance_maps:
               v += distance_maps[(i,i)] / 2
            if (j,j) in distance_maps:
               v += distance_maps[(j,j)] / 2
            distance_maps[edge] = v
         elif i==j and edge not in distance_maps:
            distance_maps[edge] = timedelta(0)

   for index, (k, _) in enumerate(maps['node'].items()):
      print(str(index) + '/' + str(len(maps['node'])))
      for i, _ in maps['node'].items():
         for j, _ in maps['node'].items():
            edge_ij = (i, j)
            edge_ik = (i, k)
            edge_kj = (k, j)
            if edge_ij not in distance_maps:
               distance_maps[edge_ij] = timedelta(2000000)
            if edge_ik not in distance_maps:
               distance_maps[edge_ik] = timedelta(2000000)
            if edge_kj not in distance_maps:
               distance_maps[edge_kj] = timedelta(2000000)
            if distance_maps[edge_ik] + distance_maps[edge_kj] < distance_maps[edge_ij]:
               distance_maps[edge_ij] = distance_maps[edge_ik] + distance_maps[edge_kj]

   import ipdb; ipdb.set_trace()
   with open(args.outputs, 'wb') as out:
      pickle.dump(distance_maps, out)


if __name__=='__main__':
   main()
