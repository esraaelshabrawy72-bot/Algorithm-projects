import json
import math
import os

# Data collected from benchmark
data = [
    {"n": 100,  "sorted_time": 0.010, "rev_time": 0.343,   "rand_time": 0.171,  "merge_sorted": 0.070, "merge_rand": 0.089, "merge_rev": 0.070, "sorted_c": 99,   "sorted_s": 0, "rev_c": 4950,     "rev_s": 4950,     "rand_c": 2568,    "rand_s": 2472},
    {"n": 250,  "sorted_time": 0.016, "rev_time": 2.112,   "rand_time": 1.048,  "merge_sorted": 0.170, "merge_rand": 0.238, "merge_rev": 0.176, "sorted_c": 249,  "sorted_s": 0, "rev_c": 31125,    "rev_s": 31125,    "rand_c": 15992,   "rand_s": 15749},
    {"n": 500,  "sorted_time": 0.036, "rev_time": 8.807,   "rand_time": 4.644,  "merge_sorted": 0.363, "merge_rand": 0.628, "merge_rev": 0.398, "sorted_c": 499,  "sorted_s": 0, "rev_c": 124750,   "rev_s": 124750,   "rand_c": 65086,   "rand_s": 64594},
    {"n": 750,  "sorted_time": 0.054, "rev_time": 21.584,  "rand_time": 10.721, "merge_sorted": 0.631, "merge_rand": 0.926, "merge_rev": 0.679, "sorted_c": 749,  "sorted_s": 0, "rev_c": 280875,   "rev_s": 280875,   "rand_c": 140722,  "rand_s": 139980},
    {"n": 1000, "sorted_time": 0.081, "rev_time": 39.255,  "rand_time": 19.911, "merge_sorted": 0.908, "merge_rand": 1.238, "merge_rev": 0.931, "sorted_c": 999,  "sorted_s": 0, "rev_c": 499500,   "rev_s": 499500,   "rand_c": 253797,  "rand_s": 252803},
    {"n": 1500, "sorted_time": 0.146, "rev_time": 98.501,  "rand_time": 47.948, "merge_sorted": 1.344, "merge_rand": 2.337, "merge_rev": 1.653, "sorted_c": 1499, "sorted_s": 0, "rev_c": 1124250,  "rev_s": 1124250,  "rand_c": 566910,  "rand_s": 565420},
    {"n": 2000, "sorted_time": 0.165, "rev_time": 159.760, "rand_time": 80.142, "merge_sorted": 1.919, "merge_rand": 2.785, "merge_rev": 1.904, "sorted_c": 1999, "sorted_s": 0, "rev_c": 1999000,  "rev_s": 1999000,  "rand_c": 1013895, "rand_s": 1011904},
    {"n": 2500, "sorted_time": 0.217, "rev_time": 244.691, "rand_time": 119.103,"merge_sorted": 2.297, "merge_rand": 3.413, "merge_rev": 2.437, "sorted_c": 2499, "sorted_s": 0, "rev_c": 3123750,  "rev_s": 3123750,  "rand_c": 1566928, "rand_s": 1564436},
    {"n": 3000, "sorted_time": 0.233, "rev_time": 387.074, "rand_time": 246.127,"merge_sorted": 2.807, "merge_rand": 5.533, "merge_rev": 4.170, "sorted_c": 2999, "sorted_s": 0, "rev_c": 4498500,  "rev_s": 4498500,  "rand_c": 2236254, "rand_s": 2233265},
    {"n": 3500, "sorted_time": 0.432, "rev_time": 846.877, "rand_time": 405.496,"merge_sorted": 6.063, "merge_rand": 7.794, "merge_rev": 5.146, "sorted_c": 3499, "sorted_s": 0, "rev_c": 6123250,  "rev_s": 6123250,  "rand_c": 3102363, "rand_s": 3098872},
    {"n": 4000, "sorted_time": 0.488, "rev_time": 1053.434,"rand_time": 582.758,"merge_sorted": 5.558, "merge_rand": 10.460,"merge_rev": 7.419, "sorted_c": 3999, "sorted_s": 0, "rev_c": 7998000,  "rev_s": 7998000,  "rand_c": 4023861, "rand_s": 4019869},
    {"n": 4500, "sorted_time": 0.629, "rev_time": 1510.569,"rand_time": 786.490,"merge_sorted": 7.128, "merge_rand": 12.675,"merge_rev": 15.461,"sorted_c": 4499, "sorted_s": 0, "rev_c": 10122750, "rev_s": 10122750, "rand_c": 5070850, "rand_s": 5066358},
    {"n": 5000, "sorted_time": 0.692, "rev_time": 2069.153,"rand_time": 971.178,"merge_sorted": 8.389, "merge_rand": 13.521,"merge_rev": 8.981, "sorted_c": 4999, "sorted_s": 0, "rev_c": 12497500, "rev_s": 12497500, "rand_c": 6216670, "rand_s": 6211681}
]

