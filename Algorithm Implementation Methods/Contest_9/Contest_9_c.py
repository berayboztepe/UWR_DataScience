from collections import defaultdict

def path_etic_mexs(num_nodes):
    adjacency_list = defaultdict(list)
    answer = [-1] * num_nodes

    for edge_id in range(1, num_nodes):
        node_a, node_b = map(int, input().split())
        adjacency_list[node_a].append(edge_id)
        adjacency_list[node_b].append(edge_id)

    max_degree_node = (0, 0)
    for node in range(1, num_nodes + 1):
        max_degree_node = max(max_degree_node, (len(adjacency_list[node]), node))

    current_label = 0

    for edge_id in adjacency_list[max_degree_node[1]]:
        answer[edge_id] = current_label
        current_label += 1

    for edge_id in range(1, num_nodes):
        if answer[edge_id] == -1:
            answer[edge_id] = current_label
            current_label += 1

    for edge_id in range(1, num_nodes):
        print(answer[edge_id])

if __name__ == "__main__":
    num_nodes = int(input())
    path_etic_mexs(num_nodes)