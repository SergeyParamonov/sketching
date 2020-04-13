from collections import defaultdict
from pudb import set_trace as bp
import copy
from itertools import product
import re

class Preprocessor():

  __dots__ = "__dots__"


  def __init__(self):
    self.current_fresh_var_id = 1

  @staticmethod
  def is_preprocessing_needed(line):
    if "[" in line and "]" in line:
      return True
    return False

  def create_fresh_var(self):
    fresh_replacement_var = "B_VAR_" + str(self.current_fresh_var_id)
    self.current_fresh_var_id += 1
    return fresh_replacement_var

  @staticmethod
  def espace_extended_syntax_with_dots(text):
    return text.replace("..",Preprocessor.__dots__)


  def replace_and_return_expression(self,line):
    left_bracket, right_bracket = line.index("["), line.index("]")
    expression   = line[left_bracket+1:right_bracket]
    fresh_var    = self.create_fresh_var()
    updated_line = line[:left_bracket] + fresh_var + line[right_bracket+1:]
    return updated_line, expression, fresh_var

  @staticmethod
  def create_arithmetic_atom(expression, fresh_var):
    atom_head = "?+"
    left, right = expression.split("?+")
    left  = left.strip()
    right = right.strip()
    atom = atom_head + "(" + left + "," + right + "," + fresh_var + ")"
    return atom


  def preprocess_line(self,line):
    number_of_expressions = line.count("[")
    updated_line = line.replace(".","")
    for i in range(number_of_expressions):
      updated_line, expression, fresh_var = self.replace_and_return_expression(updated_line)
      updated_line += Atom.atom_delimiter + Preprocessor.create_arithmetic_atom(expression, fresh_var) 
    updated_line += "."
    return updated_line
   
  @staticmethod
  def escape_sketched_negation(text):
      escaped = text.replace("?not",Program.negation_keyword)
      return escaped

