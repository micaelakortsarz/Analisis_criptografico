#Genera la distribucion de frecuencia de aparicion de letras para el idioma ingles, aleman y finlandes utilizando
# el texto en los archivos quijote_en.txt, quijote_de.txt y quijote_fi.txt, respectivamente.

import os
import argparse

#Al correr este programa se debe elegir el parametro con el cual se elige mostrar los histogramas por:
# p (pantalla), a (archivo), pya (pantalla y archivo).
parser = argparse.ArgumentParser(description='"Forma de visualizar el grafico de la distribucion"')
parser.add_argument("display", help="p (pantalla), a (archivo), pya (pantalla y archivo)", default="p")
args = parser.parse_args()

#Genera la distribucion de frecuencia de aparicion de letras para todos los idiomas
os.system("python contar_letras.py quijote_es.txt -o español.npy "+args.display)
os.system("python contar_letras.py quijote_en.txt -o inglés.npy "+args.display)
os.system("python contar_letras.py quijote_de.txt -o alemán.npy "+args.display)
os.system("python contar_letras.py quijote_fi.txt -o finlandés.npy "+args.display)