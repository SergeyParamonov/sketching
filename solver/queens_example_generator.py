from asp_engine import ASPEngine
from solver import learn_ASP_constraints
import time


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


def main():
  config = {"debug":False}
  engine = ASPEngine(config)
  problem_name = "sudoku"
  folder = "benchmark/"
  for n in [4,'only_negation']:
      base_sketch   = folder + problem_name + "_base_sketch_{n}.sasp".format(n=n)
      pos_generator = folder + problem_name + "_positive_examples_generator.asp"
      neg_generator = folder + problem_name + "_negative_examples_generator.asp"
      new_sketch_filename = folder + problem_name + "tmp_sketch_to_run.sasp"
      log_file = open("log_"+problem_name+"_sketchedvariables_{n}_time_vs_#examples".format(n=n),"w")
      print("number_of_examples,time",file=log_file)
      print('running the experiment for', problem_name, "with {n} sketched variables".format(n=n))
      for k in [1] + [x for x in range(5,251,5)]:
        text_to_append = []
        print('learning for k =', 2*k)
        engine.run(pos_generator, number_of_solutions=k)
        examples = engine.get_set_of_atoms()
        for i,example in enumerate(examples):
          text_to_append.append(make_example_str("+",example))
        engine.run(neg_generator, number_of_solutions=k)
        examples = engine.get_set_of_atoms()
        for i,example in enumerate(examples):
          text_to_append.append(make_example_str("-",example))
        create_new_sketch(new_sketch_filename, base_sketch, text_to_append)
        start = time.time()
        learn_ASP_constraints(new_sketch_filename,config)
        end = time.time()
        print(len(text_to_append),",",round(end-start,2),sep="",file=log_file)
        log_file.flush()
      log_file.close()


if __name__ == "__main__":
  main()
