import json
import math
import os

with open(r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project4\benchmark_results.json", "r") as f:
    bench_data = json.load(f)

# =====================================================================
# 1. Word Ladder State Space Graph (cold -> warm)
# =====================================================================
def make_word_ladder_graph_svg(output_path):
    width, height = 860, 480
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    svg.append(f'<text x="40" y="32" font-size="18" font-weight="700" fill="#0f172a">Word Ladder Graph State Space: "cold" → "warm"</text>')
    svg.append(f'<text x="40" y="52" font-size="12.5" fill="#64748b">Undirected graph where edges connect words differing by Hamming distance = 1. Shortest path highlighted in green.</text>')

    # Nodes: (id, x, y, is_path)
    nodes = {
        # Path nodes (cold -> cord -> word -> worm -> warm)
        "cold": (100, 240, True, "START"),
        "cord": (270, 160, True, "STEP 1"),
        "word": (450, 160, True, "STEP 2"),
        "worm": (620, 240, True, "STEP 3"),
        "warm": (770, 240, True, "TARGET"),
        
        # Neighbor / branch nodes
        "bold": (100, 120, False, ""),
        "gold": (190, 80, False, ""),
        "hold": (100, 360, False, ""),
        "sold": (190, 400, False, ""),
        "colt": (190, 280, False, ""),
        "card": (270, 80, False, ""),
        "ward": (450, 80, False, ""),
        "ford": (360, 220, False, ""),
        "lord": (450, 260, False, ""),
        "wood": (540, 120, False, ""),
        "form": (620, 350, False, ""),
        "farm": (700, 140, False, ""),
        "warn": (700, 340, False, ""),
    }

    # Edges: (u, v, is_path)
    edges = [
        # Shortest Path Edges
        ("cold", "cord", True),
        ("cord", "word", True),
        ("word", "worm", True),
        ("worm", "warm", True),

        # Non-path edges
        ("cold", "bold", False),
        ("cold", "hold", False),
        ("cold", "colt", False),
        ("bold", "gold", False),
        ("bold", "sold", False),
        ("hold", "sold", False),
        ("cord", "card", False),
        ("card", "ward", False),
        ("ward", "word", False),
        ("ward", "warm", False),
        ("cord", "ford", False),
        ("ford", "lord", False),
        ("lord", "word", False),
        ("word", "wood", False),
        ("worm", "form", False),
        ("warm", "farm", False),
        ("warm", "warn", False),
    ]

    # Draw non-path edges first
    for u, v, is_p in edges:
        if not is_p:
            x1, y1, _, _ = nodes[u]
            x2, y2, _, _ = nodes[v]
            svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="3,3"/>')

    # Draw shortest path edges with green glow
    for u, v, is_p in edges:
        if is_p:
            x1, y1, _, _ = nodes[u]
            x2, y2, _, _ = nodes[v]
            svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#16a34a" stroke-width="4.5" stroke-linecap="round"/>')

    # Draw Nodes
    for word, (x, y, is_p, role) in nodes.items():
        if is_p:
            # Highlighted node
            svg.append(f'<circle cx="{x}" cy="{y}" r="26" fill="#16a34a" stroke="#15803d" stroke-width="3"/>')
            svg.append(f'<text x="{x}" y="{y + 5}" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">{word.upper()}</text>')
            if role:
                svg.append(f'<text x="{x}" y="{y - 32}" font-size="10" font-weight="700" fill="#15803d" text-anchor="middle">{role}</text>')
        else:
            # Secondary node
            svg.append(f'<circle cx="{x}" cy="{y}" r="20" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>')
            svg.append(f'<text x="{x}" y="{y + 4}" font-size="11" font-weight="600" fill="#475569" text-anchor="middle">{word}</text>')

    # Legend
    leg_x = 40
    leg_y = 430
    svg.append(f'<line x1="{leg_x}" y1="{leg_y}" x2="{leg_x + 30}" y2="{leg_y}" stroke="#16a34a" stroke-width="4"/>')
    svg.append(f'<text x="{leg_x + 40}" y="{leg_y + 4}" font-size="11" font-weight="600" fill="#16a34a">Optimal BFS Shortest Path (Length: 5 words / 4 transformations)</text>')

    svg.append(f'<line x1="{leg_x + 380}" y1="{leg_y}" x2="{leg_x + 410}" y2="{leg_y}" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="3,3"/>')
    svg.append(f'<text x="{leg_x + 420}" y="{leg_y + 4}" font-size="11" fill="#64748b">Alternative dictionary transitions explored</text>')

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))


