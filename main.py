from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
from visual_automata.fa.nfa import VisualNFA
from visual_automata.fa.dfa import VisualDFA
import json
import sys


ip_fname = ""
if len(sys.argv) < 2:
    ip_fname = input("Enter input file name: ")
else:
    ip_fname = sys.argv[1]


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
print(transitions)

nfa = NFA(
    states={"q0", "q1", "q2"},
    input_symbols={"0", "1"},
    transitions={
        "q0": {"": {"q2"}, "1": {"q1"}},
        "q1": {"1": {"q2"}, "0": {"q0", "q2"}},
        "q2": {},
    },
    initial_state="q0",
    final_states={"q0"},
)

#initial_state = obj['initial_state']
#final_states = set(obj['final_states'])
#nfa = NFA(states=states, input_symbols=input_symbols, 
#          transitions=transitions, initial_state=initial_state, 
#          final_states=final_states)

