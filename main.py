# IMPORTACIÓN_DE_FUNCIONES

import pandas as pd

# BLOQUE_DE_DEFINICIÓN

dirTemperatura = 'temperatura_ambiente.txt'
dirPresion = 'presion_atmosferica.txt'
dirViento = 'velocidad_viento.txt'
dirHumedad = 'humedad_relativa.txt'
ejecutar = True

# DEFINICIÓN_DE_FUNCIONES

# Función encargada de ejecutar el menú principal
# Entrada: Sin parámetros de entrada 
# Salida: Sin valores de retorno
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

    tabla = []

    for i, dia in enumerate(listaTemperatura):
        numeroDia = listaTemperatura[i][0]
        for j, elemento in enumerate(dia):
            if (j != 0):
                if (j % 2 == 0): # Si es par, es porque corresponde a un valor y no una hora
                    hora = listaTemperatura[i][j - 1]
                    temperatura = listaTemperatura[i][j]
                    viento = listaViento[i][j]
                    presion = listaPresion[i][j]
                    humedad = listaHumedad[i][j]

                    tabla.append([numeroDia, hora, temperatura, humedad, viento, presion, '', ''])
    
    df = pd.DataFrame(tabla, columns=titulos)
    df.to_csv('climas.csv')

def predecirClima():
    chancesLluvia = 0
    chancesSoleado = 0
    chancesNubosidad = 0

    df = pd.read_csv('climas.csv')

    ultimoDia = df.tail(4)

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
        elif (H <= 79 and H >= 78): # PROBLEMA: ¿Qué pasa si está entre 79 y 80?
            chancesNubosidad = chancesNubosidad + 1
            chancesLluvia = chancesLluvia + 2
        elif (H < 78): # Cambiar por else cuando se solucione el problema de arriba
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
    if (mayor == chancesLluvia):
        print('Lluvia')
    if (mayor == chancesNubosidad):
        print('Nubosidad')
    

def abrirArchivo(nombre):
    archivo = open(nombre, 'r')
    contenido = archivo.readlines()
    archivo.close()
    return contenido

def archivoALista(contenido):
    dias = []
    for linea in contenido:
        lineaSinSalto = linea.strip()
        dias.append(lineaSinSalto.split(','))
    return dias

def compararResultados():
    dfReales = pd.read_csv('reales.csv')
    dfClimas = pd.read_csv('climas.csv')
    aciertos = 0
    totales = len(dfReales.index)
    
    for i, registro in dfReales.iterrows():
        climaReal = registro['Clima']
        climaSimulado = dfClimas.loc[(i * 4), 'Clima']
        if (climaReal == climaSimulado):
            aciertos = aciertos + 1
    fallos = totales - aciertos
    print('El modelo naive acertó en', aciertos, 'predicciones, y falló en', fallos)
    return (aciertos, fallos)

while (ejecutar): # Ciclo que se ejecuta para siempre, para que el menú esté disponible todo el tiempo
    menu()



    