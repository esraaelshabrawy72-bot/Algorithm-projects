"""
Sorting Benchmark Lab: Empirical Analysis of Sorting Algorithms
Algorithms: Insertion Sort, Merge Sort, Quick Sort, Python sorted() (Timsort)
Input Distributions: Sorted, Reversed, Random
Scale: n = 10^3 to 10^5 (1,000 to 100,000)
Tools: Python 3, time.perf_counter, matplotlib (with built-in SVG fallback)
"""

import time
import random
import sys
import math
import os

# Set a safe recursion limit (standard Python default is 1000; 10000 is safe on Windows)
sys.setrecursionlimit(10000)

# =====================================================================
# 1. Algorithm Implementations
# =====================================================================

def insertion_sort(arr):
    """
    Standard In-Place Insertion Sort.
    Time Complexity: Best O(n), Average O(n^2), Worst O(n^2)
    Space Complexity: O(1) auxiliary
    """
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
    """
    Standard Divide-and-Conquer 2-Way Merge Sort.
    Time Complexity: Best/Average/Worst O(n log n)
    Space Complexity: O(n) auxiliary
    """
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    merged = []
    i = j = 0
    len_left = len(left)
    len_right = len(right)
    while i < len_left and j < len_right:
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
    """
    Quick Sort with Middle-Element Pivot.
    Choosing the middle element guarantees O(n log n) recursion tree balance
    on pre-sorted and reverse-sorted data, preventing O(n^2) depth collapse.
    Time Complexity: Expected O(n log n), Worst O(n^2)
    Space Complexity: O(n) auxiliary
    """
    if len(arr) <= 1:
        return list(arr)
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def python_sorted(arr):
    """
    Python's built-in sorted() implementing Timsort in native C.
    Time Complexity: Best O(n) (adaptive run detection), Average/Worst O(n log n)
    Space Complexity: O(n)
    """
    return sorted(arr)

# =====================================================================
# 2. Correctness Verification
# =====================================================================

def verify_correctness():
    """Validates that all implementations correctly sort edge cases and random arrays."""
    test_cases = [
        [],
        [1],
        [2, 1],
        [5, 5, 5, 5],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [42, 17, 88, 3, 25, 99, 14, 25, 0, -5],
        [random.randint(-1000, 1000) for _ in range(100)]
    ]
    for case in test_cases:
        expected = sorted(case)
        assert insertion_sort(case) == expected, f"Insertion sort failed on {case}"
        assert merge_sort(case) == expected, f"Merge sort failed on {case}"
        assert quick_sort(case) == expected, f"Quick sort failed on {case}"
        assert python_sorted(case) == expected, f"Python sorted() failed on {case}"
    print("[PASS] All sorting algorithms passed correctness verification across edge cases!")

# =====================================================================
# 3. Comprehensive Benchmark Harness (n = 10^3 to 10^5)
# =====================================================================

