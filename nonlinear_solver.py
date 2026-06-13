import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def f(x):
    sin_x = math.sin(x)
    if sin_x < 0: return None
    sqrt_sin = math.sqrt(sin_x)
    if sqrt_sin > 1: return None
    return math.asin(sqrt_sin) - 0.8
def f_derivative(x):
    sin_x = math.sin(x)
    cos_x = math.cos(x)
    if sin_x <= 0: return None
    denom = 2 * math.sqrt(sin_x) * math.sqrt(1 - sin_x)
    if abs(denom) < 1e-15: return None
    return cos_x / denom
def bisection(a, b, eps=1e-14, max_iter=10 ** 6):
    fa, fb = f(a), f(b)
    history = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        history.append((a, b, c, fa, fb, fc))
        if abs(b - a) < eps: return c, i + 1, history
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c, max_iter, history
def newton(x0, eps=1e-14, max_iter=10 ** 6):
    x = x0
    history = []
    for i in range(max_iter):
        fx = f(x)
        fpx = f_derivative(x)
        history.append((x, fx, fpx))
        if fpx is None or abs(fpx) < 1e-15: break
        x_new = x - fx / fpx
        if abs(x_new - x) < eps:
            history.append((x_new, f(x_new), None))
            return x_new, i + 1, history
        x = x_new
    return x, max_iter, history
def secant_method(x0, x1, eps=1e-14, max_iter=10 ** 6):
    x_prev, x_curr = x0, x1
    history = [(x_prev, x_curr)]
    for i in range(max_iter):
        f_prev = f(x_prev)
        f_curr = f(x_curr)
        if f_prev is None or f_curr is None: break
        denom = f_curr - f_prev
        if abs(denom) < 1e-15: break

        x_next = x_curr - f_curr * (x_curr - x_prev) / denom
        history.append((x_curr, x_next))

        if abs(x_next - x_curr) < eps:
            return x_next, i + 1, history
        x_prev, x_curr = x_curr, x_next
    return x_curr, max_iter, history

a, b, eps = 2, 3, 1e-14

print("=== МЕТОД БИСЕКЦИИ ===")
root_bis, iter_bis, hist_bis = bisection(a, b, eps)
print(f"Корень: {root_bis}")
print(f"Итераций: {iter_bis}\n")
print("=== МЕТОД КАСАТЕЛЬНЫХ ===")
root_new, iter_new, hist_new = newton(2.5, eps)
print(f"Корень: {root_new}")
print(f"Итераций: {iter_new}\n")
print("=== МЕТОД ХОРД ===")
root_sec, iter_sec, hist_sec = secant_method(a, b, eps)
print(f"Корень: {root_sec}")
print(f"Итераций: {iter_sec}\n")

x_vals = [2 + i * 0.005 for i in range(201)]
y_vals = [f(x) for x in x_vals]
x_large = [i * 0.01 for i in range(0, 1260)]
y_large = []
for x in x_large:
    val = f(x)
    y_large.append(val if val is not None else float('nan'))
plt.figure(figsize=(10, 6))
plt.plot(x_large, y_large, 'b-', linewidth=1.5)
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
plt.title('ГРАФИК ФУНКЦИИ f(x) = arcsin(√sin(x)) - 0.8 на интервале [0; 4π]', fontsize=12, fontweight='bold')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True, alpha=0.3)
plt.savefig('graph_function_large.png', dpi=150, bbox_inches='tight')
plt.close()
plt.figure(figsize=(10, 8))
n_show = min(10, len(hist_bis))
for i in range(n_show):
    a_i, b_i, c_i = hist_bis[i][0], hist_bis[i][1], hist_bis[i][2]
    plt.hlines(i, a_i, b_i, color='steelblue', linewidth=3, label='Интервал [a;b]' if i == 0 else "")
    plt.scatter([c_i], [i], color='red', s=40, zorder=5, label='Середина c' if i == 0 else "")
    plt.text(b_i + 0.02, i, f'итер. {i + 1}', fontsize=8, va='center')
