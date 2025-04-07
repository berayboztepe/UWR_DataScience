# Python had difficulties and I could not optimize it. Submitted it with java version of sol-3 and got accepted.
# Sol-1, time limit exceeded

def in_love(op, l, r, segments):
    if op == '+':
        segments.append((l, r))
    elif op == '-':
        segments.remove((l, r))

    r_min = float('inf')
    l_max = -float('inf')

    for segment_l, segment_r in segments:
        r_min = min(r_min, segment_r)
        l_max = max(l_max, segment_l)

    if r_min < l_max:
        print("YES")
    else:
        print("NO")

if __name__ == '__main__':
    q = int(input())
    segments = []
    for _ in range(q):
        raw_query = input().split()
        operation = raw_query[0]
        l, r = map(int, raw_query[1:])
        in_love(operation, l, r, segments)


# Sol-2, wrong answer on test 2
import heapq

def in_love(op, l, r, segments, min_heap, max_heap, removed):
    if op == '+':
        heapq.heappush(min_heap, (r, l))
        heapq.heappush(max_heap, (-l, r))
        segments.add((l, r))
    elif op == '-':
        removed.add((l, r))
        segments.discard((l, r))

    while min_heap and (min_heap[0][1], min_heap[0][0]) in removed:
        removed_segment = heapq.heappop(min_heap)
        removed.remove((removed_segment[1], removed_segment[0]))

    while max_heap and (-max_heap[0][0], max_heap[0][1]) in removed:
        removed_segment = heapq.heappop(max_heap)
        removed.remove((-removed_segment[0], removed_segment[1]))

    if min_heap and max_heap:
        r_min = min_heap[0][0]
        l_max = -max_heap[0][0]
        if r_min < l_max:
            print("YES")
        else:
            print("NO")
    else:
        print("NO")

if __name__ == '__main__':
    q = int(input())
    segments = set()
    min_heap = []
    max_heap = []
    removed = set()
    for _ in range(q):
        raw_query = input().split()
        operation = raw_query[0]
        l, r = map(int, raw_query[1:])
        in_love(operation, l, r, segments, min_heap, max_heap, removed)


# # Sol-3, runtime error on test 1
from sortedcontainers import SortedDict

def main(operation, start, end, start_segments, end_segments):
    start = int(start)
    end = int(end)

    if operation == "+":
        add_segment(start_segments, end_segments, start, end)
    else:
        remove_segment(start_segments, end_segments, start, end)

    if is_non_intersecting(start_segments, end_segments):
        print("YES")
    else:
        print("NO")


def add_segment(start_map, end_map, start, end):
    start_map[start] = start_map.get(start, 0) + 1
    end_map[end] = end_map.get(end, 0) + 1

def remove_segment(start_map, end_map, start, end):
    if start_map[start] == 1:
        del start_map[start]
    else:
        start_map[start] -= 1

    if end_map[end] == 1:
        del end_map[end]
    else:
        end_map[end] -= 1

def is_non_intersecting(start_map, end_map):
    if not start_map or not end_map:
        return False

    return next(iter(start_map)) > next(iter(end_map))

if __name__ == "__main__":
    start_segments = SortedDict(lambda x: -x)
    end_segments = SortedDict()
    query_count = int(input().strip())
    for _ in range(query_count):
        operation, start, end = input().strip().split()
        main(operation, start, end, start_segments, end_segments)