def run_benchmark():
    """
    Runs the benchmark across n = 10^3 to 10^5 for Sorted, Reversed, and Random data.
    Gracefully handles O(n^2) Insertion Sort on n > 10,000 to prevent program freeze.
    """
    random.seed(42)
    n_values = [1000, 2500, 5000, 10000, 25000, 50000, 100000]
    
    results = {
        'sorted': {'Insertion Sort': {}, 'Merge Sort': {}, 'Quick Sort': {}, 'Python sorted()': {}},
        'reversed': {'Insertion Sort': {}, 'Merge Sort': {}, 'Quick Sort': {}, 'Python sorted()': {}},
        'random': {'Insertion Sort': {}, 'Merge Sort': {}, 'Quick Sort': {}, 'Python sorted()': {}}
    }
    
    ins_rev_coeff = None
    ins_rand_coeff = None

    print("\n" + "=" * 80)
    print("STARTING SORTING BENCHMARK LAB (n = 10^3 to 10^5)")
    print("=" * 80)

    for n in n_values:
        print(f"\n>>> Benchmarking size n = {n:,} elements...")

        # ----------------- 1. Sorted Data -----------------
        arr_sorted = list(range(n))
        
        t0 = time.perf_counter()
        _ = python_sorted(arr_sorted)
        results['sorted']['Python sorted()'][n] = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        _ = quick_sort(arr_sorted)
        results['sorted']['Quick Sort'][n] = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        _ = merge_sort(arr_sorted)
        results['sorted']['Merge Sort'][n] = (time.perf_counter() - t0) * 1000.0

        # Insertion Sort on sorted data is O(n) (only n-1 comparisons, 0 shifts)
        t0 = time.perf_counter()
        _ = insertion_sort(arr_sorted)
        results['sorted']['Insertion Sort'][n] = (time.perf_counter() - t0) * 1000.0

        print(f"  [Sorted]   Py: {results['sorted']['Python sorted()'][n]:8.3f} ms | "
              f"Quick: {results['sorted']['Quick Sort'][n]:8.3f} ms | "
              f"Merge: {results['sorted']['Merge Sort'][n]:8.3f} ms | "
              f"Insert: {results['sorted']['Insertion Sort'][n]:8.3f} ms")

        # ----------------- 2. Reversed Data -----------------
        arr_rev = list(range(n, 0, -1))
        
        t0 = time.perf_counter()
        _ = python_sorted(arr_rev)
        results['reversed']['Python sorted()'][n] = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        _ = quick_sort(arr_rev)
        results['reversed']['Quick Sort'][n] = (time.perf_counter() - t0) * 1000.0

        t0 = time.perf_counter()
        _ = merge_sort(arr_rev)
        results['reversed']['Merge Sort'][n] = (time.perf_counter() - t0) * 1000.0

        # Insertion sort on reversed data is worst-case O(n^2)
        if n <= 10000:
            t0 = time.perf_counter()
            _ = insertion_sort(arr_rev)
            t_ms = (time.perf_counter() - t0) * 1000.0
            results['reversed']['Insertion Sort'][n] = t_ms
            ins_rev_coeff = t_ms / (n ** 2)
            insert_str = f"{t_ms:8.3f} ms"
        else:
            extrap_ms = ins_rev_coeff * (n ** 2)
            results['reversed']['Insertion Sort'][n] = extrap_ms
            insert_str = f"{extrap_ms/1000.0:6.1f} s (O(n^2) est)"

        print(f"  [Reversed] Py: {results['reversed']['Python sorted()'][n]:8.3f} ms | "
              f"Quick: {results['reversed']['Quick Sort'][n]:8.3f} ms | "
              f"Merge: {results['reversed']['Merge Sort'][n]:8.3f} ms | "
              f"Insert: {insert_str}")

        # ----------------- 3. Random Data -----------------
        trials = 3 if n <= 25000 else 2
        py_t, q_t, m_t, ins_t = [], [], [], []
        
        for _ in range(trials):
            arr_rand = [random.randint(0, 10000000) for _ in range(n)]
            
            t0 = time.perf_counter()
            _ = python_sorted(arr_rand)
            py_t.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = quick_sort(arr_rand)
            q_t.append((time.perf_counter() - t0) * 1000.0)

            t0 = time.perf_counter()
            _ = merge_sort(arr_rand)
            m_t.append((time.perf_counter() - t0) * 1000.0)

            if n <= 10000:
                t0 = time.perf_counter()
                _ = insertion_sort(arr_rand)
                ins_t.append((time.perf_counter() - t0) * 1000.0)

        results['random']['Python sorted()'][n] = sum(py_t) / len(py_t)
        results['random']['Quick Sort'][n] = sum(q_t) / len(q_t)
        results['random']['Merge Sort'][n] = sum(m_t) / len(m_t)

        if n <= 10000:
            avg_ins = sum(ins_t) / len(ins_t)
            results['random']['Insertion Sort'][n] = avg_ins
            ins_rand_coeff = avg_ins / (n ** 2)
            insert_str = f"{avg_ins:8.3f} ms"
        else:
            extrap_ms = ins_rand_coeff * (n ** 2)
            results['random']['Insertion Sort'][n] = extrap_ms
            insert_str = f"{extrap_ms/1000.0:6.1f} s (O(n^2) est)"

        print(f"  [Random]   Py: {results['random']['Python sorted()'][n]:8.3f} ms | "
              f"Quick: {results['random']['Quick Sort'][n]:8.3f} ms | "
              f"Merge: {results['random']['Merge Sort'][n]:8.3f} ms | "
              f"Insert: {insert_str}")

    print("\n" + "=" * 80)
    print("BENCHMARK COMPLETED SUCCESSFULLY")
    print("=" * 80)
    return results

