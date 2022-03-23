import networkx as nx
from typing import List

from .lib.cluster import CluesteredProcessor
from .lib.list_scheduler import ListSchedulerToClusteredProcessor


NUM_CORE = 2  # コア数

def sched_sim(dag: nx.DiGraph, scheduling_list: List[int], filename: str) -> None:
    P = CluesteredProcessor(1, NUM_CORE, 1)
    S = ListSchedulerToClusteredProcessor(dag, P, scheduling_list)
    S.schedule()
    S.dump_log_to_json(filename)
