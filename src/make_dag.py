import networkx



def make_template_dag():
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
    
    return G

def make_random_dag():
    networkx.DiGraph()

    return