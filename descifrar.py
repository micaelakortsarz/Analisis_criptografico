#Muestra en pantalla el mensaje ingresado por teclado ya descifrado utilizando claves dadas por teclado

#Se importan todas las librerias requeridas por el programa.
import argparse
import math as m
from unicodedata2 import normalize

#Esta funcion retorna P para (a,b,C) dados
def convertir(a,b,C,cond):
    for i in range(27):
        if C==cond[i]:return i
    return 0

#Claves de cifrado
claves = {'A': 0 , 'B':1 , 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, 'J':9, 'K':10, 'L':11,'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, 'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25,' ':26}
keys=list(claves.keys())

#Parametros por teclado
parser = argparse.ArgumentParser(description='"Argumentos para la decodificación"')
parser.add_argument("archivo" ,help="archivo a decodificar")
parser.add_argument("a",type=float, action="store", default=0)
parser.add_argument("b",type=float, action="store", default=0)
args = parser.parse_args()

#Formatea el mensaje cifrado dejando solo espacios y letras mayusculas.
file = open(args.archivo, encoding="utf8")
data_cifrada = file.read()
file.close()
data_cifrada= normalize('NFD', data_cifrada)
permitidos = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
data_cifrada_norm = ''.join(filter(permitidos.__contains__,  data_cifrada))
data_cifrada_format =  data_cifrada_norm.upper()

#Descifra el mensaje y lo muestra en pantalla
cond = [(args.a * x + args.b) % 27 for x in range(27)]
data_descifrada=[convertir(args.a,args.b,claves[data_cifrada_format[i]],cond) for i in range(len(data_cifrada_format))]
mensaje_decodificado=[keys[int(data_descifrada[i])] for i in range (0,len(data_cifrada_format))]
print(''.join(mensaje_decodificado))
