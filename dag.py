from polynome import *

class M(object):
	def __init__(self):
		" "

	def __add__(self, b):
		return Plus(self, b)

	def __mul__(self, b):
		return Mult(self, b)

	def __sub__(self, b):
		return Plus(self, Opp(b))

class Opp( M):
	def __init__(self, a):
		self.a=a

	def eval(self, dico):
		return 0. - self.a.eval(dico)

	def evalsymb(self, dico):
		return Opp(self.a.evalsymb(dico))

	def topolent( self) :
		return opposePoly(self.a.topolent())

	def derivee(self, name) :
		return Opp(self.a.derivee(name))

class Plus(M):
	def __init__(self, a, b):
		self.a=a
		self.b=b

	def eval(self, dico):
		return self.a.eval(dico) + self.b.eval(dico)

	def evalsymb(self, dico):
		return self.a.evalsymb(dico) + self.b.evalsymb(dico)

	def topolent(self):
		return sommePoly(self.a.topolent(), self.b.topolent())

	def derivee(self, name):
		return self.a.derivee(name) + self.b.derivee(name)

class Mult(M):
	def __init__(self, a, b):
		self.a=a
		self.b=b

	def eval(self, dico):
		return self.a.eval( dico) * self.b.eval(dico)

	def evalsymb(self, dico):
		return self.a.evalsymb(dico) * self.b.evalsymb(dico)

	def topolent(self) :
		return productPoly(self.a.topolent(), self.b.topolent())

	def derivee(self, name) :
		return self.a.derivee(name) * self.b + self.a * self.b.derivee(name)


class Nb(M):
	def __init__(self, n):
		self.nb=n

	def eval(self, dico):
		return self.nb

	def evalsymb(self, dico):
		return self

	def topolent(self) :
		return [self.nb]

	def derivee(self, name) :
		return Nb(0)

class Var(M):
	def __init__(self, nom):
		self.nom=nom
	def eval(self, dico):
		if self.nom in dico :   # if dico.has_key( self.nom )
			return dico[self.nom]
		else :
			print('erreur dans Var.eval: indefini :' + self.nom)
			return 1 / 0
	def evalsymb(self, dico):
		if self.nom in dico :   # if dico.has_key( self.nom )
			return dico[self.nom]
		else :
			return self	
	def topolent(self) :
		if self.nom == 't' :
			return [ 0, 1] 
		else :
			print('erreur dans Var.topolent: pas t mais ' + self.nom)

	def derivee(self, name) :
		if name==self.nom :
			return Nb( 1.)
		else:
			return Nb( 0.)