plt.axvline(x=root_bis, color='green', linestyle='--', linewidth=1.5, label=f'Корень ≈ {root_bis:.6f}')
plt.gca().invert_yaxis()
plt.title('МЕТОД БИСЕКЦИИ: сужение интервала [a; b] по итерациям', fontsize=12, fontweight='bold')
plt.xlabel('x')
plt.ylabel('Номер итерации')
plt.legend(loc='best')
plt.grid(True, alpha=0.3, axis='x')
plt.savefig('graph_bisection_horizontal.png', dpi=150, bbox_inches='tight')
plt.close()
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
colors = ['red', 'green', 'orange', 'purple', 'brown', 'pink']
for i, (a_i, b_i, c_i, fa_i, fb_i, fc_i) in enumerate(hist_bis[:6]):
    y_c = f(c_i)
    plt.axvline(x=c_i, color=colors[i % len(colors)], linestyle='--',
                alpha=0.7, linewidth=1, label=f'Итерация {i + 1}' if i < 3 else "")
    plt.scatter([c_i], [y_c], color=colors[i % len(colors)], s=50, zorder=5)
plt.scatter([root_bis], [0], color='red', s=100, marker='*', zorder=10, label=f'Корень: {root_bis:.6f}')
plt.title('МЕТОД БИСЕКЦИИ: деление отрезка пополам', fontsize=12, fontweight='bold')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.savefig('graph_bisection_method.png', dpi=150, bbox_inches='tight')
plt.close()
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
colors_newton = ['red', 'green', 'orange', 'purple', 'brown']
for i, (x_i, fx_i, fpx_i) in enumerate(hist_new[:5]):
    if fpx_i is None: continue
    x_tangent = [x_i - 0.3, x_i + 0.3]
    y_tangent = [fx_i + fpx_i * (x - x_i) for x in x_tangent]
    plt.plot(x_tangent, y_tangent, color=colors_newton[i % len(colors_newton)],
             linestyle='--', linewidth=1.5, alpha=0.7,
             label=f'Касательная {i + 1}' if i < 2 else "")
    plt.scatter([x_i], [fx_i], color=colors_newton[i % len(colors_newton)], s=60, zorder=5)
    x_next = x_i - fx_i / fpx_i
    plt.scatter([x_next], [0], color=colors_newton[i % len(colors_newton)],
                marker='x', s=80, linewidth=2, zorder=5)
plt.scatter([root_new], [0], color='red', s=120, marker='*', zorder=10, label=f'Корень: {root_new:.6f}')
plt.title('МЕТОД КАСАТЕЛЬНЫХ: движение к корню по касательным', fontsize=12, fontweight='bold')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.savefig('graph_newton_method.png', dpi=150, bbox_inches='tight')
plt.close()
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
colors_sec = ['red', 'green', 'orange', 'purple', 'brown', 'pink']
for i, (x_prev, x_curr) in enumerate(hist_sec[:6]):
    y_prev = f(x_prev)
    y_curr = f(x_curr)
    if y_prev is None or y_curr is None: continue
    plt.plot([x_prev, x_curr], [y_prev, y_curr], color=colors_sec[i % len(colors_sec)],
             linestyle='-', linewidth=1.5, alpha=0.7,
             label=f'Хорда {i + 1}' if i < 2 else "")
    if abs(y_curr - y_prev) > 1e-15:
        x_intercept = x_curr - y_curr * (x_curr - x_prev) / (y_curr - y_prev)
        plt.axvline(x=x_intercept, color=colors_sec[i % len(colors_sec)], linestyle='--', alpha=0.4)
        plt.scatter([x_intercept], [0], color=colors_sec[i % len(colors_sec)], s=50, zorder=5)
plt.scatter([root_sec], [0], color='red', s=100, marker='*', zorder=10, label=f'Корень: {root_sec:.6f}')
plt.title('МЕТОД ХОРД: движение к корню по секущим', fontsize=12, fontweight='bold')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.savefig('graph_secant_method.png', dpi=150, bbox_inches='tight')
plt.close()

print("✅ Графики сохранены:")
print("   📄 graph_function_large.png       - общий вид функции")
print("   📄 graph_bisection_horizontal.png - сужение интервала (горизонтально)")
print("   📄 graph_bisection_method.png     - бисекция на графике функции")
print("    graph_newton_method.png        - метод касательных")
print("   📄 graph_secant_method.png        - метод хорд (секущих)")
