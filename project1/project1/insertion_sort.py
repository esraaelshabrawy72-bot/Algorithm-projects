"""
Insertion Sort & Merge Sort: Empirical Analysis and Complexity Benchmarking
Course: Algorithms: Analysis and Design
"""

import time
import random

def insertion_sort(arr):
    """
    Executes insertion sort on an array copy and counts comparisons and shifts.

    Args:
        arr (list): Input array to sort.

    Returns:
        tuple: (sorted_list, comparisons_count, shifts_count)
    """
    a = list(arr)
    comparisons = 0
    shifts = 0
    n = len(a)
    
    for i in range(1, n):
        key = a[i]
        j = i - 1
        
        # Compare key with elements in the sorted subarray a[0..i-1]
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]  # Shift element to the right
                shifts += 1
                j -= 1
            else:
                break
        
        # Place key into its correct sorted position
        a[j + 1] = key
        
    return a, comparisons, shifts

def merge_sort(arr):
    """
    Executes 2-way Merge Sort and counts key comparisons.

    Args:
        arr (list): Input array to sort.

    Returns:
        tuple: (sorted_list, comparisons_count)
    """
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

if __name__ == "__main__":
    test_array = [29, 10, 14, 37, 13]
    sorted_res, comps, shifts = insertion_sort(test_array)
    print(f"Original: {test_array}")
    print(f"Sorted:   {sorted_res}")
    print(f"Comparisons: {comps}, Shifts: {shifts}")