# =====================================================================
# 2. Search Frontier: Unidirectional BFS vs Bidirectional BFS
# =====================================================================
def make_search_frontier_svg(output_path):
    width, height = 860, 460
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    svg.append(f'<text x="40" y="32" font-size="18" font-weight="700" fill="#0f172a">Search Space Complexity: Unidirectional vs. Bidirectional BFS</text>')
    svg.append(f'<text x="40" y="52" font-size="12.5" fill="#64748b">Mathematical reason for exponential speedup: Expanding radius d (O(b^d)) vs two radii d/2 (O(2 · b^(d/2)))</text>')

    # Panel 1: Unidirectional BFS (Left)
    p1_cx, p1_cy = 220, 230
    svg.append(f'<text x="{p1_cx}" y="95" font-size="14" font-weight="700" fill="#1e293b" text-anchor="middle">Unidirectional BFS</text>')
    svg.append(f'<text x="{p1_cx}" y="115" font-size="11.5" fill="#dc2626" text-anchor="middle">States Explored: O(bᵈ) [Full Sphere]</text>')

    # Concentric circles for depth d
    radii = [30, 60, 95, 130]
    for r in radii:
        svg.append(f'<circle cx="{p1_cx}" cy="{p1_cy}" r="{r}" fill="#fee2e2" fill-opacity="0.35" stroke="#f87171" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<circle cx="{p1_cx}" cy="{p1_cy}" r="130" fill="#ef4444" fill-opacity="0.12" stroke="#dc2626" stroke-width="2"/>')

    # Start and Target nodes
    svg.append(f'<circle cx="{p1_cx}" cy="{p1_cy}" r="12" fill="#2563eb" stroke="#1d4ed8" stroke-width="2"/>')
    svg.append(f'<text x="{p1_cx}" y="{p1_cy + 4}" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">START</text>')

    target_x, target_y = p1_cx + 120, p1_cy
    svg.append(f'<circle cx="{target_x}" cy="{target_y}" r="10" fill="#dc2626" stroke="#991b1b" stroke-width="2"/>')
    svg.append(f'<text x="{target_x}" y="{target_y + 4}" font-size="8" font-weight="700" fill="#ffffff" text-anchor="middle">GOAL</text>')
    svg.append(f'<line x1="{p1_cx + 12}" y1="{p1_cy}" x2="{target_x - 10}" y2="{target_y}" stroke="#dc2626" stroke-width="2"/>')
    svg.append(f'<text x="{p1_cx + 60}" y="{p1_cy - 8}" font-size="11" font-weight="600" fill="#b91c1c">Radius d</text>')

    # Panel 2: Bidirectional BFS (Right)
    p2_cx1, p2_cy1 = 540, 230
    p2_cx2, p2_cy2 = 740, 230
    svg.append(f'<text x="{(p2_cx1 + p2_cx2)/2}" y="95" font-size="14" font-weight="700" fill="#1e293b" text-anchor="middle">Bidirectional BFS (Optimized)</text>')
    svg.append(f'<text x="{(p2_cx1 + p2_cx2)/2}" y="115" font-size="11.5" fill="#16a34a" text-anchor="middle">States Explored: O(2 · b^(d/2)) [Intersecting Spheres]</text>')

    # Circles from start
    svg.append(f'<circle cx="{p2_cx1}" cy="{p2_cy1}" r="35" fill="#dcfce7" fill-opacity="0.5" stroke="#4ade80" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<circle cx="{p2_cx1}" cy="{p2_cy1}" r="75" fill="#22c55e" fill-opacity="0.18" stroke="#16a34a" stroke-width="2"/>')

    # Circles from goal
    svg.append(f'<circle cx="{p2_cx2}" cy="{p2_cy2}" r="35" fill="#dbeafe" fill-opacity="0.5" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="3,3"/>')
    svg.append(f'<circle cx="{p2_cx2}" cy="{p2_cy2}" r="75" fill="#3b82f6" fill-opacity="0.18" stroke="#2563eb" stroke-width="2"/>')

    # Intersection point
    meet_x = (p2_cx1 + p2_cx2) / 2
    meet_y = p2_cy1
    svg.append(f'<circle cx="{meet_x}" cy="{meet_y}" r="8" fill="#eab308" stroke="#ca8a04" stroke-width="2"/>')
    svg.append(f'<text x="{meet_x}" y="{meet_y - 12}" font-size="10" font-weight="700" fill="#854d0e" text-anchor="middle">MEETING NODE</text>')

    # Start and Target
    svg.append(f'<circle cx="{p2_cx1}" cy="{p2_cy1}" r="12" fill="#2563eb" stroke="#1d4ed8" stroke-width="2"/>')
    svg.append(f'<text x="{p2_cx1}" y="{p2_cy1 + 4}" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">START</text>')

    svg.append(f'<circle cx="{p2_cx2}" cy="{p2_cy2}" r="12" fill="#16a34a" stroke="#15803d" stroke-width="2"/>')
    svg.append(f'<text x="{p2_cx2}" y="{p2_cy2 + 4}" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">GOAL</text>')

    # Radii labels
    svg.append(f'<text x="{p2_cx1 + 35}" y="{p2_cy1 - 8}" font-size="10" font-weight="600" fill="#15803d">d/2</text>')
    svg.append(f'<text x="{p2_cx2 - 45}" y="{p2_cy2 - 8}" font-size="10" font-weight="600" fill="#1e40af">d/2</text>')

    # Bottom summary box
    svg.append(f'<rect x="40" y="380" width="{width - 80}" height="55" rx="6" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>')
    svg.append(f'<text x="55" y="402" font-size="11.5" font-weight="700" fill="#0f172a">Key Insight:</text>')
    svg.append(f'<text x="135" y="402" font-size="11.5" fill="#334155">If average branching factor b = 10 and depth d = 6:</text>')
    svg.append(f'<text x="55" y="422" font-size="11.5" fill="#b91c1c">Unidirectional BFS explores: 10⁶ = 1,000,000 nodes</text>')
    svg.append(f'<text x="420" y="422" font-size="11.5" font-weight="600" fill="#15803d">Bidirectional BFS explores: 2 × 10³ = 2,000 nodes (500× reduction!)</text>')

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))


