from program import Rule
from pudb import set_trace as bp

class Solution():
  neg_keyword = "negation"
  arithmetic_keyword = "arithmetic"
  eq_keyword = "equality"
  customsketch_keyword = "predicate"
  table = [("decision_not_",neg_keyword),("decision_arithmetic_",arithmetic_keyword),("decision_eq_",eq_keyword),("decision_sketched_",customsketch_keyword)]

  decision2infix = {"ne":"!=", "eq":"=", "leq":"<=", "geq":">=", "le":"<", "ge":">", "plus":"+", "minus":"-", "mult":"*", "div":"/"}
  
  def extract_type_of_sketching(self, predicate):
#     bp()
      if "?=" in predicate:
          sketching_type = self.eq_keyword
      elif "?+" in predicate:
          sketching_type = self.arithmetic_keyword
      elif "sketched_" in predicate:
          sketching_type = self.customsketch_keyword
      else:
          sketching_type = None

      return sketching_type 

  def apply_to_program(self, program):
   #bp()
    rules = list(program.all_rules)
    for rule in rules:
#       print('old rule', rule)
        new_rule = self.apply_to_rule(rule)
#       print('new rule', new_rule)
        yield new_rule

  def apply_to_rule(self,rule):
      head, body = rule.get_head(), rule.get_body()
      if head and head.is_sketched:
          new_head = self.apply_to_atom(head)
      else:
          new_head = head
#     bp()
      new_body = []
      for atom in body:
          if atom.is_sketched:
             #bp()
              new_atom = self.apply_to_atom(atom)
              new_body.append(new_atom)
          else:
              new_body.append(atom)
      new_rule = Rule(None,head=new_head,body=new_body)      
      return new_rule
      

  def apply_to_atom(self,atom): 
#     bp()
      if atom.sketched_negation:
         decision = self.mapping[(self.neg_keyword,self._current_neg_index)]
         self._current_neg_index += 1
         if decision == "negative":
             atom.negated = True
         else:
             atom.negated = False
      predicate = atom.get_predicate()
      sketching_type = self.extract_type_of_sketching(predicate)
      if sketching_type is None:
          return atom
#     bp()
      if sketching_type == self.customsketch_keyword:
          index = predicate[len("sketched_"):]
      elif sketching_type == self.eq_keyword:
          index = self._current_eq_index
          self._current_eq_index += 1
      elif sketching_type == self.arithmetic_keyword:
          index = self._current_arithmetics_index
          self._current_arithmetics_index += 1 
      decision = self.mapping[(sketching_type,index)] 
      if decision in self.decision2infix.keys():
          decision = self.decision2infix[decision]
      if decision == "dist":
          atom.active_abs_repr = True
      atom.update_predicate(decision)    
      return atom

  def extract_index_or_name(self, name, string): 
      indx = string[len(name):]
      if name == "decision_sketched_":
          return indx
      return int(indx)

  def __init__(self, atoms):
    self._current_neg_index         = 1
    self._current_eq_index          = 1
    self._current_arithmetics_index = 1
    self.mapping = {}
    for atom in atoms:
      for name, keyword in self.table:
        predicate = atom.get_predicate()
        if name in predicate:
          index = self.extract_index_or_name(name, predicate)
          self.mapping[(keyword,index)] = atom.args[0]

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    out = "Solution" + str(self.mapping)
    return out

