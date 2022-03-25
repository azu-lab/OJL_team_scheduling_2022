import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view

# ここは触らない
### DAG定義 ###
G = networkx.DiGraph()

# ノード定義
G.add_nodes_from(range(8))
# 最悪実行時間定義
for i, exec_time in enumerate([1, 7, 3, 3, 6, 1, 2, 1]):
    G.nodes[i]["exec"] = exec_time

# エッジ定義
G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (4, 6), (5, 6), (1, 7), (2, 7), (3, 7), (6, 7)])
for edge in G.edges:
    G.edges[edge]["comm"] = 0

### DAG定義 ###



# ここが課題部分
### 優先度決定 ###
priority = [p for p in range(8)]
# コメントを外して優先を入れ替えるとエラー発生
#priority = [0, 4, 5, 1, 2, 3, 6, 7]
#priority.sort(key=lambda x:G.nodes[x]["exec"], reverse=True)

# 優先度確認
print(priority)

### 優先度決定 ###



# ここは触らない
### スケジューリング実行 ###
# スケジューリング
filename = "output/scheduling_result_"+datetime.datetime.today().strftime("%m%d%H%M")
makespan = sched_sim(G, priority, filename)

# makespan出力
print("makespan: "+str(makespan))

# HTML出力
make_scheduling_view(filename)