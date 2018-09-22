import decimal


def main():
    n = 10
    semilla = [0] * n  # arbitraria
    matriz = generar_matriz_inicializada(n)
    f = generar_termino_independiente(n)
    # Se busca el w óptimo (menor cantidad de iteraciones)
    tol = 0.01
    w = obtener_w_optimo(matriz, semilla, f, tol)
    tol = 0.0001
    x, cant_iter,p = SOR(matriz, semilla, f, w, tol)
    exportarresultadosacsv(x)


def drange(x, y, jump):
    while x < y:
        yield float(x)
        x += decimal.Decimal(jump)


def obtener_w_optimo(A, x, b, tol):
    iteraciones_w = dict()
    w_optimo = 1
    for w in drange(1, 2, '0.05'):
        x, cant_iter,p = SOR(A, x, b, w, tol)
        iteraciones_w[w] = cant_iter
        exportarresultadosacsv(x)
    minimo = 1
    for (w, cant_iter) in iteraciones_w:
        if cant_iter < minimo:
            minimo = cant_iter
            w_optimo = w
    return w_optimo


def generar_termino_independiente(n):
    b = [0]*n
    x = [0]*n
    q = [0]*n
    g = 12
    for i in range(n):
        x[i] = i/n
        q[i] = g+(g**2)*(x[i]-x[i]**2)
        b[i] = q[i]/(n**n)
    b[0] = 0
    b[n-1] = 0  # bien hardcodeado
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


def SOR(A, x, b, w, tol):
    n = len(A)
    s = x.copy()
    cant_iteraciones = 0
    e = 1
    while (e > tol):
        xant = x.copy()
        for i in range(n):
            x[i] = s[i] * (1 - w) + w * gauss_seidel(A[i], s, b[i], i, n)
        cant_iteraciones += 1
        s = x.copy()
        e = error(x, xant)
    p=calcularp(x)
    return (x, cant_iteraciones,p)
def calcularp(x)
    p=(ln((x[n-1]-x[n-2])/(x[n-2]-x[n-3])))/ln((x[n-2]-x[n-3])/(x[n-3]-x[n-4]))
    return p
def exportarresultadosacsv(x)
    import csv
    csvfile = "<path to output csv or txt>"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in x:
            writer.writerow([val])
            
            
def gauss_seidel(coeficientes, semilla, b, i, n):
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
