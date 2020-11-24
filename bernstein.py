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
      print(ci[k])
      current_bi+=(ci[k]*binom(i,k))/binom(deg,k)# evalNormalPoly(ci,k/n)
    bi.append(current_bi)
  return bi

def evalpol(ci,t):
  n = len(ci)
  p = 0
  bi = tobernstein(ci)
  for i in range(n):
    p+=bi[i]*bernstein(n,i,t)
  return p

print(tobernstein( [0., 10., 0.]))