class Program():

  
  negation_keyword = "?_negation_"
  __eq__ = "eq"
  __arithmethic__ = "arithmetic"
  
  @staticmethod
  def get_text(filename):
    with open(filename, "r") as inputfile:
      text = inputfile.read()
      text = Preprocessor.escape_sketched_negation(text)
      text = Preprocessor.espace_extended_syntax_with_dots(text)
      text = text.splitlines()
    return text

   
  def get_examples(self):
    return self.examples
 
  @staticmethod
  def remove_comment(line):
    COMMENT_SYMBOL = "%"
    line = line.strip()
    if COMMENT_SYMBOL in line:
      cut_from = line.index(COMMENT_SYMBOL)
      line = line[cut_from:]
      line = line.strip()
    return line

  def extract_predicate_dependencies(self,line):
      r = Rule(line, config=self.config)
      head = r.get_head()
      body = r.get_body()
      if self.config['debug']:
          print("call extract_predicate_dependencies: head:", head, "body:",body) 
      if body:
        return head, body, r
      else:
        return None, None, None

      

  def create_rule(self,line):
    line = Program.remove_comment(line)
    if not line:
      return None
    head, body, rule = self.extract_predicate_dependencies(line)
    if head:
      for atom in body: 
        self.dependecy_graph[atom.get_predicate()].add(head.get_predicate())
        if not atom.is_sketched and atom.sketched_negation:
          self.dependecy_graph[atom.get_predicate()].add(atom.get_predicate())
    if not rule:
      return None
    if self.config['debug']:
      print('parsing rule',rule)
    if "?" in line:
      return True, rule
    else:
      return False, rule
    

  def parse_facts_with_extended_syntax(self,raw_str):
    if (not raw_str ) or raw_str.isspace():
      return None
    if not self.__dots__ in raw_str:
      if self.config['debug']:
        print("TEST:", raw_str, "END", sep="")
      return [Atom(raw_str,to_index=True, disable_counters=True)]
    else:
      raw_str = raw_str.strip(" )")
      predicate, rest = raw_str.split("(")
      predicate = predicate.strip()
      rest = rest.strip()
      args = rest.split(",")
      listed_args = []
      for arg in args:
        if self.__dots__ in arg:
          min_val, max_val = arg.split(self.__dots__)
          values = [str(x) for x in range(int(min_val), int(max_val)+1)]
          listed_args.append(values)
        else:
          listed_args.append([arg.strip()])
      
      atoms = []
      for args in product(*listed_args):
        str_repr_atom = "{predicate}({args})".format(predicate=predicate, args=",".join(args))
        if self.config['debug']:
          print("call: parse_facts_with_extended_syntax", "str repr", str_repr_atom)
        atoms.append(Atom(str_repr_atom,to_index=True, disable_counters=True))
      return atoms
        
  def parse_line_with_facts(self,line):
    line = Program.remove_comment(line)
    if not line or line == " ":
      return None

    
    facts = []
    for raw_str in re.split('\.',line):
      if not raw_str:
        continue
      new_facts = self.parse_facts_with_extended_syntax(raw_str)
      if new_facts:
        if new_facts:
          facts += new_facts

    return facts
 
  @staticmethod
  def parse_example_line(line):
    if "positive" in line:
      is_positive  = True
    else:
      is_positive = False
    line = Program.remove_comment(line)
    if not line:
      return None
    sign, body = line.split(":")
    body = body.strip()
    facts = [Atom(fact) for fact in body.split(".") if fact]
    return is_positive,facts

  def parse_domain_line(self,line):
    if ":" in line:
      predicate, domain = line.split(":")
      predicate = predicate.strip()
      if self.__dots__ in domain:
        min_val, max_val = domain.split(self.__dots__)
        domain = [x for x in range(int(min_val),int(max_val)+1)]
      else:
        domain    = [value.strip(" .") for value in domain.split(",")]
      return predicate, domain
  
  @staticmethod
  def parse_preference_line(line):
      # special treatment for ?= and ?+ and so forth, since they are mapped to another names
      # i.e., ?= becomes eq and ?+ becomes arithmetic
      special_symbol_mapping = {"<" : "le", ">" : "ge", "<=": "leq", ">=" : "geq", "!=": "ne", "=": "eq" , "*" : "mult", "-":"minus", "/":"div", "+":"plus", "unbound":"unbound"}
      if not ":" in line:
          return None
      line = line.strip(" ,.")
      predicate, mapping_raw = line.split(":")
      predicate = predicate.strip()
      if predicate == "?=":
          predicate = Program.__eq__
      if predicate == "?+":
          predicate = Program.__arithmethic__
      else:
          predicate = predicate.replace("?", "")
      mapping_raw = mapping_raw.split(",")
      mapping = defaultdict(int)
      for arrow_pair in mapping_raw:
          left, right = arrow_pair.split("->")
          left = left.strip()
          right = right.strip()
          if left in special_symbol_mapping:
            left = special_symbol_mapping[left] 
          else:
            left = "c_" + left
          if right == "max":
            right = 100000
          mapping[left] = int(right)
      return predicate, mapping

  def parse_custom_sketch_line(self,line):
      if "/" not in line and ":" not in line:
          return None
      predicate, rest = line.split("/")
      arity, domain_raw = rest.split(":")
      predicate = predicate.strip()
      arity = int(arity.strip())
      domain = [x.strip() for x in domain_raw.split(",")]
      cleaned_sketch_predicate = self.transform_sketched_name_into_str(predicate)
      for domain_predicate in domain:
        self.dependecy_graph[domain_predicate].add(cleaned_sketch_predicate)
      return predicate, arity, domain

  
  def __init__(self, filename, config={"debug":False}):
    self.dependecy_graph = defaultdict(set)
    self.__dots__ = Preprocessor.__dots__
    preprocessor = Preprocessor()
    self.config = config
    text = self.get_text(filename)
    self.list_of_facts = []
    self.rules    = []
    self.examples = []
    self.domain   = {}
    self.not_skeched_rules = []
    self.preferences = {}
    self.custom_sketch = {}
    self.type_mapping = {}
    self.sketched_negation = False
    self.negated_sketching = False
    domain_index = 0
    mode = ""
    self.all_rules = []
    for line in text:
      line = self.delete_comments(line,"%")
      line = self.delete_comments(line,"#")
      
      if not line:
        continue

      if "[SKETCH]" in line:
        mode = "program"
        continue
      if "[EXAMPLES]" in line:
        mode = "examples"
        continue
      if "[FACTS]" in line:
        mode = "facts"
        continue
      if "[DOMAIN]" in line:
        mode = "domain"
        continue

      if "[PREFERENCES]" in line:
        mode = "preference"
        continue
      
      if "[SKETCHEDVAR]" in line:
        mode = "custom_sketch_declaration"
        continue

      if "[TEST_LATER]" in line:
        mode = "stuff_to_check_later"
        continue

      if mode == "program":
        if Preprocessor.is_preprocessing_needed(line):
          line = preprocessor.preprocess_line(line)
        output = self.create_rule(line)
        if config.get("debug",False):
            print("rule",output)
        if output:
          is_sketched, rule = output
          self.all_rules.append(rule)
          if is_sketched:
            self.rules.append(rule)
          else:
            self.not_skeched_rules.append(rule)

      if mode == "facts":
        facts = self.parse_line_with_facts(line)
        if config.get("debug",False):
            print("facts",facts)
        if facts:
          self.list_of_facts += facts

      if mode == "examples":
        example = self.parse_example_line(line)
        if config.get("debug",False):
            print("example", example)
        if example:
          self.examples.append(example)

      if mode == "domain":
        parsed_line = self.parse_domain_line(line)
        if parsed_line:
          predicate, domain = parsed_line
          if predicate == "not":
              self.negated_sketching = True
              self.domain[(predicate,"not")] = domain
          else:
            self.domain[(predicate,domain_index)] = domain
            domain_index += 1
          if config.get("debug",False):
            print("domain", predicate, domain)

      if mode == "preference":
        parsed_line = self.parse_preference_line(line)
        if parsed_line:
          predicate, mapping = parsed_line
          self.preferences[predicate] = mapping

          if config.get("debug",False):
            print("preferences", predicate, mapping)

      if mode == "custom_sketch_declaration":
          parsed_line = self.parse_custom_sketch_line(line)
          if parsed_line:
              predicate, arity, domain = parsed_line
              clean_pred = self.transform_sketched_name_into_str(predicate)
              self.type_mapping[clean_pred] = clean_pred 
              if config.get("debug",False):
                print("custom sketch", predicate, arity, domain)
              self.custom_sketch[clean_pred] = (arity, domain)
  
  def transform_sketched_name_into_str(sefl, string):
    return string.replace("?","sketched_")

  def delete_comments(self,line,symbol):
    if symbol in line:
      percent_indx = line.index(symbol)
      line = line[:percent_indx]
    return line

  def get_rules(self):
    return self.rules


  def __repr__(self):
    output = "rules\n"
    for rule in self.rules:
      output += str(rule)
    output += "\nfacts\n"
    for i,fact in enumerate(self.list_of_facts):
      output += str(fact) + Atom.atom_delimiter
      if i % 5 == 0:
        output += "\n"
    output += "\nexamples\n"
    for example in self.examples:
      is_positive, body = example
      if is_positive:
        output += "positive: "
      else:
        output += "negative: "
      for fact in body:
        output += str(fact) + Atom.atom_delimiter
      output += "\n"
    if self.sketched_negation:
      output = "sketched_not " + output
    output = output.strip("\n ")   

    return output
  
  def __str__(self):
    return self.__repr__()

  def get_facts(self):
    return self.list_of_facts

