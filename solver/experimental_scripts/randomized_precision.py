import re
from asp_engine import ASPEngine
import time 
from pudb import set_trace as bp
from os import listdir
from random import sample
from solver import Solver
import statistics


def detect_replacable(text):
    mapping = {}
    index = 0
    keywords = ["!= ", " = ", " \+ ", " - ", " < ", " > ", ">= ", "<= "]
    for keyword in keywords:
       indeces = [m.start() for m in re.finditer(keyword, text)] 
       for index in indeces:
         mapping[index] = keyword
    return mapping

def process_sketch(sketch):
    with open(sketch, "r") as sketch_file:
        data = sketch_file.read().splitlines()
        for index, line in enumerate(data):
            if "[SKETCH]" in line:
                start_index = index
            if "[END]" in line:
                end_index = index
        constraints = data[start_index+1:end_index]
        txt_constraints = "\n".join(constraints)
        txt_constraints = txt_constraints.replace("  ", " ")
        mapping = detect_replacable(txt_constraints)
        return txt_constraints,mapping, start_index, end_index, data

def replace_n_with_sketches(text, mapping, n):
  # bp()
    places = mapping.keys()
    if n <= len(places):
        to_replace = sample(places, n)
    else:
        to_replace = places
    updated_text = str(text)
    for index in to_replace:
        updated_text = replace_with_sketched(updated_text, mapping[index], index)
    updated_text = updated_text.replace("?+", " ?+")
    updated_text = updated_text.replace("?=", " ?=")
    return updated_text

def add_parenthesis(text):
    expressions = re.findall("(?P<plus>\|? *\w+ \?\+ \w+ *\|?)",text)
    for exp in set(expressions):
        if "|" in exp:
            to_replace= str(exp.replace("|",""))
        else:
            to_replace = str(exp)
        to_replace = " [ " + to_replace + " ] "
        text = text.replace(exp, to_replace)
    old_text = ""
    while len(old_text) != len(text):
        old_text = str(text)
        text = re.sub("\[ +\[", "[", text)
        text = re.sub("\] +\]", "]", text)
    return text

def replace_with_sketched(text, keyword, index):
    if "+" in keyword or "-" in keyword:
        text = text[:index] + "?+ " + text[index+3:]
    else:
        text = text[:index] + "?= " + text[index+3:]
    return text

def write_sketch_to_tmp_file(sketch, text, number, global_index):
    outfile_name = "tmp_queens/"+sketch
    with open(outfile_name,"w") as outputfile:
        print(text,file=outputfile)
    return global_index + 1,outfile_name

def generate_sketches(folder, n, global_index):
    sketched_filenames = []
    for sketch in listdir(folder):
        text, mapping, start_index, end_index, data = process_sketch(folder+sketch)
        updated_text = replace_n_with_sketches(text,mapping,n)
        updated_text = add_parenthesis(updated_text)
        updated_text = data[:start_index+1] + updated_text.splitlines() + data[end_index+1:]
        updated_text = "\n".join(updated_text)
        updated_text = updated_text.replace("  ", " ")
        global_index, outfile_name = write_sketch_to_tmp_file(sketch, updated_text,n,global_index)
        sketched_filenames.append(outfile_name)
    return sketched_filenames


def get_clean_name(text):
    text = text.replace("tmp_queens/","")
    text = text.replace(".sasp","")
    text.index
    return text

def find_background(filename):
    if "hakank" in filename:
        return "benchmark/hakank_queens_background_knowledge.asp"
    elif "potas" in filename:
        return "benchmark/potassco_queens_background_knowledge.asp"
    else:
        return "benchmark/regular_queens_background_knowledge.asp"

def run_experiment_and_record(filenames, n, log_file, only_print_number_of_solutions=False):
    number_of_examples = 6
    tmp_sketch = "tmp/sketch_to_run.sasp"
    solver = Solver(print_results=False)


    for filename in  filenames:
     if only_print_number_of_solutions is False:
         background_knowledge = find_background(filename)
         with open(background_knowledge, "r") as data:
           background_knowledge_data = data.read()
     print('running on',filename)
     data, section_header_index, indices = solver.get_examples_with_indices(filename)
     for i in range(number_of_examples-1):
      print('using #examples:', number_of_examples - i)
      new_program = solver.construct_program_without_last_n_examples(data, indices, i) #shuffle=True -- use when sketched vars are fixed
      with open(tmp_sketch,"w") as sketch_to_run:
        print(new_program,file=sketch_to_run)

      programs = solver.learn_programs(tmp_sketch)
      if only_print_number_of_solutions:
          number_of_solutions = len(list(programs))
          with open(log_file, "a") as log:
            print(get_clean_name(filename),number_of_examples - i, number_of_solutions, file=log, sep=",")
      else:
          current_models_precision = []
          for program in programs:
            n_queen_solutions = solver.run_with_background_knowledge(program,background_knowledge_data)
            precision = measure_precision(n_queen_solutions)
            current_models_precision.append(precision)

          with open(log_file, "a") as log:
            print(get_clean_name(filename),number_of_examples - i,statistics.mean(current_models_precision), file=log, sep=",")
            

def measure_precision(number):
    if number < 92:
        return 0
    return 92/number

      
def main():
    only_print_number_of_solutions = True
    folder = "n_queens_sketches/"
    global_index = 0
    n = 5
    log_file = "logs/solutions_number_n_queens_all_models_manual_examples.csv"

    if only_print_number_of_solutions:
        with open(log_file, "w") as log:
            print('model,examples,number_of_solutions',file=log)
    else:
        with open(log_file, "w") as log:
            print('model,examples,precision',file=log)


   
    for i in range(100):
        print(i," iteration")
        filenames = generate_sketches(folder, n, global_index)
        run_experiment_and_record(filenames, n,log_file, only_print_number_of_solutions=only_print_number_of_solutions)


    
   
   


if __name__ == "__main__":
    main()
