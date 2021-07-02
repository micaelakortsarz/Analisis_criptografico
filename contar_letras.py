#Genere la distribucion de frecuencia de aparicion de letras para el idioma ingresado por telcado
#Se importan todas las librerias requeridas por el programa.
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from unicodedata2 import normalize

claves = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
          'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
          'Z': 25, ' ': 26}
keys = list(claves.keys())

#Recibe el nombre del archivo a leer y el nombre del archivo de numpy donde se guararan los resultados
parser = argparse.ArgumentParser(description='"Argumentos para la decodificación"')
parser.add_argument("archivo", help="archivo a decodificar")
parser.add_argument('-o', '--output', action="store", default=sys.stdout, dest="distribucion",
                    help="archivo de numpy donde se guardara la distribución")
parser.add_argument("display", help="Forma de visualizar el grafico de la distribucion. Las opciones son: p (pantalla),a (archivo),pya (pantalla y archivo)",default="p")
args = parser.parse_args()

# Abrir, leer y cerrar el archivo
file = open(args.archivo, encoding="utf8")
quijote = file.read()
file.close()

# Quita del texto los signos diacriticos de todas las letras y omita los signos de puntuacion
# y caracteres especiales, exceptuando el caracter de espacio. Se obtiene un texto puramente con letras
# en mayuscula y espacios.

quijote = normalize('NFD', quijote)
permitidos = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
quijote_norm = ''.join(filter(permitidos.__contains__, quijote))
quijote_format = quijote_norm.upper()


# Calcula la frecuencia de aparicion de cada caracter en el texto de un archivo que
# se le pase como argumento y guarde la distribucion calculada en un archivo binario de numpy (.npy)

dist_aux = np.zeros(27)
total_letras = 0
for i in range(0, len(quijote_format)):
    for j in range(0, 27):
        if quijote_format[i] == keys[j]:
            dist_aux[j] += 1
            total_letras += 1
dist = dist_aux * 100 / total_letras
np.savetxt(args.distribucion, dist ,fmt="%10.4f")

#Grafica el histograma de frecuencias de aparicion de cada caracter en el texto

plt.bar(keys,dist, label=args.archivo,width=.8)
plt.legend()
plt.ylabel('Frecuencia de aparición (%)')
if args.display=="a" or args.display=="pya":
    plt.savefig('{}_grafico_distribucion.pdf'.format(args.archivo))
if args.display=="p" or args.display=="pya":
    plt.show()
