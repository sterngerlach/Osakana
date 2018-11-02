
# Osakana: お魚オートマトンのシミュレータ

Python 3で書かれたお魚オートマトンのシミュレータのようなものです。

## 使い方

- お魚オートマトンは、`automaton.py`に定義された`FishAutomaton`クラスを継承する必要があります。
- 幾つかの単純な戦略に対するオートマトンは既に作成済みです。しっぺ返し戦略に対しては`FishAutomatonTitForTat`クラスが、逆しっぺ返し戦略に対しては`FishAutomatonReverseTitForTat`クラスが、堪忍袋戦略に対しては`FishAutomatonTitForTwoTats`クラスが、フリードマン戦略に対しては`FishAutomatonFriedman`クラスが、善人戦略に対しては`FishAutomatonAllC`クラスが、そして悪人戦略に対しては`FishAutomatonAllD`クラスがそれぞれ用意されています。これらのクラスをみればオートマトンの定義の仕方が分かると思います。
- `FishAutomaton`クラスの`load_dfa_str`メソッドは、課題で指示されたフォーマットに従って記述された、オートマトンを表現する文字列を読み取って、`FishAutomaton`クラスのオブジェクトとして利用可能にするためのものです。
- `FishAutomaton`クラスの`to_dfa_str`メソッドは、現在の`FishAutomaton`インスタンスが表現するオートマトンを、課題で指示されたフォーマットに従って文字列に変換するためのものです。
- `FishAutomaton`クラスの`transition`メソッドは、状態遷移関数と相手の行動を元に、次の状態(と行動)を決定するためのものです。
- `simulator.py`に定義された`CompetitionSimulator`クラスは、`FishAutomaton`インスタンスが表現するお魚オートマトン同士を戦わせるためのものです。
- `CompetitionSimulator`クラスの`run`メソッドは、2つの`FishAutomaton`インスタンスと`verbose`フラグを受け取って、2つのお魚オートマトン同士を戦わせた結果(両者の得点と、勝者の番号)を返します。`verbose`フラグが`True`である場合は、戦わせた結果を標準出力に書き込みます。勝者の番号は、第1引数に指定されたお魚オートマトンが勝利した場合は`0`、第2引数に指定されたお魚オートマトンが勝利した場合は`1`、そして引き分けの場合は`-1`となります。
- `CompetitionSimulator`クラスの`run_round_robin`メソッドは、`FishAutomaton`インスタンスのリストを受け取って、総当たり戦を実行した結果(各オートマトンの勝ち数、負け数、引き分け数、総得点のリスト)を返します。
- これらのクラスの使用法は`main.py`をみれば分かると思います。
