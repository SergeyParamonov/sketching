from pudb import set_trace as bp
from collections import defaultdict
import copy
from program import Atom

class Generator():

    type_mapping = {"?=":"eq", "?+":"arithmetic"}

    def __init__(self, program, filename):
        self.program = program
        self.context = defaultdict(int, {"sketched_indices":set(),"number_of_clauses":0, "eq":0, "arithmetic":0, "not":0}) # if max num is passed it should be reassigned here
        self.context['example_predicates'] = self.get_example_predicates(program)
        self.type_mapping.update(program.type_mapping)
        self.sketched_index = defaultdict(list)
        self.generated_rules = []
        self.outfilename = filename
        self.sketched_ids = []
        with open(filename, "w") as file_cleaning: # just clean file
          pass
    
    def generate_program(self):
      filename = self.outfilename
      program = self.program
      self.init_rewriting()
      copied_sketching_negation = []
      with open(filename,"a") as output_file:
        rules = program.get_rules()
        for rule_index,rule in enumerate(rules):
          self.analyze_rule(rule_index,rule)
        domain, generators, decision_domain_not = self.generate_generators_and_domain()
        print("%%%%% DOMAIN AND GENERATORS %%%%%%",file=output_file)
        print(domain,file=output_file)
        print(generators, file=output_file)
        if self.program.negated_sketching:
          print("%%%%%% KEEP DOMAIN INFORMATION ABOUT DECISION VARIABLES %%%%%%", file=output_file)
          print(decision_domain_not, file=output_file)
        print("%%%%% NON-EXAMPLES FACTS %%%%%%",file=output_file)
        for fact in program.get_facts():
          print(fact,file=output_file, end=". ")
        print("",file=output_file)
        if self.context['eq']:
          index = self.get_specified_domain("?=")
          print(self.generate_eq_code(index),file=output_file)
        if self.context['arithmetic']:
          index = self.get_specified_domain("?+")
          print(self.generate_arithmetic_code(index), file=output_file)

        print(self.generate_all_examples_predicate(), file=output_file)

         
        custom_sketches = self.program.custom_sketch
        for key, (arity, domain) in custom_sketches.items():
          if self.program.config.get("debug",False):
            print("custom sketch", key, arity, domain)
          print(self.generate_custom_skech_code(key, arity, domain), file=output_file)

     
        print("%%%%% NON-SKETCHED INFERENCE RULES %%%%%%",file=output_file)
        for rule in program.not_skeched_rules:
          if not rule.is_integrity_rule:
            self.insert_example_var_into_not_sketched_vars(rule)
            rule.body.append(Atom("examples(Eaux)"))
            if self.program.negated_sketching:
              copied_sketching_negation += rule.rewrite_sketched_negation(self.closure)
            print(rule, file=output_file)

        print("%%%%% FAILING RULES %%%%%%",file=output_file)
        fail_rules, positive_rules, negative_rules, sketched_inference_rules = self.get_rewritten_rules()
        print(fail_rules, file=output_file)

        if self.program.config['debug']:
          pass

        print("%%%%% SKETCHED INFERENCE RULES %%%%%%",file=output_file)
        for rule in sketched_inference_rules:
            self.insert_example_var_into_sketched_atom(rule)
            self.insert_example_var_into_not_sketched_vars(rule)
            rule.body.append(Atom("examples(Eaux)"))
            if self.program.negated_sketching:
               copied_sketching_negation += rule.rewrite_sketched_negation(self.closure)
            print(rule, file=output_file)


        print("%%%%% POSITIVE SKETCHED RULES %%%%%%",file=output_file)
        for rule in positive_rules:
          if self.program.config['debug']:
            print("generating positive rules")
          if self.program.negated_sketching:
            copied_sketching_negation += rule.rewrite_sketched_negation(self.closure)
          print(rule, file=output_file)

        print("%%%%% NEGATIVE SKETCHED RULES %%%%%%",file=output_file)
        for rule in negative_rules:
          if self.program.config['debug']:
            print("generating negative rules")
          rule.rewrite_sketched_negation(self.closure) # no need to generate generators twice
          print(rule, file=output_file)
        
        if copied_sketching_negation:
          generators, reified, domain_not = self.generate_code_for_sketched_not(copied_sketching_negation)
          
          print("%%%%% DECISION ON THE NEGATION %%%%%%",file=output_file)
          print("\n".join(generators), file=output_file)
          print("%%%%% REIFICATION OF THE NEGATION %%%%%%",file=output_file)
          print("\n".join(reified), file=output_file)
          print("%%%%% DOMAIN OF THE NEGATION %%%%%%",file=output_file)
          print(domain_not, file=output_file)
        
        print("%%%%% EXAMPLES %%%%%%",file=output_file)
        for index, (is_positive, list_of_facts) in enumerate(program.get_examples()):
          if is_positive:
            sign = "positive"
          else:
            sign = "negative"

          print("{sign}({index}).".format(sign=sign, index=index), end=" ", file=output_file)

          for fact in list_of_facts:
            fact.expand_with_index(index)
            print(fact, file=output_file, end=". ")
          print("", file=output_file)
        print(self.generate_show_statements(),file=output_file)

    def include_original_sketch(self):
      with open(self.outfilename,"a") as output_file:
        print("%%%%% ORIGINAL SKETCH RULES %%%%%%",file=output_file)
        for rule in self.program.get_rules():
          if rule.is_sketched:
            print("%     ",end="",file=output_file)
            print(rule, file=output_file)

     
    def compute_transitive_example_closure(self):
      example_predicates = self.context['example_predicates']
      graph = self.program.dependecy_graph
      closure = set(example_predicates)
      if self.program.config['debug']:
        print("call: compute_transitive_example_closure")
        print("example predicates",example_predicates)
        print("graph",graph)
      while True:
        old_closure = set(closure)
        for item in closure:
          closure = closure.union(graph[item])
        if old_closure == closure:
          break

      if self.program.config['debug']:
        print('closure:', closure)
        print("call: END")
      return closure

    def init_rewriting(self):
      self.closure = self.compute_transitive_example_closure()

    def does_predicate_depend_on_example(self, predicate):
      return predicate in self.closure

    def generate_code_for_sketched_not(self, copied):
      generators = []
      reified = []
      for index, atom in copied:
        if not atom.is_rewritten:
          if (self.does_predicate_depend_on_example(atom.get_predicate())) or (atom.is_sketched and self.check_if_sketched_pre_depends_on_example(atom)):
            atom.rewrite() 
        generator = "1 {{ decision_not_{index}(positive); decision_not_{index}(negative) }} 1.".format(index=index)
        positive_head = Atom("sketched_not_{index}(".format(index=index) + ",".join(atom.args) +")")
        positive_head.gets_example_var = atom.gets_example_var
        positive_head.sketched_var = atom.sketched_var
        positive_head.set_negative_var("positive")
        positive  = str(positive_head) + " :- "+ str(atom) + "."

        negative_head = Atom("sketched_not_{index}(".format(index=index) + ",".join(atom.args) + ")")
        negative_head.gets_example_var = atom.gets_example_var
        negative_head.sketched_var = atom.sketched_var
        negative_head.set_negative_var("negative")
        domain_args = copy.deepcopy(atom.args)
        if negative_head.gets_example_var:
            domain_args.append("Eaux")
        if negative_head.sketched_var:
            domain_args.append(negative_head.sketched_var)

        negative  =  str(negative_head) + " :- not "+ str(atom) + "," + ",".join(["domain_not({X})".format(X=X) for X in domain_args if X != "Eaux"]) + ",domain_not_examples(Eaux)" + "."
        generators.append(generator)
        reified.append(positive)
        reified.append(negative)
      domain_not = self.program.domain[("not","not")] #declared domain
      domain = ""

      domain += "domain_not_example(Eaux) :- examples(Eaux).\n"
      domain += "".join(["domain_not({X}). ".format(X=X) for X in domain_not]) + "\n"
      return generators, reified, domain




    def get_example_predicates(self, program):
      examples = program.examples
      predicates = set()
      for is_positive, facts in examples:
        for fact in facts:
          predicate = fact.get_predicate()
          predicates.add(predicate)
      if self.program.config['debug']:
        print("call : get_example_predicates, output: ", predicates)
      return predicates

        
    def generate_generators_and_domain(self):
      generators = ""
      domain_declaration = "sketched_clauses(1..{number_of_clauses}).".format(number_of_clauses=self.context['number_of_clauses'])

