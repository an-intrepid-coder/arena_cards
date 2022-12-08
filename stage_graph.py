import enemy
import constants
import card_battle

class StageGraphNode:
    def __init__(self, contents, prev_node, next_node):
        self.contents = contents
        self.prev_node = prev_node
        self.next_node = next_node

def generate_stage_graph(player, stdscr):
    root = StageGraphNode(card_battle.CardBattle(player, enemy.generate_enemies(stage=1), stdscr), None, None)
    graph = [root]
    for i in range(constants.NUM_STAGES):
        stage_level = i + 1
        next_stage = card_battle.CardBattle(player, enemy.generate_enemies(stage_level), stdscr)
        next_node = StageGraphNode(next_stage, graph[i], None)
        graph[i].next_node = next_node
        graph.append(next_node)
    return graph

