#!/usr/bin/python3
#Correr como $./simulador programa.txt cintas.txt para linux o MacOS
from sys import argv
import time
import sys
#Intrucciones
d = {}
E_aceptacion = set()
tipo=None
estado='0'
#Identificar si el programa es AFD o MT
programa=open(argv[1])
for linea in programa:
    partes = linea.strip().split()
#AFD------------------------------------------------
    if not partes:
        continue 
    if len(partes) == 3:
        tipo = 'AFD'
        q, s, n = partes  # Asigna los tres elementos a q, s, n
        if '*' in q:
                q = q.strip('*')  # Elimina el asterisco del estado
                E_aceptacion.add(q)
        d[q, s] = n
#MT------------------------------------------------
    elif len(partes) == 5:
        tipo = 'MT'
        q_actual, simbolo_lectura, simbolo_escritura, direccion, q_nuevo = partes
        d[(q_actual, simbolo_lectura)] = (simbolo_escritura, direccion, q_nuevo)
programa.close()
#Mensaje de selección
#AFD------------------------------------------------
if(tipo == 'AFD'):
            print("Has seleccionado Automata finito determinista")
#MT------------------------------------------------
elif (tipo == 'MT'):
        print("Has seleccionado Maquina de Turing")


#INVALIDO------------------------------------------------
else:
    print("La entrada no coincide con MT ni AFD. Por favor revise el archivo programa.txt")
    exit(1)
#AFD------------------------------------------------
def AFD(d,q0,E_aceptacion,cinta):
    q=q0
    for simbolo in cinta:
        q=d[q,simbolo]
    return q in E_aceptacion

mensaje={True:'Aceptada',False:'Rechazada'}

if tipo == 'AFD':
    cintas=open(argv[2])
    for cinta in cintas:
        cinta=cinta.strip()
        print(d)
        print('La entrada',cinta," es ",mensaje[AFD(d,'0',E_aceptacion,cinta)])
    cintas.close()
#MT------------------------------------------------
def MT(d,q0,letra):
    #print(f"se ingresa d:{d} q0:{q0} letra:{letra}")
    q=q0
    if(q, letra) in d:
        #La instrucción existe
        letra, direccion, q = d[(q, letra)]

        return q,letra
        #La instrucción NO existe
    else:

        q, letra= None, None 
        return q,letra

if tipo == "MT":
    with open(argv[2]) as archivo:
    # Leer todo el archivo y eliminar saltos de línea
        contenido = archivo.read().replace('\n', '')

    # Crear lista con cada letra individual
    letras = list(contenido)

    # Imprimir cada letra en una línea
for i in range(len(letras)):

    antes = ''.join(letras[:i])
    actual = letras[i]
    despues = ''.join(letras[i+1:])
    linea = antes + f"({actual})" + despues  # Carácter seleccionado entre paréntesis

    # Se evalúa el valor
    estado_final, letra_final = MT(d, estado, letras[i])

    # Borra las dos líneas anteriores (si no es la primera iteración)
    if i > 0:
        sys.stdout.write('\033[2A')  # Subir 2 líneas (línea + flecha)
        sys.stdout.write('\033[2K\r')  # Borrar línea 1 (cadena con paréntesis)
        sys.stdout.write('\033[1B')    # Bajar 1 línea
        sys.stdout.write('\033[2K\r')  # Borrar línea 2 (flecha)
        sys.stdout.write('\033[1A')    # Subir 1 línea para posición correcta
    # Mostrar la línea con el símbolo seleccionado
    sys.stdout.write(linea + '\n')
    posicion_flecha = len(antes)
    sys.stdout.write(' ' * posicion_flecha + ' ↑\n')
    sys.stdout.flush()

    # Verifica si no hay transición posible
    if estado_final is None or letra_final is None:
        sys.stdout.write('\033[3A')   # Subir 3 líneas (o la cantidad suficiente para llegar a la línea anterior)
        sys.stdout.write('\033[2K\r')  # Borrar esa línea
        sys.stdout.write('\033[3B')   # Bajar 3 líneas para volver a la línea actual (con paréntesis y flecha)
        sys.stdout.flush()
        print("No existe ninguna instrucción para el estado y el simbolo actual")
        exit()

    letras[i] = letra_final
    estado = estado_final

    time.sleep(0.2)

# diccionario_programa={}
# Estados_aceptación=set()
# programa=open(argv[1])
# for linea in programa:
#     q_actual,s,q_futura=linea.split()
#     if '*' in q_actual:
#         q_actual=q_actual.strip('*')
#         Estados_aceptación.add(q_actual)
#     diccionario_programa[q_actual,s]=q_futura
# programa.close()

# # Leer cada línea del archivo 'programa.txt'
# def AFD(diccionario_programa,q0,Estados_aceptación,cinta):
#     q_actual=q0
#     for simbolo in cinta:
#         q_actual=diccionario_programa[q_actual,simbolo]
#     return q_actual in Estados_aceptación

# mensaje={True:'Aceptada',False:'Rechazada'}

# cintas=open(argv[2])
# for cinta in cintas:
#     cinta=cinta.strip()
#     print(f"La entrada {cinta} es {mensaje[AFD(diccionario_programa,'0',Estados_aceptación,cinta)]}")

# cintas.close()