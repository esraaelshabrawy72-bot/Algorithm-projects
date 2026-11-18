"""
Word Ladder Benchmark Suite: Evaluating BFS, Bidirectional BFS, and DFS
across 3-letter, 4-letter, and 5-letter word puzzles.
"""

import time
import json
import os
from word_ladder import WordLadderSolver

def run_benchmarks():
    dict_file = os.path.join(os.path.dirname(__file__), "words.txt")
    solver = WordLadderSolver(dict_file)

    benchmark_puzzles = [
        {"start": "cat",   "target": "dog",   "desc": "3-letter classic"},
        {"start": "hit",   "target": "cog",   "desc": "3-letter standard"},
        {"start": "man",   "target": "ape",   "desc": "3-letter evolution"},
        {"start": "cold",  "target": "warm",  "desc": "4-letter temperature"},
        {"start": "lead",  "target": "gold",  "desc": "4-letter alchemy"},
        {"start": "head",  "target": "tail",  "desc": "4-letter anatomy"},
        {"start": "ruby",  "target": "code",  "desc": "4-letter programming"},
        {"start": "game",  "target": "play",  "desc": "4-letter gaming"},
        {"start": "sleep", "target": "dream", "desc": "5-letter cognitive"},
        {"start": "flour", "target": "bread", "desc": "5-letter culinary"},
        {"start": "black", "target": "white", "desc": "5-letter contrast"},
        {"start": "stone", "target": "stare", "desc": "5-letter phonetics"}
    ]

    results = []

    print("=" * 110)
    print("WORD LADDER COMPREHENSIVE BENCHMARK: BFS vs BIDIRECTIONAL BFS vs DFS")
    print("=" * 110)
    print(f"{'Puzzle':<16} | {'Length':>6} | {'BFS Visited':>11} | {'BFS Time':>10} | {'Bi-BFS Visited':>14} | {'Bi-BFS Time':>11} | {'Speedup':>9}")
    print("-" * 110)

    for p in benchmark_puzzles:
        start = p["start"]
        target = p["target"]
        
        # 1. Unidirectional BFS
        t_bfs_list = []
        for _ in range(5):
            res_bfs = solver.bfs_shortest_path(start, target)
            t_bfs_list.append(res_bfs["time_ms"])
        t_bfs_avg = sum(t_bfs_list) / len(t_bfs_list)

        # 2. Bidirectional BFS
        t_bi_list = []
        for _ in range(5):
            res_bi = solver.bidirectional_bfs(start, target)
            t_bi_list.append(res_bi["time_ms"])
        t_bi_avg = sum(t_bi_list) / len(t_bi_list)

        ladder_len = res_bfs["length"]
        speedup = (t_bfs_avg / t_bi_avg) if t_bi_avg > 0 else 1.0
        visited_reduction = (res_bfs["visited_count"] / res_bi["visited_count"]) if res_bi["visited_count"] > 0 else 1.0

        results.append({
            "puzzle": f"{start} -> {target}",
            "desc": p["desc"],
            "word_len": len(start),
            "ladder_length": ladder_len,
            "path_bfs": res_bfs["path"],
            "path_bi": res_bi["path"],
            "bfs_visited": res_bfs["visited_count"],
            "bfs_time_ms": t_bfs_avg,
            "bi_visited": res_bi["visited_count"],
            "bi_time_ms": t_bi_avg,
            "speedup": speedup,
            "visited_reduction": visited_reduction
        })

        puzzle_lbl = f"{start} -> {target}"
        print(f"{puzzle_lbl:<16} | {ladder_len:6d} | {res_bfs['visited_count']:11d} | {t_bfs_avg:8.3f}ms | {res_bi['visited_count']:14d} | {t_bi_avg:9.3f}ms | {speedup:8.1f}x")

    out_json = os.path.join(os.path.dirname(__file__), "benchmark_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("-" * 110)
    print(f"Benchmark results successfully saved to {out_json}!")
    return results

if __name__ == "__main__":
    run_benchmarks()
