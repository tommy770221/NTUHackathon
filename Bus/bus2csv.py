import re
import os
import argparse

def parse():
   parser = argparse.ArgumentParser(description='bus data to csv')
   parser.add_argument('inputs', type=str, help='input directory')
   parser.add_argument('outputs', type=str, help='output csv file')
   return parser.parse_args()


def main():
   args = parse()
   dirs = os.listdir(args.inputs)
   with open(args.outputs, 'w') as out:
      for d in dirs:
         dir_path = os.path.join(args.inputs, d)
         if not os.path.isdir(dir_path):
            continue
         dir_dir = os.listdir(dir_path)
         path = os.path.join(dir_path, dir_dir[0])
         print(path)
         with open(path, 'r', errors='ignore') as f:
            f.readline()
            for line in f:
               out.write(re.sub('.*\t', '', line))

if __name__=='__main__':
   main()
