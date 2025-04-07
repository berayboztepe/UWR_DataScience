# python is slow again, used C#

MOD = int(1e9 + 7)

def explore_cycle(node, states, mapping):
    global cycle_count, cycle_sizes
    cycle_sizes[cycle_count] += 1
    states[node] = 3
    next_node = mapping[node]
    if states[next_node] != 3:
        explore_cycle(next_node, states, mapping)

def find_cycles(node, states, mapping):
    global cycle_count, cycle_sizes
    states[node] = 2
    next_node = mapping[node]
    if states[next_node] == 0:
        find_cycles(next_node, states, mapping)
    elif states[next_node] == 1:
        states[node] = 1
        return
    else:
        cycle_sizes.append(0)
        explore_cycle(node, states, mapping)
        cycle_count += 1
    states[node] = 1

def calculate_roads(num_nodes, connections):
    global cycle_count, cycle_sizes, result
    power_of_two = [1] * (num_nodes + 1)

    for i in range(1, num_nodes + 1):
        power_of_two[i] = (power_of_two[i - 1] * 2) % MOD

    states = [0] * (num_nodes + 1)

    for i in range(1, num_nodes + 1):
        if states[i] == 0:
            find_cycles(i, states, connections)

    remaining_nodes = num_nodes
    for size in cycle_sizes:
        remaining_nodes -= size
        result = (result * (power_of_two[size] - 2 + MOD)) % MOD

    result = (result * power_of_two[remaining_nodes]) % MOD
    print(result)

if __name__ == '__main__':
    cycle_sizes = []
    cycle_count = 0
    result = 1

    num_nodes = int(input())
    connections = [0] + list(map(int, input().split()))
    calculate_roads(num_nodes, connections)

