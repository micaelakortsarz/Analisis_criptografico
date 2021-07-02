#Descifra el mensaje ingresado por teclado, calcula a y b y, ademas, determina cual de los idiomas ingresados por teclado
# tiene un mayor coeficiente de correlacion de Pearsons. Muestra en pantalla los graficos requeridos por la consigna.
# Se deben ir cerrando para que el programa prosiga.

#Se importan todas las librerias requeridas por el programa. Se empieza a contar el tiempo de ejecucion
import time
start = time.time()
import numpy as np
import argparse
import math as m
from scipy import stats
from unicodedata2 import normalize
from sympy import mod_inverse
import matplotlib.pyplot as plt


#Esta funcion halla la distribucion de frecuencias de aparicion de caracteres en un texto
def calcular_distribucion(text,keys):
    dist_aux = np.zeros(27)
    total_letras = 0
    for i in range(0, len(text)):
        for j in range(0, 27):
            if text[i] == keys[j]:
                dist_aux[j] += 1
                total_letras += 1
    return dist_aux * 100 / total_letras

def metodo_de_orden(elem):
    return elem[0]

#Esta funcion compara distribuciones de frecuencias de aparicion de dos textos y retorna las distribuciones comparadas
# y las letras analogas en ambos textos
def comparar_distribuciones(dist1,dist2,keys,reorg=[]):

    dist_a=[[dist1[i],i] for i in range(0,27)]
    dist_b=[[dist2[i],i] for i in range(0,27)]
    dist_a.sort(key=metodo_de_orden,reverse=True)
    dist_b.sort(key=metodo_de_orden,reverse=True)

    for (i,j) in reorg:
        [dist_a[i][1],dist_a[j][1]]=[dist_a[j][1],dist_a[i][1]]

    comparacion_dist=[(dist_a[i][1],dist_b[i][1]) for i in range(0,27)]
    comparacion_letras = [(keys[dist_a[i][1]], keys[dist_b[i][1]]) for i in range(0, 27)]
    dist_ordenadas=[(dist_a[i][0],dist_b[i][0]) for i in range(0,27)]
    return comparacion_dist, comparacion_letras, dist_ordenadas

#Esta funcion calcula las claves a y b para dos pares (C1,P1) y (C2,P2)
def hayar_claves_por_pares(C1,P1,C2,P2):
    if P1-P2 !=0:
        a=mod_inverse((C1-C2)/(P1-P2),27)
        if a==ValueError('inverse of %s (mod %s) does not exist' % (a, m)):
            return 1,0
        else:
            b=C1-a*P1
            return int(a),int(b)
    else: return 1,0

#Esta funcion retorna P para (a,b,C) dados
def convertir(a,b,C,cond):
    for i in range(27):
        if C==cond[i]:return i
    return 0

