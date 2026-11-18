import time
import random
import sys
import math
import os

# Set recursion depth for large quicksort
sys.setrecursionlimit(300000)

def insertion_sort(arr):
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def quick_sort(arr):
    """Quicksort with middle pivot to prevent O(n^2) degradation on sorted/reversed data."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def python_sorted(arr):
    return sorted(arr)

def run_lab_benchmarks():
    random.seed(42)
    n_values = [1000, 2500, 5000, 10000, 25000, 50000, 100000]
    
    # Store results: results[distribution][algo][n] = time_ms
    results = {
        'sorted': {'Insertion': {}, 'Merge': {}, 'Quick': {}, 'Python sorted()': {}},
        'reversed': {'Insertion': {}, 'Merge': {}, 'Quick': {}, 'Python sorted()': {}},
        'random': {'Insertion': {}, 'Merge': {}, 'Quick': {}, 'Python sorted()': {}}
    }
    
    # Track constant factor for insertion sort extrapolation if needed
    insertion_rev_c = None
    insertion_rand_c = None

    for n in n_values:
        print(f"\n--- Benchmarking n = {n} ---")
        
        # 1. Sorted Data
        arr_sorted = list(range(n))
        
        # Python sorted()
        t0 = time.perf_counter()
        _ = python_sorted(arr_sorted)
        results['sorted']['Python sorted()'][n] = (time.perf_counter() - t0) * 1000.0
        
        # Quick Sort
        t0 = time.perf_counter()
        _ = quick_sort(arr_sorted)
        results['sorted']['Quick'][n] = (time.perf_counter() - t0) * 1000.0

        # Merge Sort
        t0 = time.perf_counter()
        _ = merge_sort(arr_sorted)
        results['sorted']['Merge'][n] = (time.perf_counter() - t0) * 1000.0

        # Insertion Sort (on sorted data it is O(n), very fast!)
        t0 = time.perf_counter()
        _ = insertion_sort(arr_sorted)
        results['sorted']['Insertion'][n] = (time.perf_counter() - t0) * 1000.0

        print(f"Sorted   n={n:6d}: Py={results['sorted']['Python sorted()'][n]:.3f}ms | Quick={results['sorted']['Quick'][n]:.3f}ms | Merge={results['sorted']['Merge'][n]:.3f}ms | Insert={results['sorted']['Insertion'][n]:.3f}ms")

        # 2. Reversed Data
        arr_rev = list(range(n, 0, -1))
        
        # Python sorted()
        t0 = time.perf_counter()
        _ = python_sorted(arr_rev)
        results['reversed']['Python sorted()'][n] = (time.perf_counter() - t0) * 1000.0

        # Quick Sort
        t0 = time.perf_counter()
        _ = quick_sort(arr_rev)
        results['reversed']['Quick'][n] = (time.perf_counter() - t0) * 1000.0

        # Merge Sort
        t0 = time.perf_counter()
        _ = merge_sort(arr_rev)
        results['reversed']['Merge'][n] = (time.perf_counter() - t0) * 1000.0

        # Insertion Sort on Reversed Data (Worst Case O(n^2))
        if n <= 10000:
            t0 = time.perf_counter()
            _ = insertion_sort(arr_rev)
            dur = (time.perf_counter() - t0) * 1000.0
            results['reversed']['Insertion'][n] = dur
            insertion_rev_c = dur / (n ** 2)
            print(f"Reversed n={n:6d}: Py={results['reversed']['Python sorted()'][n]:.3f}ms | Quick={results['reversed']['Quick'][n]:.3f}ms | Merge={results['reversed']['Merge'][n]:.3f}ms | Insert={dur:.3f}ms")
        else:
            # Extrapolate quadratic time
            extrap_time = insertion_rev_c * (n ** 2)
            results['reversed']['Insertion'][n] = extrap_time
            print(f"Reversed n={n:6d}: Py={results['reversed']['Python sorted()'][n]:.3f}ms | Quick={results['reversed']['Quick'][n]:.3f}ms | Merge={results['reversed']['Merge'][n]:.3f}ms | Insert={extrap_time:.1f}ms (Extrapolated O(n^2))")

        # 3. Random Data (average of 3 trials for stability)
        trials = 3 if n <= 25000 else 2
        py_times, q_times, m_times, ins_times = [], [], [], []
        
        for _ in range(trials):
            arr_rand = [random.randint(0, 10000000) for _ in range(n)]
            
            t0 = time.perf_counter()
            _ = python_sorted(arr_rand)
            py_times.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = quick_sort(arr_rand)
            q_times.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = merge_sort(arr_rand)
            m_times.append((time.perf_counter() - t0) * 1000.0)

            if n <= 10000:
                t0 = time.perf_counter()
                _ = insertion_sort(arr_rand)
                ins_times.append((time.perf_counter() - t0) * 1000.0)

        results['random']['Python sorted()'][n] = sum(py_times) / len(py_times)
        results['random']['Quick'][n] = sum(q_times) / len(q_times)
        results['random']['Merge'][n] = sum(m_times) / len(m_times)

        if n <= 10000:
            dur = sum(ins_times) / len(ins_times)
            results['random']['Insertion'][n] = dur
            insertion_rand_c = dur / (n ** 2)
            print(f"Random   n={n:6d}: Py={results['random']['Python sorted()'][n]:.3f}ms | Quick={results['random']['Quick'][n]:.3f}ms | Merge={results['random']['Merge'][n]:.3f}ms | Insert={dur:.3f}ms")
        else:
            extrap_time = insertion_rand_c * (n ** 2)
            results['random']['Insertion'][n] = extrap_time
            print(f"Random   n={n:6d}: Py={results['random']['Python sorted()'][n]:.3f}ms | Quick={results['random']['Quick'][n]:.3f}ms | Merge={results['random']['Merge'][n]:.3f}ms | Insert={extrap_time:.1f}ms (Extrapolated O(n^2))")

    import json
    with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project2\benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nBenchmark completed and results saved to benchmark_results.json!")

if __name__ == "__main__":
    run_lab_benchmarks()
