import random
import math
import numpy as np
import matplotlib.pyplot as plt

def f1(x):
    return math.sin(x)
def f2(x):
    return math.cos(x)

def monte_carlo_area(f1, f2, x_min, x_max, y_min, y_max, N):
    k = 0
    for i in range(N):
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)

        low = min(f1(x), f2(x))
        high = max(f1(x), f2(x))

        if low <= y <= high:
            k += 1

    S_rect = (x_max - x_min) * (y_max - y_min)
    return S_rect * k / N

def exact_area_analytic():
    x_intersect = math.pi / 4
    integral1 = (math.sin(x_intersect) + math.cos(x_intersect)) - (math.sin(-1) + math.cos(-1))
    integral2 = (-math.cos(1) - math.sin(1)) - (-math.cos(x_intersect) - math.sin(x_intersect))
    return integral1 + integral2

x_min = -1.0
x_max = 1.0
y_min = -1.0
y_max = 1.0
N = 10000
area = monte_carlo_area(f1, f2, x_min, x_max, y_min, y_max, N)
exact = exact_area_analytic()

print("Оценка площади:     ", round(area, 6))
print("Точная площадь:     ", round(exact, 6))
print("Погрешность:        ", round(abs(area - exact), 6))
print("Относительная погрешность:", round(abs(area - exact) / exact * 100, 4), "%")


# Построение графика
def plot_graph():
    x = np.linspace(x_min, x_max, 1000)
    y1 = np.sin(x)
    y2 = np.cos(x)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y1, label='sin(x)', color='blue', linewidth=2)
    plt.plot(x, y2, label='cos(x)', color='red', linewidth=2)
    plt.fill_between(x, y1, y2, color='gray', alpha=0.4, label='Площадь между кривыми')

    plt.axhline(y=0, color='black', linewidth=0.5)
    plt.axvline(x=0, color='black', linewidth=0.5)
    plt.grid(True, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Площадь между sin(x) и cos(x) на [-1, 1]')
    plt.legend(loc='best')
    plt.show()
plot_graph()
