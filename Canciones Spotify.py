import pandas as pd

# Sirve para cargar y generar las 36 URLs automáticamente
urls_github = []
base_url = 'https://raw.githubusercontent.com/lbabydany/Muestreo-2026/refs/heads/main/datos%20spotify/top_50_global_2024_semana_{}.txt'
for i in range(1, 37):
    urls_github.append(base_url.format(i))

lista_df = []

for url in urls_github:
    # Pandas descarga y lee el archivo directamente desde internet
    try:
        df_temp = pd.read_csv(url, sep='|', on_bad_lines='skip')
        lista_df.append(df_temp)
        print(f"Se cargó correctamente la URL.")
    except Exception as e:
        print(f"Hubo un error al leer la URL.\nDetalle del error: {e}")

# Unimos los archivos en tu Marco Muestral (Universo)
if lista_df:
    universo = pd.concat(lista_df, ignore_index=True)
    
    # Revisamos cuántas canciones hay y vemos las primeras filas
    print(f"\n¡Éxito! Tu Universo actual tiene {len(universo)} filas.")
    print("Muestra de los datos cargados desde GitHub:")
    print(universo[['artist_name', 'song_name', 'duration_ms']].head())


import math
import scipy.stats as stats

# ==============================================================================
# 1. LIMPIEZA DEL MARCO MUESTRAL
# ==============================================================================
# Eliminamos los duplicados usando el 'id' de la canción.
universo_unico = universo.drop_duplicates(subset=['id']).copy()

# Tamaño de nuestra población (N)
N = len(universo_unico)
print(f"Tamaño del Universo (N) sin canciones repetidas: {N} canciones.")

# Convertimos las duraciones a minutos y segundos para los cálculos
universo_unico['duracion_min'] = universo_unico['duration_ms'] / 60000
universo_unico['duracion_sec'] = universo_unico['duration_ms'] / 1000


# ==============================================================================
# 2. TOMA DE LA MUESTRA (n = 100)
# ==============================================================================
muestra = universo_unico.sample(n=100, random_state=42) 


# ==============================================================================
# 3. ESTIMACIÓN DE DURACIÓN Y PLAYLIST
# ==============================================================================
# Estimador de la media (y_bar) en minutos
promedio_min = muestra['duracion_min'].mean()
print(f"\n--- 1. Estimación de la Duración ---")
print(f"Duración promedio estimada por canción: {promedio_min:.2f} minutos.")

# Cálculo para la playlist de 3 horas (180 minutos)
minutos_playlist = 3 * 60
num_canciones = minutos_playlist / promedio_min
print(f"Para armar una playlist de 3 horas se requieren aproximadamente: {math.ceil(num_canciones)} canciones.")


# ==============================================================================
# 4. TAMAÑO MÍNIMO DE MUESTRA PARA UN INTERVALO DE CONFIANZA
# ==============================================================================
# Si la longitud del intervalo es de 10 segundos, el Margen de Error (E) es la mitad:
E = 10 / 2  # E = 5 segundos

# Asumiremos un Nivel de Confianza del 95% 
confianza = 0.95 
alpha = 1 - confianza
Z = stats.norm.ppf(1 - alpha/2) # Valor Z de la normal estándar (aprox. 1.96)

# Estimamos la Desviación Estándar (S) usando los datos de nuestra muestra previa
S_sec = muestra['duracion_sec'].std(ddof=1)

# Fórmula de tamaño de muestra
n0 = ((Z * S_sec) / E) ** 2

# Ajuste por Población Finita (FPC)
n_minimo = n0 / (1 + (n0 / N))

print(f"\n--- 2. Análisis del Tamaño de Muestra ---")
print(f"Nivel de Confianza asumido: {confianza*100}% (Z = {Z:.4f})")
print(f"Margen de error (E): {E} segundos")
print(f"Desviación estándar estimada (S): {S_sec:.2f} segundos")
print(f"Tamaño de muestra teórico (n0): {math.ceil(n0)} canciones")
print(f"Tamaño de muestra final ajustado por N: {math.ceil(n_minimo)} canciones.")