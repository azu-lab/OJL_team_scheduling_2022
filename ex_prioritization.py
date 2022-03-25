import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view
from src.make_dag import make_template_dag
from src.make_dag import make_random_dag



### 課題2個め以降に使っても構いません
def exec_time_order() -> [int]:
    order = []
    wait_nodes = [0]

    while(len(wait_nodes) != 0):
        max_node = wait_nodes[0]
        for i in wait_nodes:
            if G.nodes[i]["exec"] > G.nodes[max_node]["exec"]:
                max_node = i

        wait_nodes.remove(max_node)
        order.append(max_node)
        
        for v in G:
            if v not in order and v not in wait_nodes and {n for n in G.predecessors(v)} <= set(order):
                wait_nodes.append(v)

    return order

def critical_path_order() -> [int]:
    return []

def find_critical_path() -> [int]:
    return []



# DAG定義
# 0番目が入口ノードであるという前提を使って構いません
G = make_template_dag()

# クリティカルパス
critical_path = [0, 4, 6, 7]

# 実行順序決定
order = exec_time_order()
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
