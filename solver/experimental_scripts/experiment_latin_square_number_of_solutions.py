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
  base_sketch_template = folder + problem_name + "_base_sketch.sasp"
  pos_generator_template  = folder + problem_name + "_positive_examples_generator.asp"
  neg_generator_template  = folder + problem_name + "_negative_examples_generator.asp"
  
  base_sketch   = folder + "base_sketch_latin_square_rewritten.sasp"
  pos_generator = folder + "pos_generator_latin_square_rewritten.sasp"
  neg_generator = folder + "neg_generator_latin_square_rewritten.sasp"
  for n in range(13,15):
    rewrite_into_file(base_sketch_template,  n,base_sketch)
    rewrite_into_file(pos_generator_template,n,pos_generator)
    rewrite_into_file(neg_generator_template,n,neg_generator)

    new_sketch_filename = folder + problem_name + "tmp_sketch_to_run.sasp"
    log_file = open("log_"+problem_name+"_k_"+str(n)+"_time_vs_numberofexamples.csv","w")
    print("number_of_examples,time",file=log_file)
    print('running the experiment for', problem_name, "with n=",n)
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
