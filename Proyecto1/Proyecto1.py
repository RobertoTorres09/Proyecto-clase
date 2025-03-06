import pandas as pd
from scipy.optimize import linprog

# Problema de optimización de estaciones de carga para autos eléctricos
# 
# Se busca optimizar la distribución de estaciones de carga para autos eléctricos en distintos estados.
# Los datos provienen de un archivo CSV que contiene información sobre el país, estado, tipo de auto (pasajero o camión),
# cantidad de autos con batería eléctrica (BEV), cantidad de autos híbridos, cantidad de autos eléctricos (EV),
# cantidad de autos no eléctricos, cantidad de autos en total y el porcentaje de autos eléctricos.
# 
# El objetivo es minimizar el costo total de instalación de estaciones de carga asegurando que la distribución de estaciones
# en cada estado sea proporcional a la cantidad de autos eléctricos presentes en cada uno.

# Cargar datos desde un archivo CSV
df = pd.read_csv('Proyecto1/Electric_Vehicle_Population_Size_History_By_County_.csv')

# Filtrar solo autos eléctricos
df_ev = df[df['porcentaje_autos_electricos'] > 0]

# Definir los parámetros del problema
estados = df_ev['estado'].unique()
cantidad_autos = df_ev.groupby('estado')['cantidad_autos_electricos'].sum().tolist()
num_estaciones = df_ev.groupby('estado')['cantidad_autos'].count().tolist()
costo_instalacion = [500000 for _ in estados]  # Suposición de costo fijo por estado
capacidad_carga = [5 for _ in estados]  # Suposición de capacidad fija por estación

total_estados = len(estados)

# Matriz de coeficientes de restricciones
A_eq = [[1 if j == i else 0 for j in range(total_estados)] for i in range(total_estados)]
b_eq = num_estaciones  # Restricción de estaciones de carga

# Coeficientes de la función objetivo (minimizar el costo total de instalación)
c = costo_instalacion

# Definir las restricciones de capacidad de carga
bounds = [(0, None) for _ in range(total_estados)]

# Resolver el problema de optimización
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

# Mostrar resultados
if res.success:
    asignacion = res.x.round().astype(int)
    print("Distribución óptima de estaciones de carga por estado:")
    for i, estado in enumerate(estados):
        print(f"{estado}: {asignacion[i]} estaciones")
    print("Costo total mínimo de instalación:", res.fun)
else:
    print("No se encontró una solución óptima.")
