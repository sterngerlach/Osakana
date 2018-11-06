# coding: utf-8
# analyze_match_result.py

import pickle
import os

# ユーザ名(USER_NAME), ターゲットのユーザ名(TARGET_USER_NAME)は文字列定数
from config import USER_NAME, TARGET_USER_NAME

def main():
    MATCH_DATE = "2018-11-06-08-30"
    
    # ファイルに保存した対戦結果を開く
    file_dir = "match_results"
    file_name = "match_result_{}.pkl".format(MATCH_DATE)
    file_path = file_dir + os.sep + file_name
    
    with open(file_path, "rb") as f:
        match_results = pickle.load(f)
    
    print("successfully loaded match results: '{}'".format(file_name))
    
    score_table = { "g": { "g": (-1, -1), "w": (7, -3) },
                    "w": { "g": (-3, 7), "w": (1, 1) } }
    
    target_results = [match_result for match_result in match_results
                      if match_result["player0"] == TARGET_USER_NAME or
                          match_result["player1"] == TARGET_USER_NAME]
    
    pattern_max_length = 5
    target_action_patterns = { i + 1: [] for i in range(pattern_max_length) }
    
    actions_pair_done = []
    
    target_score_sum = 0
    
    to_action = lambda action_name: "g" if action_name == "GO" else "w" if action_name == "WAIT" else "?"
    
    for target_result in target_results:
        if target_result["player0"] == TARGET_USER_NAME:
            target_actions = [to_action(action)
                for action in target_result["player0_actions"]]
            opponent_actions = [to_action(action)
                for action in target_result["player1_actions"]]
        elif target_result["player1"] == TARGET_USER_NAME:
            target_actions = [to_action(action)
                for action in target_result["player1_actions"]]
            opponent_actions = [to_action(action)
                for action in target_result["player0_actions"]]
        
        if (target_actions, opponent_actions) not in actions_pair_done:
            actions_pair_done.append((target_actions, opponent_actions))
        
        target_score = 0
        opponent_score = 0
        
        for target_action, opponent_action in zip(target_actions, opponent_actions):
            target_score += score_table[target_action][opponent_action][0]
            opponent_score += score_table[target_action][opponent_action][1]
            
        target_score_sum += target_score
        
        print("id: {}".format(target_result["id"]))
        print("target: {} ({}), opponent: {} ({}), len: {}".format(
              target_result["player0"], target_score,
              target_result["player1"], opponent_score,
              len(target_actions)))
        print("target:   {}".format("".join(target_actions)))
        print("opponent: {}".format("".join(opponent_actions)))
        print("=" * 105)
        
        for i in range(pattern_max_length):
            action_pair = (target_actions[:i + 1], opponent_actions[:i])
            
            if action_pair not in target_action_patterns[i + 1]:
                target_action_patterns[i + 1].append(action_pair)
    
    print("target score sum: {}".format(target_score_sum))
    
    for i in range(pattern_max_length):
        for action_pair in target_action_patterns[i + 1]:
            print("opponent: {} <-> target: {}".format(action_pair[1], action_pair[0]))
            
if __name__ == "__main__":
    main()
    