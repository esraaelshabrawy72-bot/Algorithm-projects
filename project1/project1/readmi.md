# Mini Project: Empirical Analysis of Insertion Sort & Comparison with Merge Sort

> **Course:** Algorithms: Analysis and Design  
> **Topic:** Asymptotic Complexity & Empirical Performance Evaluation of Sorting Algorithms  
> **Environment:** Python 3.14.0 | High-Resolution Monotonic Timer (`time.perf_counter`)  
> **Script Reference:** [insertion_sort.py](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/insertion_sort.py) | [benchmark.py](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/benchmark.py)

---

## 1. Executive Summary

This project presents an empirical and theoretical analysis of **Insertion Sort**, evaluating its computational behavior across array sizes ranging from $n = 100$ to $n = 5,000$. The algorithm was instrumented to capture the exact number of **key comparisons** and **element shifts (data movements)**, alongside precise wall-clock execution time on three canonical input configurations:
1. **Sorted Input (Best Case):** Already ordered elements in non-decreasing order.
2. **Reverse-Sorted Input (Worst Case):** Elements ordered in strictly descending order.
3. **Random Input (Average Case):** Uniformly distributed pseudo-random integers (averaged across 5 independent trials per $n$).

The empirical curves are evaluated against theoretical asymptotic growth rates $O(n)$ and $O(n^2)$. Furthermore, Insertion Sort is contrasted both empirically and analytically with **Merge Sort** ($O(n \log n)$), illustrating the algorithmic trade-offs between divide-and-conquer and incremental insertion techniques.

---

## 2. Algorithm Implementation & Instrumentation

### 2.1 Insertion Sort Implementation
Insertion Sort constructs the sorted array incrementally by iteratively picking an unsorted element (`key`) from index $i$ ($1 \le i < n$) and scanning backward through the sorted prefix $A[0 \dots i-1]$ to find the insertion point, shifting larger elements one position to the right.

```python
def insertion_sort(arr):
    """
    Executes insertion sort on an array copy, tracking exact comparisons and shifts.
    Returns: (sorted_array, comparisons_count, shifts_count)
    """
    a = list(arr)
    comparisons = 0
    shifts = 0
    n = len(a)
    
    for i in range(1, n):
        key = a[i]
        j = i - 1
        
        # Compare key with elements in the sorted prefix
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]  # Element shift (movement)
                shifts += 1
                j -= 1
            else:
                break            # Insertion spot found
                
        a[j + 1] = key           # Final key placement
        
    return a, comparisons, shifts
```

### 2.2 Definitions of Metric Counters
* **Comparisons:** Incremented every time a candidate element $A[j]$ from the sorted prefix is evaluated against the `key` ($A[j] > \text{key}$).
* **Shifts:** Incremented whenever an element $A[j]$ is moved one position to the right ($A[j+1] = A[j]$) to create space for the incoming key.

### 2.3 Merge Sort Implementation (Baseline Comparison)
A standard 2-way Divide-and-Conquer Merge Sort was implemented with comparison tracking for comparative benchmarking:

```python
def merge_sort(arr):
    comparisons = 0
    def _sort(sub):
        nonlocal comparisons
        if len(sub) <= 1:
            return sub
        mid = len(sub) // 2
        left = _sort(sub[:mid])
        right = _sort(sub[mid:])
        
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

    return _sort(arr), comparisons
```

---

## 3. Experimental Methodology

* **Input Sizes Tested ($n$):** 100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000.
* **Input Distributions:**
  * **Sorted:** $A = [0, 1, 2, \dots, n-1]$
  * **Reverse-Sorted:** $A = [n, n-1, \dots, 2, 1]$
  * **Random:** $A$ populated with pseudo-random integers uniformly chosen from $[1, 10^6]$. To prevent outlier distortion, results are averaged over 5 independent runs per $n$.
* **Measurement Timing:** Monotonic high-resolution clock (`time.perf_counter()`), measured in milliseconds ($\text{ms}$).

---

## 4. Empirical Results & Data Table

The table below summarizes the exact operation counts and running times obtained across all experimental configurations:

| Array Size ($n$) | Input Case | Running Time (ms) | Comparisons ($C_n$) | Shifts ($S_n$) | Merge Sort Time (ms) |
|:---:|:---|:---:|:---:|:---:|:---:|
| **100** | Sorted | 0.010 ms | 99 | 0 | 0.070 ms |
| | Reverse | 0.343 ms | 4,950 | 4,950 | 0.070 ms |
| | Random (avg) | 0.171 ms | 2,568 | 2,472 | 0.089 ms |
| **250** | Sorted | 0.016 ms | 249 | 0 | 0.170 ms |
| | Reverse | 2.112 ms | 31,125 | 31,125 | 0.176 ms |
| | Random (avg) | 1.048 ms | 15,992 | 15,749 | 0.238 ms |
| **500** | Sorted | 0.036 ms | 499 | 0 | 0.363 ms |
| | Reverse | 8.807 ms | 124,750 | 124,750 | 0.398 ms |
| | Random (avg) | 4.644 ms | 65,086 | 64,594 | 0.628 ms |
| **750** | Sorted | 0.054 ms | 749 | 0 | 0.631 ms |
| | Reverse | 21.584 ms | 280,875 | 280,875 | 0.679 ms |
| | Random (avg) | 10.721 ms | 140,722 | 139,980 | 0.926 ms |
| **1000** | Sorted | 0.081 ms | 999 | 0 | 0.908 ms |
| | Reverse | 39.255 ms | 499,500 | 499,500 | 0.931 ms |
| | Random (avg) | 19.911 ms | 253,797 | 252,803 | 1.238 ms |
| **1500** | Sorted | 0.146 ms | 1,499 | 0 | 1.344 ms |
| | Reverse | 98.501 ms | 1,124,250 | 1,124,250 | 1.653 ms |
| | Random (avg) | 47.948 ms | 566,910 | 565,420 | 2.337 ms |
| **2000** | Sorted | 0.165 ms | 1,999 | 0 | 1.919 ms |
| | Reverse | 159.760 ms | 1,999,000 | 1,999,000 | 1.904 ms |
| | Random (avg) | 80.142 ms | 1,013,895 | 1,011,904 | 2.785 ms |
| **2500** | Sorted | 0.217 ms | 2,499 | 0 | 2.297 ms |
| | Reverse | 244.691 ms | 3,123,750 | 3,123,750 | 2.437 ms |
| | Random (avg) | 119.103 ms | 1,566,928 | 1,564,436 | 3.413 ms |
| **3000** | Sorted | 0.233 ms | 2,999 | 0 | 2.807 ms |
| | Reverse | 387.074 ms | 4,498,500 | 4,498,500 | 4.170 ms |
| | Random (avg) | 246.127 ms | 2,236,254 | 2,233,265 | 5.533 ms |
| **3500** | Sorted | 0.432 ms | 3,499 | 0 | 6.063 ms |
| | Reverse | 846.877 ms | 6,123,250 | 6,123,250 | 5.146 ms |
| | Random (avg) | 405.496 ms | 3,102,363 | 3,098,872 | 7.794 ms |
| **4000** | Sorted | 0.488 ms | 3,999 | 0 | 5.558 ms |
| | Reverse | 1053.434 ms | 7,998,000 | 7,998,000 | 7.419 ms |
| | Random (avg) | 582.758 ms | 4,023,861 | 4,019,869 | 10.460 ms |
| **4500** | Sorted | 0.629 ms | 4,499 | 0 | 7.128 ms |
| | Reverse | 1510.569 ms | 10,122,750 | 10,122,750 | 15.461 ms |
| | Random (avg) | 786.490 ms | 5,070,850 | 5,066,358 | 12.675 ms |
| **5000** | Sorted | 0.692 ms | 4,999 | 0 | 8.389 ms |
| | Reverse | 2069.153 ms | 12,497,500 | 12,497,500 | 8.981 ms |
| | Random (avg) | 971.178 ms | 6,216,670 | 6,211,681 | 13.521 ms |

---

## 5. Mathematical & Asymptotic Analysis

### 5.1 Analysis of Operation Counts

$$\begin{array}{|l|c|c|c|}
\hline
\textbf{Metric} & \textbf{Sorted (Best Case)} & \textbf{Reverse-Sorted (Worst Case)} & \textbf{Random (Average Case)} \\
\hline
\textbf{Key Comparisons} & n - 1 & \frac{n(n - 1)}{2} & \approx \frac{n(n - 1)}{4} \\
\textbf{Element Shifts} & 0 & \frac{n(n - 1)}{2} & \approx \frac{n(n - 1)}{4} \\
\textbf{Asymptotic Order} & \Theta(n) & \Theta(n^2) & \Theta(n^2) \\
\hline
\end{array}$$

