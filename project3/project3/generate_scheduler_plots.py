import json
import math
import os

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project3\benchmark_data.json", "r") as f:
    bench_data = json.load(f)

heap_scaling = bench_data["heap_scaling"]
pq_comp = bench_data["pq_comparison"]

# =====================================================================
# 1. Heap Operations Benchmark Plot (INSERT & EXTRACT-MAX vs log2 n)
# =====================================================================
def make_heap_ops_svg(output_path):
    width, height = 860, 500
    pad_l, pad_r, pad_t, pad_b = 85, 45, 75, 65
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    min_x, max_x = 0, 100000
    min_y, max_y = 0.0, 5.0

    def to_coords(x, y):
        cx = pad_l + (x / max_x) * plot_w
        cy = pad_t + plot_h - (y / max_y) * plot_h
        return cx, cy

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    svg.append(f'<text x="{pad_l}" y="32" font-size="18" font-weight="700" fill="#0f172a">Max-Heap Operations Latency vs Heap Size (n = 100 to 100,000)</text>')
    svg.append(f'<text x="{pad_l}" y="52" font-size="12.5" fill="#64748b">Empirical latency of INSERT and EXTRACT-MAX demonstrating logarithmic O(log n) efficiency</text>')

    # Y-Ticks
    for y_val in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]:
        _, cy = to_coords(0, y_val)
        svg.append(f'<line x1="{pad_l}" y1="{cy:.1f}" x2="{pad_l + plot_w}" y2="{cy:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{pad_l - 12}" y="{cy + 4:.1f}" font-size="11" fill="#64748b" text-anchor="end">{y_val:.1f} µs</text>')

    # X-Ticks
    for x_val in [0, 20000, 40000, 60000, 80000, 100000]:
        cx, _ = to_coords(x_val, 0)
        svg.append(f'<line x1="{cx:.1f}" y1="{pad_t}" x2="{cx:.1f}" y2="{pad_t + plot_h}" stroke="#f1f5f9" stroke-width="1"/>')
        svg.append(f'<line x1="{cx:.1f}" y1="{pad_t + plot_h}" x2="{cx:.1f}" y2="{pad_t + plot_h + 6}" stroke="#94a3b8" stroke-width="1"/>')
        lbl = f"{x_val//1000}K" if x_val > 0 else "0"
        svg.append(f'<text x="{cx:.1f}" y="{pad_t + plot_h + 20}" font-size="11" fill="#64748b" text-anchor="middle">{lbl}</text>')

    # Axes
    ox, oy = to_coords(0, 0)
    ex, _ = to_coords(max_x, 0)
    _, ty = to_coords(0, max_y)
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ex}" y2="{oy}" stroke="#475569" stroke-width="1.5"/>')
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{ty}" stroke="#475569" stroke-width="1.5"/>')
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{height - 15}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle">Heap Size (n Elements)</text>')
    svg.append(f'<text x="22" y="{pad_t + plot_h/2}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle" transform="rotate(-90 22 {pad_t + plot_h/2})">Operation Time (Microseconds, µs)</text>')

    # Series
    ext_pts = [(d["n"], d["extract_us"]) for d in heap_scaling]
    ins_pts = [(d["n"], d["insert_us"]) for d in heap_scaling]

    # Extract-Max Line
    p_ext = " ".join([f"{'M' if i==0 else 'L'} {to_coords(p[0], p[1])[0]:.1f} {to_coords(p[0], p[1])[1]:.1f}" for i, p in enumerate(ext_pts)])
    svg.append(f'<path d="{p_ext}" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linejoin="round"/>')
    for p in ext_pts:
        cx, cy = to_coords(p[0], p[1])
        svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"><title>EXTRACT-MAX: n={p[0]}, {p[1]:.3f}µs</title></circle>')

    # Insert Line
    p_ins = " ".join([f"{'M' if i==0 else 'L'} {to_coords(p[0], p[1])[0]:.1f} {to_coords(p[0], p[1])[1]:.1f}" for i, p in enumerate(ins_pts)])
    svg.append(f'<path d="{p_ins}" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linejoin="round"/>')
    for p in ins_pts:
        cx, cy = to_coords(p[0], p[1])
        svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"><title>INSERT: n={p[0]}, {p[1]:.3f}µs</title></circle>')

    # Legend
    leg_x = pad_l + 20
    leg_y = pad_t + 15
    svg.append(f'<rect x="{leg_x}" y="{leg_y}" width="280" height="66" rx="6" fill="#ffffff" fill-opacity="0.94" stroke="#cbd5e1" stroke-width="1"/>')
    svg.append(f'<line x1="{leg_x + 12}" y1="{leg_y + 20}" x2="{leg_x + 36}" y2="{leg_y + 20}" stroke="#2563eb" stroke-width="2.5"/>')
    svg.append(f'<circle cx="{leg_x + 24}" cy="{leg_y + 20}" r="3.5" fill="#2563eb" stroke="#ffffff" stroke-width="1"/>')
    svg.append(f'<text x="{leg_x + 46}" y="{leg_y + 24}" font-size="11.5" font-weight="500" fill="#1e293b">EXTRACT-MAX [O(log n) Sift-Down]</text>')

    svg.append(f'<line x1="{leg_x + 12}" y1="{leg_y + 45}" x2="{leg_x + 36}" y2="{leg_y + 45}" stroke="#16a34a" stroke-width="2.5"/>')
    svg.append(f'<circle cx="{leg_x + 24}" cy="{leg_y + 45}" r="3.5" fill="#16a34a" stroke="#ffffff" stroke-width="1"/>')
    svg.append(f'<text x="{leg_x + 46}" y="{leg_y + 49}" font-size="11.5" font-weight="500" fill="#1e293b">INSERT [O(log n) Sift-Up]</text>')

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))


