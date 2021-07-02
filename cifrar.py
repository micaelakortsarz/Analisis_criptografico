#Este programa toma un texto normal cualquiera y lo cifra utilizando claves a y b pasadas como argumento.

#Se importan todas las librerias requeridas por el programa.
import argparse
import math as m
import sys
from unicodedata2 import normalize
import numpy as np

#Esta funcion retorna C para (a,b,P) dados
def cifrar(a,b,P):
    return (a*P+b)%27

#Esta funcion calcula el maximo comun divisor entre dos numeros a y b cualquiera
def mcd(a,b):
    if b == 0:
        return a
    else:
        return mcd(b, a%b)

#Claves de cifrado
claves = {'A': 0 , 'B':1 , 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11,'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,' ':26}
keys=list(claves.keys())

#Parametros ingresados por teclado
parser = argparse.ArgumentParser(description='"Argumentos para la codificación"')
parser.add_argument("archivo" ,help="archivo a codificar")
parser.add_argument("a",type=float, action="store", default=0)
parser.add_argument("b",type=float, action="store", default=0)
parser.add_argument('-o', '--output', action="store", default=sys.stdout, dest="nombre")
args = parser.parse_args()


#El programa determina si la clave a proporcionada es invalida (no es cooprima con 27). En tal caso, da un mensaje de error.
if mcd(args.a,27)!=1:
    print("La clave a proporcionada es inválida, no es cooprima con 27")
else:
    #Formatea el archivo dejando solo espacios y letras mayusculas
    file = open(args.archivo, encoding="utf8")
    data_descifrada = file.read()
    file.close()
    data_descifrada= normalize('NFD', data_descifrada)
    permitidos = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    data_descifrada_norm = ''.join(filter(permitidos.__contains__,  data_descifrada))
    data_descifrada_format =  data_descifrada_norm.upper()

    #Cifra el mensaje utilizando las claves a y b ingresadas por el usuario
    data_cifrada = [cifrar(args.a, args.b, claves[data_descifrada_format[i]]) for i in
                       range(0, len(data_descifrada_format))]
    mensaje_codificado = [keys[int(data_cifrada[i])] for i in range(0, len(data_cifrada))]
    #Segun el usuario disponga, guarda el nuevo mensaje cifrado en un archivo o lo muestra por pantalla
    np.savetxt(args.nombre, mensaje_codificado,fmt='%s', newline='')
    print("\n")