# =====================================================================
# 3. Benchmark States Explored Bar Chart
# =====================================================================
def make_benchmark_chart_svg(output_path):
    width, height = 860, 480
    pad_l, pad_r, pad_t, pad_b = 85, 40, 75, 70
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    # Filter 7 key benchmark puzzles
    selected = [
        d for d in bench_data if d["puzzle"] in [
            "cat -> dog", "hit -> cog", "cold -> warm", "lead -> gold", "head -> tail", "game -> play", "black -> white"
        ]
    ]

    max_visited = max(d["bfs_visited"] for d in selected) * 1.15

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; font-family:-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif;">')
    svg.append(f'<text x="{pad_l}" y="32" font-size="18" font-weight="700" fill="#0f172a">Explored States: Unidirectional BFS vs Bidirectional BFS</text>')
    svg.append(f'<text x="{pad_l}" y="52" font-size="12.5" fill="#64748b">Total nodes visited during shortest ladder discovery across benchmark test cases</text>')

    # Y-Ticks
    y_ticks = 5
    for i in range(y_ticks + 1):
        v = (max_visited / y_ticks) * i
        cy = pad_t + plot_h - (v / max_visited) * plot_h
        svg.append(f'<line x1="{pad_l}" y1="{cy:.1f}" x2="{pad_l + plot_w}" y2="{cy:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{pad_l - 12}" y="{cy + 4:.1f}" font-size="11" fill="#64748b" text-anchor="end">{int(v):,}</text>')

    # Bars
    group_w = plot_w / len(selected)
    bar_w = group_w * 0.32

    for i, d in enumerate(selected):
        gx = pad_l + i * group_w + group_w / 2

        # BFS bar (Red)
        bfs_val = d["bfs_visited"]
        bfs_h = (bfs_val / max_visited) * plot_h
        bfs_x = gx - bar_w - 2
        bfs_y = pad_t + plot_h - bfs_h
        svg.append(f'<rect x="{bfs_x:.1f}" y="{bfs_y:.1f}" width="{bar_w:.1f}" height="{bfs_h:.1f}" fill="#ef4444" rx="3">')
        svg.append(f'<title>{d["puzzle"]} (BFS): {bfs_val} nodes</title></rect>')
        svg.append(f'<text x="{bfs_x + bar_w/2:.1f}" y="{bfs_y - 6:.1f}" font-size="9" font-weight="600" fill="#b91c1c" text-anchor="middle">{bfs_val}</text>')

        # Bi-BFS bar (Green)
        bi_val = d["bi_visited"]
        bi_h = (bi_val / max_visited) * plot_h
        bi_x = gx + 2
        bi_y = pad_t + plot_h - bi_h
        svg.append(f'<rect x="{bi_x:.1f}" y="{bi_y:.1f}" width="{bar_w:.1f}" height="{bi_h:.1f}" fill="#16a34a" rx="3">')
        svg.append(f'<title>{d["puzzle"]} (Bi-BFS): {bi_val} nodes</title></rect>')
        svg.append(f'<text x="{bi_x + bar_w/2:.1f}" y="{bi_y - 6:.1f}" font-size="9" font-weight="600" fill="#15803d" text-anchor="middle">{bi_val}</text>')

        # Label
        svg.append(f'<text x="{gx:.1f}" y="{pad_t + plot_h + 20}" font-size="11" font-weight="600" fill="#334155" text-anchor="middle">{d["puzzle"]}</text>')
        svg.append(f'<text x="{gx:.1f}" y="{pad_t + plot_h + 35}" font-size="9.5" fill="#64748b" text-anchor="middle">L={d["ladder_length"]}</text>')

    # Legend
    leg_x = pad_l + 15
    leg_y = pad_t + 10
    svg.append(f'<rect x="{leg_x}" y="{leg_y}" width="320" height="32" rx="6" fill="#ffffff" fill-opacity="0.95" stroke="#cbd5e1" stroke-width="1"/>')
    svg.append(f'<rect x="{leg_x + 12}" y="{leg_y + 10}" width="12" height="12" fill="#ef4444" rx="2"/>')
    svg.append(f'<text x="{leg_x + 30}" y="{leg_y + 20}" font-size="11" font-weight="500" fill="#1e293b">Unidirectional BFS</text>')

    svg.append(f'<rect x="{leg_x + 160}" y="{leg_y + 10}" width="12" height="12" fill="#16a34a" rx="2"/>')
    svg.append(f'<text x="{leg_x + 178}" y="{leg_y + 20}" font-size="11" font-weight="500" fill="#1e293b">Bidirectional BFS</text>')

    svg.append('</svg>')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(svg))


if __name__ == "__main__":
    out_dir = r"c:\Users\Khaled\OneDrive\Desktop\Algorism Projects (part 2)\project4"
    make_word_ladder_graph_svg(os.path.join(out_dir, "word_ladder_graph.svg"))
    make_search_frontier_svg(os.path.join(out_dir, "bfs_search_frontier.svg"))
    make_benchmark_chart_svg(os.path.join(out_dir, "benchmark_metrics_chart.svg"))
    print("All Word Ladder plots generated successfully!")
