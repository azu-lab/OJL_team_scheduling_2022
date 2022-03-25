import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view
from src.make_dag import make_template_dag
from src.make_dag import make_random_dag



# DAG定義
G = make_template_dag()

# 実行順序決定
order = [p for p in range(8)]
# ここで実行順序決定アルゴリズムを書く

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



### 課題2個め以降に使っても構いません
def exec_time_order() -> [int]:
    return []

def critical_path_order() -> [int]:
    return []

def find_critical_path() -> [int]:
    return []
