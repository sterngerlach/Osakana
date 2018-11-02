# coding: utf-8
# simulator.py

import numpy as np

class CompetitionSimulator(object):
    """
    対戦用のクラス
    """
    
    def __init__(self):
        # 得点表の設定
        self.score_table = { "g": { "g": (-1, -1), "w": (7, -3) },
                             "w": { "g": (-3, 7), "w": (1, 1) } }
    
    def run(self, player0, player1, verbose=True):
        score0 = 0
        score1 = 0
        
        for i in range(250):
            # 行動を元に得点を加算
            action0 = player0.states[player0.current_state]
            action1 = player1.states[player1.current_state]
            score = self.score_table[action0][action1]
            score0 += score[0]
            score1 += score[1]
            
            # 状態遷移
            player0.transition(action1)
            player1.transition(action0)
        
        if verbose:
            print("player0({0}): {1}".format(type(player0).__name__, score0))
            print("player1({0}): {1}".format(type(player1).__name__, score1))
            print("player0 won" if score0 > score1 else
                  "player1 won" if score1 > score0 else
                  "draw")
        
        winner = 0 if score0 > score1 else 1 if score1 > score0 else -1
        
        return (winner, score0, score1)
    
    def run_round_robin(self, players):
        player_num = len(players)
        num_of_wins = [0 for i in range(player_num)]
        num_of_loses = [0 for i in range(player_num)]
        num_of_draws = [0 for i in range(player_num)]
        scores = [0 for i in range(player_num)]
        
        for i in range(player_num):
            for j in range(i, player_num):
                if i == j:
                    continue
                
                winner, score0, score1 = self.run(players[i], players[j], False)
                winner_id = i if winner == 0 else j if winner == 1 else -1
                loser_id = j if winner == 0 else i if winner == 1 else -1
                
                # 勝敗数を更新
                if winner_id != -1:
                    num_of_wins[winner_id] += 1
                    num_of_loses[loser_id] += 1
                else:
                    num_of_draws[i] += 1
                    num_of_draws[j] += 1
                
                # 総得点を更新
                scores[i] += score0
                scores[j] += score1
        
        for i in np.argsort(scores)[::-1]:
            print("player({0}): {1} wins, {2} loses, {3} draws, "
                  "total: {4}, average: {5}"
                  .format(players[i].name,
                          num_of_wins[i], num_of_loses[i],
                          num_of_draws[i], scores[i],
                          round(scores[i] / player_num, 1)))
        
        return (num_of_wins, num_of_loses, num_of_draws, scores)
