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
  if(n==2 and i == 1):
    return 2
  if(i<2 or n<2):
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
    if(v[x]<_max):
      _max = v[x]
  return _max

# recherche des racines dans la base de bernstein
def solve(epsilon,tab,t1,t2,soluc):
  if(mintab(tab)>=0 and maxtab(tab)<=0):
    return 0
  else: 
    if(t2-t1<epsilon):
      return 0#cons((t1+t2/2),soluc)
    else:
      return 0