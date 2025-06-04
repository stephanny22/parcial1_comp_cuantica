#!/usr/bin/python3
from sys import argv
import time
import sys

# Instrucciones
d = {}
E_aceptacion = set()
tipo = None
estado = '0'

# Identificar si el programa es AFD o MT
programa = open(argv[1])
for linea in programa:
    partes = linea.strip().split()
    if not partes:
        continue
    if len(partes) == 3:
        tipo = 'AFD'
        q, s, n = partes
        if '*' in q:
            q = q.strip('*')
            E_aceptacion.add(q)
        d[q, s] = n
    elif len(partes) == 5:
        tipo = 'MT'
        q_actual, simbolo_lectura, simbolo_escritura, direccion, q_nuevo = partes
        d[(q_actual, simbolo_lectura)] = (simbolo_escritura, direccion.lower(), q_nuevo)
programa.close()

# Mensaje de selección
if tipo == 'AFD':
    print("Has seleccionado Automata finito determinista")
elif tipo == 'MT':
    print("Has seleccionado Maquina de Turing")
else:
    print("La entrada no coincide con MT ni AFD. Por favor revise el archivo programa.txt")
    exit(1)

# Función AFD
def AFD(d, q0, E_aceptacion, cinta):
    q = q0
    for simbolo in cinta:
        q = d[q, simbolo]
    return q in E_aceptacion

mensaje = {True: 'Aceptada', False: 'Rechazada'}

if tipo == 'AFD':
    cintas = open(argv[2])
    for cinta in cintas:
        cinta = cinta.strip()
        print('La entrada', cinta, "es", mensaje[AFD(d, '0', E_aceptacion, cinta)])
    cintas.close()

# Función MT corregida
def MT(d, estado_actual, simbolo):
    if (estado_actual, simbolo) in d:
        simbolo_escrito, direccion, nuevo_estado = d[(estado_actual, simbolo)]
        return nuevo_estado, simbolo_escrito, direccion
    else:
        return None, None, None

# Simulación de MT
if tipo == "MT":
    with open(argv[2]) as archivo:
        contenido = archivo.read().replace('\n', '')
    letras = list(contenido)

    i = 0  # Posición de la cabeza
    estado = '0'

    while True:
        if i < 0:
            letras.insert(0, '_')
            i = 0
        elif i >= len(letras):
            letras.append('_')

        simbolo_actual = letras[i]
        estado_final, simbolo_escrito, direccion = MT(d, estado, simbolo_actual)

        # Mostrar cinta con cabeza
        antes = ''.join(letras[:i])
        actual = letras[i]
        despues = ''.join(letras[i+1:])
        linea = antes + f"({actual})" + despues

        if i > 0:
            sys.stdout.write('\033[2A')  # Subir 2 líneas
        sys.stdout.write('\033[2K\r' + linea + '\n')
        sys.stdout.write('\033[2K\r' + ' ' * len(antes) + ' ↑\n')
        sys.stdout.flush()
        time.sleep(0.2)

        if estado_final is None:
            sys.stdout.write('\033[3A')
            sys.stdout.write('\033[2K\r')
            sys.stdout.write('\033[3B')
            sys.stdout.flush()
            print("No existe ninguna instrucción para el estado y el símbolo actual")
            break

        letras[i] = simbolo_escrito
        estado = estado_final

        if direccion == 'r':
            i += 1
        elif direccion == 'l':
            i -= 1
        else:
            print("Dirección inválida:", direccion)
            break