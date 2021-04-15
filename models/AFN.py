import sys
from models.Automato import *
class AFN(Automato):
    def __init__(self, sigma, states, program_function, initial_state, finals_states):

        for key,value in enumerate(program_function):
            for transition in program_function[value]:
                if transition[0] == None:
                    raise ValueError("AFN nao suporta indeterminismo")

        super().__init__(sigma, states, program_function, initial_state, finals_states)
        
    

    
    def starDelta(self, states, word):
        
        if word == None or word == '':
            return states

        aux = None
        aux2 = None

        aux = word[0]
        aux2 = word[1:]

        if aux2 == '':
            aux2 = None

        result = set()
        
        for state in states:
            if state not in self.states:
                 raise Exception("Estado não existe")
            
            if state in self.program_function:
                transitions = self.program_function[state]
                for transition in transitions:
                    if transition[0] == aux:
                        result = result.union(transition[1])
        
        if len(result) == 0:
            return result
        
        return self.starDelta(result, aux2)    

        

   