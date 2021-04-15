from models.AFNE import *
from models.AFN import *
from models.AFD import *
import string
from functions import *


ALPHABET = list(string.ascii_lowercase)
ALPHABET.append('1')
ALPHABET.append('0')




def erToAFNe(regular_expression):
    regular_expression = regular_expression.replace(' ', '').replace(
        '(', '').replace(')', '').replace(',', '')[::-1]
    aux = []
    
    while len(regular_expression) > 0:
       
        char = regular_expression[0]
        regular_expression = regular_expression[1:]
        
       
            
        if char in ALPHABET:
            aux.append(char)
        else:
            first_term = aux.pop()

            if first_term in ALPHABET:
                first_term = create_afne(first_term)

            new_first_term = update_afne_states('1', first_term)

            second_term = None
            new_second_term = None
            sigma = None

            if(char != "*"):
                second_term = aux.pop()

                if second_term in ALPHABET:
                    second_term = create_afne(second_term)

                new_second_term = update_afne_states('2', second_term)
                sigma = new_first_term.sigma.union(new_second_term.sigma)
            else:
                sigma = new_first_term.sigma.copy()
            if char == '.':
  
                states = new_first_term.states.union(
                    new_second_term.states)

                program_function = {list(new_first_term.finals_states)[0]: [
                    (None, {new_second_term.initial_state})]}
                program_function.update(new_first_term.program_function)
                program_function.update(new_second_term.program_function)
                initial_state = new_first_term.initial_state

                finals_states = {list(new_second_term.finals_states)[0]}

                resulting_afne = AFNe(
                    sigma, states, program_function, initial_state, finals_states)

                aux.append(resulting_afne)
            elif(char == '+'):
                states = new_first_term.states.union(new_second_term.states)
                states.add('q0')
                states.add('qf')

                program_function = {
                    'q0': [(None, {new_first_term.initial_state}), (None, {new_second_term.initial_state})],
                    list(new_first_term.finals_states)[0]: [(None, {'qf'})],
                    list(new_second_term.finals_states)[0]: [(None, {'qf'})]
                }
                program_function.update(new_first_term.program_function)
                program_function.update(new_second_term.program_function)

                initial_state = 'q0'
                finals_states = {'qf'}

                result_afne = AFNe(
                    sigma, states, program_function, initial_state, finals_states)

                aux.append(result_afne)
            
            elif char == '*':   
                
                states = new_first_term.states
                states.add('q0')
                states.add('qf')

                program_function = {
                                    'q0': [(None, {'qf'}), (None, {new_first_term.initial_state})],
                                    list(new_first_term.finals_states)[0]:[(None, {new_first_term.initial_state}), (None, {'qf'})],

                                }
                program_function.update(new_first_term.program_function)
                
                initial_state = 'q0'
                finals_states = {'qf'}

                resulting_afne = AFNe(sigma, states, program_function, initial_state, finals_states)

                aux.append(resulting_afne)    
    last_element = aux.pop()

    if last_element in {'*', '.', '+'}:
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
            result = afne.starDelta({state}, char)
            if len(result) != 0:
                if state in program_function:
                    program_function[state].append((char, result))
                else:
                    program_function[state] = [(char, result)]

    afn = AFN(sigma, states, program_function, initial_state, finals_states)
    return afn


def afnToAFD(afn):
    sigma = afn.sigma.copy()
    states = set()
    program_function = {}
    initial_state = None
    finals_states = set()

    final_states = []
    initial_states = [{afn.initial_state}]

    all_transitions = []

    
    while len(initial_states) > 0:
        e = initial_states.pop(0)
        final_states.append(e)

        for char in sigma:
            final = afn.starDelta(e, char)
            if len(final) > 0:
                all_transitions.append([e.copy(), char, final])
                if final not in final_states:
                    initial_states.append(final)

    counter_state_name = 0
    for transition in all_transitions:
        state = transition[0]
        destiny = transition[2]

        
        if isinstance(state, set):

            states.add('q'+str(counter_state_name))

            if not state.isdisjoint(afn.finals_states):
                finals_states.add('q'+str(counter_state_name))

            if list(state)[0] == afn.initial_state and initial_state == None:
                initial_state = 'q'+str(counter_state_name)

            for t in all_transitions:
                if t[0] == state:
                    t[0] = 'q'+str(counter_state_name)
                if t[2] == state:
                    t[2] = 'q'+str(counter_state_name)
            counter_state_name += 1

        if state != destiny:

            
            if isinstance(destiny, set):

                states.add('q'+str(counter_state_name))

                if not destiny.isdisjoint(afn.finals_states):
                    finals_states.add('q'+str(counter_state_name))

                if list(destiny)[0] == afn.initial_state and initial_state == None:
                    initial_state = 'q'+str(counter_state_name)

                for t in all_transitions:
                    if t[0] == destiny:
                        t[0] = 'q'+str(counter_state_name)
                    if t[2] == destiny:
                        t[2] = 'q'+str(counter_state_name)
                counter_state_name += 1

    
    for transition in all_transitions:
        state = transition[0]
        term = transition[1]
        destiny = transition[2]

        if state not in program_function:
            program_function[state] = [(term, {destiny})]
        else:
            program_function[state].append((term, {destiny}))

    afd = AFD(sigma, states, program_function, initial_state, finals_states)

    return afd


def afdToAFDmin(afd):

    if not isinstance(afd, AFD):
        raise Exception(
            "Automato precisa ser deterministico para ser minimizado")

    afdmin = AFD(afd.sigma.copy(), afd.states.copy(
    ), afd.program_function.copy(), afd.initial_state, afd.finals_states.copy())

    removes_inaccessible_states(afdmin)
    totals(afdmin)
    table = table_generation(afdmin)
    table_process(afdmin, table)

    resulting_assemblies = []
    unified_states = []

    for state in table:
        final_states = False
        for cr in resulting_assemblies:
            if state in cr:
                final_states = True
                break

        if not final_states:
            resulting_assemblies.append(close_equivalence(table, state))

    for i in range(len(resulting_assemblies)):
        unified_states.append('q'+str(i))

    afdmin.states = set(unified_states)

    resulting_program_function = {}
    all_transitions = []

    
    for state in afdmin.program_function:
        for transition in afdmin.program_function[state]:
            all_transitions.append([state, transition[0], transition[1]])

    
    for transition in all_transitions:
        inicio = transition[0]
        inicio_traduzido = None
        destiny = list(transition[2])[0]
        translate_destiny = None

        for index, group in enumerate(resulting_assemblies):
            if inicio in group:
                inicio_traduzido = unified_states[index]

            if destiny in group:
                translate_destiny = unified_states[index]

        transition[0] = inicio_traduzido
        transition[2] = {translate_destiny}

    
    for transition in all_transitions:
        if transition[0] not in resulting_program_function:
            resulting_program_function[transition[0]] = []

        
        if (transition[1], transition[2]) not in resulting_program_function[transition[0]]:
            resulting_program_function[transition[0]].append(
                (transition[1], transition[2]))

    resulting_stats_finals = set()
    resulting_initial_state = None

    
    for index, group in enumerate(resulting_assemblies):
        for state in group:
            if state in afdmin.finals_states:
                resulting_stats_finals.add(unified_states[index])

            if state == afdmin.initial_state:
                resulting_initial_state = unified_states[index]

    afdmin.initial_state = resulting_initial_state
    afdmin.finals_states = resulting_stats_finals
    afdmin.program_function = resulting_program_function

    remove_useless_states(afdmin)

    return afdmin
