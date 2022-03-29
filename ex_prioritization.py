import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view
from src.make_dag import make_template_dag
from src.make_dag import make_template_dag2
from src.make_dag import make_random_dag



### DAG定義

# 課題1のDAG
G, target_makespan = make_template_dag()
# 課題2のDAG
G, target_makespan = make_template_dag2()
# ランダムDAG生成（引数はシード値）
#G, target_makespan = make_random_dag(123)



### 実行順序決定

order = [o for o in range(len(G.nodes))]

# ここに実行順序を書く（課題部分）
#order = []

# 実行順序確認
print("order:\t\t"+str(order))



### 以下は触らない
# スケジューリング
filename = "output/scheduling_result_"+datetime.datetime.today().strftime("%m%d%H%M")
makespan = sched_sim(G, order, filename)

# makespan出力
print("makespan:\t"+str(makespan))

if target_makespan != 0:
    if makespan <= target_makespan:
        print("result:\t\t"+"\033[32m"+"Succeed!"+"\033[0m")
    else:
        print("result:\t\t"+"\033[31m"+"Failed..."+"\033[0m")

# HTML出力
make_scheduling_view(filename)
