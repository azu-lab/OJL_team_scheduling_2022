import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view
from src.make_dag import make_template_dag
from src.make_dag import make_template_dag2
from src.make_dag import make_random_dag



# 実行時間が大きい順
def exec_time_order() -> [int]:
    # 実行順序
    ext_order = []
    # 待機状態のノード
    wait_nodes = [0]

    while(len(wait_nodes) != 0):
        # ルールに従って次の実行順序のノードを決定（以下にコードを書く）
        node = max(wait_nodes, key=lambda x: G.nodes[x]['exec'])



        # 決定したノードを待機状態から削除
        wait_nodes.remove(node)
        # 決定したノードを順序に挿入
        ext_order.append(node)
        
        # 決定したノードの後続ノードを待機状態に（ノード依存関係の遵守）
        for v in G:
            if v not in ext_order and v not in wait_nodes and {n for n in G.predecessors(v)} <= set(ext_order):
                wait_nodes.append(v)

    return ext_order

# クリティカルパス検索関数
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

    # 出口から入口まで、最も終了時間が大きいノードを辿る
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

# クリティカルパス優先
def critical_path_order() -> [int]:
    cp_order = []
    wait_nodes = [0]
    critical_path = find_critical_path()

    while(len(wait_nodes) != 0):
        for w in wait_nodes:
            if w in critical_path:
                node = w
                break
        else:
            node = max(wait_nodes, key=lambda x: G.nodes[x]['exec'])



        wait_nodes.remove(node)
        cp_order.append(node)
        
        for v in G:
            if v not in cp_order and v not in wait_nodes and {n for n in G.predecessors(v)} <= set(cp_order):
                wait_nodes.append(v)

    return cp_order



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
order = critical_path_order()

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
