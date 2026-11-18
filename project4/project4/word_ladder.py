"""
Word Ladder Solver: Graph Search Algorithms for Shortest Transformation Sequences
Algorithms: Breadth-First Search (BFS), Bidirectional BFS, Depth-First Search (DFS)
Optimizations: Wildcard Pattern Pre-indexing (O(N * L^2)), Frontier Balancing
"""

import collections
import time
import os
from typing import List, Set, Dict, Optional, Tuple, Any

class WordLadderSolver:
    """
    Solves Word Ladder puzzles using unweighted graph search algorithms.
    Nodes: Valid words of length L.
    Edges: Pairs of words differing by exactly one character (Hamming distance = 1).
    """

    def __init__(self, word_list_or_file: Any):
        """
        Initializes the solver from an iterable of words or a text file path.
        """
        if isinstance(word_list_or_file, str) and os.path.exists(word_list_or_file):
            with open(word_list_or_file, "r", encoding="utf-8") as f:
                self.words: Set[str] = {line.strip().lower() for line in f if line.strip()}
        else:
            self.words = {w.strip().lower() for w in word_list_or_file}

        # Cache of pattern maps keyed by word length
        self._pattern_cache: Dict[int, Dict[str, List[str]]] = {}

    def _get_pattern_map(self, length: int) -> Dict[str, List[str]]:
        """
        Builds or returns a cached wildcard pattern dictionary for words of given length.
        Pattern format: 'c*ld', '*old', 'co*d', 'col*'.
        Complexity to build: O(N * L^2) where N is number of words of length L.
        """
        if length not in self._pattern_cache:
            p_map: Dict[str, List[str]] = collections.defaultdict(list)
            words_of_len = [w for w in self.words if len(w) == length]
            for word in words_of_len:
                for i in range(length):
                    pattern = word[:i] + "*" + word[i + 1:]
                    p_map[pattern].append(word)
            self._pattern_cache[length] = dict(p_map)
        return self._pattern_cache[length]

    def get_neighbors(self, word: str) -> List[str]:
        """Returns all valid dictionary words differing from `word` by exactly 1 letter."""
        L = len(word)
        pattern_map = self._get_pattern_map(L)
        neighbors = set()
        for i in range(L):
            pattern = word[:i] + "*" + word[i + 1:]
            for neighbor in pattern_map.get(pattern, []):
                if neighbor != word:
                    neighbors.add(neighbor)
        return list(neighbors)

    def bfs_shortest_path(self, begin_word: str, end_word: str) -> Dict[str, Any]:
        """
        Standard Unidirectional Breadth-First Search (BFS).
        Guarantees the shortest transformation sequence (minimum ladder length).
        Time Complexity: O(V + E) ~ O(N * L^2)
        Space Complexity: O(N * L) for queue and visited set.
        """
        t0 = time.perf_counter()
        begin = begin_word.lower()
        end = end_word.lower()

        if len(begin) != len(end):
            return {"path": None, "length": 0, "visited_count": 0, "time_ms": 0.0, "status": "Length mismatch"}

        if begin == end:
            return {"path": [begin], "length": 1, "visited_count": 1, "time_ms": 0.0, "status": "Identical words"}

        # Ensure pattern map exists
        L = len(begin)
        pattern_map = self._get_pattern_map(L)

        # BFS queue stores (current_word)
        queue = collections.deque([begin])
        parent: Dict[str, Optional[str]] = {begin: None}
        visited: Set[str] = {begin}
        visited_count = 0
        found = False

        while queue:
            current = queue.popleft()
            visited_count += 1

            if current == end:
                found = True
                break

            # Explore neighbors via intermediate patterns
            for i in range(L):
                pattern = current[:i] + "*" + current[i + 1:]
                for neighbor in pattern_map.get(pattern, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        parent[neighbor] = current
                        queue.append(neighbor)

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        if not found:
            return {"path": None, "length": 0, "visited_count": visited_count, "time_ms": elapsed_ms, "status": "No path exists"}

        # Reconstruct path from parent pointers
        path = []
        curr: Optional[str] = end
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path.reverse()

        return {
            "path": path,
            "length": len(path),
            "visited_count": visited_count,
            "time_ms": elapsed_ms,
            "status": "Success"
        }

    def bidirectional_bfs(self, begin_word: str, end_word: str) -> Dict[str, Any]:
        """
        Optimized Bidirectional Breadth-First Search.
        Expands frontiers from both begin_word and end_word simultaneously,
        always advancing the smaller frontier. Halves the effective search depth d,
        reducing states from O(b^d) to O(2 * b^(d/2)).
        """
        t0 = time.perf_counter()
        begin = begin_word.lower()
        end = end_word.lower()

        if len(begin) != len(end):
            return {"path": None, "length": 0, "visited_count": 0, "time_ms": 0.0, "status": "Length mismatch"}

        if begin == end:
            return {"path": [begin], "length": 1, "visited_count": 1, "time_ms": 0.0, "status": "Identical words"}

        if end not in self.words:
            # Check if end_word is valid
            return {"path": None, "length": 0, "visited_count": 0, "time_ms": 0.0, "status": "Target word not in dictionary"}

        L = len(begin)
        pattern_map = self._get_pattern_map(L)

        # Forward search state
        forward_queue = collections.deque([begin])
        forward_parent: Dict[str, Optional[str]] = {begin: None}
        forward_visited: Set[str] = {begin}

        # Backward search state
        backward_queue = collections.deque([end])
        backward_parent: Dict[str, Optional[str]] = {end: None}
        backward_visited: Set[str] = {end}

        visited_count = 0
        meeting_word: Optional[str] = None

        while forward_queue and backward_queue:
            # Always expand the smaller frontier for minimum state exploration
            if len(forward_queue) <= len(backward_queue):
                # Expand one level forward
                level_size = len(forward_queue)
                for _ in range(level_size):
                    current = forward_queue.popleft()
                    visited_count += 1

                    for i in range(L):
                        pattern = current[:i] + "*" + current[i + 1:]
                        for neighbor in pattern_map.get(pattern, []):
                            if neighbor in backward_visited:
                                # Found intersection!
                                forward_parent[neighbor] = current
                                meeting_word = neighbor
                                break
                            if neighbor not in forward_visited:
                                forward_visited.add(neighbor)
                                forward_parent[neighbor] = current
                                forward_queue.append(neighbor)
                        if meeting_word:
                            break
                    if meeting_word:
                        break
            else:
                # Expand one level backward
                level_size = len(backward_queue)
                for _ in range(level_size):
                    current = backward_queue.popleft()
                    visited_count += 1

                    for i in range(L):
                        pattern = current[:i] + "*" + current[i + 1:]
                        for neighbor in pattern_map.get(pattern, []):
                            if neighbor in forward_visited:
                                # Found intersection!
                                backward_parent[neighbor] = current
                                meeting_word = neighbor
                                break
                            if neighbor not in backward_visited:
                                backward_visited.add(neighbor)
                                backward_parent[neighbor] = current
                                backward_queue.append(neighbor)
                        if meeting_word:
                            break
                    if meeting_word:
                        break

            if meeting_word:
                break

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        if not meeting_word:
            return {"path": None, "length": 0, "visited_count": visited_count, "time_ms": elapsed_ms, "status": "No path exists"}

        # Reconstruct path from forward_parent and backward_parent through meeting_word
        # Forward part: meeting_word -> begin
        f_path = []
        curr = meeting_word
        while curr is not None:
            f_path.append(curr)
            curr = forward_parent[curr]
        f_path.reverse()

        # Backward part: meeting_word's neighbor towards end
        b_path = []
        curr = backward_parent[meeting_word]
        while curr is not None:
            b_path.append(curr)
            curr = backward_parent[curr]

        full_path = f_path + b_path

        return {
            "path": full_path,
            "length": len(full_path),
            "visited_count": visited_count,
            "time_ms": elapsed_ms,
            "meeting_word": meeting_word,
            "status": "Success"
        }

    def dfs_search(self, begin_word: str, end_word: str, max_depth: int = 15) -> Dict[str, Any]:
        """
        Depth-First Search (DFS) for educational comparison.
        Demonstrates that DFS can find valid paths, but DOES NOT guarantee
        the shortest path and often wanders into deep suboptimal branches.
        """
        t0 = time.perf_counter()
        begin = begin_word.lower()
        end = end_word.lower()

        if len(begin) != len(end):
            return {"path": None, "length": 0, "visited_count": 0, "time_ms": 0.0, "status": "Length mismatch"}

        L = len(begin)
        visited_count = 0
        best_path: Optional[List[str]] = None

        def _dfs(current: str, path: List[str], visited: Set[str], depth: int):
            nonlocal visited_count, best_path
            visited_count += 1

            if current == end:
                if best_path is None or len(path) < len(best_path):
                    best_path = list(path)
                return

            if depth >= max_depth:
                return

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    # Prune if already longer than best found path
                    if best_path is not None and len(path) + 1 >= len(best_path):
                        continue
                    visited.add(neighbor)
                    _dfs(neighbor, path + [neighbor], visited, depth + 1)
                    visited.remove(neighbor)

        _dfs(begin, [begin], {begin}, 0)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "path": best_path,
            "length": len(best_path) if best_path else 0,
            "visited_count": visited_count,
            "time_ms": elapsed_ms,
            "status": "Success" if best_path else "Exceeded max depth / No path"
        }


