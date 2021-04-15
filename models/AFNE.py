from models.Automato import *
class AFNe(Automato):
  
  
  def __init__(self, sigma, states, program_function, initial_state, finals_states):
    super().__init__(sigma, states, program_function, initial_state, finals_states)
  
    
  def starDelta(self, states, word ):
    if word == None:
      final = set()

      for state in states:
        final = final.union(self.emptyLock(state))

      return final
    
    aux = None
    aux2 = None

    if(word[:-1] != ''):
      aux = word[:-1] 

    aux2 = word[-1] 

    a = self.starDelta(states, aux)
    b = set()

    for s in a:
      if s in self.program_function:
        possibilidades = self.program_function[s]
        for p in possibilidades:
          if p[0] == aux2:
            b = b.union(p[1])
            
    
    final = set()

    for t in b:
      final = final.union(self.emptyLock(t))

    return final
    
  def emptyLock(self, state):
    
    final = set()
      
    final_array = set()
    initial_array = [state]
    
    while(len(initial_array) > 0):
      aux_state = initial_array[0]
      final.add(aux_state)
      
      if aux_state in  self.program_function:
        achievable_states = self.program_function[aux_state]
        
        for achievable_state in  achievable_states:
          if achievable_state[0] == None:
            if final_array == set():
              for p in  achievable_state[1]:
                initial_array.append(p)
            else:
              for p in  achievable_state[1]:
                if p not in final_array:
                  initial_array.append(p)
      initial_array.remove(aux_state)
      final_array.add(aux_state)
    return final             