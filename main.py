# IMPORTACIÓN_DE_FUNCIONES

import pandas as pd

# BLOQUE_DE_DEFINICIÓN

dirTemperatura = 'temperatura_ambiente.txt' # Nombre del archivo donde se guardan las temperaturas ambientes
dirPresion = 'presion_atmosferica.txt' # Nombre del archivo donde se guardan las presiones atmosféricas
dirViento = 'velocidad_viento.txt' # Nombre del archivo donde se guardan las velocidades del viento
dirHumedad = 'humedad_relativa.txt' # Nombre del archivo donde se guardan las humedades relativas
ejecutar = True

# DEFINICIÓN_DE_FUNCIONES

# Ejecuta el menú para que el usuario pueda interactuar con el programa
# Entrada: No hay entrada
# Salida: No hay salida
def menu():
    o = -1
    while (o != 0 and o != 1 and o != 2 and o != 3):
        print("\n\nMENÚ\n")
        print("\n1.- Procesar variables")
        print("\n2.- Simular y predecir climas")
        print("\n3.- Comparar resultados")
        print("\n0.- SALIR")
        o = eval(input("\nSeleccione una opción: "))
    
    if (o == 1):
        procesarVariables()
        print("Se creó el archivo climas.csv correctamente")
    elif (o == 2):
        predecirClima()
    elif (o == 3):
        compararResultados()
    else:
        ejecutar = False

# Procesa todas las variables para crear el archivo CSV final
# Entrada: No hay entrada
# Salida: No hay salida
def procesarVariables():
    titulos = ['Dia', 'Hora', 'Temperatura ambiente', 'Humedad relativa', 'Velocidad del viento', 'Presion atmosferica', 'Estacion', 'Clima']
    archivoTemperatura = abrirArchivo(dirTemperatura)
    archivoViento = abrirArchivo(dirViento)
    archivoPresion = abrirArchivo(dirPresion)
    archivoHumedad = abrirArchivo(dirHumedad)

    listaTemperatura = archivoALista(archivoTemperatura)
    listaViento = archivoALista(archivoViento)
    listaPresion = archivoALista(archivoPresion)
    listaHumedad = archivoALista(archivoHumedad)

    tabla = [] # Lista donde se guardaran las listas con los datos ordenados

    for i, dia in enumerate(listaTemperatura):
        numeroDia = listaTemperatura[i][0] # El número del día corresponde al primer elemento [0]
        for j, elemento in enumerate(dia):
            if (j != 0):
                if (j % 2 == 0): # Si es par
                    # Si el registro [j] es de un numero par, es porque el elemento 
                    # corresponde a un valor y no a una hora
                    hora = listaTemperatura[i][j - 1] # La hora va a ser igual al elemento anterior [j - 1]
                    temperatura = listaTemperatura[i][j]
                    viento = listaViento[i][j]
                    presion = listaPresion[i][j]
                    humedad = listaHumedad[i][j]

                    tabla.append([numeroDia, hora, temperatura, humedad, viento, presion, '', '']) # Se agregan una lista con los datos ordenados a otra lista
    
    df = pd.DataFrame(tabla, columns=titulos) # Convierte la lista de listas en formato CSV
    df.to_csv('climas.csv') # Crea el nuevo archivo climas.csv

# Predice el clima del último día registrado
# Entrada: No hay entrada
# Salida: No hay salida
def predecirClima():
    chancesLluvia = 0
    chancesSoleado = 0
    chancesNubosidad = 0

    df = pd.read_csv('climas.csv') # Carga el archivo climas.csv

    ultimoDia = df.tail(4) # Obtiene los últimos 4 registros, es decir, el último día

    for index, registro in ultimoDia.iterrows():
        T = registro['Temperatura ambiente']
        H = registro['Humedad relativa']
        V = registro['Velocidad del viento']
        P = registro['Presion atmosferica']
        estacion = registro['Estacion']

        if (P >= 1015 and P <= 1016):
            chancesNubosidad = chancesNubosidad + 1
        if (P >= 1016 and P <= 1017):
            chancesSoleado = chancesSoleado + 2
            chancesLluvia = chancesLluvia + 1
        if (P > 1017):
            chancesLluvia = chancesLluvia + 2

        if (V <= 12):
            chancesSoleado = chancesSoleado + 2
        else:
            chancesNubosidad = chancesNubosidad + 2
            chancesLluvia = chancesLluvia + 1

        if (T < 20):
            chancesLluvia = chancesLluvia + 2
        else:
            chancesSoleado = chancesSoleado + 2
            chancesNubosidad = chancesNubosidad + 1

        if (H >= 80):
            chancesSoleado = chancesSoleado + 1
        elif (H < 80 and H >= 78): # NOTA: Se cambió la condición, ya que no contemplaba el rango ]79, 80[
            chancesNubosidad = chancesNubosidad + 1
            chancesLluvia = chancesLluvia + 2
        else:
            chancesLluvia = chancesLluvia + 1

        if (estacion == 'Invierno'):
            chancesNubosidad = chancesNubosidad + 2
            chancesLluvia = chancesLluvia + 1
        elif (estacion == 'Primavera'):
            chancesSoleado = chancesSoleado + 1
            chancesNubosidad = chancesNubosidad + 1
            chancesLluvia = chancesLluvia + 1
        elif (estacion == 'Otoño'):
            chancesSoleado = chancesSoleado + 1
            chancesNubosidad = chancesNubosidad + 2
        else:
            chancesSoleado = chancesSoleado + 3
    
    mayor = max([chancesLluvia, chancesSoleado, chancesNubosidad])

    # PROBLEMA: ¿Qué pasa si dos o más chances son iguales?
    if (mayor == chancesSoleado):
        print('Soleado')
    if (mayor == chancesNubosidad):
        print('Nubosidad')
    if (mayor == chancesLluvia):
        print('Lluvia')
    
# Abre un archivo para devolver su contenido
# Entrada: El nombre del archivo que se abrirá
# Salida: El contenido del archivo
def abrirArchivo(nombre):
    archivo = open(nombre, 'r')
    contenido = archivo.readlines()
    archivo.close()
    return contenido

# Convierte el archivo a una lista con cada elemento y día separados
# Entrada: El contenido del archivo devuelto por abrirArchivo(nombre)
# Salida: Retorna la lista de días con cada elemento separado en cada día
def archivoALista(contenido):
    dias = []
    for linea in contenido:
        lineaSinSalto = linea.strip()
        elementos = lineaSinSalto.split(',') # Separa la línea donde encuentre una coma
        dias.append(elementos) # Agrega la lista de elementos a la lista de días
    return dias

# Compara los resultados reales contra los resultados simulados
# Entrada: No hay entrada
# Salida: Retorna el número de aciertos y el número de fallos
def compararResultados():
    dfReales = pd.read_csv('reales.csv') # Carga el archivo reales.csv
    dfClimas = pd.read_csv('climas.csv') # Carga el archivo climas.csv
    aciertos = 0
    totales = len(dfReales.index) # Obtiene la cantidad de registros en reales.csv
    
    for i, registro in dfReales.iterrows():
        climaReal = registro['Clima'] # Obtiene el clima real
        climaSimulado = dfClimas.loc[(i * 4), 'Clima'] # Obtiene el clima simulado a partir del índice
        if (climaReal == climaSimulado):
            aciertos = aciertos + 1
    fallos = totales - aciertos
    print('El modelo naive acertó en', aciertos, 'predicciones, y falló en', fallos)
    return (aciertos, fallos)

while (ejecutar): # Ciclo que se ejecuta para siempre, para que el menú esté disponible todo el tiempo
    menu()



    