import numpy as np

# Класична матриця виграшів для гри камінь-ножиці-папір
# Рядки — гравець A, стовпці — гравець B
payoff_matrix = np.array([
    [ 0, -1,  1],  # Камінь
    [ 1,  0, -1],  # Ножиці
    [-1,  1,  0]   # Папір
])

def optimal_strategy_A(matrix):
    # Вибираємо найменші втрати для кожної стратегії A
    return np.argmin(matrix, axis=1)

def optimal_strategy_B(matrix):
    # Вибираємо найменші втрати для кожної стратегії B
    return np.argmin(matrix, axis=0)

def nash_equilibrium(matrix):
    a_opt = optimal_strategy_A(matrix)
    b_opt = optimal_strategy_B(matrix)
    nash_eq = [(i, j) for i in range(len(a_opt)) for j in range(len(b_opt))
               if a_opt[i] == j and b_opt[j] == i]
    return nash_eq

print("Матриця виграшів:")
print(payoff_matrix)

print("\nОптимальна стратегія гравця A (мінімальні втрати):")
print(optimal_strategy_A(payoff_matrix))

print("\nОптимальна стратегія гравця B (мінімальні втрати):")
print(optimal_strategy_B(payoff_matrix))

print("\nРівновага Неша:")
print(nash_equilibrium(payoff_matrix))