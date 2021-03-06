# IMPORTACIÓN_DE_FUNCIONES

import pandas as pd

# BLOQUE_DE_DEFINICIÓN

dirTemperatura = 'temperatura_ambiente.txt' # Nombre del archivo donde se guardan las temperaturas ambientes
dirPresion = 'presion_atmosferica.txt' # Nombre del archivo donde se guardan las presiones atmosféricas
dirViento = 'velocidad_viento.txt' # Nombre del archivo donde se guardan las velocidades del viento
dirHumedad = 'humedad_relativa.txt' # Nombre del archivo donde se guardan las humedades relativas

estaciones = ['Otoño', 'Invierno', 'Primavera', 'Verano']

estacionInicial = 'Otoño'

# DEFINICIÓN_DE_FUNCIONES

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

    estacion = estacionInicial

    tabla = [] # Lista donde se guardaran las listas con los datos ordenados

    for i, dia in enumerate(listaTemperatura):
        numeroDia = listaTemperatura[i][0] # El número del día corresponde al primer elemento [0]
        if (eval(numeroDia) % 31 == 0):
            indexEstacionSiguiente = estaciones.index(estacion) + 1
            if (indexEstacionSiguiente >= len(estaciones)):
                indexEstacionSiguiente = 0
            
            estacion = estaciones[indexEstacionSiguiente]

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

                    tabla.append([numeroDia, hora, temperatura, humedad, viento, presion, estacion, '']) # Se agregan una lista con los datos ordenados a otra lista
    
    df = pd.DataFrame(tabla, columns=titulos) # Convierte la lista de listas en formato CSV
    df.to_csv('climas.csv') # Crea el nuevo archivo climas.csv

# Predice el clima de los días registrados en climas.csv
# Entrada: No hay entrada
# Salida: No hay salida
def simularClima():
    df = pd.read_csv('climas.csv', index_col=0) # Carga el archivo climas.csv
    chancesLluvia = 0
    chancesSoleado = 0
    chancesNubosidad = 0

    for index, registro in df.iterrows():
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

        if ((index - 8) >= 0): # Se descartan los dos primeros días
            climaAnteayer = df.loc[(index - 8), 'Clima']
            climaAyer = df.loc[(index - 4), 'Clima']

            if (climaAnteayer == 'Soleado'):
                chancesSoleado = chancesSoleado + 1
            elif (climaAnteayer == 'Nubosidad'):
                chancesNubosidad = chancesNubosidad + 1
            else:
                chancesLluvia = chancesLluvia + 1
            
            if (climaAyer == 'Soleado'):
                chancesSoleado = chancesSoleado + 1
            elif (climaAyer == 'Nubosidad'):
                chancesNubosidad = chancesNubosidad + 1
            else:
                chancesLluvia = chancesLluvia + 1

        if ((index + 1) % 4 == 0): # Cada cuatro registro se cambia un día
            mayor = max([chancesLluvia, chancesSoleado, chancesNubosidad])    
            clima = ''

            if (mayor == chancesSoleado):
                clima = 'Soleado'
            if (mayor == chancesNubosidad):
                clima = 'Nubosidad'
            if (mayor == chancesLluvia):
                clima = 'Lluvia'
            
            if (index != 0):
                df.loc[index - 3, 'Clima'] = clima
                df.loc[index - 2, 'Clima'] = clima
                df.loc[index - 1, 'Clima'] = clima
                df.loc[index, 'Clima'] = clima

            chancesLluvia = 0
            chancesSoleado = 0
            chancesNubosidad = 0
    
    df.to_csv('climas.csv')
    
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
    dfReales = pd.read_csv('reales.csv', index_col=0) # Carga el archivo reales.csv
    dfClimas = pd.read_csv('climas.csv', index_col=0) # Carga el archivo climas.csv
    aciertos = 0
    totales = len(dfReales.index) # Obtiene la cantidad de registros en reales.csv
    
    for i, registro in dfReales.iterrows():
        climaReal = registro['Clima'] # Obtiene el clima real
        climaSimulado = dfClimas.loc[(i * 4), 'Clima'] # Obtiene el clima simulado a partir del índice
        print(climaSimulado)
        if (climaReal == climaSimulado):
            aciertos = aciertos + 1
    fallos = totales - aciertos
    print('El modelo naive acertó en', aciertos, 'predicciones, y falló en', fallos)
    return (aciertos, fallos)

procesarVariables()
print("Se creó el archivo climas.csv correctamente")
simularClima()
print("Se simuló correctamente el clima de 120 días")
compararResultados()



    