# =====================================================================
# 2. Priority Queue Structure Comparison (Max-Heap vs Lists)
# =====================================================================
def make_pq_comp_svg(output_path):
    width, height = 860, 500
    pad_l, pad_r, pad_t, pad_b = 85, 45, 75, 65
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    min_x, max_x = 1000, 10000
    min_y, max_y = 0.0, 360.0

    def to_coords(x, y):
        cx = pad_l + ((x - min_x) / (max_x - min_x)) * plot_w
        cy = pad_t + plot_h - (y / max_y) * plot_h
        return cx, cy

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    svg.append(f'<text x="{pad_l}" y="32" font-size="18" font-weight="700" fill="#0f172a">Extract-Max Latency: Max-Heap vs Unsorted List (n = 1,000 to 10,000)</text>')
    svg.append(f'<text x="{pad_l}" y="52" font-size="12.5" fill="#64748b">Demonstrating the catastrophic O(n) linear search bottleneck of Unsorted Lists vs O(log n) Max-Heap</text>')

    # Y-Ticks
    for y_val in [0, 50, 100, 150, 200, 250, 300, 350]:
        _, cy = to_coords(min_x, y_val)
        svg.append(f'<line x1="{pad_l}" y1="{cy:.1f}" x2="{pad_l + plot_w}" y2="{cy:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{pad_l - 12}" y="{cy + 4:.1f}" font-size="11" fill="#64748b" text-anchor="end">{y_val} µs</text>')

    # X-Ticks
    for x_val in [1000, 2500, 5000, 7500, 10000]:
        cx, _ = to_coords(x_val, 0)
        svg.append(f'<line x1="{cx:.1f}" y1="{pad_t}" x2="{cx:.1f}" y2="{pad_t + plot_h}" stroke="#f1f5f9" stroke-width="1"/>')
        svg.append(f'<line x1="{cx:.1f}" y1="{pad_t + plot_h}" x2="{cx:.1f}" y2="{pad_t + plot_h + 6}" stroke="#94a3b8" stroke-width="1"/>')
        svg.append(f'<text x="{cx:.1f}" y="{pad_t + plot_h + 20}" font-size="11" fill="#64748b" text-anchor="middle">{x_val:,}</text>')

    # Axes
    ox, oy = to_coords(min_x, 0)
    ex, _ = to_coords(max_x, 0)
    _, ty = to_coords(min_x, max_y)
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ex}" y2="{oy}" stroke="#475569" stroke-width="1.5"/>')
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{ty}" stroke="#475569" stroke-width="1.5"/>')
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{height - 15}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle">Queue Capacity (n Tasks)</text>')
    svg.append(f'<text x="22" y="{pad_t + plot_h/2}" font-size="13" font-weight="600" fill="#334155" text-anchor="middle" transform="rotate(-90 22 {pad_t + plot_h/2})">Extract-Max Latency (µs)</text>')

    # Unsorted List Extract Line O(n)
    unsort_pts = [(d["n"], d["unsorted_ext"]) for d in pq_comp]
    p_u = " ".join([f"{'M' if i==0 else 'L'} {to_coords(p[0], p[1])[0]:.1f} {to_coords(p[0], p[1])[1]:.1f}" for i, p in enumerate(unsort_pts)])
    svg.append(f'<path d="{p_u}" fill="none" stroke="#dc2626" stroke-width="2.5" stroke-linejoin="round"/>')
    for p in unsort_pts:
        cx, cy = to_coords(p[0], p[1])
        svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#dc2626" stroke="#ffffff" stroke-width="1.5"><title>Unsorted List: {p[1]:.1f}µs</title></circle>')

    # Max-Heap Extract Line O(log n)
    heap_pts = [(d["n"], d["heap_ext"]) for d in pq_comp]
    p_h = " ".join([f"{'M' if i==0 else 'L'} {to_coords(p[0], p[1])[0]:.1f} {to_coords(p[0], p[1])[1]:.1f}" for i, p in enumerate(heap_pts)])
    svg.append(f'<path d="{p_h}" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linejoin="round"/>')
    for p in heap_pts:
        cx, cy = to_coords(p[0], p[1])
        svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"><title>Max-Heap: {p[1]:.2f}µs</title></circle>')

    # Legend
    leg_x = pad_l + 20
    leg_y = pad_t + 15
    svg.append(f'<rect x="{leg_x}" y="{leg_y}" width="340" height="66" rx="6" fill="#ffffff" fill-opacity="0.94" stroke="#cbd5e1" stroke-width="1"/>')
    svg.append(f'<line x1="{leg_x + 12}" y1="{leg_y + 20}" x2="{leg_x + 36}" y2="{leg_y + 20}" stroke="#dc2626" stroke-width="2.5"/>')
    svg.append(f'<circle cx="{leg_x + 24}" cy="{leg_y + 20}" r="3.5" fill="#dc2626" stroke="#ffffff" stroke-width="1"/>')
    svg.append(f'<text x="{leg_x + 46}" y="{leg_y + 24}" font-size="11.5" font-weight="500" fill="#1e293b">Unsorted List EXTRACT-MAX [O(n) Linear Scan]</text>')

    svg.append(f'<line x1="{leg_x + 12}" y1="{leg_y + 45}" x2="{leg_x + 36}" y2="{leg_y + 45}" stroke="#2563eb" stroke-width="2.5"/>')
    svg.append(f'<circle cx="{leg_x + 24}" cy="{leg_y + 45}" r="3.5" fill="#2563eb" stroke="#ffffff" stroke-width="1"/>')
    svg.append(f'<text x="{leg_x + 46}" y="{leg_y + 49}" font-size="11.5" font-weight="500" fill="#1e293b">Max-Heap EXTRACT-MAX [O(log n) Tree Sift]</text>')

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))


