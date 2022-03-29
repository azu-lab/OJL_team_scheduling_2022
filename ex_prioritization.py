import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view
from src.make_dag import make_template_dag
from src.make_dag import make_template_dag2
from src.make_dag import make_random_dag



### 課題2個め以降に使っても構いません
def exec_time_order() -> [int]:
    ext_order = []
    wait_nodes = [0]

    while(len(wait_nodes) != 0):
        max_node = wait_nodes[0]
        for node in wait_nodes:
            if G.nodes[node]["exec"] > G.nodes[max_node]["exec"]:
                max_node = node

        wait_nodes.remove(max_node)
        ext_order.append(max_node)
        
        for v in G:
            if v not in ext_order and v not in wait_nodes and {n for n in G.predecessors(v)} <= set(ext_order):
                wait_nodes.append(v)

    return ext_order

def critical_path_order() -> [int]:
    cp_order = []
    wait_nodes = [0]

    while(len(wait_nodes) != 0):
        max_node = wait_nodes[0]
        for node in wait_nodes:
            if node in critical_path:
                max_node = node
                break
            if G.nodes[node]["exec"] > G.nodes[max_node]["exec"]:
                max_node = node

        wait_nodes.remove(max_node)
        cp_order.append(max_node)
        
        for v in G:
            if v not in cp_order and v not in wait_nodes and {n for n in G.predecessors(v)} <= set(cp_order):
                wait_nodes.append(v)

    return cp_order

def find_critical_path() -> [int]:
    # 終了時間計算関数
    def culc_fn_time(idx: int, time):
        if time > fn_times[idx]:
            fn_times[idx] = time
            for suc in G.successors(idx):
                culc_fn_time(suc, time + G.nodes[suc]["exec"])

    cp = []
    # 終了時間計算
    fn_times = [0 for v in G.nodes]
    culc_fn_time(0, G.nodes[0]["exec"])

    cp_elem = len(G.nodes) - 1
    cp.append(cp_elem)
    while(len([v for v in G.predecessors(cp_elem)]) != 0):
        max_idx = 0
        for p in G.predecessors(cp_elem):
            if fn_times[p] > fn_times[max_idx]:
                max_idx = p
        cp_elem = max_idx
        cp.append(cp_elem)

    cp.reverse()
    return cp




### DAG定義

# 課題1のDAG
G, target_makespan = make_template_dag()
# 課題2のDAG
#G, target_makespan = make_template_dag2()
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
