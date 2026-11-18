import json
import math
import os

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project2\benchmark_results.json", "r") as f:
    results = json.load(f)

# Helper to generate Log-Log SVG Plot
def make_loglog_svg(title, subtitle, xlabel, ylabel, series_list, min_x=1000, max_x=100000, min_y=0.001, max_y=500000, width=880, height=540):
    padding_left = 95
    padding_right = 50
    padding_top = 75
    padding_bottom = 65

    plot_w = width - padding_left - padding_right
    plot_h = height - padding_top - padding_bottom

    log_min_x = math.log10(min_x)
    log_max_x = math.log10(max_x)
    log_min_y = math.log10(min_y)
    log_max_y = math.log10(max_y)

    def to_coords(x, y):
        # clamp y
        y = max(y, min_y)
        lx = math.log10(x)
        ly = math.log10(y)
        cx = padding_left + ((lx - log_min_x) / (log_max_x - log_min_x)) * plot_w
        cy = padding_top + plot_h - ((ly - log_min_y) / (log_max_y - log_min_y)) * plot_h
        return cx, cy

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')

    # Title & Subtitle
    svg.append(f'<text x="{padding_left}" y="32" font-size="18" font-weight="700" fill="#0f172a">{title}</text>')
    if subtitle:
        svg.append(f'<text x="{padding_left}" y="52" font-size="12.5" fill="#64748b">{subtitle}</text>')

    # Y-Grid (Powers of 10)
    y_decades = [-3, -2, -1, 0, 1, 2, 3, 4, 5]
    y_labels = {
        -3: "0.001 ms",
        -2: "0.01 ms",
        -1: "0.1 ms",
        0: "1 ms",
        1: "10 ms",
        2: "100 ms",
        3: "1 s (10³ ms)",
        4: "10 s (10⁴ ms)",
        5: "100 s (10⁵ ms)"
    }
    for dec in y_decades:
        val = 10 ** dec
        if min_y <= val <= max_y:
            _, cy = to_coords(min_x, val)
            cx0 = padding_left
            cx1 = padding_left + plot_w
            svg.append(f'<line x1="{cx0}" y1="{cy:.1f}" x2="{cx1}" y2="{cy:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
            svg.append(f'<text x="{cx0 - 12}" y="{cy + 4:.1f}" font-size="10.5" fill="#64748b" text-anchor="end">{y_labels.get(dec, f"10^{dec} ms")}</text>')

    # X-Grid (Powers of 10 and half-decades)
    x_ticks = [1000, 2500, 5000, 10000, 25000, 50000, 100000]
    x_labels = {
        1000: "10³ (1K)",
        2500: "2.5K",
        5000: "5K",
        10000: "10⁴ (10K)",
        25000: "25K",
        5000: "50K",
        100000: "10⁵ (100K)"
    }
    for xv in x_ticks:
        cx, _ = to_coords(xv, min_y)
        cy0 = padding_top
        cy1 = padding_top + plot_h
        svg.append(f'<line x1="{cx:.1f}" y1="{cy0}" x2="{cx:.1f}" y2="{cy1}" stroke="#f1f5f9" stroke-width="1"/>')
        svg.append(f'<line x1="{cx:.1f}" y1="{cy1}" x2="{cx:.1f}" y2="{cy1 + 6}" stroke="#94a3b8" stroke-width="1"/>')
        lbl = x_labels.get(xv, str(xv))
        svg.append(f'<text x="{cx:.1f}" y="{cy1 + 20}" font-size="11" fill="#64748b" text-anchor="middle">{lbl}</text>')

    # Axes
    ox, oy = to_coords(min_x, min_y)
    ex, _ = to_coords(max_x, min_y)
    _, ty = to_coords(min_x, max_y)
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ex}" y2="{oy}" stroke="#475569" stroke-width="1.5"/>')
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{ty}" stroke="#475569" stroke-width="1.5"/>')

    # Axis Labels
    svg.append(f'<text x="{padding_left + plot_w/2}" y="{height - 15}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle">{xlabel}</text>')
    svg.append(f'<text x="22" y="{padding_top + plot_h/2}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle" transform="rotate(-90 22 {padding_top + plot_h/2})">{ylabel}</text>')

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
                dash_border = "1.5"
                svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{color}" stroke="#ffffff" stroke-width="{dash_border}">')
                svg.append(f'<title>{s["name"]}: (n={px}, {py:.3f} ms)</title>')
                svg.append(f'</circle>')

    # Legend
    legend_x = padding_left + 18
    legend_y = padding_top + 14
    legend_h = len(series_list) * 22 + 14
    legend_w = 285

    svg.append(f'<rect x="{legend_x}" y="{legend_y}" width="{legend_w}" height="{legend_h}" rx="6" fill="#ffffff" fill-opacity="0.94" stroke="#cbd5e1" stroke-width="1"/>')
    for i, s in enumerate(series_list):
        item_y = legend_y + 16 + i * 22
        color = s.get("color", "#2563eb")
        dash = s.get("dash", "")
        dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
        svg.append(f'<line x1="{legend_x + 12}" y1="{item_y}" x2="{legend_x + 36}" y2="{item_y}" stroke="{color}" stroke-width="2.5" {dash_attr}/>')
        if s.get("show_points", True):
            svg.append(f'<circle cx="{legend_x + 24}" cy="{item_y}" r="3.5" fill="{color}" stroke="#ffffff" stroke-width="1"/>')
        svg.append(f'<text x="{legend_x + 44}" y="{item_y + 4}" font-size="11.5" font-weight="500" fill="#1e293b">{s["name"]}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)

# Extract points for a given distribution
def get_points(dist, algo):
    d = results[dist][algo]
    return [(int(n), float(t)) for n, t in d.items()]

# 1. Random Distribution Plot (Log-Log)
series_random = [
    {
        "name": "Insertion Sort [O(n²) Average]",
        "points": get_points("random", "Insertion"),
        "color": "#dc2626", # red
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Merge Sort [O(n log n)]",
        "points": get_points("random", "Merge"),
        "color": "#9333ea", # purple
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Quick Sort (Mid-Pivot) [O(n log n)]",
        "points": get_points("random", "Quick"),
        "color": "#2563eb", # blue
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Python sorted() (Timsort C) [O(n log n)]",
        "points": get_points("random", "Python sorted()"),
        "color": "#16a34a", # green
        "width": 2.5,
        "show_points": True
    }
]

svg_rand = make_loglog_svg(
    title="Sorting Lab: Runtime on Random Data (n = 10³ to 10⁵)",
    subtitle="Log-Log Scale: Demonstrating O(n²) slope (Insertion) vs O(n log n) slope (Merge, Quick, Timsort)",
    xlabel="Array Size (n) [Logarithmic Scale]",
    ylabel="Running Time [Logarithmic Scale]",
    series_list=series_random,
    min_x=1000,
    max_x=100000,
    min_y=0.01,
    max_y=300000
)

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project2\random_benchmark.svg", "w", encoding="utf-8") as f:
    f.write(svg_rand)

# 2. Sorted Distribution Plot (Log-Log)
series_sorted = [
    {
        "name": "Quick Sort [O(n log n)]",
        "points": get_points("sorted", "Quick"),
        "color": "#2563eb",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Merge Sort [O(n log n)]",
        "points": get_points("sorted", "Merge"),
        "color": "#9333ea",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Insertion Sort [O(n) Best Case]",
        "points": get_points("sorted", "Insertion"),
        "color": "#d97706", # amber
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Python sorted() [O(n) Adaptive C]",
        "points": get_points("sorted", "Python sorted()"),
        "color": "#16a34a",
        "width": 2.5,
        "show_points": True
    }
]

svg_sort = make_loglog_svg(
    title="Sorting Lab: Runtime on Pre-Sorted Data (n = 10³ to 10⁵)",
    subtitle="Log-Log Scale: Linear O(n) adaptive behavior (Python sorted & Insertion Sort) vs O(n log n)",
    xlabel="Array Size (n) [Logarithmic Scale]",
    ylabel="Running Time [Logarithmic Scale]",
    series_list=series_sorted,
    min_x=1000,
    max_x=100000,
    min_y=0.001,
    max_y=500
)

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project2\sorted_benchmark.svg", "w", encoding="utf-8") as f:
    f.write(svg_sort)

# 3. Reversed Distribution Plot (Log-Log)
series_reversed = [
    {
        "name": "Insertion Sort [O(n²) Worst Case]",
        "points": get_points("reversed", "Insertion"),
        "color": "#dc2626",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Merge Sort [O(n log n)]",
        "points": get_points("reversed", "Merge"),
        "color": "#9333ea",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Quick Sort [O(n log n)]",
        "points": get_points("reversed", "Quick"),
        "color": "#2563eb",
        "width": 2.5,
        "show_points": True
    },
    {
        "name": "Python sorted() [O(n) Inversion Optimization]",
        "points": get_points("reversed", "Python sorted()"),
        "color": "#16a34a",
        "width": 2.5,
        "show_points": True
    }
]

svg_rev = make_loglog_svg(
    title="Sorting Lab: Runtime on Reverse-Sorted Data (n = 10³ to 10⁵)",
    subtitle="Log-Log Scale: Worst-Case Insertion Sort degradation vs Timsort linear reversal and Divide-and-Conquer",
    xlabel="Array Size (n) [Logarithmic Scale]",
    ylabel="Running Time [Logarithmic Scale]",
    series_list=series_reversed,
    min_x=1000,
    max_x=100000,
    min_y=0.001,
    max_y=500000
)

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project2\reversed_benchmark.svg", "w", encoding="utf-8") as f:
    f.write(svg_rev)

# 4. Multi-Distribution Bar Chart Summary at n = 10,000 (Linear Scale Comparison)
def make_grouped_bar_svg(width=880, height=480):
    padding_left = 80
    padding_right = 40
    padding_top = 70
    padding_bottom = 70

    plot_w = width - padding_left - padding_right
    plot_h = height - padding_top - padding_bottom

    categories = ["Sorted Data", "Reversed Data", "Random Data"]
    algo_keys = ["Python sorted()", "Quick", "Merge", "Insertion"]
    algo_labels = ["Python sorted()", "Quick Sort", "Merge Sort", "Insertion Sort"]
    colors = ["#16a34a", "#2563eb", "#9333ea", "#dc2626"]

    # Gather data at n = 10000
    n_target = "10000"
    raw_vals = [
        [results["sorted"][algo][n_target] for algo in algo_keys],
        [results["reversed"][algo][n_target] for algo in algo_keys],
        [results["random"][algo][n_target] for algo in algo_keys]
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    svg.append(f'<text x="{padding_left}" y="32" font-size="18" font-weight="700" fill="#0f172a">Runtime Distribution Breakdown at n = 10,000</text>')
    svg.append(f'<text x="{padding_left}" y="52" font-size="12.5" fill="#64748b">Comparison of execution time in milliseconds (Log scale on Y-axis to visualize both 0.07 ms and 2854 ms)</text>')

    # Y-axis log scale from 0.01 to 5000 ms
    min_y = 0.01
    max_y = 5000.0
    l_min = math.log10(min_y)
    l_max = math.log10(max_y)

    def val_to_y(v):
        v = max(v, min_y)
        return padding_top + plot_h - ((math.log10(v) - l_min) / (l_max - l_min)) * plot_h

    # Grid
    for p in [-2, -1, 0, 1, 2, 3]:
        v = 10 ** p
        cy = val_to_y(v)
        svg.append(f'<line x1="{padding_left}" y1="{cy:.1f}" x2="{padding_left + plot_w}" y2="{cy:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        lbl = { -2: "0.01 ms", -1: "0.1 ms", 0: "1 ms", 1: "10 ms", 2: "100 ms", 3: "1,000 ms" }[p]
        svg.append(f'<text x="{padding_left - 10}" y="{cy + 4:.1f}" font-size="11" fill="#64748b" text-anchor="end">{lbl}</text>')

    # Bars
    group_width = plot_w / len(categories)
    bar_width = (group_width * 0.7) / len(algo_labels)
    
    for c_idx, cat in enumerate(categories):
        group_center = padding_left + c_idx * group_width + group_width / 2
        start_x = group_center - (len(algo_labels) * bar_width) / 2

        # Category label
        svg.append(f'<text x="{group_center}" y="{padding_top + plot_h + 24}" font-size="13" font-weight="600" fill="#1e293b" text-anchor="middle">{cat}</text>')

        for a_idx, algo in enumerate(algo_labels):
            bx = start_x + a_idx * bar_width
            val = raw_vals[c_idx][a_idx]
            by = val_to_y(val)
            bh = (padding_top + plot_h) - by
            color = colors[a_idx]

            svg.append(f'<rect x="{bx + 1:.1f}" y="{by:.1f}" width="{bar_width - 2:.1f}" height="{bh:.1f}" fill="{color}" rx="3">')
            svg.append(f'<title>{algo} on {cat}: {val:.3f} ms</title>')
            svg.append(f'</rect>')

            # Value label on top of bar
            text_val = f"{val:.2f}ms" if val < 100 else f"{val:.0f}ms"
            svg.append(f'<text x="{bx + bar_width/2:.1f}" y="{by - 6:.1f}" font-size="9.5" font-weight="600" fill="#334155" text-anchor="middle">{text_val}</text>')

    # Legend
    leg_x = padding_left + 15
    leg_y = padding_top + 10
    svg.append(f'<rect x="{leg_x}" y="{leg_y}" width="440" height="30" rx="6" fill="#ffffff" fill-opacity="0.95" stroke="#cbd5e1" stroke-width="1"/>')
    for a_idx, algo in enumerate(algo_labels):
        lx = leg_x + 12 + a_idx * 105
        ly = leg_y + 15
        svg.append(f'<rect x="{lx}" y="{ly - 6}" width="12" height="12" fill="{colors[a_idx]}" rx="2"/>')
        svg.append(f'<text x="{lx + 16}" y="{ly + 4}" font-size="11" font-weight="500" fill="#1e293b">{algo.split()[0]}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)

svg_summary = make_grouped_bar_svg()
with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project2\distribution_summary_bar.svg", "w", encoding="utf-8") as f:
    f.write(svg_summary)

print("All lab SVG plots generated successfully!")
