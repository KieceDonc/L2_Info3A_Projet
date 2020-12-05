# coding=utf−8

import math
import random
infini=float("inf")


def vecteur(n, f):
	return [f(i) for i in range(0, n)]

def is_num(v):
	return (type( v) is float) or (type( v) is int)

def neq(a, b):
	return not( a==b)

def eq(a, b):
	return a==b

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

# foldl( +, 0, (1, (2, (3, None)))) rend la somme des elts de la liste
def foldl(operation, silistevide, liste):
	if None==liste :
		return silistevide
	else:
		return foldl( operation, operation( silistevide, hd( liste)), tl( liste))

#longueur d'une liste:
def lgr(liste):
	return foldl( (lambda n, li : n+1), 0, liste)

#on supprime les elts en tete de liste qui ne satisfont pas pred
def eteter(predicat_keep, l):
	if None==l or predicat_keep( hd(l)):
		return l
	else:
		return eteter( predicat_keep, tl( l))

def filtrage(tokeep, l):
	if None==l:
		return None
	elif tokeep( hd( l)):
		return cons( hd( l), filtrage( tokeep, tl( l)))
	else:
		return filtrage( tokeep, tl( l))

def mymap(f, l):
	if None==l:
		return None
	else:
		return cons(f( hd( l)), mymap( f, tl( l)))

#renverse une liste
def reverse( l):
	pile=None
	while neq( None, l) :
		pile=cons( hd(l), pile)
		l= tl( l)
	return pile
def milieu(a, b):
	return (a+b) / 2.

def milieux(v):
	return vecteur(len( v) - 1, (lambda i: milieu( v[i], v[i+1])))


# a et b sont 2 listes d'intervalles
# on calcule leur intersection: une liste d'intervalles
def inter(a, b):
	if None==a or None==b :
		return None
	else:
		((a1,a2), qa) = (hd(a), tl(a))
		((b1,b2), qb) = (hd(b), tl(b))
		assert( a1 <= a2)
		assert( b1 <= b2)
		if a1 > b1 :
			return inter(b, a)
		elif a2 < b1 :
			return inter(qa, b)
		elif b2 <= a2 :
			return cons((b1, b2), inter(a, qb))
		else:
			return cons((b1, a2), inter(qa, b))

#convertir vecteur v en liste:
def vtol(v):
	l=None
	for i in range(len(v)-1, -1, -1):
		l=cons(v[i], l) 
	return l

#convertir liste en vecteur:
def ltov(l):
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

def intersec(vec1, vec2):
	return ltov(inter(vtol(vec1),vtol(vec2)))


def vec2xyz(v):
	assert( len( v) == 4 and v[3]==1)
	return (v[0], v[1], v[2])

def vec2abc(v ):
	assert( len( v) == 4 and v[3]==0)
	return (v[0], v[1], v[2])

def vec2abcd(v) :
	assert( len( v) == 4 )
	return (v[0], v[1], v[2], v[3])

def xyz2vec(pt):
	(x, y, z) = pt
	return [x, y, z, 1]

def abc2vec(abc):
	(a, b, c) = abc
	return [a, b, c, 0]

def abcd2vec(abcd):
	(a, b, c, d)=abcd
	return [a, b, c, d]

def plus_vect(u, v):
	assert( len(u)==len(v))
	return [u[i]+v[i] for i in range( 0, len(u), 1)]

def moins_vect(u, v):
	assert( len(u)==len(v))
	return [u[i]-v[i] for i in range( 0, len(u), 1)]

def pscal(u, v):
	assert( len(u)==len(v))
	s=0
	for i in range( 0, len(u), 1):
		s += u[i]*v[i]
	return s

def matrice(nl, nc, f):
	return vecteur( nl, (lambda l : vecteur( nc, (lambda c: f( l, c)))))

#produit matrice vecteur, attention: le vecteur [1, 2, 3...] est un vecteur colonne
def mat_vec(m, v):
	nl= len( m)
	nc= len( m[0])
	assert( nc==len(v))
	return vecteur( nl, (lambda li : sigma( 0, nc-1, (lambda co: m[li][co] * v[ co] ))))

