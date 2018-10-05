import decimal
import math
from decimal import Decimal
import numpy as np
def main():
    n = 10
    largo = n + 1
    semilla = [10] * largo  # arbitraria
    matriz = generar_matriz_inicializada(largo)
    f = generar_termino_independiente(n)
    # Se busca el w óptimo (menor cantidad de iteraciones)
    tol = 0.0001
    w = obtener_w_optimo(matriz, semilla, f, tol)
    tol = 0.0001
    p = 1
    x, cant_iter= SOR(matriz, semilla, f, w, tol, True, True)
    x = np.asarray(x)
    print("x",x)
    f = np.asarray(f)
    print("f",f)
    matriz = np.asarray(matriz)
    casif = np.dot(x,matriz)
    error = np.subtract(casif, f)
    print("error", error)
#graficar_resultado(x)


def drange(x, y, jump):
    while x < y:
        yield float(x)
        x += decimal.Decimal(jump)


def obtener_w_optimo(A, semilla, b, tol):
    iteraciones_w = dict()
    w_optimo = 1
    archivo = open("w_iteraciones_n.txt", "w")

    for w in drange(1, 2, '0.05'):
        x, cant_iter = SOR(A, semilla, b, w, tol)
        iteraciones_w[w] = cant_iter
        # exportarresultadosacsv(x)
    minimo = iteraciones_w[1]
    for i in drange(1, 2, '0.05'):
        if iteraciones_w[i] < minimo:
            minimo = iteraciones_w[i]
            w_optimo = i
    escribir_dict(iteraciones_w, archivo)

    return w_optimo


def generar_termino_independiente(n):
    largo = n + 1
    b = [0] * largo
    x = [0] * largo
    q = [0] * largo
    g = 12
    for i in range(largo):
        x[i] = i / n
        q[i] = g + (g ** 2) * (x[i] - x[i] ** 2)
        b[i] = q[i] / (n ** 4)
    b[0] = 0
    b[largo - 1] = 0
    return b


def matriz_ceros(n):
    matriz = []
    for i in range(n):
        vector_ceros = [0] * n
        matriz.append(vector_ceros)
    return matriz


def generar_matriz_inicializada(n):
    if n < 5:
        return 0
    matriz = matriz_ceros(n)
    matriz[0][0] = 1  # i = 0
    # i = 1:
    matriz[1][0] = -4
    matriz[1][1] = 5
    matriz[1][2] = -4
    matriz[1][3] = 1
    # i:
    k = 0
    for i in range(2, n - 2):
        vect = [1, -4, 6, -4, 1]
        for j in range(k, 5 + k):
            matriz[i][j] = vect.pop()
        k += 1
    matriz[n - 2] = matriz[1][::-1]  # n-1
    matriz[n - 1][n - 1] = 1  # n

    return matriz

def normaInfinito(vect):
    return abs(max(vect, key = lambda x: abs(x)))

def calcular_p(dic):
    n = len(dic)
    x1 = dic[n - 1]
    x2 = dic[n - 2]
    x3 = dic[n - 3]
    x4 = dic[n - 4]
    num = normaInfinito(restar(x1, x2)) / normaInfinito(restar(x2, x3))
    div = normaInfinito(restar(x2, x3)) / normaInfinito(restar(x3, x4))
    p = math.log(num) / math.log(div)
    return p


"""def exportar_dict_csv(res):
    import csv
    csvfile = "res.csv"
    with open(csvfile, 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        for i in res:
            writer.writerow([i, res[i]])
"""
"""def truncar(vect, tol): # LE ESTOY PASANDO U NDICCIONARIO, MAL
    truncado = []
    for x in vect:
        print('x', x, 'tol', tol)
        truncado.append(decimal.Decimal(str(x)).quantize(decimal.Decimal(tol)))
    return truncado
"""

def escribir_resultados(res, archivo):

    """dump de los datos de la res seleccionada, formateado para mejor exportacion"""
    n = len(res)
    for i in range(n):
        if i == 0:
            archivo.write("{:.4E}".format(Decimal(res[i])))
        else:
            archivo.write("|" + "{:.4E}".format(Decimal(res[i])))
    archivo.write("\n")

def escribir_p(p, archivo):

    archivo.write("p es {:.4E} \n".format(Decimal(p)))

def escribir_dict(dicti, archivo):

    archivo.write("w|cantidad de iteraciones\n")

    for i in dicti:
        archivo.write("{}|{}\n".format(i, dicti[i]))


"""def escribir_w_iter(iter, w, archivo):
    for i in range(len(iter)):
        archivo.write("%d    %.2f\n" % (iter[i], w[i]))
"""

def SOR(A, s, b, w, tol, optimo=False, p=False):
    n = len(A)
    cant_iteraciones = 0
    e = 1
    k = 0
    x_res = s.copy()
    if optimo:
        resultados = dict()
        archivo = open("res_final.txt", "w")
    else:
        archivo = open("res_w_{}.txt".format(w), "w")
    while e > tol:
        if optimo:
            resultados[k] = x_res.copy()
        x_ant = x_res.copy()
        for i in range(n):
            x_gs = gauss_seidel(A[i], x_res, b[i], i, n)
            x_res[i] = x_res[i] * (1 - w) + w * x_gs
        escribir_resultados(x_res, archivo)
        cant_iteraciones += 1
        e = error(x_res, x_ant)
        k += 1
    if optimo and p:
        escribir_p(calcular_p(resultados), archivo)
    archivo.close()
    return x_res, cant_iteraciones

def gauss_seidel(coeficientes, semilla, b, i, n):
    suma=0
    for j in range(n):
        if j != i and coeficientes[j] != 0:
            suma += (coeficientes[j] * semilla[j]) / coeficientes[i]
    return (b / coeficientes[i] )- suma

"""def SOR(A, s, b, w, tol):
    n = len(A)
    cant_iteraciones = 0
    e = 1
    x_ant = s.copy()
    x_res = s.copy()
    while e > tol:
        x_ant = x_res.copy()
        x_gs = gauss_seidel(A, x_ant, b, n)
        for i in range(n):
            x_res[i] = x_ant[i] * (1 - w) + w * x_gs[i]
        cant_iteraciones += 1
        e = error(x_res, x_ant)
    return x_res, cant_iteraciones

def gauss_seidel (matriz, semilla, b, n):
    s = semilla.copy()
    for i in range(n):
        suma = 0
        for j in range(n):
            if j != i:
                suma += matriz[i][j] * s[j] / matriz[i][i]
        s[i] = b[i] / matriz[i][i] - suma
    return s"""

def restar(x, y):
    #print('voy a restar',x,'con y',y)
    #print(x[1],'-',y[1],'=',)
    return [x[i] - y[i] for i in range(len(x))]


def error(x, xant):
    return normaInfinito(restar(x,xant))/normaInfinito(x)

def graficar_resultado(res):
    n = len(res)

    x = [i for i in range(n)]

    plt.plot(x,res)
    plt.show()
main()