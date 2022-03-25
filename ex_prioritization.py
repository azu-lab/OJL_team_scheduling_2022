import datetime
import networkx
from src.sched_sim import sched_sim
from src.scheduling_viewer import make_scheduling_view
from src.make_dag import make_template_dag
from src.make_dag import make_random_dag



# DAG定義
G = make_template_dag()

# 実行順序決定
priority = [p for p in range(8)]
# コメントを外して優先を入れ替えるとエラー発生
#priority = [0, 4, 5, 1, 2, 3, 6, 7]
#priority.sort(key=lambda x:G.nodes[x]["exec"], reverse=True)

# 優先度確認
print(priority)



### 以下は触らない
# スケジューリング
filename = "output/scheduling_result_"+datetime.datetime.today().strftime("%m%d%H%M")
makespan = sched_sim(G, priority, filename)

# makespan出力
print("makespan: "+str(makespan))

# HTML出力
make_scheduling_view(filename)