# =====================================================================
# 3. OS Scheduler Execution Gantt Chart Timeline
# =====================================================================
def make_gantt_chart_svg(output_path):
    width, height = 900, 480
    pad_l, pad_r, pad_t, pad_b = 90, 50, 80, 50
    plot_w = width - pad_l - pad_r

    # Timeline data from task_scheduler.py simulation
    gantt_non_preemptive = [
        {"task": "T1", "start": 0, "end": 3, "prio": 95, "color": "#ef4444"},
        {"task": "T2", "start": 3, "end": 7, "prio": 80, "color": "#f97316"},
        {"task": "T5", "start": 7, "end": 9, "prio": 90, "color": "#06b6d4"},
        {"task": "T4", "start": 9, "end": 14, "prio": 85, "color": "#3b82f6"},
        {"task": "T8", "start": 14, "end": 18, "prio": 70, "color": "#8b5cf6"},
        {"task": "T3", "start": 18, "end": 24, "prio": 60, "color": "#ec4899"},
        {"task": "T7", "start": 24, "end": 31, "prio": 30, "color": "#eab308"},
        {"task": "T6", "start": 31, "end": 39, "prio": 20, "color": "#64748b"}
    ]

    gantt_preemptive = [
        {"task": "T1", "start": 0, "end": 3, "prio": 95, "color": "#ef4444"},
        {"task": "T2", "start": 3, "end": 4, "prio": 80, "color": "#f97316"},
        {"task": "T4", "start": 4, "end": 7, "prio": 85, "color": "#3b82f6"},
        {"task": "T5", "start": 7, "end": 9, "prio": 90, "color": "#06b6d4"},
        {"task": "T2", "start": 9, "end": 10, "prio": 85, "color": "#f97316"},
        {"task": "T4", "start": 10, "end": 12, "prio": 90, "color": "#3b82f6"},
        {"task": "T2", "start": 12, "end": 14, "prio": 85, "color": "#f97316"},
        {"task": "T8", "start": 14, "end": 18, "prio": 75, "color": "#8b5cf6"},
        {"task": "T3", "start": 18, "end": 24, "prio": 70, "color": "#ec4899"},
        {"task": "T7", "start": 24, "end": 30, "prio": 45, "color": "#eab308"},
        {"task": "T6", "start": 30, "end": 33, "prio": 45, "color": "#64748b"},
        {"task": "T7", "start": 33, "end": 34, "prio": 50, "color": "#eab308"},
        {"task": "T6", "start": 34, "end": 39, "prio": 45, "color": "#64748b"}
    ]

    max_time = 39
    scale_x = plot_w / max_time

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    svg.append(f'<text x="{pad_l}" y="32" font-size="18" font-weight="700" fill="#0f172a">OS Task Scheduler CPU Execution Gantt Chart Timeline</text>')
    svg.append(f'<text x="{pad_l}" y="52" font-size="12.5" fill="#64748b">Comparison: Non-Preemptive vs Preemptive Priority Scheduling with Task Aging</text>')

    # Row 1: Non-Preemptive
    row1_y = 110
    row_h = 42
    svg.append(f'<text x="{pad_l - 12}" y="{row1_y + 26}" font-size="12" font-weight="600" fill="#334155" text-anchor="end">Non-Preemptive</text>')
    for b in gantt_non_preemptive:
        bx = pad_l + b["start"] * scale_x
        bw = (b["end"] - b["start"]) * scale_x
        svg.append(f'<rect x="{bx:.1f}" y="{row1_y}" width="{bw:.1f}" height="{row_h}" fill="{b["color"]}" stroke="#ffffff" stroke-width="1.5" rx="4"/>')
        if bw > 18:
            svg.append(f'<text x="{bx + bw/2:.1f}" y="{row1_y + 25}" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">{b["task"]}</text>')

    # Row 2: Preemptive with Aging
    row2_y = 210
    svg.append(f'<text x="{pad_l - 12}" y="{row2_y + 26}" font-size="12" font-weight="600" fill="#334155" text-anchor="end">Preemptive + Aging</text>')
    for b in gantt_preemptive:
        bx = pad_l + b["start"] * scale_x
        bw = (b["end"] - b["start"]) * scale_x
        svg.append(f'<rect x="{bx:.1f}" y="{row2_y}" width="{bw:.1f}" height="{row_h}" fill="{b["color"]}" stroke="#ffffff" stroke-width="1.5" rx="4"/>')
        if bw > 14:
            svg.append(f'<text x="{bx + bw/2:.1f}" y="{row2_y + 25}" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">{b["task"]}</text>')

    # Time Axis & Grid
    axis_y = 285
    svg.append(f'<line x1="{pad_l}" y1="{axis_y}" x2="{pad_l + plot_w}" y2="{axis_y}" stroke="#475569" stroke-width="1.5"/>')
    for t in range(0, max_time + 1, 3):
        tx = pad_l + t * scale_x
        svg.append(f'<line x1="{tx:.1f}" y1="{axis_y}" x2="{tx:.1f}" y2="{axis_y + 6}" stroke="#475569" stroke-width="1.5"/>')
        svg.append(f'<line x1="{tx:.1f}" y1="95" x2="{tx:.1f}" y2="{axis_y}" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="2,2"/>')
        svg.append(f'<text x="{tx:.1f}" y="{axis_y + 20}" font-size="11" fill="#64748b" text-anchor="middle">{t}</text>')
    svg.append(f'<text x="{pad_l + plot_w/2}" y="{axis_y + 40}" font-size="12.5" font-weight="600" fill="#334155" text-anchor="middle">CPU Time Units (Clock Cycles)</text>')

    # Task Legend
    tasks_legend = [
        ("T1", "Kernel Int (95)", "#ef4444"),
        ("T2", "Audio (80)", "#f97316"),
        ("T4", "UI (85)", "#3b82f6"),
        ("T5", "Network (90)", "#06b6d4"),
        ("T8", "Browser (70)", "#8b5cf6"),
        ("T3", "Disk IO (60)", "#ec4899"),
        ("T7", "Virus Scan (30)", "#eab308"),
        ("T6", "Backup Daemon (20)", "#64748b")
    ]
    leg_y = 365
    svg.append(f'<rect x="{pad_l}" y="{leg_y}" width="{plot_w}" height="80" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>')
    svg.append(f'<text x="{pad_l + 12}" y="{leg_y + 20}" font-size="11.5" font-weight="700" fill="#1e293b">Task Legend (ID, Name & Base Priority):</text>')
    for i, (t_id, desc, col) in enumerate(tasks_legend):
        col_idx = i % 4
        row_idx = i // 4
        lx = pad_l + 15 + col_idx * 180
        ly = leg_y + 42 + row_idx * 24
        svg.append(f'<rect x="{lx}" y="{ly - 10}" width="14" height="14" fill="{col}" rx="3"/>')
        svg.append(f'<text x="{lx + 20}" y="{ly + 2}" font-size="11" fill="#334155">{t_id}: {desc}</text>')

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))