#Esta funcion obtiene las claves a y b para la mayor cantidad de combinaciones de pares (C1,P1) y (C2,P2) de modo de maximizar
# el coeficiente de correlacion de Pearsons. Se utilizan todos los idiomas porque ayudo a maximizar la variedad de pares (C,P)
def criptoanalisis(reorg=[]):
    # Aqui se guardara el coeficiente de correlacion de Pearsons maximo, mejor a y mejor b que se alcance con cada idioma
    idiomas=["español","inglés","alemán","finlandés"]
    pearsons_maximo = np.zeros(len(idiomas))
    a_cor = np.zeros(len(idiomas))
    b_cor = np.zeros(len(idiomas))
    for i in range(len(idiomas)):
        #Abrir la distribucion de frecuencias del idioma para cada idioma
        dist_idioma=np.loadtxt(idiomas[i] + ".npy")

        #Leer el archivo cifrado y guardarlo para descifrarlo
        file = open(args.archivo, encoding="utf8")
        data_cifrada = file.read()
        file.close()

        #Calcular distribucion de frecuencia de aparicion de los caracteres y compararlo con la del idioma
        dist_cifrado=calcular_distribucion(data_cifrada,keys)
        dist_comparadas, letras_analogas, dist_ord= comparar_distribuciones(dist_cifrado,dist_idioma,keys,reorg)

        #Probando con distintos pares (C1,P1), (C2,P2) para hallar la maxima correlacion posible en cada idioma
        for j in range(1,6):
                for k in range(18):
                        #Halla las claves a y b
                        a,b=hayar_claves_por_pares(dist_comparadas[j][0],dist_comparadas[j][1],dist_comparadas[k][0],dist_comparadas[k][1])
                        cond = [(a * x + b) % 27 for x in range(27)]

                        #Descifra el mensaje
                        data_descifrada = [convertir(a, b, claves[data_cifrada[x]], cond) for x in range(len(data_cifrada))]
                        mensaje_decodificado = [keys[int(data_descifrada[x] % 27)] for x in range(len(data_descifrada))]

                        #Calcula la distribucion de frecuencias de aparicion de cada caracter en el mensaje descifrado
                        # para las a y b encontradas
                        dist_men_cif = calcular_distribucion(mensaje_decodificado, keys)

                        #Calcula el coeficiente de correlacion de Pearsons
                        pearsons=stats.pearsonr(dist_men_cif, dist_idioma)

                        #Halla el mayor coefieciente de correlacion de Pearsons obtenido y guarda las claves a y b
                        # correspondientes a ese caso
                        if pearsons_maximo[i]-pearsons[0]<0:
                            pearsons_maximo[i]=pearsons[0]
                            a_cor[i]=a
                            b_cor[i]=b
    return pearsons_maximo,a_cor,b_cor,dist_ord,letras_analogas,dist_idioma,dist_men_cif,data_cifrada,dist_cifrado

#Esta funcion grafica y muestras la comparacion de los caracteres del mensaje cifrado con los del idioma detectado
def grafica_comparacion_distribuciones(letras_cif,letras_id,s_d_cif,d_id,m_i ):
    fig, axs = plt.subplots(2, 1,squeeze=True)
    labels=["Mensaje cifrado","Idioma "+''.join(args.idiomas[m_i])]
    fig.subplots_adjust(hspace=0)
    axs[0].bar(letras_cif,d_cif, label=args.archivo ,width=.8,alpha=0.95)
    axs[0].xaxis.set_ticks_position('top')
    axs[0].set_xticks(letras_cif)
    axs[0].set_axisbelow(True)
    axs[0].grid(axis="x")

    axs[1].bar(letras_id,d_id, label=m_i,width=.8,color="orange",alpha=0.95)
    axs[1].set_xticks(letras_id)
    axs[1].set_ylim(max(d_id)+1, 0.01)
    axs[1].set_axisbelow(True)
    axs[1].grid(axis="x")

    fig.text(0.06, 0.5, 'Frecuencia de aparición (%)', ha='center', va='center', rotation='vertical')
    fig.legend(labels, loc="upper right", bbox_to_anchor=(0.85, 0.85))

    plt.show()

#Esta funcion grafica y muestra la correlacion entre la frecuencia de aparicion de
# letras del mensaje descifrado y la del idioma detectado
def grafica_correlacion(dist_idioma,dist_cifrado,dist_men_cif,m_i ):
    x = np.linspace(0, max(dist_idioma), 10)
    plt.plot(dist_idioma, dist_cifrado, "o", label="Cifrado", alpha=0.5, )
    plt.plot(dist_idioma, dist_men_cif, "o", label="Descifrado", color="black")
    plt.plot(x, x, color="gray", ls="--", label="Correlación perfecta")
    plt.ylabel('Frecuencia de aparición en el mensaje')
    plt.xlabel('Frecuencia de aparición en el idioma ' + ''.join(args.idiomas[m_i]))
    plt.legend(loc="upper right")
    plt.show()

#Claves de cifrado
claves = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
          'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
          'Z': 25, ' ': 26}
keys = list(claves.keys())