def mat_mat(a, b):
	la= len( a)
	lb= len( b)
	ca= len( a[0])
	cb= len( b[0])
	assert( ca==lb)
	return matrice( la, cb, \
		(lambda l, c: sigma( 0, ca-1, (lambda k: a[l][k] * b[k][c]))))

#produit vecteur matrice, attention: le vecteur [1, 2, 3...] est un vecteur ligne
def vec_mat( v, a):
	la = len( a)
	ca = len( a[0])
	assert( len( v) ==la)
	return vecteur( ca, (lambda c: sigma( 0, la-1, (lambda k: v[k]*a[k][c]))))

#gestion des transformations 3D
def mat_trans( tx, ty, tz):
	return [[1., 0., 0., tx],
			[0., 1., 0., ty],
			[0., 0., 1., tz],
			[0., 0., 0., 1.]]

#scaling, ou affinite
def mat_affinite( sx, sy, sz):
	assert( not( sx * sy * sz == 0))
	return [[sx, 0., 0., 0.],
			[0., sy, 0., 0.],
			[0., 0., sz, 0.],
			[0., 0., 0., 1.]]

def mat_rota_Oz( theta):
	c= math.cos( theta)
	s= math.sin( theta)
	return [[c, -s, 0., 0.],
			[s, c, 0., 0.],
			[0., 0., 1., 0.],
			[0., 0., 0., 1.] ]

def mat_rota_Ox( theta):
	c= math.cos( theta)
	s= math.sin( theta)
	return [[1., 0., 0., 0.],
			[0, c, -s, 0.],
			[0, s, c,  0.],
			[0., 0., 0., 1.] ]

def mat_rota_Oy( theta):
	c= math.cos( theta)
	s= math.sin( theta)
	return [[c, 0, s, 0],
		[0, 1, 0, 0],
		[-s, 0, c, 0],
		[0, 0, 0, 1]]


class Trfo( object):
	def __init__( self, direct, inverse):
		self.direct = direct
		self.inverse = inverse

def trf_trans( tx, ty, tz):
	return Trfo( mat_trans( tx, ty, tz), mat_trans( -tx, -ty, -tz))

def trf_affinite( x, y, z):
	return Trfo( mat_affinite( x, y, z), mat_affinite( 1./x, 1./y, 1./z))

def trf_rota_Oz( theta):
	return Trfo( mat_rota_Oz( theta), mat_rota_Oz( -theta))

def trf_rota_Ox( theta):
	return Trfo( mat_rota_Ox( theta), mat_rota_Ox( -theta))

def trf_rota_Oy( theta):
	return Trfo( mat_rota_Oy( theta), mat_rota_Oy( -theta))

def trf_inverse( transformation ):
	return Trfo( transformation.inverse, transformation.direct)


def pscal3(tup1, tup2):
    (x1,y1,z1) = tup1
    (x2,y2,z2) = tup2
    return x1*x2 + y1*y2 + z1*z2

def clamp(mi, ma, v):
    return min(ma, max( mi, v))

def interpole(x1, y1, x2, y2, x) :
    # x=x1 -> y=y1
    # x=x2 -> y=y2
    x1, y1, x2, y2, x= float(x1), float(y1), float( x2), float(y2), float(x)
    return (x-x2)/(x1-x2)*y1 + (x-x1)/(x2-x1)*y2

def normalize3(tup):
    (a, b, c) = tup
    (a,b,c)=(float(a),float(b),float(c))
    n=math.sqrt(a*a+b*b+c*c)
    if 0.==n:
        return (0.,0.,0.)
    else:
        return (a/n, b/n, c/n)

#somme des fi( i) pour i de i1 a i2
def sigma( i1, i2, fi):
	if i1==i2:
		return fi( i1)
	else:
		return fi( i1 ) + sigma( i1+1, i2, fi)

def topolent( e):
	return e.topolent()