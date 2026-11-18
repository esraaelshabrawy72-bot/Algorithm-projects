"""
Empirical Benchmarking of Max-Heap Priority Queue Operations (INSERT & EXTRACT-MAX)
Contrasting Max-Heap vs Unsorted List vs Sorted Array across varying scale n.
"""

import time
import random
import math
import json
import sys

# Unsorted List Priority Queue implementation for baseline comparison
class UnsortedListPQ:
    def __init__(self):
        self.data = []

    def insert(self, priority: int):
        self.data.append(priority)  # O(1)

    def extract_max(self) -> int:
        if not self.data:
            raise IndexError("Empty PQ")
        max_idx = 0
        max_val = self.data[0]
        for i in range(1, len(self.data)):  # O(n)
            if self.data[i] > max_val:
                max_val = self.data[i]
                max_idx = i
        self.data[max_idx] = self.data[-1]
        self.data.pop()
        return max_val

# Sorted List Priority Queue implementation for baseline comparison
class SortedListPQ:
    def __init__(self):
        self.data = []

    def insert(self, priority: int):
        # Bisect insertion O(n)
        import bisect
        bisect.insort(self.data, priority)

    def extract_max(self) -> int:
        if not self.data:
            raise IndexError("Empty PQ")
        return self.data.pop()  # O(1)

# Raw integer MaxHeap for fast throughput testing
class IntMaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, val: int):
        self.heap.append(val)
        idx = len(self.heap) - 1
        while idx > 0:
            p = (idx - 1) // 2
            if self.heap[idx] > self.heap[p]:
                self.heap[idx], self.heap[p] = self.heap[p], self.heap[idx]
                idx = p
            else:
                break

    def extract_max(self) -> int:
        if not self.heap:
            raise IndexError("Empty heap")
        max_v = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            idx = 0
            size = len(self.heap)
            while True:
                left = 2 * idx + 1
                right = 2 * idx + 2
                largest = idx
                if left < size and self.heap[left] > self.heap[largest]:
                    largest = left
                if right < size and self.heap[right] > self.heap[largest]:
                    largest = right
                if largest != idx:
                    self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
                    idx = largest
                else:
                    break
        return max_v

def run_heap_scaling_benchmark():
    random.seed(42)
    n_values = [100, 500, 1000, 5000, 10000, 25000, 50000, 100000]
    num_ops = 5000  # Number of operations measured per size

    print(f"{'Heap Size (n)':>14} | {'Insert (µs)':>12} | {'Extract-Max (µs)':>16} | {'log2(n)':>8}")
    print("-" * 60)

    heap_results = []

    for n in n_values:
        # Pre-fill heap with n elements
        h = IntMaxHeap()
        for _ in range(n):
            h.insert(random.randint(1, 10000000))

        # 1. Benchmark INSERT
        insert_vals = [random.randint(1, 10000000) for _ in range(num_ops)]
        t0 = time.perf_counter()
        for v in insert_vals:
            h.insert(v)
        t_insert_total = time.perf_counter() - t0
        avg_insert_us = (t_insert_total / num_ops) * 1e6

        # 2. Benchmark EXTRACT-MAX
        t0 = time.perf_counter()
        for _ in range(num_ops):
            h.extract_max()
        t_extract_total = time.perf_counter() - t0
        avg_extract_us = (t_extract_total / num_ops) * 1e6

        log_n = math.log2(n)
        heap_results.append({
            "n": n,
            "insert_us": avg_insert_us,
            "extract_us": avg_extract_us,
            "log2_n": log_n
        })

        print(f"{n:14d} | {avg_insert_us:12.3f} | {avg_extract_us:16.3f} | {log_n:8.2f}")

    return heap_results

def run_pq_comparison():
    """Compares Max-Heap vs Unsorted List vs Sorted Array for n = 1,000 to 10,000."""
    print("\n" + "=" * 65)
    print("DATA STRUCTURE COMPARISON: MAX-HEAP vs LIST vs SORTED ARRAY")
    print("=" * 65)
    
    sizes = [1000, 2500, 5000, 7500, 10000]
    ops = 1000
    comp_results = []

    print(f"{'Size (n)':>8} | {'Heap Ins':>9} | {'Heap Ext':>9} | {'Unsort Ins':>10} | {'Unsort Ext':>10} | {'Sort Ins':>9} | {'Sort Ext':>9}")
    print("-" * 75)

    for n in sizes:
        # Pre-fill
        h = IntMaxHeap()
        u = UnsortedListPQ()
        s = SortedListPQ()
        initial_vals = [random.randint(1, 1000000) for _ in range(n)]
        for v in initial_vals:
            h.insert(v)
            u.insert(v)
            s.insert(v)

        test_vals = [random.randint(1, 1000000) for _ in range(ops)]

        # Heap
        t0 = time.perf_counter()
        for v in test_vals:
            h.insert(v)
        t_h_ins = (time.perf_counter() - t0) / ops * 1e6

        t0 = time.perf_counter()
        for _ in range(ops):
            h.extract_max()
        t_h_ext = (time.perf_counter() - t0) / ops * 1e6

        # Unsorted List
        t0 = time.perf_counter()
        for v in test_vals:
            u.insert(v)
        t_u_ins = (time.perf_counter() - t0) / ops * 1e6

        t0 = time.perf_counter()
        for _ in range(ops):
            u.extract_max()
        t_u_ext = (time.perf_counter() - t0) / ops * 1e6

        # Sorted List
        t0 = time.perf_counter()
        for v in test_vals:
            s.insert(v)
        t_s_ins = (time.perf_counter() - t0) / ops * 1e6

        t0 = time.perf_counter()
        for _ in range(ops):
            s.extract_max()
        t_s_ext = (time.perf_counter() - t0) / ops * 1e6

        comp_results.append({
            "n": n,
            "heap_ins": t_h_ins,
            "heap_ext": t_h_ext,
            "unsorted_ins": t_u_ins,
            "unsorted_ext": t_u_ext,
            "sorted_ins": t_s_ins,
            "sorted_ext": t_s_ext
        })

        print(f"{n:8d} | {t_h_ins:8.2f}µ | {t_h_ext:8.2f}µ | {t_u_ins:9.2f}µ | {t_u_ext:9.2f}µ | {t_s_ins:8.2f}µ | {t_s_ext:8.2f}µ")

    with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project3\benchmark_data.json", "w") as f:
        json.dump({"heap_scaling": heap_results, "pq_comparison": comp_results}, f, indent=2)

    return comp_results

if __name__ == "__main__":
    heap_results = run_heap_scaling_benchmark()
    comp_results = run_pq_comparison()
