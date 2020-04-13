from asp_engine import ASPEngine
from solver import Solver
import time
import random


def make_example_str(example_type, examples):
  out = ""
  if example_type == '+':
    out += "positive : "
  else:
    out += "negative : "

  for atom in examples:
    out += str(atom) + ". "

  return out

def create_new_sketch(new_sketch_filename, base_filename, examples):
  with open(new_sketch_filename,"w") as sketch_file, open(base_filename,"r") as base_sketch:
    base = base_sketch.read()
    print(base,file=sketch_file)
    print("",file=sketch_file)
    print("\n".join(examples),file=sketch_file)

keyword_to_replace = "#SUB"

def rewrite_into_file(original_file, k, output_file):
  with open(original_file, "r") as inputfile:
    data = inputfile.read().replace(keyword_to_replace, str(k))

  with open(output_file,"w") as output_file:
    print(data, file=output_file)


def main():
  config = {"debug":False}
  engine = ASPEngine(config)
  problem_name = "latin_square"
  folder = "benchmark/"
  pos_generator_template = folder + problem_name + "_positive_examples_generator.asp"
  neg_generator_template = folder + problem_name + "_negative_examples_generator.asp"
  solver =Solver()
  
  pos_generator  = folder + "pos_generator_latin_square_rewritten.sasp"
  neg_generator  = folder + "neg_generator_latin_square_rewritten.sasp"
  rewrite_into_file(pos_generator_template,3,pos_generator)
  rewrite_into_file(neg_generator_template,3,neg_generator)
  engine.run(pos_generator, number_of_solutions=0)
  pos_examples = engine.get_set_of_atoms()

  engine.run(neg_generator, number_of_solutions=0)
  neg_examples = engine.get_set_of_atoms()
  
# examples = list(map(lambda x: ("pos",x), pos_examples)) + 
  pos = list(map(lambda x: ("pos",x), pos_examples))
  neg = list(map(lambda x: ("neg",x), neg_examples))
  max_examples = 12
  for v in range(4,0,-1):
    base_sketch  = folder + "latin_square_sketch_3_by_3_vars_{v}.sasp".format(v=v)
    log_file = open("current_test/log_number_of_solutions_latin_square_preferences_vars_{v}.csv".format(v=v),"w")
    print("iteration_index,number_of_examples,solutions,without_preferences",file=log_file)
    for n in range(1,100):
      new_sketch_filename = folder + problem_name + "tmp_sketch_to_run.sasp"
      
      pos_sample = random.sample(pos,max_examples) 
      neg_sample = random.sample(neg,max_examples)
      for k in [x for x in range(1,max_examples+1,1)]:
        sample = pos_sample[:k] + neg_sample[:k]
        text_to_append = []
        for i,(sign,example) in enumerate(sample):
          if sign == "pos":
            text_to_append.append(make_example_str("+",example))
          elif sign == "neg":
            text_to_append.append(make_example_str("-",example))
          else:
            raise Exception('wtf')
            
        create_new_sketch(new_sketch_filename, base_sketch, text_to_append)
        sols, before_pref = solver.learn_ASP_constraints(new_sketch_filename,config)
        print(n,len(text_to_append),len(sols),before_pref,sep=",",file=log_file)
        log_file.flush()
  # log_file.close() something fishy going with closing this file


if __name__ == "__main__":
  main()
