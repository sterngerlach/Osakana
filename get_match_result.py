# coding: utf-8
# get_match_result.py

from bs4 import BeautifulSoup

import os
import pickle
import requests
import time

# 学籍番号(STUDENT_ID), パスワード(PASSWORD), ユーザ名(USER_NAME)はいずれも文字列定数
from config import STUDENT_ID, PASSWORD, USER_NAME

def main():
    MATCH_DATE = "2018-11-06-08-30"
    RESULT_ID_MIN = 13141
    RESULT_ID_MAX = 15768
    
    # セッションを開始
    sess = requests.Session()
    
    # ログイン
    login_info = { "studentId": STUDENT_ID,
                   "password": PASSWORD }
    login_url = "http://osakana.ailab.ics.keio.ac.jp/login"
    
    res = sess.post(login_url, data=login_info)
    res.raise_for_status()
    
    # 対戦結果の取得
    match_result_url = "http://osakana.ailab.ics.keio.ac.jp/histories/matches/{}"
    
    # 対戦結果のリスト
    match_results = []
    
    for i in range(RESULT_ID_MIN, RESULT_ID_MAX + 1):
        res = sess.get(match_result_url.format(i), timeout=5)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, "html.parser")
        
        table_element = soup.find("table")
        thead_element = table_element.find("thead")
        tbody_element = table_element.find("tbody")
        
        player_names = thead_element.findAll("td")
        player0_name = player_names[0].text.replace(" state", "")
        player1_name = player_names[1].text.replace(" state", "")
        
        print("result {}: player0: {}, player1: {}"
              .format(i, player0_name, player1_name))
        
        match_result = { "player0": player0_name,
                         "player1": player1_name,
                         "player0_actions": [],
                         "player1_actions": [],
                         "id": i }
        steps = []
        
        action_pairs = tbody_element.findAll("tr")
        
        for action_pair in action_pairs:
            step_num = action_pair.find("th").text
            actions = action_pair.findAll("td")
            player0_action = actions[0].text
            player1_action = actions[1].text
            steps.append(int(step_num))
            match_result["player0_actions"].append(player0_action)
            match_result["player1_actions"].append(player1_action)
        
        match_result["player0_actions"] = [action for _, action in
            sorted(zip(steps, match_result["player0_actions"]))]
        match_result["player1_actions"] = [action for _, action in
            sorted(zip(steps, match_result["player1_actions"]))]
        
        match_results.append(match_result)
        
        time.sleep(0.1)
    
    # 取得した対戦結果をファイルに保存
    file_dir = "match_results"
    file_name = "match_result_{}.pkl".format(MATCH_DATE)
    file_path = file_dir + os.sep + file_name
    
    with open(file_path, "wb") as f:
        pickle.dump(match_results, f)
    
    # 対戦結果の取得を終了
    print("done: match results written to pickle '{}'".format(file_name))

if __name__ == "__main__":
    main()
    