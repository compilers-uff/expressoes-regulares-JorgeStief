from models.AFNE import *
from models.AFN import *
import string
from functions import *


ALPHABET = list(string.ascii_lowercase)

def match(er, word):
  return afneToAFN(erToAFNe(er))


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
      sigma = None
      
      if(char != "*"):
        second_term = aux.pop()
        
        if second_term in ALPHABET:
          second_term = create_afne(second_term)
        
        new_second_term  = update_afne_states('2',second_term) 
        sigma = new_first_term.sigma.union(new_second_term.sigma)
      else:
        sigma = new_first_term.sigma.copy()
        
      
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

        result_afne = AFNe(sigma, states, program_function, initial_state, finals_states)

        aux.append(result_afne) 
        
  last_element = aux.pop()
  
  if last_element in {'*','.','+'}:
    exit("Notacao errada para ER")

  if last_element in ALPHABET:
    last_element = create_afne(last_element)
  return last_element 

def afneToAFN(afne):
  
    sigma = afne.sigma.copy()
    states = afne.states.copy()
    program_function = {}
    initial_state = afne.initial_state
    finals_states = set()

    
    for state in states:
        reached_states = afne.emptyLock(state)

        if not reached_states.isdisjoint(afne.finals_states):
            finals_states.add(state)

        for char in sigma:
            result = afne.startDelta({state}, char)
            if len(result) != 0:
                if state in program_function:
                    program_function[state].append((char, result))
                else:
                    program_function[state] = [(char, result)]

    afn = AFN(sigma, states, program_function, initial_state, finals_states)

    return afn