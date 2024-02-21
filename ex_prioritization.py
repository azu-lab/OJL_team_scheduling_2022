import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view
from src.make_dag import make_template_dag
from src.make_dag import make_template_dag2
from src.make_dag import make_random_dag



# 実行時間が大きい順
def exec_time_order() -> list[int]:
    # 実行順序
    ext_order = []
    # 待機状態のノード
    wait_nodes = [0]

    while(len(wait_nodes) != 0):
        # wait_nodesの中で最も優先度が高いノードをnodeに代入（以下にコードを書く）
        # ヒント: G.nodes[0]['exec'] でノード0の実行時間を取得
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
def find_critical_path() -> list[int]:
    # 終了時間計算関数
    def culc_fn_time(idx: int, time):
        # 遅い時間が与えられたら更新し、後続を再計算
        if time > finish_times[idx]:
            finish_times[idx] = time
            for suc in G.successors(idx):
                culc_fn_time(suc, time + G.nodes[suc]['exec'])

    # 終了時間計算
    finish_times = [0 for v in G.nodes]
    culc_fn_time(0, G.nodes[0]['exec'])

    # 出口から入口まで、最も終了時間が大きいノードを辿る
    critical_path = []
    critical_path.append(len(G.nodes) - 1) # 出口ノードを通るのは確定
    while len(list(G.predecessors(critical_path[0]))) != 0: # 前任の数が0=入口が先頭に格納されるまで繰り返す
        max_idx = None
        # 前任のうち終了時刻が最も大きいノードを検出
        for p in G.predecessors(critical_path[0]):
            if max_idx is None or finish_times[p] > finish_times[max_idx]:
                max_idx = p
        critical_path.insert(0, max_idx)

    return critical_path

# クリティカルパス優先
def critical_path_order() -> list[int]:
    cp_order = []
    wait_nodes = [0]
    critical_path = find_critical_path()

    while(len(wait_nodes) != 0):
        # wait_nodesの中で最も優先度が高いノードをnodeに代入（以下にコードを書く）
        # 基本やることは実行時間が大きい順と同じ。クリティカルパスの優先度を上げる
        # ヒント: G.nodes[0]['exec'] でノード0の実行時間を取得
        # ヒント: critical_path はクリティカルパスのノード番号配列（[0, 2, 5, 8]など）
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
# G, target_makespan = make_template_dag2()
# ランダムDAG生成（引数はシード値）
#G, target_makespan = make_random_dag(123)



### 実行順序決定

order = [o for o in range(len(G.nodes))]

# ここに実行順序を書く（課題部分）
# order = [0, 1, 4, 2, 3, 5, 6, 7] # 課題1の正答
# order = [0, 3, 5, 1, 2, 4, 6, 7, 8] # 課題2の正答
order = exec_time_order()

# 実行順序確認
print('order:\t\t'+str(order))



### 以下は触らない
# スケジューリング
filename = 'output/scheduling_result_'+datetime.datetime.today().strftime('%m%d%H%M')
makespan = sched_sim(G, order, filename)

# makespan出力
print('makespan:\t'+str(makespan))

if target_makespan != 0:
    if makespan <= target_makespan:
        print('result:\t\t'+'\033[32m'+'Succeed!'+'\033[0m')
    else:
        print('result:\t\t'+'\033[31m'+'Failed...'+'\033[0m')

# HTML出力
make_scheduling_view(filename)
