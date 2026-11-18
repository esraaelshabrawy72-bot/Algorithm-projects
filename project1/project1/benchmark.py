import time
import random
import math
import os

def insertion_sort(arr):
    """
    Standard Insertion Sort with comparisons and shifts counter.
    Returns: (sorted_array, comparisons, shifts)
    """
    a = list(arr)
    comparisons = 0
    shifts = 0
    n = len(a)
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comparisons, shifts

def merge_sort(arr):
    """
    Standard 2-way Merge Sort with comparison counter.
    Returns: (sorted_array, comparisons)
    """
    comparisons = 0
    def _merge_sort(a):
        nonlocal comparisons
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = _merge_sort(a[:mid])
        right = _merge_sort(a[mid:])
        
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    sorted_arr = _merge_sort(arr)
    return sorted_arr, comparisons

def run_benchmarks():
    n_values = [100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    random.seed(42)
    trials_random = 5
    
    results = []

    print(f"{'n':>6} | {'Case':<14} | {'Time (ms)':>10} | {'Comparisons':>12} | {'Shifts':>12} | {'MergeTime(ms)':>14}")
    print("-" * 75)

    for n in n_values:
        # 1. Sorted
        sorted_input = list(range(n))
        t0 = time.perf_counter()
        _, comps_sorted, shifts_sorted = insertion_sort(sorted_input)
        time_sorted_ms = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        _, comps_merge_sorted = merge_sort(sorted_input)
        time_merge_sorted_ms = (time.perf_counter() - t0) * 1000.0

        # 2. Reverse-Sorted
        rev_input = list(range(n, 0, -1))
        t0 = time.perf_counter()
        _, comps_rev, shifts_rev = insertion_sort(rev_input)
        time_rev_ms = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        _, comps_merge_rev = merge_sort(rev_input)
        time_merge_rev_ms = (time.perf_counter() - t0) * 1000.0

        # 3. Random (averaged over trials)
        rand_times = []
        rand_comps = []
        rand_shifts = []
        rand_merge_times = []
        for _ in range(trials_random):
            rand_input = [random.randint(1, 1000000) for _ in range(n)]
            
            t0 = time.perf_counter()
            _, c, s = insertion_sort(rand_input)
            rand_times.append((time.perf_counter() - t0) * 1000.0)
            rand_comps.append(c)
            rand_shifts.append(s)

            t0 = time.perf_counter()
            _, _ = merge_sort(rand_input)
            rand_merge_times.append((time.perf_counter() - t0) * 1000.0)

        time_rand_ms = sum(rand_times) / len(rand_times)
        comps_rand = sum(rand_comps) / len(rand_comps)
        shifts_rand = sum(rand_shifts) / len(rand_shifts)
        time_merge_rand_ms = sum(rand_merge_times) / len(rand_merge_times)

        results.append({
            'n': n,
            'sorted': {'time_ms': time_sorted_ms, 'comps': comps_sorted, 'shifts': shifts_sorted, 'merge_time_ms': time_merge_sorted_ms},
            'reverse': {'time_ms': time_rev_ms, 'comps': comps_rev, 'shifts': shifts_rev, 'merge_time_ms': time_merge_rev_ms},
            'random': {'time_ms': time_rand_ms, 'comps': comps_rand, 'shifts': shifts_rand, 'merge_time_ms': time_merge_rand_ms}
        })

        print(f"{n:6d} | {'Sorted':<14} | {time_sorted_ms:10.3f} | {comps_sorted:12d} | {shifts_sorted:12d} | {time_merge_sorted_ms:14.3f}")
        print(f"{n:6d} | {'Reverse':<14} | {time_rev_ms:10.3f} | {comps_rev:12d} | {shifts_rev:12d} | {time_merge_rev_ms:14.3f}")
        print(f"{n:6d} | {'Random (avg)':<14} | {time_rand_ms:10.3f} | {int(comps_rand):12d} | {int(shifts_rand):12d} | {time_merge_rand_ms:14.3f}")
        print("-" * 75)

    return results

if __name__ == '__main__':
    run_benchmarks()
