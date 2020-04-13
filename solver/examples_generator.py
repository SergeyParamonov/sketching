from random import sample
from asp_engine import ASPEngine

def generate_sudoku_positive_negative_examples(k):
    
  config = {"debug":False}
  engine = ASPEngine(config)
  max_solution_number = 5000
  problem_name = "sudoku"
  folder = "benchmark/"
  pos_generator  = folder + problem_name + "_positive_examples_generator.asp"
  neg_generator  = folder + problem_name + "_negative_examples_generator.asp"
  new_sketch_filename = folder + problem_name + "tmp_sketch_to_run.sasp"

  engine.run(pos_generator, number_of_solutions=max_solution_number)
  pos_examples = sample(engine.get_set_of_atoms(),k)
  engine.run(neg_generator, number_of_solutions=max_solution_number)
  neg_examples = sample(engine.get_set_of_atoms(),k)
  return pos_examples, neg_examples

def generate_queens_positive_negative_examples(k):
    
  config = {"debug":False}
  engine = ASPEngine(config)
  max_solution_number = 5000
  problem_name = "queens"
  folder = "benchmark/"
  pos_generator  = folder + "regular_queens_positive.asp"
  neg_generator  = folder + "regular_queens_negative.asp"
  new_sketch_filename = folder + problem_name + "tmp_sketch_to_run.sasp"

  engine.run(pos_generator, number_of_solutions=max_solution_number)
  pos_examples = sample(engine.get_set_of_atoms(),72)
  engine.run(neg_generator, number_of_solutions=max_solution_number)
  neg_examples = sample(engine.get_set_of_atoms(),k)
  return pos_examples, neg_examples

