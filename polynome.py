def somme(p,q):
  n = len(p)
  m = len(q)
  r = max(n,m)
  k = 0 
  t = []
  while k<r:
    if(k<n and k<m):
      t.insert(k,p[k] + q[k])
    elif(k <n):
      t.insert(k,p[k])
    else :
      t.insert(k,q[k])
    k+=1
  return t

#p = [6,4,3,17]
#q = [8,0,5]
#print(somme(p,q))

def product(p,q):
  n = len(p)-1
  m = len(q)-1
  k = 0 
  t = [0 for i in range (n+m+1)]
  for k in range(n+m+1):
    ck = 0
    for i in range(k+1) :
      if (k-i<=m and i<=n):
        ck+=p[i]*q[k-i]
    t[k]=ck
  return t

#p = [5,1]
#q = [3,2,1]
#print(product(p,q))

def oppose(p):
  t = []
  for i in range(len(p)):
    t.insert(i,p[i]*-1)
  return t

def evalPoly(coeffs,val):
  result = 0 
  for k in range(len(coeffs)):
    result+=coeffs[k]*val**k
  return result