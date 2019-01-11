import random

dirTemperatura = 'temperatura_ambiente.txt' # Nombre del archivo donde se guardan las temperaturas ambientes
dirPresion = 'presion_atmosferica.txt' # Nombre del archivo donde se guardan las presiones atmosféricas
dirViento = 'velocidad_viento.txt' # Nombre del archivo donde se guardan las velocidades del viento
dirHumedad = 'humedad_relativa.txt' # Nombre del archivo donde se guardan las humedades relativas

def crearArchivos(dias):
    dia = 1
    temperatura = open(dirTemperatura, 'w')
    humedad = open(dirHumedad, 'w')
    presion = open(dirPresion, 'w')
    viento = open(dirViento, 'w')

    while (dia <= dias):
        humedad.write(generarDia(dia, 79, 3000, 100, 2))
        presion.write(generarDia(dia, 1016, 5, 1, 0))
        viento.write(generarDia(dia, 12, 10, 1, 0))
        temperatura.write(generarDia(dia, 20, 10, 1, 0))
        dia = dia + 1
    
    humedad.close()
    temperatura.close()
    presion.close()
    viento.close()

    print('Se creo correctamente') 


def generarDia(dia, inicial, radio, divisor, digitos):
    hora = 1
    linea = str(dia) + ','
    while (hora <= 4):
        horaStr = str(hora * 6) + ':00'
        if (horaStr == '6:00'):
            horaStr = '06:00'
        
        aleatorio = random.randrange((radio * -1), radio)
        valor = inicial + (aleatorio / divisor)
        valor = round(valor, digitos)

        final = ','
        if (hora == 4):
            final = ''

        linea = linea + horaStr + ',' + str(valor) + final
        hora = hora + 1
    return linea + '\n'

def generarReales():
    

crearArchivos(120)