#     domain_declaration += "number(1..{max_num}).\n".format(max_num=self.context['max_num']) args must be specified explicitely

      if self.context['eq'] > 0:
        domain_declaration += """equalities(eq). equalities(eq).  equalities(leq). \nequalities(geq). equalities(le). equalities(ge). equalities(ne). equalities(unbound).\n"""
      if self.context['arithmetic'] > 0:
        domain_declaration += "ops(plus). ops(minus). ops(mult). ops(div). ops(dist).\n"
     
      custom_sketches = self.program.custom_sketch
      
      negated_sketching = self.program.negated_sketching
      
      if negated_sketching:
        domain_not = ""
      else:
        domain_not = None
     
      for key in custom_sketches.keys():
        arity, domain = custom_sketches[key]
        domain_str = [key + "_choice(c_{val})".format(val=x) for x in domain] 
        domain_declaration += ".".join(domain_str) + ".\n"
        if negated_sketching:
          domain_not += "domain_not(X) :- " + key + "_choice(X).\n"

      for list_of_triples in self.sketched_index.values():
        for triple in list_of_triples:
          indx, sketched_id, sketched_type = triple
          if sketched_type == "eq":
            generators += "1 {{ decision_{sketch_id}(X) :  equalities(X) }} 1.\n".format(sketch_id=sketched_id)
          elif sketched_type == "arithmetic":
            generators += "1 {{ decision_{sketch_id}(X) :  ops(X) }} 1.\n".format(sketch_id=sketched_id)
          elif sketched_type != "not":
            generators += "1 {{ decision_{sketch_id}(X) :  {sketch_type}_choice(X) }} 1.\n".format(sketch_id=sketched_id, sketch_type=sketched_type)

            
      return domain_declaration, generators, domain_not

    def generate_positive_rule(self, rule):
      positive_rule = copy.deepcopy(rule)
      head = Atom("fail", boolean=True)
      positive_rule.set_new_head(head)
      positive_rule.body.append(Atom("positive(Eaux)"))
      self.insert_example_var_into_sketched_atom(positive_rule)
      self.insert_example_var_into_not_sketched_vars(positive_rule)
      return positive_rule



    def generate_negative_rule(self, rule):
      negative_rule = copy.deepcopy(rule)
      head = Atom("neg_sat(Eaux)")
      negative_rule.set_new_head(head)
      negative_rule.body.append(Atom("negative(Eaux)"))
      self.insert_example_var_into_sketched_atom(negative_rule)
      self.insert_example_var_into_not_sketched_vars(negative_rule)
      return negative_rule

    def check_if_sketched_pre_depends_on_example(self, atom):
      predicate = atom.get_predicate()

      if self.program.config.get('debug', False):
          print("check_if_sketched_pre_depends_on_example function, predicate: ",)
          print("custom sketches: ", self.program.custom_sketch)
      
      custom_sketches    = self.program.custom_sketch
      if predicate in custom_sketches.keys():
        arity, domain      = custom_sketches[predicate]
      else:
        domain = [predicate] # the case of negation without sketching
      
      for dependent_predicate in self.closure:
        if dependent_predicate in domain:
          return True
      else:
        return False

    def insert_example_var_into_sketched_atom(self,rule):
      for atom in rule.get_body():
        if atom.is_sketched and not atom.is_predefined_sketch_type and self.check_if_sketched_pre_depends_on_example(atom):
          atom.gets_example_var = True
          atom.is_rewritten = True

    def insert_example_var_into_not_sketched_vars(self,rule):
      if self.program.config['debug']:
        print("CALL: insert_example_var_into_not_sketched_vars)")
        print("argument rule:", rule)
      if rule.is_integrity_rule:
        atoms = rule.get_body()
      else:
        atoms = [rule.get_head()] + rule.get_body()
      for atom in atoms:
        if self.program.config['debug']:
          print('atom in the loop:', atom)
        if not atom.is_sketched and self.does_predicate_depend_on_example(atom.get_predicate()):
          atom.gets_example_var = True
          atom.is_rewritten = True


    def get_rewritten_rules(self):
      fail_rules = """fail :- not neg_sat(E), negative(E).\n:- fail."""
      rewritten_positive_rules = []
      rewritten_negative_rules = []
      sketched_inference_rules = []
      for indx, list_of_triples in self.sketched_index.items():
        rule = self.program.get_rules()[indx]
        for triple in list_of_triples:
          atom_indx, sketch_id, sketch_type = triple
          if sketch_type != "not":
            rule.rewrite_atom_and_append_decision_atom(atom_indx, sketch_id, sketch_type)
        if rule.is_integrity_rule:
          rewritten_positive_rules.append(self.generate_positive_rule(rule))
          rewritten_negative_rules.append(self.generate_negative_rule(rule))
        else:
          sketched_inference_rules.append(rule)
      
      for rule in self.program.not_skeched_rules:
        if rule.is_integrity_rule:
          rewritten_positive_rules.append(self.generate_positive_rule(rule))
          rewritten_negative_rules.append(self.generate_negative_rule(rule))

      return fail_rules, rewritten_positive_rules, rewritten_negative_rules, sketched_inference_rules




    def generate_show_statements(self):
      text = ["#show neg_sat/1."]
      for sketched_id in self.sketched_ids:
        if sketched_id != "not":
          text += ["#show decision_{sketched_id}/1.".format(sketched_id=sketched_id)]
      for i in range(1,self.program.config['negation_counter']):
        text += ["#show decision_not_{i}/1.".format(i=i)]
      return "\n".join(text)


    def analyze_rule(self, rule_index, rule):
      if not rule.is_sketched:
        return rule

      for index, atom in enumerate(list(rule.get_body())):
        if atom.is_sketched:
          self.update_sketched(index, atom, rule_index, rule)

    def update_sketched(self, index, atom, rule_index, rule):
      predicate = atom.get_predicate()
      for sketch_keyword,sketch_type in Generator.type_mapping.items():
        if predicate == sketch_keyword:
          self.context[sketch_type] += 1
          if self.program.config['debug']:
            print("call: update sketched", "sketch type:", sketch_type)
          if sketch_type in ["eq", "arithmetic"]: 
            sketch_id = sketch_type + "_" + str(self.context[sketch_type])
          else:
            sketch_id = sketch_type
          self.context['sketched_indices'].add(rule_index)
          self.context['number_of_clauses'] = len(self.context['sketched_indices'])
          self.sketched_index[rule_index].append((index,sketch_id,sketch_type))
          self.sketched_ids.append(sketch_id)
          break

      if atom.sketched_negation:
        sketch_type = "not"
        sketch_id = "not"
        self.context['not'] += 1
        self.context['sketched_indices'].add(rule_index)
        self.context['number_of_clauses'] = len(self.context['sketched_indices'])
        self.sketched_index[rule_index].append((index,sketch_id,sketch_type))
        self.sketched_ids.append(sketch_id)
        

    def get_specified_domain(self, predicate):
      domain = self.program.domain
      for dom_predicate, domain_index in domain.keys():
        if predicate == dom_predicate:
          return domain_index
      else:
        return None

    def generate_suffix_plus_extra(self, index, predicate_type):
      if index is None:
        suffix = ""
        extra  = ""
      else:
        suffix = str(index)
      domain_values = self.program.domain[(predicate_type,index)]
      extra = "\n%%%%%% SET DOMAIN VALUES %%%%%%\n"
      for value in domain_values:
        extra += "domain{suffix}({value}). ".format(suffix=suffix,value=value)
      extra += "\n"
      return suffix, extra

    def generate_all_examples_predicate(self):
      return "examples(E) :- negative(E).\nexamples(E) :- positive(E).\ndomain_not_examples(E) :- examples(E)."
    
    def generate_eq_code(self,index):
      suffix, extra = self.generate_suffix_plus_extra(index, "?=")
      text = """%%%%%%  MATERIALIZED EQUALITY %%%%%%
          eq(eq , X, Y) :- X == Y, domain{suffix}(X), domain{suffix}(Y).
          eq(leq, X, Y) :- X <= Y, domain{suffix}(X), domain{suffix}(Y).
          eq(geq, X, Y) :- X >= Y, domain{suffix}(X), domain{suffix}(Y).
          eq(le , X, Y) :- X <  Y, domain{suffix}(X), domain{suffix}(Y).
          eq(ge , X, Y) :- X >  Y, domain{suffix}(X), domain{suffix}(Y).
          eq(ne , X, Y) :- X != Y, domain{suffix}(X), domain{suffix}(Y).
          eq(unbound, X, Y) :- domain{suffix}(X), domain{suffix}(Y).
      """.format(suffix=suffix)
      return text + extra 

    def generate_arithmetic_code(self, index):
      suffix, extra = self.generate_suffix_plus_extra(index, "?+")
      text = """ %%%%%%  MATERIALIZED ARITHMETIC %%%%%%
          arithmetic(plus, X, Y, Z)  :- Z = X + Y,  domain{suffix}(X), domain{suffix}(Y).
          arithmetic(minus, X, Y, Z) :- Z = X - Y,  domain{suffix}(X), domain{suffix}(Y).
          arithmetic(mult, X, Y, Z)  :- Z = X * Y,  domain{suffix}(X), domain{suffix}(Y).
          arithmetic(div, X, Y, Z)   :- Z = X / Y,  domain{suffix}(X), domain{suffix}(Y).
          arithmetic(dist, X, Y, Z)  :- Z = |X - Y|,domain{suffix}(X), domain{suffix}(Y). 
      """ .format(suffix=suffix)                    
      return text + extra

    def generate_custom_skech_code(self, predicate, arity, domain):
      out = ""
      example_predicates = self.context['example_predicates']

      is_dependent_on_example = False
      for example_predicate in self.closure:
        if example_predicate in domain:
          is_dependent_on_example = True

      extra_var = "Eaux"
      for choice in domain:
        domain_variables = ",".join(["X" + str(i) for i in range(arity)])
        if is_dependent_on_example and choice in self.closure:
          line = predicate + "(" + extra_var + "," + "c_"  + choice +"," + domain_variables  + ") :- " + choice + "("+ extra_var +","+ domain_variables +")."
        elif is_dependent_on_example:
          line = predicate + "(" + extra_var + "," + "c_"  + choice +"," + domain_variables  + ") :- " + choice + "("+ domain_variables +")," + "examples(Eaux)."
        elif arity == 0:
          line = predicate + "(" + "c_"  + choice +") :- " + choice +"."                    
        else:
          line = predicate + "(" + "c_"  + choice +"," +             domain_variables  + ") :- " + choice + "("+ domain_variables +")."                   
        out += line + "\n"
      return out

    


      