# =====================================================================
# 4. Visualization Generator (Matplotlib with robust SVG Fallback)
# =====================================================================

def plot_benchmark_results(results, output_dir="."):
    """
    Attempts to plot using matplotlib. If matplotlib is not available,
    generates pristine standalone vector SVG files so the user never encounters errors.
    """
    algos = ['Python sorted()', 'Quick Sort', 'Merge Sort', 'Insertion Sort']
    colors = {
        'Python sorted()': '#16a34a',
        'Quick Sort': '#2563eb',
        'Merge Sort': '#9333ea',
        'Insertion Sort': '#dc2626'
    }

    # Dynamically check for Matplotlib to avoid IDE / Pylance "missing import" errors
    plt = None
    try:
        import importlib
        plt = importlib.import_module("matplotlib.pyplot")
    except (ImportError, ModuleNotFoundError):
        plt = None

    if plt is not None:
        print("\n[INFO] Matplotlib found. Generating PNG benchmark figures...")

        for dist in ['random', 'sorted', 'reversed']:
            plt.figure(figsize=(9, 6))
            for algo in algos:
                n_vals = sorted([int(k) for k in results[dist][algo].keys()])
                times = [results[dist][algo][k] for k in n_vals]
                plt.plot(n_vals, times, marker='o', label=algo, color=colors[algo], linewidth=2.5)

            plt.xscale('log')
            plt.yscale('log')
            plt.title(f"Sorting Benchmark Lab: {dist.capitalize()} Data (n = 10³ to 10⁵)", fontsize=14, fontweight='bold')
            plt.xlabel("Array Size (n) [Log Scale]", fontsize=12)
            plt.ylabel("Running Time (ms) [Log Scale]", fontsize=12)
            plt.grid(True, which="both", ls="--", alpha=0.5)
            plt.legend(fontsize=11)
            plt.tight_layout()
            png_path = os.path.join(output_dir, f"{dist}_benchmark.png")
            plt.savefig(png_path, dpi=300)
            plt.close()
            print(f"  -> Saved: {png_path}")

        print("[SUCCESS] Matplotlib PNG figures generated successfully!")
        return

    print("\n[NOTE] Matplotlib is not installed. Using built-in SVG generator to produce publication-grade charts...")

    # Fallback to high-quality SVG generation
    for dist in ['random', 'sorted', 'reversed']:
        svg_filename = os.path.join(output_dir, f"{dist}_benchmark.svg")
        _generate_svg_chart(results, dist, algos, colors, svg_filename)
        print(f"  -> Saved Vector SVG: {svg_filename}")
    print("[SUCCESS] All vector SVG benchmark figures generated successfully with 0 errors!")

