"""
I learned something new today. DFS didn't seem like the right solution because of having to find "all" paths and
the tree size being huge. But you can use memoization which is when you cache answers to expensive questions. Doing
the recursive DFS with a cache annotation in it will prevent unnecessary crawling through the tree.
"""
import collections
from collections import defaultdict
from functools import lru_cache

from utils import puzzle




@puzzle
def part1(puzzle_input):
    start, end = 'you', 'out'
    m = defaultdict(set)
    for line in puzzle_input:
        items = [item.strip() for item in line.split() if item.strip()]
        m[items[0].replace(':', '')] |= set(items[1:])

    result  = bfs(m, start, end)
    print(result)


def bfs(m: dict, start: str, end: str) -> int:
    q = collections.deque({start})
    result = 0
    while q:
        item = q.popleft()
        children = m[item]
        for child in children:
            if child == end:
                result += 1
            else:
                q.append(child)
    return result





@puzzle
def part2(puzzle_input):
    m = defaultdict(set)
    for line in puzzle_input:
        items = [item.strip() for item in line.split() if item.strip()]
        m[items[0].replace(':', '')] |= set(items[1:])

    @lru_cache(maxsize=None)
    def dfs(node: str, dac: bool = False, fft: bool = False) -> int:
        if node == 'out' and dac and fft:
            return 1
        total = 0
        for child in m.get(node, []):
            total += dfs(child, dac or child == 'dac', fft or child == 'fft')

        return total

    result = dfs('svr')
    print(result)



def _print_map(m):
    with open('/Users/ericdufresne/Library/Application Support/JetBrains/PyCharm2025.1/scratches/scratch.txt', 'w+') as f:
        f.writelines([f'{k}: {','.join(v)}\n' for k, v in m.items()])





if __name__ == '__main__':
    part2()