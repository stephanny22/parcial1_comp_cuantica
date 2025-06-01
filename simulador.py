#!/usr/bin/python3
#Correr como $./simulador programa.txt cintas.txt para linux o MacOS
from sys import argv
import time
import sys
import os

d = {}
E_aceptacion = set()
tipo=None

#Identificar si el programa es AFD o MT
programa=open(argv[1])
for linea in programa:
    partes = linea.strip().split()
#AFD------------------------------------------------
    if not partes:
        continue 
    if len(partes) == 3:
        tipo = 'AFD'
        print("Has seleccionado Automata finito determinista")
        q, s, n = partes  # Asigna los tres elementos a q, s, n
        if '*' in q:
                q = q.strip('*')  # Elimina el asterisco del estado
                E_aceptacion.add(q)
        d[q, s] = n
#MT------------------------------------------------
    elif len(partes) == 5:
        tipo = 'MT'
        print("Has seleccionado Maquina de Turing")
#INVALIDO------------------------------------------------
    else:
        print("La entrada no coincide con MT ni AFD. Por favor revise el archivo programa.txt")
        exit(1)
programa.close()    
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
        print(cinta)
        print('La entrada',cinta," es ",mensaje[AFD(d,'0',E_aceptacion,cinta)])
    cintas.close()
#MT------------------------------------------------
def MT(d,q0,E_aceptacion,cinta):
    q=q0
    for simbolo in cinta:
        q=d[q,simbolo]
    return q in E_aceptacion

mensaje={True:'Aceptada',False:'Rechazada'}

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

    # Borra las dos líneas anteriores (si no es la primera iteración)
    if i > 0:
        sys.stdout.write('\033[2A')  # Mover cursor arriba 2 líneas

    sys.stdout.write('\033[2K\r')  # Borra línea actual
    sys.stdout.write(linea + '\n')  # Imprime la línea con el símbolo entre paréntesis
    sys.stdout.write('\033[2K\r')  # Borra línea actual para la flecha

    # Espacios para posicionar la flecha debajo del paréntesis izquierdo
    posicion_flecha = len(antes)  # Posición donde abre paréntesis '(' empieza
    sys.stdout.write(' ' * posicion_flecha + ' ↑\n')

    sys.stdout.flush()
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