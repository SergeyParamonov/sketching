import sys
import argparse
from pudb import set_trace as bp
from program import Program
from generator import Generator
from asp_engine import ASPEngine
from solution import Solution
import re
import random
import os

class Solver():
  
  def __init__(self, print_results=None, config={"debug" : False, "verbose_grounding_solving":True, "negation_counter":1}
):
      self.config = config
      if print_results is not None:
          self.config['print_results'] = print_results

      self.asp_engine = ASPEngine(self.config)
     
  def run_dull_grounder(self, filename, ground_output):
    asp_output_program_name = "tmp_asp_script.asp"
    program = Program(filename, config=self.config)
     
    generator = Generator(program, asp_output_program_name)
    generator.include_original_sketch()
    generator.generate_program()
    
    command = 'gringo {} > {}'.format(asp_output_program_name, ground_output)
    os.system(command)

  def run_dull_clasp(self, grounded_file):
    command = 'clasp {} 0 > tmp/solution'.format(grounded_file)
    os.system(command)


  def create_set_of_solutions(self,solutions):
    for solution_atoms in solutions: 
        solution = Solution(solution_atoms)
        yield solution

  def create_new_asp_program(self,rules):
    program_str = "\n".join(map(lambda x: str(x),rules))
    return program_str

  def learn_programs(self, script_name):
    print_results = self.config.get("print_results",True)
    solutions, _ = self.learn_ASP_constraints(script_name, print_results=print_results)
    solutions = self.create_set_of_solutions(solutions)

    for solution in solutions:
      self.config['negation_counter'] = 1
      program = Program(script_name, config=self.config)
      new_program = self.create_new_asp_program(solution.apply_to_program(program))
      yield new_program

  

  def learn_ASP_constraints(self, script_name, config=None,print_results=False):
      if self.config["debug"]:
          print("DEBUGGING MODE IS ON")
      asp_output_program_name = "tmp_asp_script.asp"
          
      program = Program(script_name, config=self.config)
       
      generator = Generator(program, asp_output_program_name)
      generator.include_original_sketch()
      generator.generate_program()

      self.asp_engine.run(asp_output_program_name)
      before_dominance_check = self.asp_engine.get_number_of_solutions()
      print("before dominance models:", before_dominance_check)
    # bp()
      self.asp_engine.remove_dominated(program)
      if print_results:
        self.asp_engine.print_result()
      solutions = self.asp_engine.get_set_of_atoms()
      print('after dominance models:', len(solutions))
      
      if self.config.get("debug",False):
          print("DEBUGGING MODE: END OF THE OUTPUT")
      return solutions, before_dominance_check


  def read_input_script(self):
    parser = argparse.ArgumentParser(prog='sketcher')
    parser.add_argument('sketch', nargs=1, help='Sketched ASP program')
    args = parser.parse_args()
    script_name = args.sketch[0]
    return script_name

  def get_examples_with_indices(self, filename):
    with open(filename, "r") as sketch:
        data = sketch.read().splitlines()
    indices = []
    for index, line in enumerate(data):
        if "[EXAMPLES]" in line:
            section_header_index = index
        if re.search("positive *: *",line) or re.search("negative *: *",line):
            indices.append(index)
    if not section_header_index:
        raise Exception("no examples given?")
    return data, section_header_index, indices

  def construct_program_with_n_examples(self, program, indices, n):
    selected = random.sample(indices,n)
    new_program = program[:]
    for i in selected:
        new_program[i] = "%" + program[i] # comment out the example
    
    return "\n".join(new_program)

  def construct_program_without_last_n_examples(self, program, indices, n, shuffle=False):
    if not n:
        indices_to_cut = []
    else:
        if shuffle:
            random.shuffle(indices)
        indices_to_cut = indices[-n:]
    new_program = []
    for indx,line in enumerate(program):
        if indx not in indices_to_cut:
            new_program.append(line)
    return "\n".join(new_program)

  def classify(self, program, example):
      tmp_script = "tmp/classify_asp_script.asp"
      with open(tmp_script, "w") as tmp:
          pass #just cleaning
      with open(tmp_script, "a") as tmp:
          print(program, file=tmp)
          print(example, file=tmp)

      self.asp_engine.run(tmp_script)
      if self.asp_engine.get_number_of_solutions() != 0:
          return "positive"
      else:
          return "negative"
       
  def run_with_background_knowledge(self, program, background_knowledge): 
      tmp_script = "tmp/precision_asp_script.asp"
      with open(tmp_script, "w") as tmp:
          pass #just cleaning
      with open(tmp_script, "a") as tmp:
          print(program, file=tmp)
          print(background_knowledge, file=tmp)

      self.asp_engine.run(tmp_script)
      number_of_solutions = self.asp_engine.get_number_of_solutions()
      return number_of_solutions

 

def main():
    solver = Solver()
    script_name = solver.read_input_script()
    programs = solver.learn_programs(script_name)
    for index, program in enumerate(programs):
        print("Solution {}".format(index+1))
        print(program)
  # solver.learn_ASP_constraints(script_name, print_results=True)

    

if __name__ == "__main__":
    main()
