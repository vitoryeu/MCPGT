import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sympy import symbols, Eq, solve

# Підготовка вихідних даних
market_data = {
    'price_levels': {
        'EcoRide': [10000, 12000, 14000],
        'SpeedGo': [10000, 12000, 14000]
    },
    'costs': {
        'EcoRide': {
            'fixed': 300000,
            'variable': 6000
        },
        'SpeedGo': {
            'fixed': 280000,
            'variable': 5800
        }
    },
    'demand_parameters': {
        'base_demand': 500,
        'price_sensitivity': 0.03,
        'cross_sensitivity': 0.02
    }
}

# Функції для обчислень
def calculate_demand(price_own, price_competitor, demand_parameters):
    base_demand = demand_parameters['base_demand']
    price_sensitivity = demand_parameters['price_sensitivity']
    cross_sensitivity = demand_parameters['cross_sensitivity']
    demand = base_demand - price_sensitivity * price_own + cross_sensitivity * price_competitor
    return max(0, demand)

def calculate_profit(price, quantity, fixed_costs, variable_cost_per_unit):
    revenue = price * quantity
    total_cost = fixed_costs + (variable_cost_per_unit * quantity)
    profit = revenue - total_cost
    return profit

def search_mixed_strategies(payment_matrix, company_name):
    q1, q2, q3 = symbols('q1 q2 q3')
    A = payment_matrix
    eq1 = Eq(A[0,0]*q1 + A[0,1]*q2 + A[0,2]*q3, A[1,0]*q1 + A[1,1]*q2 + A[1,2]*q3)
    eq2 = Eq(A[1,0]*q1 + A[1,1]*q2 + A[1,2]*q3, A[2,0]*q1 + A[2,1]*q2 + A[2,2]*q3)
    eq3 = Eq(q1 + q2 + q3, 1)
    solution = solve((eq1, eq2, eq3), (q1, q2, q3))
    print("\nЙмовірності використання змішаних стратегій для " +  company_name + " (q1, q2, q3):")
    print(solution)
    if all(value >= 0 for value in solution.values()):
        print("\nРішення є валідним: всі ймовірності невід'ємні")
    else:
        print("\n⚠️ Увага: деякі ймовірності від'ємні або некоректні.")

# Побудова платіжних матриць
prices_A = market_data['price_levels']['EcoRide']
prices_B = market_data['price_levels']['SpeedGo']
costs_A = market_data['costs']['EcoRide']
costs_B = market_data['costs']['SpeedGo']
demand_parameters = market_data['demand_parameters']

payoff_A = np.zeros((len(prices_A), len(prices_B)))
payoff_B = np.zeros((len(prices_A), len(prices_B)))

for i, price_A in enumerate(prices_A):
    for j, price_B in enumerate(prices_B):
        demand_A = calculate_demand(price_A, price_B, demand_parameters)
        demand_B = calculate_demand(price_B, price_A, demand_parameters)
        profit_A = calculate_profit(price_A, demand_A, costs_A['fixed'], costs_A['variable'])
        profit_B = calculate_profit(price_B, demand_B, costs_B['fixed'], costs_B['variable'])
        payoff_A[i, j] = profit_A
        payoff_B[i, j] = profit_B

# Аналіз чистих стратегій
def analyze_saddle_point(matrix, player_label, row_labels, col_labels):
    row_mins = np.min(matrix, axis=1)
    col_maxs = np.max(matrix, axis=0)
    saddle_points = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == row_mins[i] and matrix[i, j] == col_maxs[j]:
                saddle_points.append((i, j, matrix[i, j]))
    df = pd.DataFrame(matrix, index=row_labels, columns=col_labels)
    plt.figure(figsize=(8, 6))
    sns.heatmap(df, annot=True, fmt=".0f", cmap="YlGnBu", center=np.mean(matrix))
    plt.title(f"Матриця виграшів для {player_label}")
    plt.tight_layout()
    plt.show()
    print(f"\nАналіз для {player_label}:")
    print(f"Мінімуми по рядках: {row_mins}")
    print(f"Максимуми по стовпцях: {col_maxs}")
    if saddle_points:
        print("\nСідлові точки знайдено:")
        for point in saddle_points:
            print(f"Позиція ({point[0]+1}, {point[1]+1}) зі значенням {point[2]:.0f}")
    else:
        print("\nСідлової точки не знайдено. Потрібно шукати змішані стратегії.")
    return saddle_points

row_labels = [f"EcoRide:{p}" for p in prices_A]
col_labels = [f"SpeedGo:{p}" for p in prices_B]

saddle_points_A = analyze_saddle_point(payoff_A, "EcoRide (A)", row_labels, col_labels)
saddle_points_B = analyze_saddle_point(payoff_B, "SpeedGo (B)", row_labels, col_labels)

# Пошук змішаних стратегій (якщо потрібно)
if not saddle_points_A:
    search_mixed_strategies(payoff_A, "EcoRide")
if not saddle_points_B:
    search_mixed_strategies(payoff_B, "SpeedGo")