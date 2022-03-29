import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view
from src.make_dag import make_template_dag
from src.make_dag import make_template_dag2
from src.make_dag import make_random_dag



### 課題2個め以降に使っても構いません
def exec_time_order() -> [int]:
    return []

def critical_path_order() -> [int]:
    return []

def find_critical_path() -> [int]:
    return []



### DAG定義
# 0番目が入口ノード、len(G.nodes)-1番目が出繰りノードであるという前提を使って構いません

# 実行時間優先のテンプレート
G = make_template_dag()
# クリティカルパス優先のテンプレート
#G = make_template_dag2()
# ランダムDAG生成（引数はシード値）
#G = make_random_dag(123)



### クリティカルパス

critical_path = [0, 4, 6, 7]
# 余裕があればクリティカルパス検出アルゴリズムを作成
#critical_path = ...



### 実行順序決定

order = [o for o in range(len(G.nodes))]
# ここで実行順序決定アルゴリズムを書く
#order = ...

# 実行順序確認
print("order:\t\t"+str(order))



### 以下は触らない
# スケジューリング
filename = "output/scheduling_result_"+datetime.datetime.today().strftime("%m%d%H%M")
makespan = sched_sim(G, order, filename)

# makespan出力
print("makespan:\t"+str(makespan))

# HTML出力
make_scheduling_view(filename)
