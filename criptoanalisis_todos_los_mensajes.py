# Descifra los mensajes del 1 al 9, calcula a y b y, ademas, determina el idioma que con mayor coeficiente de
#correlacion de Pearsons. Muestra en pantalla los graficos requeridos por la consigna. Se deben ir cerrando para que el
#programa prosiga.

import os
import time

start = time.time()
os.system("python criptoanalisis.py mensaje_cifrado_01.txt --idiomas español inglés alemán finlandés")
os.system("python criptoanalisis.py mensaje_cifrado_02.txt --idiomas español inglés alemán finlandés")
os.system("python criptoanalisis.py mensaje_cifrado_03.txt --idiomas español inglés alemán finlandés")
os.system("python criptoanalisis.py mensaje_cifrado_04.txt --idiomas español inglés alemán finlandés")
os.system("python criptoanalisis.py mensaje_cifrado_05.txt --idiomas español inglés alemán finlandés")
os.system("python criptoanalisis.py mensaje_cifrado_06.txt --idiomas español inglés alemán finlandés")
os.system("python criptoanalisis.py mensaje_cifrado_07.txt --idiomas español inglés alemán finlandés")
os.system("python criptoanalisis.py mensaje_cifrado_08.txt --idiomas español inglés alemán finlandés")
os.system("python criptoanalisis.py mensaje_cifrado_09.txt --idiomas español inglés alemán finlandés")
end = time.time()

#Muesta el tiempo que demora en descifrar todos los mensajes (incluye el tiempo que los graficos estan abiertos)
print("Tiempo para descifrar todos los mensajes: {} s (incluye el tiempo que los graficos estan abiertos)".format(end - start))