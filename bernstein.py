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
def inter_constant( epsilon, polca):
	assert( 1==len(polca))
	if polca[ 0] <= 0 :
		return cons( (epsilon, 1.), None)
	else:
		return None

def inter_lineaire( epsilon, polca):
	assert( 2==len(polca))
	a=polca[1]
	b=polca[0]
	if 0.==a :
		return inter_constant( epsilon,  [b] )
	else:
		y0=b 
		y1=a+b
		cas = y0 * y1
		if cas > 0 :
			if y0 <= 0. :
				return cons( (epsilon, 1.), None)
			else:
				return None
		else :			
			#il y a une racine:
			rac= (0.-b) / float(a)
			if y1 <= 0. :
				return cons( (rac, 1.), None)
			else:
				return cons( (epsilon, rac), None)

'''
polca est un polynome dans la base canonique
on retourne [0, 1] inter { x | polca(x) <= 0} : c'est une liste d'intervalles (un intervalle est une paire: (a: un nombre, b: un nombre >= a) tq polca est négatif dans ces intervalles)
'''

# kons est un cons special pour study_interval : 
# on fusionne le premier intervalle (t1, t2) et le suivant (t3, t4) dans la liste si t2==t3
def kons( t1t2, liste):
	(t1, t2)=t1t2
	if None==liste:
		return cons( (t1, t2), liste)
	else:
		((t3, t4), q) = (hd( liste), tl( liste))
		if t2==t3:
			return cons( (t1,t4), q)
		else:
			return cons( (t1, t2), liste)

def study_interval( epsilon, polbe, t1, t2, liste_a_droite) :
	(mi, ma)= (mintab( polbe), maxtab( polbe))
	if 0. < mi : # polynome > 0. donc vide
		return liste_a_droite
	elif ma <= 0. :
		return kons( (t1, t2), liste_a_droite) 
	else:
		dt = t2 - t1
		tm = (t1+t2)/2.
		if dt < epsilon :
			return kons( (t1, t2), liste_a_droite)
		(pol1, pol2)= casteljau( polbe)
		return study_interval( epsilon, pol1, t1, tm, \
			study_interval( epsilon, pol2, tm, t2, liste_a_droite))

# intervalle (t1, t2) dans [0, 1] --> (1/t2, 1/t1)
def inverse_interval(t1t2): 
	(t1,t2) = t1t2
	if 0.== t1:
		return (1./t2, 1e20)
	return (1./t2, 1./t1)
	
def inter_polca(epsilon, polca):
	n=len(polca)
	polinv = [polca[n-i-1] for i in range( 0, n)]
	ivals=inter_polca_01(epsilon,  polinv)
	#les racines sont dans (0, 1), on les inverse :
	ivals = reverse(ivals) # car 1/x est decroissant
	return mymap( inverse_interval, ivals)

# inter_polca_01 rend une liste d'intervalle dans [0, 1] où polca est négatif :
def inter_polca_01( epsilon,  polca):
	#on elimine les coefficients nuls de bas degre
	polca= ltov( eteter( (lambda coeff: abs( coeff) >= 1e-6), vtol( polca)))
	n=len( polca)
	if 0==n : # polynome identiquement nul
		return cons( (epsilon, 1.), None)
	elif 1==n: # cas polynome constant
		return inter_constant( epsilon, polca)
	elif 2==n : # cas polynome degre 1: a*t+b
		return inter_lineaire( epsilon, polca)
	else:
		polbe= tobernstein( polca)
		ivals = study_interval( epsilon, polbe, 0., 1., None)
		return ivals