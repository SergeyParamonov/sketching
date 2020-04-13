import re
from asp_engine import ASPEngine
import time 
from pudb import set_trace as bp
from os import listdir
from random import sample
from solver import learn_ASP_constraints

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

def run_experiment_and_record(filenames, n, solutions_log, time_log):
    config = {"debug":False}
    engine = ASPEngine(config)
    pos_generator = "benchmark/regular_queens_positive.asp"
    neg_generator = "benchmark/regular_queens_negative.asp"
    output_filename = "tmp_queens/tmp_script.asp"

    max_examples = 50
    engine.run(pos_generator)
    pos_examples = sample(engine.get_set_of_atoms(),max_examples)
    engine.run(neg_generator,number_of_solutions=50000)
    neg_examples = sample(engine.get_set_of_atoms(),max_examples)
    for filename in  filenames:
        print('running on',filename)
        for k in [x for x in range(1,11)] + [x for x in range(10,max_examples+1,5)]:
            text_to_append = []
            print('learning for k =', 2*k)
            for i,example in enumerate(pos_examples[:k]):
              text_to_append.append(make_example_str("+",example))
            for i,example in enumerate(neg_examples[:k]):
              text_to_append.append(make_example_str("-",example))
            create_new_sketch(output_filename, filename, text_to_append)
            start = time.time()
            programs = solver.learn_programs(output_filename)
            print(get_clean_name(filename),2*k,n,len(solutions),before,sep=",",file=solutions_log)
            end = time.time()
            print(get_clean_name(filename),2*k,n,round(end-start,2),sep=",",file=time_log)
            solutions_log.flush()
            time_log.flush()

       

def main():
    folder = "n_queens_sketches/"
    global_index = 0
    n = 5
    config = {"debug" : False } 
    solutions_log = open("logs/different_n_queens_solutions.csv","w")
    time_log = open("logs/different_n_queens_time.csv","w")
    print("task,n,sol,before_dominance")
    print("task,#examples,#sketched,#solutions,#before_dominance",file=solutions_log)
    print("task,#examples,#sketched,time(s)",file=time_log)
   
    for i in range(100):
        print(i," iteration")
        filenames = generate_sketches(folder, n, global_index)
        run_experiment_and_record(filenames, n, solutions_log, time_log)

    solutions_log.close()
    time_log.close()

    
   
   


if __name__ == "__main__":
    main()
