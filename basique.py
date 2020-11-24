def vecteur(n, f):
	return [f(i) for i in range(0, n)]

def cons( t, q):
	return (t, q)

def hd(l):
	assert(None != l) # None  != l
	(t, q)= l
	return t

def tl(l):
  assert(None != l) # None  != l
  (t, q)= l
  return q

def mymap(f, l):
	if None==l:
		return None
	else:
		return cons(f( hd( l)), mymap( f, tl( l)))

def reverse(l, pile):
  if None==l:
    return pile
  else:
    return reverse(tl(l), cons(hd( l), pile))

def milieu(a, b):
	return (a+b) / 2.

def milieux( v):
	return vecteur(len( v) - 1, (lambda i: milieu( v[i], v[i+1])))


# a et b sont 2 listes d'intervalles
# on calcule leur intersection: une liste d'intervalles
def inter( a, b):
	if None==a or None==b :
		return None
	else:
		((a1,a2), qa) = (hd(a), tl(a))
		((b1,b2), qb) = (hd(b), tl(b))
		assert( a1 <= a2)
		assert( b1 <= b2)
		if a1 > b1 :
			return inter( b, a)
		elif a2 < b1 :
			return inter( qa, b)
		elif b2 <= a2 :
			return cons( (b1, b2), inter( a, qb))
		else:
			return cons( (b1, a2), inter( qa, b))

#convertir vecteur v en liste:
def vtol( v):
	l=None
	for i in range( len(v)-1, -1, -1):
		l=cons( v[i], l) 
	return l

#convertir liste en vecteur:
def ltov( l):
	n=0
	l2=l
	while l2 != None:	
		l2=tl( l2)
		n += 1
	v=[None]*n
	l2=l
	for i in range( 0, n, 1):
		v[i]= hd( l2)
		l2= tl( l2)	
	return v

def intersec( vec1, vec2):
	return ltov( inter( vtol( vec1), vtol( vec2)))
