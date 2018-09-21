import decimal


def drange(x, y, jump):
    while x < y:
        yield float(x)
        x += decimal.Decimal(jump)


def main():
    n = 10
    semilla = [0] * n
    matriz = generar_matriz_inicializada(n)
    f = [0] * n
    iteraciones_w = dict()
    tol = 0.01
    for w in drange(1, 2, '0.05'):
        x, cant_iter = SOR(matriz, semilla, f, w, tol)
        iteraciones_w[w] = cant_iter
    minimo = 1
    for (w, cant_iter) in iteraciones_w:
        if cant_iter < minimo:
            minimo = cant_iter
            w_optimo = w
    tol = 0.0001
    x, cant_iter = SOR(matriz, semilla, f, w_optimo, tol)


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


def SOR(A, x, b, w, tol):
    n = len(A)
    s = x.copy()
    cant_iteraciones = 0
    e = 1
    while (e > tol):
        xant = x.copy()
        for i in range(n):
            x[i] = s[i] * (1 - w) + w * GS(A[i], s, b[i], i, n)
        cant_iteraciones += 1
        s = x.copy()
        e = error(x, xant)
    return (x, cant_iteraciones)


def GS(coeficientes, semilla, b, i, n):
    suma = 0
    # der
    j = i + 1
    if j != n:
        while j < n & coeficientes[j] != 0:
            suma += coeficientes[j] * semilla[j] / coeficientes[i]
            j += 1
    # izq
    j = i - 1
    if j != -1:
        while j >= 0 & coeficientes[j] != 0:
            suma += coeficientes[j] * semilla[j] / coeficientes[i]
            j = j - 1
    return b / coeficientes[i] - suma


def error(x, xant):
    resultado = []
    for i in range(len(x)):
        resultado.append((x[i] - xant[i]))
    norma = max(resultado) / max(x)
    return norma

generar_matriz_inicializada(10)
