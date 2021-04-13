from models.AFNE import *
import string 
from functions import *

ALPHABET = list(string.ascii_lowercase)
aux_states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 
              'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19', }
i = 0
def match(er, word):
  return erToAFNe(er)


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


def erToAFNe(regular_expression):
  regular_expression = regular_expression.replace(' ', '').replace('(', '').replace(')', '').replace(',', '')[::-1]
  
  aux = []
  while len(regular_expression) > 0:
    char = regular_expression[0]
    regular_expression = regular_expression[1:]
    print("char",char)
    print("er", regular_expression)
    
    if char in ALPHABET:
      aux.append(char)
    else:
      first_term = aux.pop()
      
      if first_term in ALPHABET:
        first_term = create_afne(first_term)
        
      new_first_term =  update_afne_states('1', first_term)
      
      second_term = None
      new_second_term = None
      alphabet = None
      
      if(char != "*"):
        second_term = aux.pop()
        
        if second_term in ALPHABET:
          second_term = create_afne(second_term)
        
        new_second_term  = update_afne_states('2',second_term) 
        alphabet = new_first_term.alphabet.union(new_second_term.alphabet)
      else:
        alphabet = new_first_term.alphabet.copy()
        
      
      if(char == '+'):
        states = new_first_term.states.union(new_second_term.states)
        states.add('q0')
        states.add('qf')
        
        program_function = {
                              'q0': [(None, {new_first_term.initial_state}), (None, {new_second_term.initial_state})],
                              list(new_first_term.finals_states)[0]:[(None,{'qf'})],
                              list(new_second_term.finals_states)[0]:[(None,{'qf'})]
                            }
        program_function.update(new_first_term.program_function)
        program_function.update(new_second_term.program_function)

        initial_state = 'q0'
        finals_states = {'qf'}

        result_afne = AFNe(alphabet, states, program_function, initial_state, finals_states)

        aux.append(result_afne) 
        
  last_element = aux.pop()
  
  if last_element in {'*','.','+'}:
    exit("Notacao errada para ER")

  if last_element in ALPHABET:
    last_element = create_afne(last_element)
  return last_element 