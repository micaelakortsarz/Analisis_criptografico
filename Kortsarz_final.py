#Resuelve el final completo utilizando las lineas de comando especificadas en las consignas, llamando a los scripts de
#python requeridos. Al correr este programa se debe elegir el parametro requerido por la consigna del inciso 2 para mostrar
# los histogramas por: p (pantalla), a (archivo), pya (pantalla y archivo).

import os
import time
import argparse

start = time.time()

#Inciso 1: Muestra en pantalla el mensaje_cifrado_00.txt descifrado utilizando las claves dadas en la consigna
os.system("python descifrar.py mensaje_cifrado_00.txt 7 25")


#Inciso 2: Genera las distribuciones de frecuencia de los caracteres para todos los idiomas dados y muestra en pantalla y/o
#guarda en archivos los histogramas generados
parser = argparse.ArgumentParser(description='"Forma de visualizar el grafico de la distribucion"')
parser.add_argument("display", help="p (pantalla), a (archivo), pya (pantalla y archivo)", default="p")
args = parser.parse_args()
os.system("python contar_letras_varios_idiomas.py "+args.display)

#Inciso 3: Descifra los mensajes del 1 al 9, calcula a y b y, ademas, determina el idioma que con mayor coeficiente de
#correlacion de Pearsons. Muestra en pantalla los graficos requeridos por la consigna. Se deben ir cerrando para que el
#programa prosiga.
os.system("python criptoanalisis_todos_los_mensajes.py")

#Extra 1: Cifra el texto dado (por ejemplo yo use y adjunte el poema "No te rindas" de Mario Benedetti). En la primer corrida
#muestra el texto cifrado en pantalla y, en la segunda, lo guarda en el archivo mensaje_cifrado.txt. Luego, con las claves a y b
#con las cuales se cifro (1,3), usando el script del inciso 1, descifro el archivo mensaje_cifrado.txt y reobtengo el texto original
#sin los signos diacriticos de todas las letras, los signos de puntuacion y caracteres especiales, exceptuando el caracter de
# espacio
os.system("python cifrar.py mensaje.txt 1 3")
os.system("python cifrar.py mensaje.txt 1 3 -o mensaje_cifrado.txt")
os.system("python descifrar.py mensaje_cifrado.txt 1 3")

#Extra 2: COMO COSTO JAJA :P
os.system("python criptoanalisis_men10.py mensaje_cifrado_10.txt")

end = time.time()
print("Tiempo para resolver el final: {} s".format(end - start))