def _generate_svg_chart(results, dist, algos, colors, output_path):
    """Internal helper to write clean Log-Log SVG charts without dependencies."""
    width, height = 880, 540
    pad_l, pad_r, pad_t, pad_b = 95, 50, 75, 65
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    min_x, max_x = 1000.0, 100000.0
    min_y = 0.001 if dist == 'sorted' else 0.01
    max_y = 500.0 if dist == 'sorted' else 300000.0

    l_min_x, l_max_x = math.log10(min_x), math.log10(max_x)
    l_min_y, l_max_y = math.log10(min_y), math.log10(max_y)

    def to_coords(x, y):
        y = max(y, min_y)
        cx = pad_l + ((math.log10(x) - l_min_x) / (l_max_x - l_min_x)) * plot_w
        cy = pad_t + plot_h - ((math.log10(y) - l_min_y) / (l_max_y - l_min_y)) * plot_h
        return cx, cy

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:sans-serif;">')
    svg.append(f'<text x="{pad_l}" y="32" font-size="18" font-weight="700" fill="#0f172a">Sorting Benchmark Lab: {dist.capitalize()} Data (n = 10³ to 10⁵)</text>')
    svg.append(f'<text x="{pad_l}" y="52" font-size="12.5" fill="#64748b">Log-Log Scale: Comparing empirical scaling of Python sorted(), Quick Sort, Merge Sort, and Insertion Sort</text>')

    # Y-Ticks
    y_decades = range(int(math.floor(l_min_y)), int(math.ceil(l_max_y)) + 1)
    for dec in y_decades:
        val = 10 ** dec
        if min_y <= val <= max_y:
            _, cy = to_coords(min_x, val)
            svg.append(f'<line x1="{pad_l}" y1="{cy:.1f}" x2="{pad_l + plot_w}" y2="{cy:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
            lbl = f"10^{dec} ms" if dec not in [-2, -1, 0, 1, 2, 3] else {-2:"0.01 ms", -1:"0.1 ms", 0:"1 ms", 1:"10 ms", 2:"100 ms", 3:"1 s"}[dec]
            svg.append(f'<text x="{pad_l - 12}" y="{cy + 4:.1f}" font-size="10.5" fill="#64748b" text-anchor="end">{lbl}</text>')

    # X-Ticks
    for x_val in [1000, 2500, 5000, 10000, 25000, 50000, 100000]:
        cx, _ = to_coords(x_val, min_y)
        svg.append(f'<line x1="{cx:.1f}" y1="{pad_t}" x2="{cx:.1f}" y2="{pad_t + plot_h}" stroke="#f1f5f9" stroke-width="1"/>')
        svg.append(f'<line x1="{cx:.1f}" y1="{pad_t + plot_h}" x2="{cx:.1f}" y2="{pad_t + plot_h + 6}" stroke="#94a3b8" stroke-width="1"/>')
        lbl = {1000:"10³", 10000:"10⁴", 100000:"10⁵"}.get(x_val, f"{x_val//1000}K")
        svg.append(f'<text x="{cx:.1f}" y="{pad_t + plot_h + 20}" font-size="11" fill="#64748b" text-anchor="middle">{lbl}</text>')

    # Axis Lines
    ox, oy = to_coords(min_x, min_y)
    ex, _ = to_coords(max_x, min_y)
    _, ty = to_coords(min_x, max_y)
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ex}" y2="{oy}" stroke="#475569" stroke-width="1.5"/>')
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{ty}" stroke="#475569" stroke-width="1.5"/>')
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{height - 15}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle">Array Size (n) [Log Scale]</text>')
    svg.append(f'<text x="22" y="{pad_t + plot_h/2}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle" transform="rotate(-90 22 {pad_t + plot_h/2})">Running Time (ms) [Log Scale]</text>')

    # Plot Lines & Points
    for algo in algos:
        c = colors[algo]
        n_vals = sorted([int(k) for k in results[dist][algo].keys()])
        pts = [(n, results[dist][algo][n]) for n in n_vals]
        path = " ".join([f"{'M' if i==0 else 'L'} {to_coords(px, py)[0]:.1f} {to_coords(px, py)[1]:.1f}" for i, (px, py) in enumerate(pts)])
        svg.append(f'<path d="{path}" fill="none" stroke="{c}" stroke-width="2.5" stroke-linejoin="round"/>')
        for px, py in pts:
            cx, cy = to_coords(px, py)
            svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{c}" stroke="#ffffff" stroke-width="1.5"><title>{algo}: n={px}, {py:.2f}ms</title></circle>')

    # Legend
    svg.append(f'<rect x="{pad_l + 18}" y="{pad_t + 14}" width="250" height="{len(algos)*22 + 14}" rx="6" fill="#ffffff" fill-opacity="0.95" stroke="#cbd5e1" stroke-width="1"/>')
    for i, algo in enumerate(algos):
        ly = pad_t + 30 + i * 22
        svg.append(f'<line x1="{pad_l + 30}" y1="{ly}" x2="{pad_l + 54}" y2="{ly}" stroke="{colors[algo]}" stroke-width="2.5"/>')
        svg.append(f'<circle cx="{pad_l + 42}" cy="{ly}" r="3.5" fill="{colors[algo]}" stroke="#ffffff" stroke-width="1"/>')
        svg.append(f'<text x="{pad_l + 62}" y="{ly + 4}" font-size="11.5" font-weight="500" fill="#1e293b">{algo}</text>')

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))

# =====================================================================
# Main Execution Entrypoint
# =====================================================================

if __name__ == "__main__":
    # 1. Correctness Checks
    verify_correctness()

    # 2. Run Benchmarks
    benchmark_data = run_benchmark()

    # 3. Generate Visualizations (Matplotlib if installed, else Vector SVG)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    plot_benchmark_results(benchmark_data, output_dir=script_dir)
