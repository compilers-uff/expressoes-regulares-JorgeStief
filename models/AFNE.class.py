class AFNE:
  '''
    @param set    alphabet
    @param set    states
    @param dict   transition_function Exemplo: {'q0': [('a', {'q1'}), ('b', {'q2'})]}.
    @param string initial_state
    @param set    finals_states
  '''
  
  def __init__(self, alphabet, states, transition_function, initial_state, finals_states):
    self.alphabet = alphabet
    self.states = states
    self.transition_function = transition_function
    self.initial_state = initial_state
    self.finals_states = finals_states
    
    
  def startDelta(self, states, word ):
    if word == None:
      final = set()

      for state in states:
        final = final.union(self.emptyLock(state))

      return final
    
  def emptyLock(self, state):
    
    final = set()
      
    final_array = []
    initial_array = [state]
    
    while(len(initial_array) > 0):
      aux_state = initial_array[0]
      final.add(aux_state)
      
      if aux_state in  self.transition_function:
        achievable_states = self.transition_function[aux_state]
        
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