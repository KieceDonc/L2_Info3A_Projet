from dag import *
from basique import *

def casteljau(polbe) :
	n = len(polbe)
	couches=[None]*n
	couches[0] = polbe
	for c in range(1, n):
		couches[ c ] = milieux( couches[ c-1 ])
	return (vecteur( n, (lambda i : couches[i][0])), vecteur( n, (lambda i : couches[n-i-1][i])))

# calcul un factoriel
def fact(n): 
  if(n<2):
    return 1
  x=1
  for i in range(2,n+1):
      x*=i
  return x

# calcul le coefficient binomial de (n)
#                                   (i)
def binom(n,i):
  if(i<1 or n<1):
    return 1
  n_fac = fact(n) # valeur de n!
  i_fac = fact(i) # valeur de i!
  n_less_i_fac = fact(n-i)

  return n_fac/(i_fac*n_less_i_fac)

# calcul B,i,n(t)
def bernstein(n,i,t):
  return binom(n,i)*t**i*(1-t)**(n-i) # a**b = a^b 

# calcul les coefficients de bernstein bi de degré n
def tobernstein(ci):
  deg = len(ci)-1
  bi = []
  for i in range(deg+1):
    current_bi = 0
    for k in range(min(i+1,deg+1)):
      current_bi+=(ci[k]*binom(i,k))/binom(deg,k)
    bi.append(current_bi)
  return bi

# évalue la valeur d'un polynome à base canonique ( aux coefficients ci ) vers la base de bernstein
def evalPoly(ci,t):
  deg = len(ci)-1
  p = 0
  bi = tobernstein(ci)
  for i in range(deg+1):
    p+=bi[i]*bernstein(deg,i,t)
  return p

# recherche l'élément le plus petit dans le tableau
def mintab(v):
  _min = v[0]
  for x in range(len(v)):
    if(v[x]<_min):
      _min = v[x]
  return _min

# recherche l'élément le plus grand dans le tableau
def maxtab(v):
  _max = v[0]
  for x in range(len(v)):
    if(v[x]>_max):
      _max = v[x]
  return _max

'''
si polynome p est dans la base de bernstein, alors p( [0, 1]) est dans [mintab( p_i), maxtab( p_i)] , les p_i etant les coefs de p dans la base de bernstein
casterljau( p dans la base de bernstein) rend p1(X: 0..0.5) les coefs de p( 2x) 
et de p2(X:0.5, 1) les coefs de p( 2x-1)
'''

def solve(epsilon, polbe, t1, t2, racines):
	(mi, ma) = (mintab( polbe), maxtab( polbe))	
	if ma < 0 or 0 < mi :
		return racines
	else:
		tm = milieu(t1, t2)
		dt = t2 - t1
		if dt < epsilon :
			return cons(tm, racines)
		else :
			(p1, p2)=casteljau(polbe)
			return solve(epsilon, p1, t1, tm, solve(epsilon, p2, tm, t2, racines))

'''
	print( solve( 1e-10, [ 1, -2, -2, 1], 0., 1., None))
	print( solve( 1e-10, [ 1, -3, 3, -1], 0., 1., None)) 
'''

def solvegt1(epsilon, polca):
	n= len(polca)
	d= n-1
	aux = vecteur(n, (lambda i: polca[d-i]))
	polbe= tobernstein( aux)
	zeros= solve(epsilon, polbe, 0., 1., None)
	return reverse(mymap((lambda x: 1. / x), zeros), None)	

def racines(eps, polca):
	return solvegt1(eps, polca)
'''
print(solvegt1( 1e-10, [ -7, 1] ) ) # 7
print(solvegt1( 1e-10, [15, -8, 1]) ) # 3, 5
t=Var('t')
print(solvegt1( 1e-10, ((t-Nb(3))*(t-Nb(5))).topolent()))
print(solvegt1( 1e-10, ((t-Nb(3))*(t-Nb(13.))*(t-Nb(5))).topolent()))
'''