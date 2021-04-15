from models.Automato import *
class AFD(Automato):
    def __init__(self, sigma, states, program_function, initial_state, finals_states):
        
        for key,value in enumerate(program_function):
            for transition in program_function[value]:
                if len(transition[1]) > 1 or transition[0] == None:
                    raise ValueError("jkhhhghg")
        super().__init__(sigma, states,program_function, initial_state, finals_states)
        

    
    
    def starDelta(self, state, word):

        if list(state)[0] not in self.states:
            raise Exception("O estado Não existe")

        if word == None or word == '':
            return state

        if list(state)[0] not in self.program_function:
            return None

        a = None
        w = None

        a = word[0]
        w = word[1:]

        if w == '':
            w = None

        resultado = None

        for transicao in self.program_function[list(state)[0]]:
            if transicao[0] == a:
                resultado = transicao[1]

        
        if resultado == None:
            return None

        return self.starDelta(resultado, w)

    
    def accepted(self,w):
        
        reached_state = self.starDelta({self.initial_state}, w) 

        if reached_state and not reached_state.isdisjoint(self.finals_states):
            return True
        
        return False  