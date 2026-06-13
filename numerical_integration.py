import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

A = 0.0
B = 1.5
N_DEMO = 10
CURVE_SAMPLES = 1000
COLORS = {
    'curve': 'firebrick',
    'fill': 'salmon',
    'method': '#4A90E2',
    'edge': '#2E5C8A',
    'monte_carlo': '#9B59B6',
    'simpson': '#27AE60',
}

def f(x):
    x_arr = np.asarray(x)
    return np.arcsin(x_arr / 3)
def compute_true_integral():
    x = sp.symbols('x')
    f_sym = sp.asin(x / 3)  # arcsin в sympy
    S_sym = sp.integrate(f_sym, (x, A, B))
    S_num = float(S_sym.evalf())
    return S_sym, S_num
TRUE_FORMULA, TRUE_VALUE = compute_true_integral()

def left_rectangles_area(n):
    dx = (B - A) / n
    x_left = A + np.arange(n) * dx
    return dx * np.sum(f(x_left))
def right_rectangles_area(n):
    dx = (B - A) / n
    x_right = A + np.arange(1, n + 1) * dx
    return dx * np.sum(f(x_right))
def midpoint_rectangles_area(n):
    dx = (B - A) / n
    x_mid = A + (np.arange(n) + 0.5) * dx
    return dx * np.sum(f(x_mid))
def trapezoids_area(n):
    dx = (B - A) / n
    x_pts = np.linspace(A, B, n + 1)
    y_pts = f(x_pts)
    return dx * (0.5 * y_pts[0] + np.sum(y_pts[1:-1]) + 0.5 * y_pts[-1])
def simpson_area(n):
    m = 2 * n
    dx = (B - A) / m
    x_pts = np.linspace(A, B, m + 1)
    y_pts = f(x_pts)
    return dx / 3 * (y_pts[0] + y_pts[-1] + 4 * np.sum(y_pts[1:-1:2]) + 2 * np.sum(y_pts[2:-1:2]))
def monte_carlo_area(n):
    rng = np.random.default_rng(42)
    x_rand = rng.uniform(A, B, n)
    return (B - A) * np.mean(f(x_rand))

def plot_base_function(ax, label_true):
    x_vals = np.linspace(A, B, CURVE_SAMPLES)
    y_vals = f(x_vals)
    ax.plot(x_vals, y_vals, color=COLORS['curve'], lw=2.2, label=r'$f(x) = \arcsin(x/3)$', zorder=3)
    ax.fill_between(x_vals, y_vals, color=COLORS['fill'], alpha=0.15, label=label_true, zorder=1)
    ax.set_xlim(A, B)
    ax.set_ylim(0, np.max(y_vals) * 1.2)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel('x', fontsize=10)
    ax.set_ylabel('f(x)', fontsize=10)
def plot_left_rectangles(ax, n):
    dx = (B - A) / n
    x_left = A + np.arange(n) * dx
    heights = f(x_left)
    ax.bar(x_left, heights, width=dx, align='edge',
           color=COLORS['method'], edgecolor=COLORS['edge'], alpha=0.5, linewidth=1.2, label='Левые прямоугольники', zorder=2)
    return left_rectangles_area(n)
def plot_right_rectangles(ax, n):
    dx = (B - A) / n
    x_right = A + np.arange(1, n + 1) * dx
    heights = f(x_right)
    ax.bar(x_right - dx, heights, width=dx, align='edge',
           color=COLORS['method'], edgecolor=COLORS['edge'], alpha=0.5, linewidth=1.2, label='Правые прямоугольники', zorder=2)
    return right_rectangles_area(n)
def plot_midpoint_rectangles(ax, n):
    dx = (B - A) / n
    x_left = A + np.arange(n) * dx
    x_mid = x_left + dx / 2
    heights = f(x_mid)
    ax.bar(x_left, heights, width=dx, align='edge',
           color=COLORS['method'], edgecolor=COLORS['edge'], alpha=0.5, linewidth=1.2, label='Средние прямоугольники', zorder=2)
    ax.scatter(x_mid, heights, color=COLORS['edge'], s=25, zorder=4, label='Средние точки')
    return midpoint_rectangles_area(n)
