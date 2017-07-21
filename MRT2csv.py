import re
import argparse

def parse():
   parser = argparse.ArgumentParser(description='MRT data to csv')
   parser.add_argument('inputs', type=str, help='input file')
   return parser.parse_args()


def main():
   args = parse()
   with open(args.inputs, 'r') as f, open(args.inputs + '.csv', 'w') as out:
      for index, line in enumerate(f):
         line = re.sub(' +', ',', line)
         if index != 1:
            out.write(line)


if __name__=='__main__':
   main()
