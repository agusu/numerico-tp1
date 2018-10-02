import decimal
import math


def prueba():
    A = [[10, 2, 6], [1, 10, 4], [2, -7, -10]]
    x, cant_iter, p = SOR(A,[1, 2, 3],[28, 7, -17], 1.033, 0.02, 1)
    print(x,cant_iter,p)


def main():
    n = 5
    semilla = [1] * n  # arbitraria
    matriz = generar_matriz_inicializada(n)
    print(matriz)
    f = generar_termino_independiente(n)
    print(f)
    # Se busca el w óptimo (menor cantidad de iteraciones)
    tol = 0.01
    w = obtener_w_optimo(matriz, semilla, f, tol)
    print('w', w)
    tol = 0.0001
    p = 1
    x, cant_iter, p = SOR(matriz, semilla, f, w, tol, p)
    print(x, cant_iter, p)

    # exportarresultadosacsv(x)


def drange(x, y, jump):
    while x < y:
        yield float(x)
        x += decimal.Decimal(jump)


def obtener_w_optimo(A, semilla, b, tol):
    iteraciones_w = dict()
    w_optimo = 1
    for w in drange(1, 2, '0.05'):
        x, cant_iter = SOR(A, semilla, b, w, tol)
        print(cant_iter)
        iteraciones_w[w] = cant_iter
        # exportarresultadosacsv(x)
    minimo = iteraciones_w[1]
    for i in drange(1, 2, '0.05'):
        if iteraciones_w[i] < minimo:
            minimo = iteraciones_w[i]
            w_optimo = w
    return w_optimo


def generar_termino_independiente(n):
    b = [0] * n
    x = [0] * n
    q = [0] * n
    g = 12
    for i in range(n):
        x[i] = i / n
        q[i] = g + (g ** 2) * (x[i] - x[i] ** 2)
        b[i] = q[i] / (n ** 4)
    b[0] = 0
    b[n - 1] = 0
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


def SOR(A, s, b, w, tol, p=None):
    n = len(A)
    cant_iteraciones = 0
    e = 1
    x_ant = s.copy()
    x_res = s.copy()
    while e > tol:
        x_ant = x_res.copy()
        for i in range(n):
            gs = gauss_seidel(A[i], x_ant, b[i], i, n)
            x_res[i] = x_ant[i] * (1 - w) + w * gs
        cant_iteraciones += 1
        e = error(x_res, x_ant)
    if p:
        return x_res, cant_iteraciones, p
    return x_res, cant_iteraciones


def calcular_p(x):
    n = len(x)
    num = abs(x[n - 1] - x[n - 2]) / abs(x[n - 2] - x[n - 3])
    div = abs(x[n - 2] - x[n - 3]) / abs(x[n - 3] - x[n - 4])
    p = math.log(num) / math.log(div)
    return p


"""def exportarresultadosacsv(x):
    import csv
    csvfile = "<path to output csv or txt>"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in x:
            writer.writerow([val])
   """


def gauss_seidel(coeficientes, semilla, b, i, n):
    suma = 0
    # der
    j = i + 1
    if j != n-1:
        while j < n:
            if coeficientes[j] != 0:
                suma += coeficientes[j] * semilla[j] / coeficientes[i]
            j += 1
    # izq
    j = i - 1
    if j != -1:
        while j >= 0:
            if coeficientes[j] != 0:
                suma += coeficientes[j] * semilla[j] / coeficientes[i]
            j = j - 1
    return b / coeficientes[i] - suma

def error(x, xant):
    resultado = []
    for i in range(len(x)):
        resultado.append((x[i] - xant[i]))
    norma = abs(max(resultado) / max(x))
    return norma

prueba()