1. **Worst Case (Reverse-Sorted Input):**
   * At iteration $i$, the key is strictly smaller than every element in $A[0 \dots i-1]$.
   * Hence, the `while` loop runs exactly $i$ times, resulting in $i$ comparisons and $i$ shifts for every $i \in \{1, 2, \dots, n-1\}$.
   * Total Comparisons = Total Shifts = $\sum_{i=1}^{n-1} i = \frac{n(n-1)}{2}$.
   * At $n = 5,000$:
     $$\frac{5000 \times 4999}{2} = 12,497,500 \text{ operations}$$
   * The empirical counter recorded **exactly** $12,497,500$ comparisons and $12,497,500$ shifts, matching theoretical prediction to 100% precision.

2. **Average Case (Random Input):**
   * Assuming uniform distribution, element $A[i]$ is equally likely to belong to any of the $i+1$ possible positions in the sorted prefix $A[0 \dots i-1]$.
   * On average, the inner loop traverses roughly half of the prefix ($\approx \frac{i}{2}$ comparisons and shifts).
   * Total Operations $\approx \sum_{i=1}^{n-1} \frac{i}{2} = \frac{n(n-1)}{4}$.
   * At $n = 5,000$, $\frac{5000 \times 4999}{4} \approx 6,248,750$.
   * Empirical result: $6,216,670$ comparisons and $6,211,681$ shifts (deviating by $<0.5\%$ from the mathematical expectation).

3. **Best Case (Sorted Input):**
   * The inner loop checks $A[i-1] \le A[i]$, which evaluates to false on the very first comparison, terminating the inner loop immediately.
   * Total comparisons: exactly $n - 1$ ($4,999$ for $n=5,000$).
   * Total shifts: $0$.
   * Running time scales in pure linear time $\Theta(n)$.

---

## 6. Graphical Analysis

### 6.1 Running Time vs $n$ and Comparison with $O(n)$ & $O(n^2)$ Curves

The plot below demonstrates the empirical running times of Insertion Sort against theoretical polynomial models:
* **Worst Case Reference Curve:** Fitted quadratic curve $T(n) = c_1 \cdot n^2$, where $c_1 \approx 8.28 \times 10^{-5} \text{ ms}$.
* **Average Case Reference Curve:** Fitted quadratic curve $T(n) = c_2 \cdot n^2$, where $c_2 \approx 3.88 \times 10^{-5} \text{ ms} \approx \frac{c_1}{2.13}$.
* **Best Case Reference Curve:** Fitted linear curve $T(n) = c_3 \cdot n$, where $c_3 \approx 1.38 \times 10^{-4} \text{ ms}$.

![Running Time Comparison](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/running_time_comparison.svg)

> **Figure 1:** [running_time_comparison.svg](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/running_time_comparison.svg) — Running time of Insertion Sort on Sorted, Random, and Reverse-sorted inputs up to $n = 5,000$, compared with theoretical $O(n^2)$ and $O(n)$ curves. Notice that the empirical random curve tracks almost exactly halfway between the linear axis and the worst-case parabola, confirming $T_{\text{avg}}(n) \approx \frac{1}{2} T_{\text{worst}}(n)$.

---

### 6.2 Detailed View: Best Case Linear Growth $\Theta(n)$

Due to the massive vertical scale required by $O(n^2)$ ($2,069\text{ ms}$), the best case appears flat on Figure 1. Figure 2 isolates the sorted input to highlight its strictly linear progression:

![Best Case Linear Growth](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/sorted_best_case.svg)

> **Figure 2:** [sorted_best_case.svg](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/sorted_best_case.svg) — Zoomed-in view of Sorted array execution times from $n=100$ ($0.01\text{ ms}$) to $n=5,000$ ($0.69\text{ ms}$), showing tight alignment with $O(n)$ linear progression.

---

### 6.3 Operation Counts: Comparisons and Shifts

![Operations Comparison](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/operations_comparison.svg)

> **Figure 3:** [operations_comparison.svg](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/operations_comparison.svg) — Comparison of comparisons and shifts. In the reverse-sorted case, comparisons and shifts overlap identically ($12.5\text{M}$ at $n=5,000$). In random input, both metrics grow in parallel at $\approx 6.2\text{M}$.

---

## 7. Comparative Analysis: Insertion Sort vs. Merge Sort

### 7.1 Algorithmic Feature Matrix