class Rule():
  SKETCH_PREFIX = "?"

  def __init__(self, head, body):
    self.head = head
    self.body = body

  def __init__(self, string, head=None, body=None, config=None):

    if body:
      # this way is only for non-sketched rules
      # it doesn't really check if atoms are sketched
      self.head = head
      self.body = body
      self.is_integrity_rule = True if head is None else False

    if head is None and body is None and string is not None:
      # that's a proper way to parse an input string
      # all checks
      try:
        head, body = string.split(":-")
      except:
        print(string)
        raise Exception("Something is wrong")
      if self.SKETCH_PREFIX in string:
        self.is_sketched = True
      else:
        self.is_sketched = False
      self.head = head.strip()
      if not self.head:
        self.head = None
        self.is_integrity_rule = True 
      else:
        self.is_integrity_rule = False

      body = body.strip()

      if not self.is_integrity_rule:
        self.head = Atom(head)

      self.body = []
      for atom in body.split(Atom.atom_delimiter):
        self.body.append(Atom(atom,to_index=True,config=config))

  def get_head(self):
      return self.head

  def set_new_head(self, head):
    self.is_integrity_rule = False
    self.head = head

  def rewrite_atom_and_append_decision_atom(self,atom_indx,sketch_id,sketch_type):
    atom = self.get_body()[atom_indx]
    atom.rewrite_predicate_and_expand(sketch_type,sketch_id)
    self.body.append(Atom("decision_{sketch_id}(Q_{sketch_id})".format(sketch_id=sketch_id)))

  def get_body(self):
    return self.body

  def __repr__(self):
    if not self.is_integrity_rule:
      output = str(self.head) + " :- "
    else:
      output = " :- "
    output += ",".join(map(lambda x: str(x), self.body))
    output += "."
    return output

  def __str__(self):
    return self.__repr__()

  def rewrite_sketched_negation(self, closure):
    atoms = self.get_body()
    copied = []
    decisions_to_add = []
    for atom in list(atoms):
      if atom.sketched_negation:
        if not atom.is_rewritten and atom.get_predicate() in closure:
          atom.rewrite()
        negative_var = "Not_D"+str(atom.negative_index)
        copied.append((atom.negative_index,copy.deepcopy(atom)))
        atom.set_negative_var(negative_var)
        atom.predicate = "sketched_not_{index}".format(index=atom.negative_index)
        decisions_to_add.append(negative_var)
        self.body.append(Atom("decision_not_{index}({var})".format(var=negative_var,index=atom.negative_index)))

    return copied
        
