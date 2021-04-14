#Classe "Mãe"
class Automato():
    
    def __init__(self, sigma, states, program_function, initial_state, finals_states):
        self.sigma = sigma
        self.states = states
        self.initial_state = initial_state
        self.program_function = program_function
        self.finals_states = finals_states
    
   