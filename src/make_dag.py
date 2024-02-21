import networkx
import random



def make_template_dag() -> tuple[networkx.DiGraph, int]:
    G = networkx.DiGraph()

    # ノード定義
    nodes = [1, 7, 3, 3, 6, 1, 2, 1]
    G.add_nodes_from(range(len(nodes)))
    # 最悪実行時間定義
    for i, exec_time in enumerate(nodes):
        G.nodes[i]['exec'] = exec_time

    # エッジ定義
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (4, 6), (5, 6), (1, 7), (2, 7), (3, 7), (6, 7)])
    for edge in G.edges:
        G.edges[edge]['comm'] = 0
    
    return G, 14

def make_template_dag2() -> tuple[networkx.DiGraph, int]:
    G = networkx.DiGraph()

    # ノード定義
    nodes = [1, 4, 3, 1, 1, 5, 1, 3, 1]
    G.add_nodes_from(range(len(nodes)))
    # 最悪実行時間定義
    for i, exec_time in enumerate(nodes):
        G.nodes[i]['exec'] = exec_time

    # エッジ定義
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 4), (2, 8), (3, 5), (3, 6), (4, 8), (5, 7), (6, 7), (7, 8)])
    for edge in G.edges:
        G.edges[edge]['comm'] = 0
    
    return G, 13

def make_random_dag(seed: int) -> tuple[networkx.DiGraph, int]:
    random.seed(seed)
    G = networkx.DiGraph()

    layer = random.randrange(2, 5) # 層の数
    
    # 各層のノード定義
    # [0], [1, 2], [3, 4], [5] のようになる
    idx = 1
    node_metrics = [[0]] # 入口 1ノード
    for _ in range(layer):
        raw = random.randrange(2, 5) # 1層のノード数
        node_metrics.append([idx + i for i in range(raw)])
        idx += raw
    node_metrics.append([idx]) # 出口 1ノード

    # ノード登録
    G.add_nodes_from(sum(node_metrics, []))
    # 実行時間定義
    for i in G.nodes:
        G.nodes[i]['exec'] = random.randrange(1, 10)
    print('random: nodes')
    print(node_metrics)
    print('random: exec')
    print([G.nodes[i]['exec'] for i in G.nodes])
    
    # エッジ定義
    for i, nodes in enumerate(node_metrics):
        if i == len(node_metrics)-1:
            continue
        for node in nodes:
            # 次のレイヤーから1~4個のノードに接続する
            out_dig = random.sample(node_metrics[i+1], min(random.randrange(1, 4), len(node_metrics[i+1])))
            G.add_edges_from([(node, d) for d in out_dig])

    # DAG条件補完
    for i, nodes in enumerate(node_metrics):
        for node in nodes:
            # 前任がないノードはランダムに前の層と接続
            if i !=0 and len(list(G.predecessors(node))) == 0:
                G.add_edge(random.choice(node_metrics[i-1]), node)

    # 通信時間定義
    for edge in G.edges:
        G.edges[edge]['comm'] = 0
    print('random: edges')
    print([edge for edge in G.edges])
    print('')

    return G, 0