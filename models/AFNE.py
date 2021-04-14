class AFNe:
  '''
    @param set    alphabet
    @param set    states
    @param dict   transition_function Exemplo: {'q0': [('a', {'q1'}), ('b', {'q2'})]}.
    @param string initial_state
    @param set    finals_states
  '''
  
  def __init__(self, alphabet, states, program_function, initial_state, finals_states):
    self.alphabet = alphabet
    self.states = states
    self.program_function = program_function
    self.initial_state = initial_state
    self.finals_states = finals_states
    
  
  def __str__(self):
    return "alphabet: "+str(self.alphabet)+"\n"+"states: "+str(self.states)+"\n"+"transition_function: "+str(self.program_function)+"\n"+"initial_state: "+str(self.initial_state)+"\n"+"finals_states: "+str(self.finals_states)
  
  def startDelta(self, states, word ):
    if word == None:
      final = set()

      for state in states:
        final = final.union(self.emptyLock(state))

      return final
    
    aux = None
    aux2 = None

    if(word[:-1] != ''):
      aux = word[:-1] #n primeiros caracteres excluindo o ultimo

    aux2 = word[-1] #ultimo caracter

    a = self.startDelta(states, aux)
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