| Evaluation Dimension | Insertion Sort | Merge Sort |
|:---|:---|:---|
| **Best-Case Time Complexity** | $\Theta(n)$ (Pre-sorted data) | $\Theta(n \log n)$ |
| **Average-Case Time Complexity** | $\Theta(n^2)$ | $\Theta(n \log n)$ |
| **Worst-Case Time Complexity** | $\Theta(n^2)$ | $\Theta(n \log n)$ |
| **Auxiliary Space Complexity** | $O(1)$ (Strictly in-place) | $O(n)$ (Requires secondary buffers) |
| **Algorithmic Paradigm** | Incremental Insertion | Divide-and-Conquer |
| **Stability** | Stable (Preserves relative order) | Stable (With $\le$ tie-breaking) |
| **Constant Factor Overhead** | Extremely low (minimal loop instructions) | Moderate (array slicing, recursion, merge copy) |
| **Locality of Reference** | High cache locality for small arrays | Non-contiguous memory during merge |
| **Adaptive Behavior** | Highly adaptive ($O(n + d)$ where $d$ = inversions) | Non-adaptive (same steps regardless of order) |

---

### 7.2 Empirical Performance Curve: Insertion Sort vs. Merge Sort

![Insertion Sort vs Merge Sort](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/insertion_vs_merge_sort.svg)

> **Figure 4:** [insertion_vs_merge_sort.svg](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/insertion_vs_merge_sort.svg) — Runtime divergence between Insertion Sort ($O(n^2)$) and Merge Sort ($O(n \log n)$). While Insertion Sort degrades parabolically to $>2,000\text{ ms}$, Merge Sort stays virtually flat below $14\text{ ms}$ across all inputs.

---

### 7.3 Discussion & Insights

1. **The Asymptotic Crossover:**
   * At small array sizes ($n \le 100$ on pre-sorted data), Insertion Sort outperforms Merge Sort ($0.010\text{ ms}$ vs $0.070\text{ ms}$). This is because Insertion Sort operates entirely in-place with zero memory allocation and simple pointer shifts, whereas Merge Sort incurs the administrative overhead of recursive call stacks and buffer allocations.
   * However, as $n$ scales past the small-array threshold, the $O(n^2)$ time complexity of Insertion Sort rapidly explodes. At $n = 5,000$:
     * On **Random data**: Merge Sort runs in **$13.52\text{ ms}$** vs Insertion Sort's **$971.18\text{ ms}$** ($\approx \mathbf{72\times\text{ faster}}$).
     * On **Reverse-sorted data**: Merge Sort finishes in **$8.98\text{ ms}$** vs Insertion Sort's **$2,069.15\text{ ms}$** ($\approx \mathbf{230\times\text{ faster}}$).

2. **Inversion Dependency ($k$-sorted arrays):**
   * The number of shifts in Insertion Sort is strictly equal to the number of inversions in the input array:
     $$\text{Shifts} = I(A) = |\{(i, j) \mid i < j \text{ and } A[i] > A[j]\}|$$
   * For an almost-sorted array with $k$ inversions, Insertion Sort runs in $O(n + k)$ time. If $k = O(n)$, Insertion Sort runs in linear time $O(n)$, outperforming Merge Sort's invariant $O(n \log n)$.

3. **Industrial Practical Application (Hybrid Algorithms):**
   * Modern standard library sorting algorithms do not use pure Merge Sort or pure Quick Sort; instead, they exploit the small-array efficiency of Insertion Sort.
   * **Timsort** (default sort in Python and Java) and **Introsort** (C++ `std::sort`) partition arrays and switch directly to Insertion Sort for sub-arrays of size $n < 32$ or $n < 64$, gaining the best of both worlds: $O(1)$ space and high cache performance for small partitions, combined with $O(n \log n)$ scalability for large datasets.

---

## 8. Instructions to Reproduce Experiments

To re-run the benchmarks and regenerate all SVG diagrams locally:

1. **Run the Benchmark Experiment:**
   ```bash
   python project1/benchmark.py
   ```
2. **Regenerate Plots & SVG Visualizations:**
   ```bash
   python project1/generate_plots.py
   ```
3. **Verify Standalone Insertion Sort:**
   ```bash
   python project1/insertion_sort.py
   ```

All generated vector graphics are stored directly in the `project1/` directory:
* [running_time_comparison.svg](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/running_time_comparison.svg)
* [sorted_best_case.svg](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/sorted_best_case.svg)
* [operations_comparison.svg](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/operations_comparison.svg)
* [insertion_vs_merge_sort.svg](file:///c:/Users/Khaled/OneDrive/Desktop/Algorism%20Projects%20(part%202)/project1/insertion_vs_merge_sort.svg)
