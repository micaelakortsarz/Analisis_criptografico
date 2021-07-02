#
#Se importan todas las librerias requeridas por el programa.
import time
start = time.time()
import numpy as np
import argparse
import math as m
from scipy import stats
from unicodedata2 import normalize
from sympy import mod_inverse,zoo
import matplotlib.pyplot as plt
import time
print("Demora un ratito, tenganle paciencia por favor :)")

#Esta funcion cuenta la cantidad de palabras en español
def cuenta_palabras(unique,palabras):
    total_palabras = 0
    for i in range(len(palabras)):
        for j in range(len(unique)):
            if palabras[i] == unique[j]:
                total_palabras += 1
    return total_palabras

#Esta funcion calcula las claves a y b para dos pares (C1,P1) y (C2,P2)
def hayar_claves_por_pares(C1,P1,C2,P2):
    if P1-P2 !=0:
        a=mod_inverse((C1-C2)/(P1-P2),27)
        if a==ValueError('inverse of %s (mod %s) does not exist' % (a, m)):
            return 1,0
        elif a==zoo: return 1,0
        else:
            b=C1-a*P1
            return int(a),int(b)
    else: return 1,0

#Esta funcion retorna P para (a,b,C) dados
def convertir(a,b,C,cond):
    for i in range(27):
        if C==cond[i]:return i
    return 0

#Claves de cifrado
claves = {'A': 0 , 'B':1 , 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11,'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,' ':26}
keys=list(claves.keys())


#Recibe el nombre del archivo a leer
parser = argparse.ArgumentParser(description='"Argumentos para la decodificación"')
parser.add_argument("archivo", help="archivo a decodificar")
args = parser.parse_args()



# Abrir, leer y cerrar el archivo y el capitulo del quijote en español
file = open("quijote_es.txt", encoding="utf8")
quijote = file.read()
file.close()

file = open(args.archivo, encoding="utf8")
mensaje = file.read()
file.close()

# Quita del texto los signos diacriticos de todas las letras y omita los signos de puntuacion
# y caracteres especiales, exceptuando el caracter de espacio. Se obtiene un texto puramente con letras
# en mayuscula y espacios. Finalmente se obtiene las palabras diferentes que hay en el capitulo del quijote

quijote = normalize('NFD', quijote)
permitidos = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
quijote_norm = ''.join(filter(permitidos.__contains__, quijote))
quijote_format = quijote_norm.upper()

quijote_palabras=quijote_format.split()
quijote_unique=np.unique(quijote_palabras)

#Inicializa variables auxiliares
aux=0
max_pal=0
a_cor=0
b_cor=0

#Recorre todos los pares (C1,P1), (C2,P2) posibles y halla las claves a y b para las cuales se forman la mayor cantidad
#de palabras en español
for i,j,k,l in np.ndindex(27,27,27,27):
    a, b = hayar_claves_por_pares(i,j,k,l)
    cond = [(a * x + b) % 27 for x in range(27)]
    data_descifrada = [convertir(a, b, claves[mensaje[x]], cond) for x in range(len(mensaje))]
    mensaje_decodificado = [keys[int(data_descifrada[x] % 27)] for x in range(len(data_descifrada))]
    mensaje_decodificado=''.join(mensaje_decodificado)
    mensaje_decodificado2=mensaje_decodificado.split()
    aux=cuenta_palabras(quijote_unique,mensaje_decodificado2)
    if max_pal-aux<0:
        max_pal=aux
        a_cor=a
        b_cor=b
        if max_pal>100:
            break

print("El mensaje secreto es:\n")
print (mensaje_decodificado)
end = time.time()

print("Tiempo para descifrar el mensaje: {} s".format(end - start))

