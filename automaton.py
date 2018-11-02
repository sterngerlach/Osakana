# coding: utf-8
# automaton.py

import re

class FishAutomaton(object):
    """
    戦略のオートマトンのクラス
    """
    
    def __init__(self, name):
        self.states = {}
        self.alphabets = ["g", "w"]
        self.transitions = {}
        self.init_state = None
        self.current_state = None
        self.name = name
        
    def load_dfa_str(self, dfa_str):
        pattern = r"^(\d+):([gw]),(\d+),(\d+)$"
        first_line = True
        
        for line in dfa_str.splitlines():
            line = "".join(line.split())
            m = re.match(pattern, line)
            
            if m is None:
                raise ValueError("FishAutomaton::load_dfa_str(): invalid syntax")
            
            state = int(m.group(1))
            action = m.group(2)
            next_state_go = int(m.group(3))
            next_state_wait = int(m.group(4))
            
            if action not in self.alphabets:
                raise ValueError("FishAutomaton::load_dfa_str(): invalid action: {0}".format(action))
            
            self.states[state] = action
            self.transitions[state] = { "g": next_state_go, "w": next_state_wait }
            
            if first_line:
                self.init_state = state
                self.current_state = state
                first_line = False
        
    def to_dfa_str(self):
        dfa_str = ""
        
        for state, trans in self.transitions.items():
            dfa_str += "{0}:{1},{2},{3}\n".format(
                        state, self.states[state],
                        trans["g"], trans["w"])
        
        return dfa_str.rstrip()
        
    def transition(self, action):
        self.current_state = self.transitions[self.current_state][action]

"""
class FishAutomatonNFA(object):
    
    def __init__(self, name):
        self.states = {}
        self.alphabets = ["g", "w"]
        self.transitions = {}
        self.init_state = None
        self.current_state = None
        self.name = name
        
    def dfa_transition_states(self, states, action):
        new_states = []
        
        for state in states:
            for new_state in self.transitions[state][action]:    
                new_states.append(self.transitions[state][action])
        
        return list(set(new_states))
    
    def nfa_to_dfa(self):
        states = {}
        states[1] = { "group": [self.init_state],
                      "action": self.states[self.init_state] }
        transitions = {}
        state = 1
        j = 1
        
        while j <= state:
            for action in ("g", "w"):
                transition_states = self.dfa_transition_states(states[j]["group"], action)
                
                for i, item in states.items():
                    if set(item["group"]) == set(transition_states):
                        transitions[j][action] = i
                    else:
                        state += 1
                        
                        if len(set([self.states[trans] for trans in transition_states])) != 1:
                            raise ValueError("FishAutomatonNFA::nfa_to_dfa(): multiple possible actions")
                        
                        states[state] = { "group": transition_states, 
                                          "action": self.states[transition_states[0]] }
                        transitions[j] = {}
                        transitions[j][action] = state
        
            j += 1
        
        dfa = FishAutomaton(self.name)
        dfa.states = { state: item["action"] for state, item in states.items() }
        dfa.transitions = transitions
        dfa.init_state = 1
        dfa.current_state = 1
        
        return dfa
"""

class FishAutomatonTitForTat(FishAutomaton):
    """
    しっぺ返し戦略のオートマトンのクラス
    """
    
    def __init__(self):
        super().__init__("Tit For Tat")
        
        # 最初は協調を選択
        self.states[1] = "w"
        
        # 2回目以降は前回に相手が出した手と同じ手を選択
        self.transitions[1] = { "g": 2, "w": 3 }
        self.states[2] = "g"
        self.states[3] = "w"
        
        self.transitions[2] = { "g": 2, "w": 3 }
        self.transitions[3] = { "g": 2, "w": 3 }
        
        # 初期状態を設定
        self.init_state = 1
        self.current_state = 1

class FishAutomatonReverseTitForTat(FishAutomaton):
    """
    逆しっぺ返し戦略のオートマトンのクラス
    """
    
    def __init__(self):
        super().__init__("Reverse Tit For Tat")
        
        # 最初は裏切りを選択
        self.states[1] = "g"
        
        # 2回目以降は前回に相手が出した手と同じ手を選択
        self.transitions[1] = { "g": 2, "w": 3 }
        self.states[2] = "g"
        self.states[3] = "w"
        
        self.transitions[2] = { "g": 2, "w": 3 }
        self.transitions[3] = { "g": 2, "w": 3 }
        
        # 初期状態を設定
        self.init_state = 1
        self.current_state = 1

class FishAutomatonTitForTwoTats(FishAutomaton):
    """
    堪忍袋戦略のオートマトンのクラス
    """
    
    def __init__(self):
        super().__init__("Tit For Two Tats")
        
        # 最初は協調を選択
        self.states[1] = "w"
        
        # 相手が2回連続で裏切りを選んだときは次回に裏切りを選択
        # それ以外の場合では協調を選択
        self.transitions[1] = { "g": 2, "w": 1 }
        self.states[2] = "w"
        self.transitions[2] = { "g": 3, "w": 1 }
        self.states[3] = "g"
        self.transitions[3] = { "g": 2, "w": 1 }
        
        # 初期状態を設定
        self.init_state = 1
        self.current_state = 1

class FishAutomatonFriedman(FishAutomaton):
    """
    フリードマン戦略のオートマトンのクラス
    """
    
    def __init__(self):
        super().__init__("Friedman")
        
        # 最初は協調を選択
        self.states[1] = "w"
        
        # 相手が1回でも裏切りを選んだら以降は最後まで裏切りを選択
        self.transitions[1] = { "g": 2, "w": 1 }
        self.states[2] = "g"
        self.transitions[2] = { "g": 2, "w": 2 }
        
        # 初期状態を設定
        self.init_state = 1
        self.current_state = 1

class FishAutomatonAllC(FishAutomaton):
    """
    善人戦略のオートマトンのクラス
    """
    
    def __init__(self):
        super().__init__("AllC")
        
        # 常に協調を選択
        self.states[1] = "w"
        self.transitions[1] = { "g": 1, "w": 1 }
        
        # 初期状態を設定
        self.init_state = 1
        self.current_state = 1

class FishAutomatonAllD(FishAutomaton):
    """
    悪人戦略のオートマトンのクラス
    """
    
    def __init__(self):
        super().__init__("AllD")
        
        # 常に裏切りを選択
        self.states[1] = "g"
        self.transitions[1] = { "g": 1, "w": 1 }
        
        # 初期状態を設定
        self.init_state = 1
        self.current_state = 1
