
# 1. Cargar los datos
datos <- read.csv(file.choose()) #Escogemos el archivo "vector_estimaciones.csv"

x <- datos$x # Extraemos la columna 'x' como un vector numérico

n <- length(x) # Tamaño de la muestra

hist(x, 
     main = "Histograma de Estimaciones",
     xlab = "Valores de x",
     ylab = "Frecuencia",
     col = "red",
     border = "black")

# Media
media_muestral <- mean(x)
cat("Media:", media_muestral, "\n")

# Desviación Estándar
desviacion_estandar <- sd(x)
cat("Desviación Estándar:", desviacion_estandar, "\n")

# --- PREGUNTA 2: Calcular P(X <= 5) 

prob_menor_5 <- pnorm(5, mean = media_muestral, sd = desviacion_estandar)

cat("=== PREGUNTA 2: Probabilidad P(X <= 5) ===\n")
cat("Probabilidad Teórica:", prob_menor_5, "(Prácticamente 0)\n\n")

# --- PREGUNTA 3: Calcular P(15 <= X <= 16) ---
# Calculamos la probabilidad acumulada hasta 16 y restamos la de hasta 15
prob_entre_15_16 <- pnorm(16, mean = media_muestral, sd = desviacion_estandar) - 
  pnorm(15, mean = media_muestral, sd = desviacion_estandar)

cat("=== PREGUNTA 3: Probabilidad P(15 <= X <= 16) ===\n")
cat("Resultado:", prob_entre_15_16, "\n")

# --- PREGUNTA 4: Intervalo de Confianza (para el 95% de nivel de confianza)
# Fórmula: Media +/- Z * (Desviación / Raiz(n))
n <- length(x)
nivel_confianza <- 0.95
z <- qnorm((1 + nivel_confianza) / 2) # Valor Z para 95% (aprox 1.96)

# Error estándar (usando la desviación de tus datos cargados)
error_estandar <- desviacion_estandar / sqrt(n)
limite_inferior <- media_muestral - z * error_estandar
limite_superior <- media_muestral + z * error_estandar

cat("=== PREGUNTA 4: Intervalo de Confianza 95% ===\n")
cat("Intervalo calculado con datos del CSV: [", limite_inferior, ", ", limite_superior, "]\n")

# --- PREGUNTA 5: Cuantiles ---
# Calculamos los cuantiles del vector que subiste
cuantiles_vector <- quantile(x, probs = c(0.05, 0.10, 0.50, 0.975))

cat("PREGUNTA 5: Cuantiles del vector cargado \n")
print(cuantiles_vector)
