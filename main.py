# coding: utf-8
# main.py

from automaton import (FishAutomaton,
                       FishAutomatonTitForTat,
                       FishAutomatonReverseTitForTat,
                       FishAutomatonTitForTwoTats,
                       FishAutomatonFriedman,
                       FishAutomatonAllC,
                       FishAutomatonAllD)
from simulator import CompetitionSimulator
from custom import CustomAutomaton

def main():
    fish_automaton_initial = FishAutomaton("Initial")
    fish_automaton_initial.load_dfa_str("1:g,2,2\n2:g,3,3\n3:w,1,1")
    print("States: {}".format(fish_automaton_initial.states))
    print("Transitions: {}".format(fish_automaton_initial.transitions))
    print(fish_automaton_initial.to_dfa_str())
    
    fish_automaton_custom = CustomAutomaton()
    print("States: {}".format(fish_automaton_custom.states))
    print("Transitions: {}".format(fish_automaton_custom.transitions))
    print(fish_automaton_custom.to_dfa_str())
    
    simulator = CompetitionSimulator()
    
    simulator.run_round_robin([
        fish_automaton_initial,
        fish_automaton_custom,
        FishAutomatonTitForTat(),
        FishAutomatonReverseTitForTat(),
        FishAutomatonTitForTwoTats(),
        FishAutomatonFriedman(),
        FishAutomatonAllC(),
        FishAutomatonAllD()])
    
    simulator.run(fish_automaton_custom, fish_automaton_initial)
    
if __name__ == "__main__":
    main()
    