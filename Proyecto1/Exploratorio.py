import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Cargar datos desde un archivo CSV
df = pd.read_csv('Proyecto1/Electric_Vehicle_Population_Size_History_By_County_.csv')

# Análisis Exploratorio de Datos (EDA)
# 1. Descripción del dataset
print("Información del dataset:")
print(df.info())
print("\nPrimeras filas del dataset:")
print(df.head())

# 2. Estadística descriptiva
print("\nEstadísticas descriptivas:")
print(df.describe())

# 3. Detección de valores faltantes y outliers
print("\nValores faltantes por columna:")
print(df.isnull().sum())

# Tratamiento preliminar de valores faltantes (rellenamos con la media en columnas numéricas)
df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)

# Identificación de outliers con boxplots
plt.figure(figsize=(12, 6))
sns.boxplot(data=df[['Battery Electric Vehicles (BEVs)', 'Plug-In Hybrid Electric Vehicles (PHEVs)',
                     'Electric Vehicle (EV) Total', 'Non-Electric Vehicle Total']])
plt.title("Detección de outliers")
plt.show()

# 4. Visualizaciones básicas
# Histogramas
df[['cantidad_autos_con_bateria_electrica', 'cantidad_autos_hibridos',
    'cantidad_autos_electricos', 'cantidad_autos_no_electricos']].hist(figsize=(12, 8), bins=20)
plt.suptitle("Distribución de vehículos por tipo")
plt.show()

# Relación entre autos eléctricos y estaciones de carga
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['cantidad_autos_electricos'], y=df['cantidad_autos'])
plt.xlabel("Cantidad de autos eléctricos")
plt.ylabel("Cantidad total de autos")
plt.title("Relación entre autos eléctricos y total de autos")
plt.show()

# Visualización de todas las variables relevantes
plt.figure(figsize=(12, 8))
df.drop(columns=['pais', 'estado', 'uso_auto']).hist(figsize=(12, 8), bins=20)
plt.suptitle("Distribución de todas las variables relevantes")
plt.show()

# 5. Identificación de relaciones
# Matriz de correlación
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de correlación entre variables")
plt.show()

# Optimización de estaciones de carga
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
    print("\nDistribución óptima de estaciones de carga por estado:")
    for i, estado in enumerate(estados):
        print(f"{estado}: {asignacion[i]} estaciones")
    print("Costo total mínimo de instalación:", res.fun)
else:
    print("No se encontró una solución óptima.")