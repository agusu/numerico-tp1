def main():
    s = [0]*n #semilla
    m = generarMatriz(n) #matriz 
    f = generarFuncion(n) #valores de la funcion, termino independiente
    itersw= dict()
    tol = 0.01
    #Se prueban con diferentes w para saber cual es el optimo, el que de menos
    #iteraciones 
    for w in range(1,2,0.05): #w del metodo SOR
        x, nroiter = SOR(m,s,f,w,tol)
        itersw[w]=nroiter
    minimo=1
    for (w, nroiter) in itersw:
        if nroiter<minimo:
            minimo=nroiter
            wopt=w
    tol = 0.0001
    x, nroiter = SOR(m,s,f,wopt,tol)
    
def generarFuncion(n):
    f=[0]*n
    x=[0]*n
    q=[0]*n
    g=2 #este es el numero de grupo lo deberiamos cambiar cuando nos digan que grupo somos
    for i in range(n):
        x[i]=i/n
        q[i]=g+(g*g)*(x[i]-x[i]*x[i])
        f[i]=q[i]/(n*n*n*n) #ya se que es horrible

    f[0]=0
    f[n-1]=0#bien hardcodeado
    print (f)
    return f
def generarCeros(n):
    matriz = []
    for i in range(n):
        vect=[0]*n
        matriz.append(vect)
    return matriz

def generarMatriz(n):
    if n < 5:
        return 0
    matriz = generarCeros(n)
    matriz[0][0]=1
    #1
    matriz[1][0]=-4
    matriz[1][1]=5
    matriz[1][2]=-4
    matriz[1][3]=1
    #i
    k=0
    for i in range(2,n-2):
        vect=[1,-4,6,-4,1]
        for j in range(k,5+k):
            matriz[i][j]=vect.pop()
        k+=1
    #n-1
    matriz[n-2]=matriz[1][::-1]
    #n
    matriz[n-1][n-1]=1



def SOR(A,x,b,w,tol):
    n = len(A)
    s = x.copy()
    xant = [None]*n
    nroiter = 0
    while(e > tol):
        xant = x.copy()
        for i in range(n):
            x[i] = s[i]*(1-w)+w*GS(A[i],s,b[i],i,n)
        nroiter += 1
        s = x.copy()
        e = error(x,xant)
    return (x, nroiter)

   
def GS(a,s,b,i,n):
    suma = 0
    #der
    j = i +1
    if (j != n):
        while (j<n & a[j] != 0):
            suma += a[j]*s[j]/a[i]
            j +=1
    #izq
    j = i -1
    if (j != -1):
        while (j >= 0 & a[j] != 0): 
            suma += a[j]*s[j]/a[i]
            j = j-1
    return b/a[i]-suma

def error(x,xant):
    resultado = []
    for i in range(len(x)):
        resultado.append((x[i]-xant[i]))
    norma = max(resultado)/max(x)
    return norma

generarMatriz(10)
generarFuncion(10)
