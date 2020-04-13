from os import listdir
from solver import learn_ASP_constraints
import re

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

def construct_program_without_last_n_examples(program, indices, n):
    if not n:
        indices_to_cut = []
    else:
        indices_to_cut = indices[-n:]
    new_program = []
    for indx,line in enumerate(program):
        if indx not in indices_to_cut:
            new_program.append(line)
    return "\n".join(new_program)
        



def main():
    sketch_folder = "test_sketches/"
    sketched_files = [x for x in listdir(sketch_folder)]
    tmp_sketch = "tmp/sketch_to_run.sasp"
    config = {"debug":False}
    log = open("logs/number_of_solutions_experiment.txt","w")
    print("sketch,number_of_examples,overall_examples,number_of_solutions,before_dominance_check",file=log)
    for afile in sketched_files:
        data, section_header_index, indices = get_examples_with_indices(sketch_folder+afile)
        number_of_examples = len(indices)
        for i in range(number_of_examples):
            new_program = construct_program_without_last_n_examples(data, indices, i)
            with open(tmp_sketch,"w") as sketch_to_run:
                print(new_program,file=sketch_to_run)
            solutions,before_dominance_check = learn_asp_constraints(tmp_sketch,config,false)
            print("{sketch},{n},{number_of_examples},{solutions},{before_dominance_check}".format(n=(number_of_examples-i),number_of_examples=number_of_examples,sketch=afile,solutions=str(len(solutions)),before_dominance_check=before_dominance_check),file=log)
            log.flush()
    log.close()


if __name__ == "__main__":
    main()
