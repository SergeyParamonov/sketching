from program import Program
from solution import Solution
from solver import Solver
from collections import defaultdict
from pudb import set_trace as bp
import copy
from itertools import product
from os import listdir
from examples_generator import generate_queens_positive_negative_examples 

def run_experiment_learning_experiment(solver, background_knowledge, sketched_file, repeat=1):
  
  with open(background_knowledge, "r") as data:
    background_knowledge_data = data.read()
  
  for i in range(repeat):
    tmp_sketch = "tmp/sketch_to_run.sasp"
    data, section_header_index, indices = solver.get_examples_with_indices(sketched_file)
    number_of_examples = len(indices)
    for i in range(1,number_of_examples):
      print('using #examples:', number_of_examples - i)
      new_program = solver.construct_program_without_last_n_examples(data, indices, i, shuffle=True)
      with open(tmp_sketch,"w") as sketch_to_run:
        print(new_program,file=sketch_to_run)
      programs = list(solver.learn_programs(tmp_sketch))
      for program in programs:
        print('program # solutions: ', solver.run_with_background_knowledge(program,background_knowledge_data))



def convert_asp_atoms_to_str_facts(example):
  out = " ".join([str(atom) + "." for atom in example])
  return out

def measure_accuracy(solver, program, pos_examples, neg_examples):
  overall_pos = len(pos_examples)
  overall_neg = len(neg_examples)
  positive_count = 0
  negative_count = 0
  for example in pos_examples:
    str_example = convert_asp_atoms_to_str_facts(example)
    if "positive" == solver.classify(program, str_example):
      positive_count += 1

  for example in neg_examples:
    str_example = convert_asp_atoms_to_str_facts(example)
    if "negative" == solver.classify(program, str_example):
      negative_count += 1

  return (positive_count+negative_count)/(overall_pos+overall_neg)





def main():
  sketch_folder = "benchmark/queens_different_vars/"
# sketched_files = [x for x in listdir(sketch_folder)]
  sketched_files = ["queens4.sasp"]
  
  solver = Solver(print_results=False)

# pos_examples, neg_examples = generate_queens_positive_negative_examples(5000)
  

  background_knowledge = "benchmark/regular_queens_background_knowledge.asp"
  
  for sketch in sketched_files:
    run_experiment_learning_experiment(solver, background_knowledge, sketch_folder+sketch, repeat=4)


  

 #for example_file in ["tmp/test_example{i}".format(i=i) for i in range(1,4)]:
 #  with open(example_file,"r") as file_handler:
 #    example = file_handler.read()
 #  print(solver.classify(program,example))

    
# run_experiment_learning_experiment(solver, sketch_folder+"latin_square.sasp", repeat=10)
 #for sketch in sketched_files:
 #  print('*** SKETCH ', sketch,"***")
 #  programs = list(solver.learn_programs(sketch_folder+sketch))
 #  for program in programs:
 #    print('solution program')
 #    print(program)

  
  



  

if __name__ == "__main__":
  main()
