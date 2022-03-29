import networkx
import random



def make_template_dag():
    G = networkx.DiGraph()

    # ノード定義
    nodes = [1, 7, 3, 3, 6, 1, 2, 1]
    G.add_nodes_from(range(len(nodes)))
    # 最悪実行時間定義
    for i, exec_time in enumerate(nodes):
        G.nodes[i]["exec"] = exec_time

    # エッジ定義
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (4, 6), (5, 6), (1, 7), (2, 7), (3, 7), (6, 7)])
    for edge in G.edges:
        G.edges[edge]["comm"] = 0
    
    return G

def make_template_dag2():
    G = networkx.DiGraph()

    # ノード定義
    nodes = [1, 3, 2, 1, 1, 4, 1, 2, 1]
    G.add_nodes_from(range(len(nodes)))
    # 最悪実行時間定義
    for i, exec_time in enumerate(nodes):
        G.nodes[i]["exec"] = exec_time

    # エッジ定義
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 4), (2, 8), (3, 5), (3, 6), (4, 8), (5, 7), (6, 7), (7, 8)])
    for edge in G.edges:
        G.edges[edge]["comm"] = 0
    
    return G

def make_random_dag(seed: int):
    random.seed(seed)
    G = networkx.DiGraph()

    nodes = [[0]]
    layer = random.randrange(2, 5)
    idx = 1
    
    # ノード定義
    for l in range(layer):
        raw = random.randrange(2, 5)
        nodes.append([idx + i for i in range(raw)])
        idx += raw
    nodes.append([idx])

    # ノード登録
    G.add_nodes_from([node for raw in nodes for node in raw])
    for i in G.nodes:
        G.nodes[i]["exec"] = random.randrange(1, 10)
    print("random: nodes")
    print(nodes)
    print("random: exec")
    print([G.nodes[node]["exec"] for raw in nodes for node in raw])
    
    # エッジ定義
    for i, vs in enumerate(nodes):
        if i == len(nodes)-1:
            break
        for v in vs:
            out_dig = random.sample(nodes[i+1], min(random.randrange(1, 4), len(nodes[i+1])))
            G.add_edges_from([(v, d) for d in out_dig])

    # DAG条件補完
    for i, vs in enumerate(nodes):
        for v in vs:
            if i !=0 and len([node for node in G.predecessors(v)]) == 0:
                G.add_edge(random.choice(nodes[i-1]), v)

    # 通信時間定義
    for edge in G.edges:
        G.edges[edge]["comm"] = 0
    print("random: edges")
    print([edge for edge in G.edges])
    print("")

    return G