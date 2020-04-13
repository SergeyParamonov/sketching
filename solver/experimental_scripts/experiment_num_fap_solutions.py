from os import listdir
from solver import learn_ASP_constraints
import re
import random
import numpy as np

def get_examples_with_indices(filename):
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

def construct_program_with_n_examples(program, indices, n):
    selected = random.sample(indices,n)
    new_program = program[:]
    for i in selected:
        new_program[i] = "%" + program[i] # comment out the example
    
    return "\n".join(new_program)
        



def main():
    sketch_folder = "fap_versions/"
    sketched_files = [x for x in listdir(sketch_folder) if ".sasp" in x and x[0] != '.']
    print(sketched_files)
    tmp_sketch = "tmp/sketch_to_run.sasp"
    config = {"debug":False}
    log = open(sketch_folder+"number_of_solutions.txt","w")
    print("sketch,number_of_examples,number_of_solutions,before_preferences",file=log)
    for afile in sketched_files:
        data, section_header_index, indices = get_examples_with_indices(sketch_folder+afile)
        number_of_examples = len(indices)
        print(afile)
        for i in range(number_of_examples):
            to_aggregate = []
            before = []
            print('i',i)
            for j in range(20):
                new_program = construct_program_with_n_examples(data, indices, i)
                print('j',j)
                with open(tmp_sketch,"w") as sketch_to_run:
                    print(new_program,file=sketch_to_run)
                solutions,before_dominance_check = learn_ASP_constraints(tmp_sketch,config,False)
                to_aggregate.append(len(solutions))
                before.append(before_dominance_check)
            averaged = np.mean(to_aggregate)
            averaged_before = np.mean(before)
            print("{sketch},{n},{solutions},{before}".format(n=(number_of_examples-i),sketch=afile,solutions=str(averaged),before=averaged_before),file=log)
            log.flush()
    log.close()


if __name__ == "__main__":
    main()
