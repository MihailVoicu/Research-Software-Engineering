from argparse import ArgumentParser, FileType
from .laboratory import Laboratory
import os, yaml

def process():
   parser = ArgumentParser(description="Simulate laboratory reactions")

   parser.add_argument("--reactions", help="print number of reactions", action="store_true")
   parser.add_argument("input", help="yaml input file", type=FileType('r'))  
   arguments = parser.parse_args()
   
   data = yaml.load(arguments.input)
   lab = Laboratory(data)
   lower_shelf, upper_shelf, no_experiments = lab.run_full_experiment()
   shelves = {'lower': lower_shelf, 'upper': upper_shelf}
   
   if arguments.reactions:
       print(no_experiments)
   else:
       print(yaml.safe_dump(shelves))	   
	   
if __name__ == "__main__":
    process()