class Atom():
  atom_delimiter = "&"
  special_keywords = ["?=", "<=", ">=", "!=", "=", "<", ">", "+", "-","*", "/"]
  def __init__(self, string, boolean=False, to_index=False, config=None, disable_counters=False):
    self.is_expanded_by_example = False
    self.is_predefined_sketch_type = False
    self.boolean = boolean
    self.is_rewritten = False
    self.gets_example_var = False
    self.negative_var = None
    self.sketched_var = None
    self.is_sketched = False
    self.active_abs_repr = False

    if Program.negation_keyword in string:
        self.sketched_negation = True
        string = string.replace(Program.negation_keyword, "")
        if to_index and not disable_counters:
          self.negative_index = int(config['negation_counter'])
          config['negation_counter'] += 1
    else:
        self.sketched_negation = False

    if "not " in string:
        self.negated = True
        string = string.replace("not ", "")
    else:
        self.negated = False
     
    if not ")" in string:
      is_special = False
      for keyword in Atom.special_keywords:
        if keyword in string:
          is_special = True
          self.predicate   = keyword
          self.original_predicate = keyword
          if keyword == "?=":
            self.is_sketched = True
            self.is_predefined_sketch_type = True
          else:
            self.is_sketched = False
          string           = string.strip("., ")
          self.args        = [x.strip() for x in string.split(keyword)]
          break
      if not is_special and (boolean or ("(" not in string and ")" not in string)):
        string = string.strip(" .")
        if "?" in string:
          self.is_sketched = True
          self.predicate = string.replace("?", "sketched_")
        else:
          self.is_sketched = False
          self.predicate = string
        self.args = []
      elif not is_special:
          raise Exception("Parser error, cannot parse the string '" + string + "' as an atom")
    else:
      string           = string.strip(" ).,")
      try:
        predicate, args  = string.split("(") 
        self.predicate = predicate.strip()
        if self.predicate == "?+":
          self.is_sketched = True 
        elif "?" in self.predicate:
          self.predicate = self.predicate.replace("?", "sketched_")
          self.is_sketched = True 
        elif self.sketched_negation:
          self.is_sketched = True
        else:
          self.is_sketched = False
        self.original_predicate = self.predicate
        self.args = [x.strip() for x in args.split(",")]
      except:
        self.predicate = string.strip()
        self.boolean = True
        self.args = []
        if "?" in self.predicate:
          self.predicate = self.predicate.replace("?", "sketched_")
          self.is_sketched = True
  
  def rewrite(self):
    self.gets_example_var = True
    self.is_rewritten = True

  def set_negative_var(self, negative_var):
    self.negative_var = negative_var

  def __repr__(self):
    vars_to_display = copy.deepcopy(self.args)

       
    # order is important here p(Eaux,Not_D_i, Sketched_j, Args..)
    if self.sketched_var:
      vars_to_display.insert(0,self.sketched_var)

    if self.negative_var:
      vars_to_display.insert(0,self.negative_var)

    if self.gets_example_var:
      vars_to_display.insert(0,"Eaux")


    if len(vars_to_display) == 0: # boolean case
      return self.predicate
    if self.predicate in Atom.special_keywords:
      if len(self.args) == 2:
        out = self.args[0] + " "+ self.predicate + " " + self.args[1]
      if len(self.args) == 3:
        out = self.args[2] + " = " + self.args[0] + " "+ self.predicate + " " + self.args[1]
    else:
      out = self.predicate + "(" +",".join(vars_to_display) + ")" 
    if self.negated:
        out = "not " + out
    if self.active_abs_repr:
      A,B,Total = self.args
      out = Total + " = ""| " + A + " - " + B + " |"
    return out

  def __str__(self):
    return self.__repr__()

  def get_predicate(self):
    return self.predicate

  def update_predicate(self, new_predicate):
    self.predicate = new_predicate

  def update_args(self, new_args):
    self.args = new_args

  def get_args(self):
    return self.args

  def rewrite_predicate_and_expand(self,sketch_type,sketch_id):
    if sketch_type != "not":
      self.predicate = sketch_type
      self.sketched_var = "Q_"+sketch_id
  
  def expand_with_index(self,index):
    self.args.insert(0, str(index))
