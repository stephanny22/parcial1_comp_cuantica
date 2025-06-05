#!/usr/bin/python3
from sys import argv
import time
import sys

# Instrucciones
d = {}
E_aceptacion = set()
tipo = None
estado = '0'

# Determinar el tipo de autómata al leer el archivo de definiciones
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

# ✅ Mensaje indicando el tipo de autómata
if tipo == 'AFD':
    print("Has seleccionado Automata Finito Determinista (AFD)")
elif tipo == 'MT':
    print("Has seleccionado Máquina de Turing (MT)")
else:
    print("La entrada no coincide con MT ni AFD. Por favor revise el archivo programa.txt")
    exit(1)

# Función AFD
def AFD(d, q0, E_aceptacion, cinta):
    q = q0
    for simbolo in cinta:
        try:
            q = d[q, simbolo]
        except KeyError:
            return False
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

    # Buscar el índice de "->" para fijar la posición de la cabeza
    if '->' in contenido:
        i = contenido.index('->')
        contenido = contenido.replace('->', '', 1)  # Elimina solo la primera aparición
    else:
        i = 0  # Si no se encuentra, empieza desde el inicio

    letras = list(contenido)
    estado = '0'

    time.sleep(2)
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

        # CORREGIR animación
        
        if sys.stdout.isatty():  # Solo si es una terminal interactiva
            
            sys.stdout.write('\033[2A')  # Subir 2 líneas (borrar anteriores)
            sys.stdout.write('\033[2K\r' + linea + '\n')  # Línea con cinta
            sys.stdout.write('\033[2K\r' + ' ' * len(antes) + ' ↑\n')  # Línea con flecha
            sys.stdout.flush()
        else:
            print(linea)
            print(' ' * len(antes) + ' ↑')
        time.sleep(0.5)

        if estado_final is None:
            print(f"El carácter '{simbolo_actual}' no está disponible para validación en el estado '{estado}'")
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
