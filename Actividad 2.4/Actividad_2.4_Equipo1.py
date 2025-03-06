#Roberto Torres
#David Hernandez
#Roberto Bruijnzeels

import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

df = pd.read_csv('Actividad 2.4/mochila_almno_.csv')

# Función para convertir listas en formato string a listas de enteros
def convert_string_to_list(value):
    return list(map(int, value.strip('[]').split()))

# Aplicar la conversión a las columnas de pesos y precios
df["Weights"] = df["Weights"].apply(convert_string_to_list)
df["Prices"] = df["Prices"].apply(convert_string_to_list)

# Lista para almacenar los resultados
best_picks_list = []
best_price_list = []
average_weights_list = []
average_prices_list = []
cost_function_list = []
constraint_list = []

# Iterar sobre cada problema en el dataset
for index, row in df.iterrows():
    weights = row["Weights"]
    prices = row["Prices"]
    capacity = row["Capacity"]
    num_items = len(weights)

    # Definir el problema de optimización
    prob = LpProblem("Knapsack_Problem", LpMaximize)

    # Definir las variables de decisión (0 o 1 para cada ítem)
    x = [LpVariable(f"x{i}", cat="Binary") for i in range(num_items)]

    # Función objetivo: maximizar el valor total de los ítems seleccionados
    prob += lpSum(prices[i] * x[i] for i in range(num_items)), "Total Value"

    # Restricción: la suma de los pesos no debe exceder la capacidad de la mochila
    prob += lpSum(weights[i] * x[i] for i in range(num_items)) <= capacity, "Weight Constraint"

    # Guardar la función objetivo y restricción como cadenas
    cost_function_str = f"Maximize: {' + '.join([f'{prices[i]}*x{i}' for i in range(num_items)])}"
    constraint_str = f"Constraint: {' + '.join([f'{weights[i]}*x{i}' for i in range(num_items)])} <= {capacity}"

    # Resolver el problema
    prob.solve()

    # Obtener la solución óptima
    best_picks = [int(x[i].varValue) for i in range(num_items)]
    best_price = sum(prices[i] * best_picks[i] for i in range(num_items))

    # Calcular los promedios
    avg_weight = sum(weights) / num_items
    avg_price = sum(prices) / num_items

    # Guardar los resultados en listas
    best_picks_list.append(best_picks)
    best_price_list.append(best_price)
    average_weights_list.append(avg_weight)
    average_prices_list.append(avg_price)
    cost_function_list.append(cost_function_str)
    constraint_list.append(constraint_str)

# Agregar los resultados al dataframe
df["Best picks"] = best_picks_list
df["Best price"] = best_price_list
df["Average Weights"] = average_weights_list
df["Average Prices"] = average_prices_list
df["Cost function"] = cost_function_list
df["Constraint"] = constraint_list

# Guardar el resultado en un nuevo archivo CSV
output_file = "mochila_resultado.csv"
df.to_csv(output_file, index=False)

print(f"Archivo guardado: {output_file}")