def run_demonstration():
    dict_file = os.path.join(os.path.dirname(__file__), "words.txt")
    solver = WordLadderSolver(dict_file)

    puzzles = [
        ("cold", "warm"),
        ("lead", "gold"),
        ("hit", "cog"),
        ("cat", "dog"),
        ("head", "tail"),
        ("stone", "money"),
        ("wheat", "bread")
    ]

    print("=" * 80)
    print("WORD LADDER SOLVER BENCHMARK & DEMONSTRATION")
    print("=" * 80)
    print(f"Loaded Dictionary: {len(solver.words):,} words from {dict_file}\n")

    print(f"{'Puzzle':<16} | {'Algorithm':<18} | {'Ladder Path':<35} | {'Length':>6} | {'Visited':>8} | {'Time (ms)':>10}")
    print("-" * 102)

    for start, target in puzzles:
        # 1. Unidirectional BFS
        res_bfs = solver.bfs_shortest_path(start, target)
        path_str = " -> ".join(res_bfs["path"]) if res_bfs["path"] else "None"
        if len(path_str) > 35:
            path_str = path_str[:32] + "..."
        print(f"{start + ' -> ' + target:<16} | {'Unidirectional BFS':<18} | {path_str:<35} | {res_bfs['length']:6d} | {res_bfs['visited_count']:8d} | {res_bfs['time_ms']:10.3f}")

        # 2. Bidirectional BFS
        res_bi = solver.bidirectional_bfs(start, target)
        path_str_bi = " -> ".join(res_bi["path"]) if res_bi["path"] else "None"
        if len(path_str_bi) > 35:
            path_str_bi = path_str_bi[:32] + "..."
        print(f"{'':<16} | {'Bidirectional BFS':<18} | {path_str_bi:<35} | {res_bi['length']:6d} | {res_bi['visited_count']:8d} | {res_bi['time_ms']:10.3f}")
        print("-" * 102)

if __name__ == "__main__":
    run_demonstration()
