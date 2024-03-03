from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
import json
import sys

ip_fname = ""
if len(sys.argv) < 2:
    ip_fname = input("Enter input file name: ")
else:
    ip_fname = sys.argv[1]

op_fname = ""
if len(sys.argv) < 3:
    op_fname = input("Enter output file name: ")
else:
    op_fname = sys.argv[2]

obj = {}
with open(ip_fname) as f:
    obj = json.load(f)

states = set(obj['states'])
input_symbols = set(obj['input_symbols'])
transitions = dict()
for k, v in dict(obj['transitions']).items():
    transitions[k] = dict()
    for sym, n in dict(v).items():
        transitions[k][sym] = set(n)
initial_state = obj['initial_state']
final_states = set(obj['final_states'])
nfa = NFA(states=states, input_symbols=input_symbols, 
          transitions=transitions, initial_state=initial_state, 
          final_states=final_states)

nfa.show_diagram().draw("nfa.png")

lambda_mapping = {}
transitions = {}

for state in nfa.states:
    try:
        lambdas = nfa.transitions[state][""]
        lambda_mapping[state] = frozenset({state}.union(lambdas))
    except KeyError:
        lambda_mapping[state] = frozenset({state})
has_phi = False
for state in nfa.states:
    transitions[state] = {}
    for ip in nfa.input_symbols:
        result = set()
        try:
            for i in nfa.transitions[state][ip]:
                result = result.union(lambda_mapping[i])
        except KeyError:
            has_phi = True
        transitions[state][ip] = frozenset(result)
if has_phi:
    transitions["phi"] = {}
    for ip in nfa.input_symbols:
        transitions["phi"][ip] = frozenset({ "phi" })

states_left = {lambda_mapping[nfa.initial_state]}

def get_next(cur: frozenset, ip: str) -> frozenset:
    result = set()
    for state in cur:
        try:
            result = result.union(transitions[state][ip])
        except KeyError:
            pass
    if len(result) == 0:
        result = {"phi"}
    return frozenset(result)

dfa_states = set()
dfa_transitions = {}
dfa_final_states = set()
while len(states_left) > 0:
    cur_state :frozenset = states_left.pop()
    if cur_state in dfa_states:
        continue
    dfa_states.add(cur_state)
    if not cur_state.isdisjoint(nfa.final_states):
        dfa_final_states.add(cur_state)
    dfa_transitions[cur_state] = {}
    for ip in nfa.input_symbols:
        next_states = get_next(cur_state, ip)
        if next_states not in dfa_states:
            states_left.add(next_states)
        dfa_transitions[cur_state][ip] = next_states
def stringify(fs: frozenset):
    if len(fs) == 1:
        return set(fs).pop()
    return "{" + ",".join(fs) + "}"

dfat_s = {}
for  k,v in dfa_transitions.items():
    v2 = {}
    for ip, n in v.items():
        v2[ip] = stringify(n)
    dfat_s[stringify(k)] = v2

obj = {
        "states": [stringify(s) for s in dfa_states],
        "input_symbols": list(nfa.input_symbols),
        "transitions": dfat_s,
        "final_states": [stringify(s) for s in dfa_final_states],
        "initial_state": stringify(lambda_mapping[nfa.initial_state])
    }
nfa.show_diagram().draw('nfa.png')

with open(op_fname, 'w') as f:
    json.dump(obj, f, indent=4)

states = set(obj['states'])
input_symbols = set(obj['input_symbols'])
transitions = dict()
for k, v in dict(obj['transitions']).items():
    transitions[k] = dict()
    for sym, n in dict(v).items():
        transitions[k][sym] = n
initial_state = obj['initial_state']
final_states = set(obj['final_states'])
dfa = DFA(states=states, input_symbols=input_symbols, 
          transitions=transitions, initial_state=initial_state, 
          final_states=final_states)

dfa.show_diagram().draw('dfa.png')