def plot_trapezoids(ax, n):
    dx = (B - A) / n
    x_pts = np.linspace(A, B, n + 1)
    y_pts = f(x_pts)
    for i in range(n):
        px = [x_pts[i], x_pts[i], x_pts[i + 1], x_pts[i + 1]]
        py = [0, y_pts[i], y_pts[i + 1], 0]
        ax.fill(px, py, color=COLORS['method'], edgecolor=COLORS['edge'], alpha=0.45, linewidth=1, zorder=2)
    ax.plot(x_pts, y_pts, color=COLORS['edge'], lw=1.5, label='Трапеции', zorder=3)
    return trapezoids_area(n)
def plot_simpson(ax, n):
    m = 2 * n
    dx = (B - A) / m
    x_pts = np.linspace(A, B, m + 1)
    y_pts = f(x_pts)
    for k in range(n):
        i = 2 * k
        x_local = x_pts[i:i + 3]
        y_local = y_pts[i:i + 3]
        coeffs = np.polyfit(x_local, y_local, 2)
        x_dense = np.linspace(x_local[0], x_local[-1], 100)
        y_dense = np.polyval(coeffs, x_dense)
        ax.fill_between(x_dense, 0, y_dense, color=COLORS['simpson'], alpha=0.35, edgecolor=COLORS['edge'],
                        linewidth=0.8, zorder=2)
        ax.plot(x_dense, y_dense, color=COLORS['simpson'], lw=1.3, zorder=3)
    ax.scatter(x_pts, y_pts, color=COLORS['edge'], s=20, zorder=4, label='Узлы')
    return simpson_area(n)
def plot_monte_carlo(ax, n):
    rng = np.random.default_rng(42)
    x_rand = rng.uniform(A, B, n)
    y_rand = f(x_rand)
    width = (B - A) / n * 0.9
    ax.bar(x_rand, y_rand, width=width, color=COLORS['monte_carlo'],
           edgecolor=COLORS['edge'], alpha=0.4, linewidth=0.8, label='Случайные выборки', zorder=2)
    ax.scatter(x_rand, y_rand, color=COLORS['monte_carlo'], s=30, edgecolors='white', linewidth=0.5, zorder=4)
    return monte_carlo_area(n)

PLOTTERS = {
    "ЛПР ": ("Левые прямоугольники ", plot_left_rectangles, left_rectangles_area),
    "ППР ": ("Правые прямоугольники ", plot_right_rectangles, right_rectangles_area),
    "СПР ": ("Средние прямоугольники ", plot_midpoint_rectangles, midpoint_rectangles_area),
    "ТР  ": ("Трапеции ", plot_trapezoids, trapezoids_area),
    "СИМП": ("Симпсон ", plot_simpson, simpson_area),
    "ММК ": ("Монте-Карло ", plot_monte_carlo, monte_carlo_area),
}

def plot_all_methods(n):
    fig, axes = plt.subplots(3, 2, figsize=(14, 16))
    axes = axes.ravel()
    label_true = f'Истинная площадь: {TRUE_VALUE:.8f}'
    for idx, (short_name, (title_ru, plot_func, area_func)) in enumerate(PLOTTERS.items()):
        ax = axes[idx]
        plot_base_function(ax, label_true)
        estimate = plot_func(ax, n)

        abs_err = abs(estimate - TRUE_VALUE)
        rel_err = abs_err / abs(TRUE_VALUE) * 100
        ax.set_title(f'{short_name}: {title_ru}\n'
                     f'Ŝ = {estimate:.8f} | Δ = {abs_err:.2e} | δ = {rel_err:.4f}%',
                     fontsize=11, pad=10, fontweight='bold')
        ax.legend(fontsize=9, loc='upper right', framealpha=0.9)
    fig.suptitle(f'Численное интегрирование $f(x) = \\arcsin(x/3)$ на $[0, 1.5]$,  n = {n}',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    print(f" Истинное значение интеграла: {TRUE_FORMULA}")
    print(f" Численно: {TRUE_VALUE:.10f}\n")
    print(f" Строим графики для n = {N_DEMO}")
    plot_all_methods(N_DEMO)
