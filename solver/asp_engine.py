from pyasp.asp import *
from pudb import set_trace as bp
from program import Atom
import itertools
#from timeout import timeout

class ASPEngine():
  def __init__(self,config):
    self.config = config
    self.goptions = ''
    self.soptions = '0'
    self.solver = Gringo4Clasp(gringo_options=self.goptions, clasp_options=self.soptions)
    
# @timeout(60)
  def run(self,filename,number_of_solutions=10000): # change this 10000 to 0 when not writting the randomized precision example
    if number_of_solutions:
      self.soptions = str(number_of_solutions)
      self.solver = Gringo4Clasp(gringo_options=self.goptions, clasp_options=self.soptions)

    result = self.solver.run([filename],collapseTerms=False,collapseAtoms=False)
    self.result = result

  def get_number_of_solutions(self):
    return len(self.result)

  def print_result(self):
    if self.config.get("debug",False):
      print(self.result)
    for i,s in enumerate(self.result): 
      print('solution #',i)
      for a in sorted(s, key=lambda x: x.pred()):
        if self.config.get("debug",True):
          print(a.pred(), "is" , a.args())
        else:
          if "neg_sat" not in a.pred():
            print(a.pred(), "is" , a.args())
          
  def get_set_of_atoms(self):
    if self.config.get("debug",False):
      print(self.result)
    atoms = []
    for i,s in enumerate(self.result): 
      new_solution = []
      atoms.append(new_solution)
      for a in s:
        atom_str = a.pred() + "("+",".join(map(lambda x: str(x),a.args()))+")"
        atom = Atom(atom_str)
        new_solution.append(atom)
    return atoms



  def parse_predicate(self, raw_predicate, program):
    if not "decision" in raw_predicate:
      return None
    raw_predicate = raw_predicate.replace("decision_","")
    raw_predicate = raw_predicate.replace("sketched_","")
    if program.__eq__ in raw_predicate or program.__arithmethic__ in raw_predicate:
      index_type = raw_predicate.rfind("_")
      pred_type = raw_predicate[:index_type]
      index = raw_predicate[index_type+1:]
      return pred_type, index
    else:
      index = -1
      predicate = raw_predicate.strip("_ ")
      return predicate, index
      


  def make_preference_tuple(self, solution, program):
    preferences = program.preferences
    preference_solution = {}
    for a in solution:
      result = self.parse_predicate(a.pred(), program)
      if not result:
        continue
      predicate, index = result
      if predicate in preferences:
        pred_preferences = preferences[predicate]
        value = a.args()[0]
        if index != -1:
          preference_solution[predicate+"_"+index] = pred_preferences[value]
        else:
          preference_solution[predicate] = pred_preferences[value]

    return preference_solution

  # i1 dominates i2
  def check_dominance(self,i1,i2,pref):
    map1 = pref[i1]
    map2 = pref[i2]
    keys = map1.keys()
    flag = False
    for key in keys:
      if map1[key] < map2[key]:
        return False
      if map1[key] > map2[key]:
        flag = True
    if flag:
      return True
    else:
      return False



  def remove_dominated(self, program):
    pref = {}
    dominated_index = []
  # bp()
    for i1,sol1 in enumerate(self.result):
      pref[i1] = self.make_preference_tuple(sol1,program)
      if i1 in dominated_index:
        continue
      for i2,sol2 in enumerate(self.result):
        if i1 > i2 or i2 in dominated_index:
          continue
        if not i2 in pref:
          pref[i2] = self.make_preference_tuple(sol2,program)
        if self.check_dominance(i1,i2,pref):
          dominated_index.append(i2)
        if self.check_dominance(i2,i1,pref):
          dominated_index.append(i1)
          break
    
    if self.config.get("debug",False):
      print('dom index',dominated_index) 
      print('pref', pref)
    condensed = []
    for i, sol in enumerate(self.result):
      if not i in dominated_index:
        condensed.append(sol)

    self.result = condensed
    




  

