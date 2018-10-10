import decimal
import math
from decimal import Decimal


def main():
    n = 10
    largo = n + 1
    semilla = [10] * largo  # arbitraria
    matriz = generar_matriz_inicializada(largo)
    f = generar_termino_independiente(n)
    # Se busca el w óptimo (menor cantidad de iteraciones)
    tol = 0.01
    w = obtener_w_optimo(matriz, semilla, f, tol)
    tol = 0.0001
    x, cant_iter = SOR(matriz, semilla, f, w, tol, True, True)


def obtener_w_optimo(A, semilla, b, tol):
    iteraciones_w = dict()
    w_optimo = 1
    archivo = open("w_iteraciones_n.txt", "w")

    for w in drange(1, 2, '0.05'):
        x, cant_iter = SOR(A, semilla, b, w, tol)
        iteraciones_w[w] = cant_iter
    minimo = iteraciones_w[1]
    for i in drange(1, 2, '0.05'):
        if iteraciones_w[i] < minimo:
            minimo = iteraciones_w[i]
            w_optimo = i
    escribir_dicc_iteraciones(iteraciones_w, archivo)

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


def SOR(A, s, b, w, tol, optimo=False, p=False):
    """Realiza SOR para la matriz dada y crea archivos con los resultados.
    Con optimo=True, el archivo resultante es 'res_final.txt' y además devuelve un diccionario
    de resultados {nº iteración: vector resultado}
    si además p=True, también calcula el valor de p y se exporta al archivo."""
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
    escribir_error(x_res, e, archivo)
    archivo.close()
    return x_res, cant_iteraciones


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


def calcular_p(dic):
    """Calcula p dado un diccionario del tipo {nº iteración: resultado}"""
    n = len(dic)
    x1 = dic[n - 1]
    x2 = dic[n - 2]
    x3 = dic[n - 3]
    x4 = dic[n - 4]
    num = normaInfinito(restar_vectores(x1, x2)) / normaInfinito(restar_vectores(x2, x3))
    div = normaInfinito(restar_vectores(x2, x3)) / normaInfinito(restar_vectores(x3, x4))
    p = abs(math.log(num) / math.log(div))
    return p


def escribir_resultados(res, archivo):
    """Exporta los resultados a un archivo."""
    n = len(res)
    for i in range(n):
        if i == 0:
            archivo.write("{:.4E}".format(Decimal(res[i])))
        else:
            archivo.write("|" + "{:.4E}".format(Decimal(res[i])))
    archivo.write("\n")


def escribir_p(p, archivo):
    archivo.write("p es {:.4E} \n".format(Decimal(p)))


def escribir_dicc_iteraciones(dicti, archivo):
    """Exporta la cantidad de iteraciones de cada w utilizado al buscar el óptimo"""
    archivo.write("w|cantidad de iteraciones\n")

    for i in dicti:
        archivo.write("{}|{}\n".format(i, dicti[i]))


def gauss_seidel(coeficientes, semilla, b, i, n):
    """Realiza el procedimiento de Gauss-Seidel para una fila de la matriz"""
    suma = 0
    for j in range(n):
        if j != i and coeficientes[j] != 0:
            suma += (coeficientes[j] * semilla[j]) / coeficientes[i]
    return (b / coeficientes[i]) - suma


def normaInfinito(vect):
    return abs(max(vect, key=lambda x: abs(x)))


def drange(x, y, jump):
    """range para saltos decimales"""
    while x < y:
        yield float(x)
        x += decimal.Decimal(jump)


def matriz_ceros(n):
    matriz = []
    for i in range(n):
        vector_ceros = [0] * n
        matriz.append(vector_ceros)
    return matriz


def restar_vectores(x, y):
    return [x[i] - y[i] for i in range(len(x))]


def error(x, xant):
    """Calcula el error relativo entre dos vectores."""
    return normaInfinito(restar_vectores(x, xant)) / normaInfinito(x)


def escribir_error(x, error, archivo):
    e = normaInfinito(x) * error
    archivo.write("El error absoluto es {:.4E} \n".format(Decimal(e)))


main()