#Parametros ingresados por teclado
parser = argparse.ArgumentParser(description='"Idiomas a analizar"')
parser.add_argument("archivo" ,help="archivo a decodificar")
parser.add_argument('-i', '--idiomas', action="store", dest="idiomas", nargs='*',
                    help="archivo de numpy donde se guardara la distribución")
args = parser.parse_args()

#Resuelve el problema del criptoanalisis
pearsons_maximo,a_cor,b_cor,dist_ord,letras_analogas,dist_idioma,dist_men_cif,data_cifrada,dist_cifrado=criptoanalisis()
m_idx=np.argmax(pearsons_maximo)

#En caso de que no se haya alcanzado un coeficiente de correlacion de Pearsons mayor a 0.8, esta parte del script
# da flexibilidad al programa intercambiando algunas de las letras mas frecuentes
posibles_cambios=[[(0,3)],[(0,5),(1,6)],[(0,1),(2,3)],[(0,2)],[(0,5)],[(1,7),(0,3),(2,6)],[[0,4],[1,5]]]
mejor_cambio=[]
m_p=0
if pearsons_maximo[m_idx]<0.8:

    for cambios in posibles_cambios:
        if m_p<0.8:
            pearsons_maximo,a_cor,b_cor,dist_ord,letras_analogas,dist_idioma,dist_men_cif,data_cifrada,dist_cifrado=criptoanalisis(cambios)
            m_idx = np.argmax(pearsons_maximo)
            if (m_p-pearsons_maximo[m_idx])<0:
                mejor_cambio=cambios
                m_p=pearsons_maximo[m_idx]
    pearsons_maximo,a_cor,b_cor,dist_ord,letras_analogas,dist_idioma,dist_men_cif,data_cifrada,dist_cifrado=criptoanalisis(mejor_cambio)


#Obtiene los a, b correctos y mensaje descifrado
m_idx=np.argmax(pearsons_maximo)
a=a_cor[m_idx]
b=b_cor[m_idx]
cond = [(a * x + b) % 27 for x in range(27)]
data_descifrada = [convertir(a, b, claves[data_cifrada[x]], cond) for x in range(len(data_cifrada))]
mensaje_decodificado = [keys[int(data_descifrada[x] % 27)] for x in range(len(data_descifrada))]
dist_men_cif = calcular_distribucion(mensaje_decodificado, keys)

#Identifica el idioma que obtuvo la mejor correlacion
m_p=0
for i in range(len(args.idiomas)):
    dist_m_idioma=np.loadtxt(args.idiomas[i] + ".npy")
    pearsons = stats.pearsonr(dist_men_cif, dist_m_idioma)
    if (m_p-pearsons[0]) < 0:
        m_p=pearsons[0]
        m_id=i
mejor_idioma=args.idiomas[m_id]

#Muestra en pantalla los resultados
print("Los coeficientes a y b obtenidos son {} y {} respectivamente. El idioma que mejor se correlaciona es {}, dando un coeficiente de correlacion de Pearson de {}".format(a_cor[m_idx],b_cor[m_idx],mejor_idioma,m_p))
print("El mensaje descifrado es:")
print(''.join(mensaje_decodificado))

#Grafica los graficos requeridos por la consigna
dist_m_idioma = np.loadtxt(args.idiomas[m_id] + ".npy")
dist_comp,letras_analogas,dist_ord=comparar_distribuciones(dist_cifrado,dist_m_idioma,keys)
d_cif=[dist_ord[i][0] for i in range(len(dist_ord))]
d_id=[dist_ord[i][1] for i in range(len(dist_ord))]
letras_cif=[letras_analogas[i][0] for i in range(27)]
letras_id=[letras_analogas[i][1] for i in range(27)]
end = time.time()
grafica_comparacion_distribuciones(letras_cif,letras_id,d_cif,d_id,m_id)
grafica_correlacion(dist_m_idioma,dist_cifrado,dist_men_cif,m_id)


#Muestra en pantalla el tiempo requerido para descifrar el mensaje con este programa
print("Tiempo para descifrar el mensaje: {} s".format(end - start))