# =====================================================================
# 4. Max-Heap Data Structure Tree Diagram
# =====================================================================
def make_heap_tree_svg(output_path):
    width, height = 800, 360
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    svg.append(f'<text x="40" y="32" font-size="17" font-weight="700" fill="#0f172a">Max-Heap Binary Tree & Array Invariant Structure</text>')
    svg.append(f'<text x="40" y="52" font-size="12" fill="#64748b">Heap Property: Priority(Parent) ≥ Priority(Children) | Parent(i) = (i-1)//2, Left = 2i+1, Right = 2i+2</text>')

    # Tree Nodes: (x, y, label, priority, index)
    nodes = [
        (400, 100, "T1 (Kernel)", 95, 0),
        (240, 170, "T5 (Net)", 90, 1),
        (560, 170, "T4 (UI)", 85, 2),
        (160, 240, "T2 (Audio)", 80, 3),
        (320, 240, "T8 (JS)", 70, 4),
        (480, 240, "T3 (Disk)", 60, 5),
        (640, 240, "T7 (Scan)", 30, 6)
    ]

    # Edges
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    for u, v in edges:
        x1, y1 = nodes[u][0], nodes[u][1]
        x2, y2 = nodes[v][0], nodes[v][1]
        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#94a3b8" stroke-width="2"/>')

    # Draw Nodes
    for x, y, name, prio, idx in nodes:
        svg.append(f'<circle cx="{x}" cy="{y}" r="22" fill="#2563eb" stroke="#1e40af" stroke-width="2"/>')
        svg.append(f'<text x="{x}" y="{y + 5}" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{prio}</text>')
        svg.append(f'<text x="{x}" y="{y - 28}" font-size="10.5" font-weight="600" fill="#1e293b" text-anchor="middle">{name}</text>')
        svg.append(f'<text x="{x}" y="{y + 35}" font-size="10" fill="#64748b" text-anchor="middle">A[{idx}]</text>')

    # Array representation bar at bottom
    arr_y = 310
    svg.append(f'<text x="40" y="{arr_y + 18}" font-size="12" font-weight="700" fill="#334155">Array:</text>')
    start_x = 90
    cell_w = 95
    for idx, (_, _, name, prio, _) in enumerate(nodes):
        bx = start_x + idx * cell_w
        svg.append(f'<rect x="{bx}" y="{arr_y}" width="{cell_w - 4}" height="28" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" rx="3"/>')
        svg.append(f'<text x="{bx + (cell_w-4)/2}" y="{arr_y + 19}" font-size="11" font-weight="600" fill="#0f172a" text-anchor="middle">{prio} ({name.split()[0]})</text>')
        svg.append(f'<text x="{bx + (cell_w-4)/2}" y="{arr_y + 40}" font-size="9.5" fill="#64748b" text-anchor="middle">[{idx}]</text>')

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))


if __name__ == "__main__":
    out_dir = r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project3"
    make_heap_ops_svg(os.path.join(out_dir, "heap_operations_benchmark.svg"))
    make_pq_comp_svg(os.path.join(out_dir, "pq_comparison_chart.svg"))
    make_gantt_chart_svg(os.path.join(out_dir, "gantt_chart_scheduler.svg"))
    make_heap_tree_svg(os.path.join(out_dir, "max_heap_structure.svg"))
    print("All 4 scheduler SVG charts generated successfully!")