def make_svg_plot(title, subtitle, xlabel, ylabel, series_list, max_x=5000, max_y=None, y_ticks_count=6, width=850, height=520, y_format="{:.0f}"):
    padding_left = 90
    padding_right = 50
    padding_top = 70
    padding_bottom = 60
    
    plot_w = width - padding_left - padding_right
    plot_h = height - padding_top - padding_bottom
    
    # compute max_y if not given
    if max_y is None:
        max_val = 0
        for s in series_list:
            for pt in s["points"]:
                if pt[1] > max_val:
                    max_val = pt[1]
        max_y = max_val * 1.08 if max_val > 0 else 1.0

    def to_coords(x, y):
        cx = padding_left + (x / max_x) * plot_w
        cy = padding_top + plot_h - (y / max_y) * plot_h
        return cx, cy

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    
    # Title and Subtitle
    svg.append(f'<text x="{padding_left}" y="32" font-size="18" font-weight="700" fill="#0f172a">{title}</text>')
    if subtitle:
        svg.append(f'<text x="{padding_left}" y="52" font-size="13" fill="#64748b">{subtitle}</text>')
        
    # Grid & Y-ticks
    for i in range(y_ticks_count + 1):
        y_val = (max_y / y_ticks_count) * i
        cx0, cy = to_coords(0, y_val)
        cx1, _ = to_coords(max_x, y_val)
        svg.append(f'<line x1="{cx0}" y1="{cy:.1f}" x2="{cx1}" y2="{cy:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        formatted_val = y_format.format(y_val)
        svg.append(f'<text x="{cx0 - 12}" y="{cy + 4:.1f}" font-size="11" fill="#64748b" text-anchor="end">{formatted_val}</text>')

    # Grid & X-ticks
    x_ticks = [0, 1000, 2000, 3000, 4000, 5000]
    for x_val in x_ticks:
        cx, cy0 = to_coords(x_val, 0)
        _, cy1 = to_coords(x_val, max_y)
        svg.append(f'<line x1="{cx:.1f}" y1="{cy0}" x2="{cx:.1f}" y2="{cy1}" stroke="#f1f5f9" stroke-width="1"/>')
        svg.append(f'<line x1="{cx:.1f}" y1="{cy0}" x2="{cx:.1f}" y2="{cy0 + 6}" stroke="#94a3b8" stroke-width="1"/>')
        svg.append(f'<text x="{cx:.1f}" y="{cy0 + 20}" font-size="11" fill="#64748b" text-anchor="middle">{x_val}</text>')

    # Axes
    origin_x, origin_y = to_coords(0, 0)
    end_x, _ = to_coords(max_x, 0)
    _, top_y = to_coords(0, max_y)
    svg.append(f'<line x1="{origin_x}" y1="{origin_y}" x2="{end_x}" y2="{origin_y}" stroke="#475569" stroke-width="1.5"/>')
    svg.append(f'<line x1="{origin_x}" y1="{origin_y}" x2="{origin_x}" y2="{top_y}" stroke="#475569" stroke-width="1.5"/>')

    # Axis Labels
    svg.append(f'<text x="{padding_left + plot_w/2}" y="{height - 15}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle">{xlabel}</text>')
    svg.append(f'<text x="24" y="{padding_top + plot_h/2}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle" transform="rotate(-90 24 {padding_top + plot_h/2})">{ylabel}</text>')

    # Plot Series
    for s in series_list:
        color = s.get("color", "#2563eb")
        stroke_dash = s.get("dash", "")
        stroke_width = s.get("width", 2.5)
        points = s["points"]
        path_data = []
        for i, (px, py) in enumerate(points):
            cx, cy = to_coords(px, py)
            cmd = "M" if i == 0 else "L"
            path_data.append(f"{cmd} {cx:.1f} {cy:.1f}")
        
        dash_attr = f'stroke-dasharray="{stroke_dash}"' if stroke_dash else ""
        svg.append(f'<path d="{" ".join(path_data)}" fill="none" stroke="{color}" stroke-width="{stroke_width}" {dash_attr} stroke-linejoin="round" stroke-linecap="round"/>')
        
        # Draw points
        if s.get("show_points", True):
            for px, py in points:
                cx, cy = to_coords(px, py)
                svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="{color}" stroke="#ffffff" stroke-width="1.5">')
                svg.append(f'<title>{s["name"]}: (n={px}, y={py:.2f})</title>')
                svg.append(f'</circle>')

    # Legend
    legend_x = padding_left + 20
    legend_y = padding_top + 15
    legend_h = len(series_list) * 22 + 14
    legend_w = 270
    
    svg.append(f'<rect x="{legend_x}" y="{legend_y}" width="{legend_w}" height="{legend_h}" rx="6" fill="#ffffff" fill-opacity="0.92" stroke="#cbd5e1" stroke-width="1"/>')
    for i, s in enumerate(series_list):
        item_y = legend_y + 16 + i * 22
        color = s.get("color", "#2563eb")
        dash = s.get("dash", "")
        dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
        svg.append(f'<line x1="{legend_x + 12}" y1="{item_y}" x2="{legend_x + 36}" y2="{item_y}" stroke="{color}" stroke-width="2.5" {dash_attr}/>')
        if s.get("show_points", True):
            svg.append(f'<circle cx="{legend_x + 24}" cy="{item_y}" r="3" fill="{color}" stroke="#ffffff" stroke-width="1"/>')
        svg.append(f'<text x="{legend_x + 46}" y="{item_y + 4}" font-size="11.5" font-weight="500" fill="#1e293b">{s["name"]}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)

# 1. Plot 1: Insertion Sort Running Time with Theoretical O(n) and O(n^2) Curves
# Theoretical curve fitting:
# Reverse case: c_rev * n^2. At n=5000, time = 2069.15 ms -> c_rev = 2069.15 / (5000^2) = 8.2766e-5
# Random case: c_rand * n^2. At n=5000, time = 971.18 ms -> c_rand = 971.18 / (5000^2) = 3.8847e-5
# Sorted case: c_sort * n. At n=5000, time = 0.692 ms -> c_sort = 0.692 / 5000 = 1.384e-4

c_rev = 2069.153 / (5000**2)
c_rand = 971.178 / (5000**2)
theo_steps = [x for x in range(100, 5001, 100)]
theo_rev_points = [(x, c_rev * (x**2)) for x in theo_steps]
theo_rand_points = [(x, c_rand * (x**2)) for x in theo_steps]

series_plot1 = [
    {
        "name": "Reverse-Sorted (Worst Case empirical)",
        "points": [(d["n"], d["rev_time"]) for d in data],
        "color": "#dc2626", # red
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Theoretical Worst O(n²) fit [c·n²]",
        "points": theo_rev_points,
        "color": "#991b1b", # dark red
        "width": 1.8,
        "dash": "5,4",
        "show_points": False
    },
    {
        "name": "Random Input (Average Case empirical)",
        "points": [(d["n"], d["rand_time"]) for d in data],
        "color": "#2563eb", # blue
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Theoretical Average O(n²) fit [c/2·n²]",
        "points": theo_rand_points,
        "color": "#1e40af", # dark blue
        "width": 1.8,
        "dash": "5,4",
        "show_points": False
    },
    {
        "name": "Sorted Input (Best Case empirical: O(n))",
        "points": [(d["n"], d["sorted_time"]) for d in data],
        "color": "#16a34a", # green
        "width": 2.5,
        "show_points": True
    }
]

svg1 = make_svg_plot(
    title="Insertion Sort: Running Time vs Array Size (n = 100 to 5,000)",
    subtitle="Empirical running times compared with theoretical O(n²) and O(n) growth models",
    xlabel="Array Size (n)",
    ylabel="Running Time (milliseconds)",
    series_list=series_plot1,
    max_x=5000,
    max_y=2200,
    y_ticks_count=6,
    y_format="{:.0f} ms"
)

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project1\running_time_comparison.svg", "w", encoding="utf-8") as f:
    f.write(svg1)

# 2. Plot 2: Best Case O(n) Zoom-in
c_sort = 0.692 / 5000
theo_sort_points = [(x, c_sort * x) for x in theo_steps]

series_plot_sorted = [
    {
        "name": "Sorted Input (Empirical Best Case)",
        "points": [(d["n"], d["sorted_time"]) for d in data],
        "color": "#16a34a",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Theoretical Linear O(n) fit [c·n]",
        "points": theo_sort_points,
        "color": "#15803d",
        "width": 2.0,
        "dash": "5,4",
        "show_points": False
    }
]

svg_sort = make_svg_plot(
    title="Insertion Sort: Best Case Linear Growth O(n) Detailed View",
    subtitle="Running time on pre-sorted arrays exhibits pure linear scaling (0.01 ms to 0.69 ms)",
    xlabel="Array Size (n)",
    ylabel="Running Time (milliseconds)",
    series_list=series_plot_sorted,
    max_x=5000,
    max_y=0.8,
    y_ticks_count=5,
    y_format="{:.2f} ms"
)

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project1\sorted_best_case.svg", "w", encoding="utf-8") as f:
    f.write(svg_sort)

# 3. Plot 3: Operations (Comparisons & Shifts)
series_ops = [
    {
        "name": "Reverse: Comparisons [n(n-1)/2]",
        "points": [(d["n"], d["rev_c"] / 1000000.0) for d in data],
        "color": "#dc2626",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Reverse: Shifts [n(n-1)/2]",
        "points": [(d["n"], d["rev_s"] / 1000000.0) for d in data],
        "color": "#f97316", # orange
        "width": 2.0,
        "dash": "3,3",
        "show_points": True
    },
    {
        "name": "Random: Comparisons [~n²/4]",
        "points": [(d["n"], d["rand_c"] / 1000000.0) for d in data],
        "color": "#2563eb",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Random: Shifts [~n²/4]",
        "points": [(d["n"], d["rand_s"] / 1000000.0) for d in data],
        "color": "#06b6d4", # cyan
        "width": 2.0,
        "dash": "3,3",
        "show_points": True
    },
    {
        "name": "Sorted: Comparisons [n - 1] (nearly 0 on M scale)",
        "points": [(d["n"], d["sorted_c"] / 1000000.0) for d in data],
        "color": "#16a34a",
        "width": 2.5,
        "show_points": True
    }
]

svg_ops = make_svg_plot(
    title="Insertion Sort: Operation Counts (Comparisons and Shifts)",
    subtitle="Measured exact comparisons and element shifts vs theoretical n(n-1)/2 and n²/4 bounds",
    xlabel="Array Size (n)",
    ylabel="Operations (Millions)",
    series_list=series_ops,
    max_x=5000,
    max_y=13.5,
    y_ticks_count=6,
    y_format="{:.1f}M"
)

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project1\operations_comparison.svg", "w", encoding="utf-8") as f:
    f.write(svg_ops)

# 4. Plot 4: Insertion Sort vs Merge Sort
series_merge = [
    {
        "name": "Insertion Sort (Reverse - Worst Case)",
        "points": [(d["n"], d["rev_time"]) for d in data],
        "color": "#dc2626",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Insertion Sort (Random - Average Case)",
        "points": [(d["n"], d["rand_time"]) for d in data],
        "color": "#2563eb",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Merge Sort (Random Input - O(n log n))",
        "points": [(d["n"], d["merge_rand"]) for d in data],
        "color": "#7c3aed", # purple
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Merge Sort (Reverse Input - O(n log n))",
        "points": [(d["n"], d["merge_rev"]) for d in data],
        "color": "#a855f7", # light purple
        "width": 2.0,
        "dash": "4,3",
        "show_points": True
    },
    {
        "name": "Insertion Sort (Sorted - Best Case: O(n))",
        "points": [(d["n"], d["sorted_time"]) for d in data],
        "color": "#16a34a",
        "width": 2.0,
        "show_points": True
    }
]

svg_merge = make_svg_plot(
    title="Insertion Sort vs Merge Sort: Empirical Runtime Comparison",
    subtitle="Quadratic O(n²) explosion vs asymptotically superior O(n log n) scalability",
    xlabel="Array Size (n)",
    ylabel="Running Time (milliseconds)",
    series_list=series_merge,
    max_x=5000,
    max_y=2200,
    y_ticks_count=6,
    y_format="{:.0f} ms"
)

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project1\insertion_vs_merge_sort.svg", "w", encoding="utf-8") as f:
    f.write(svg_merge)

print("All 4 SVG plots successfully generated!")
