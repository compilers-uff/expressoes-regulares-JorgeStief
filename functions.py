from models.AFNE import *
from models.AFN import *


def create_afne(term):

    program_function = {'q0': [(term, {'q1'})]}
    afne = AFNe({term}, {'q0', 'q1'}, program_function, 'q0', {'q1'})
    return afne


def add_value_transitions(value, transitions):
    final = []

    for transition in transitions:
        final.append(
            (transition[0], set(map(lambda elem: elem+value, transition[1]))))

    return final


def update_afne_states(value, afne):
    states = afne.states
    states = set(map(lambda elem: elem+value, states))

    program_function = afne.program_function
    program_function = dict(map(lambda kv: (
        kv[0]+value, add_value_transitions(value, kv[1])), program_function.items()))
    initial_state = afne.initial_state+value

    finals_states = afne.finals_states
    finals_states = set(map(lambda elem: elem+value, finals_states))
    return AFNe(afne.sigma, states, program_function, initial_state, finals_states)


def removes_inaccessible_states(afd):
    visited = set()
    visit = [afd.initial_state]
   
    while len(visit) > 0:
        current_state = visit.pop(0)
        visited.add(current_state)

        if current_state in afd.program_function:
            for transition in afd.program_function[current_state]:
                if list(transition[1])[0] not in visited:
                    visit.append(list(transition[1])[0])

    states_inacessiveis = afd.states - visited

    afd.states = afd.states - states_inacessiveis

    afd.finals_states = afd.finals_states - states_inacessiveis

   
    for state in states_inacessiveis:
        if state in afd.program_function:
            del afd.program_function[state]


def totals(afd):
    sink_created = False
    sink = 'd'

    while(sink in afd.states):  
        sink = sink+'d'

    existing_states = set()
    for state in afd.program_function:
        existing_states.add(state)
        existing_transitions = set()
        for transition in afd.program_function[state]:
            existing_transitions.add(transition[0])
        
        if existing_transitions != afd.sigma:
            if not sink_created:
                sink_created = True
                afd.states.add(sink)
            transitions_add = afd.sigma - existing_transitions
            for char in transitions_add:
                afd.program_function[state].append((char, {sink}))

    
    states_add = afd.states - existing_states
    if len(states_add) > 0:
        if not sink_created:
            sink_created = True
            afd.states.add(sink)
            states_add.add(sink)

        for state in states_add:
            afd.program_function[state] = []
            for char in afd.sigma:
                afd.program_function[state].append((char, {sink}))


def table_generation(afd):
    table = {}
    states = list(afd.states)

    for state in states:
        table[state] = {}
        for e in states:
            if e != state:  
                if e in afd.finals_states and state not in afd.finals_states:
                    table[state][e] = False 
                elif e not in afd.finals_states and state in afd.finals_states:
                    table[state][e] = False 
                else:
                    table[state][e] = True
    return table


def table_process(afd, table):

    def head_list_close(states, lista, table):
        for elem in lista:
            if elem[0] == states:
                for i in range(1, len(elem)):
                    if table[list(elem[i])[0]][list(elem[i])[1]]:
                        table[list(elem[i])[0]][list(elem[i])[1]] = False
                        table[list(elem[i])[1]][list(elem[i])[0]] = False
                        head_list_close(elem[i], lista, table)

    def head_list_add(states1, states2, lista, table):
        head = False
        key = None

        for i, elem in enumerate(lista):
            if elem[0] == states1:
                head = True
                key = i

        
        if head:
            lista[key].append(states2)
        else:
            lista.append([states1, states2])

    states = list(afd.states)
    dependency_lists = []
    visited = []

    for state in states:
        for e in states:
            if e != state and table[state][e] and {state, e} not in visited:
                visited.append({state, e})
                for char in afd.sigma:
                    result1 = list(afd.starDelta({state}, char))[0]
                    result2 = list(afd.starDelta({e}, char))[0]
                    if result1 != result2:
                       
                        if not table[result1][result2]:
                            table[state][e] = False
                            table[e][state] = False
                            head_list_close(
                                {state, e}, dependency_lists, table)
                            break  
                        else:
                            head_list_add({result1, result2}, {
                                          state, e}, dependency_lists, table)


def close_equivalence(table, state):
    final = set()
    final.add(state)

    final_states = []
    initial_state = [state]

    while len(initial_state) > 0:
        e = initial_state.pop(0)
        final_states.append(e)

        for elem in table[e]:
            if table[e][elem]: 
                final.add(elem)
                if elem not in final_states:
                    initial_state.append(elem)

    return final


def remove_useless_states(afd):

    useless_states = set()

    for state in afd.states:
        visited = set()
        visit = [state]

        
        while len(visit) > 0:
            current_state = visit.pop(0)
            visited.add(current_state)

            if current_state in afd.program_function:
                for transition in afd.program_function[current_state]:
                    if list(transition[1])[0] not in visited:
                        visit.append(list(transition[1])[0])

        if visited.isdisjoint(afd.finals_states):
            useless_states.add(state)

    afd.states = afd.states - useless_states

    afd.finals_states = afd.finals_states - useless_states

    
    for state in useless_states:
        if state in afd.program_function:
            del afd.program_function[state]

    useless_transition = []
    
    for state in afd.program_function:
        new_transactions = []

        for transition in afd.program_function[state]:
            if list(transition[1])[0] not in useless_states:
                new_transactions.append(transition)

        if len(new_transactions) == 0:
            useless_transition.append(state)

        afd.program_function[state] = new_transactions

    for state in useless_transition:
        del afd.program_function[state]
