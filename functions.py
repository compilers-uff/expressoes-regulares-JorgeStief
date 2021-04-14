from models.AFNE import *
from models.AFN import *





def create_afne(term):
  
    program_function = {'q0': [(term, {'q1'})] }
    afne = AFNe({term}, {'q0','q1'}, program_function, 'q0', {'q1'})
    return afne

def add_value_transitions(value, transitions):
  retorno = []

  for transition in transitions:
    retorno.append((transition[0], set(map(lambda elem: elem+value, transition[1]))))        

  return retorno    

def update_afne_states(value, afne):
  states = afne.states
  states = set(map(lambda elem: elem+value, states))

  program_function = afne.program_function
  program_function = dict(map(lambda kv: (kv[0]+value, add_value_transitions(value,kv[1])), program_function.items()))
  print("program_function: ", program_function)     
  initial_state = afne.initial_state+value
        
  finals_states = afne.finals_states
  finals_states = set(map(lambda elem: elem+value, finals_states))   
  return AFNe(afne.alphabet, states, program_function, initial_state, finals_states)


