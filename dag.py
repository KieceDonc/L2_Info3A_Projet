class M(object):
  def __init__(self):
    "   "

  def __add__( self, b):
    return Plus(self, b)

  def __mul__( self, b):
    return Mult(self, b)

  def __sub__(self, b):
    return Plus(self, Opp(b))


class Opp(M):
  def __init__(self, a):
    self.a=a

  def eval(self,dico):
    return (0-self.a.eval(dico))

  def evalsymb(self,dico):
    return (Opp(self.a.evalsymb(dico)))

  def derivee(self,nomvar):
    return Opp(self.a.derivee(nomvar))


class Plus(M):
  def __init__(self, a, b):
    self.a=a
    self.b=b
 
  def eval(self,dico):
    return(self.a.eval(dico)+self.b.eval(dico))

  def evalsymb(self,dico):
    return self.a.evalsymb(dico)+self.b.evalsymb(dico)

  def derivee(self,nomvar):
    return Plus(self.a.derivee(nomvar),self.b.derivee(nomvar))


class Mult(M):
  def __init__(self, a, b):
    self.a=a
    self.b=b

  def eval(self,dico):
    return(self.a.eval(dico)*self.b.eval(dico))

  def evalsymb(self,dico):
    return self.a.evalsymb(dico)*self.b.evalsymb(dico)

  def derivee(self,nomvar):
    return Mult(self.a*self.b.derivee(nomvar),self.b*self.a.derivee(nomvar))
    

class Nb(M):
  def __init__(self, n):
    self.nb=n

  def eval(self,dico):
    return self.nb

  def evalsymb(self,dico):
    return self.nb

  def derivee(self,nomvar):
    if(self.nb==nomvar):
      return Nb(1)
    else:
      return (Nb(0))


class Var(M):
  def __init__(self, nom):
    self.nom=nom

  def eval(self,dico):
    if(self.nom in dico):
      return(dico[self.nom]) # pas sur
    else :
      return None # pas sur

  def evalsymb(self,dico):
    if(self.nom in dico):
      return dico[self.nom]
    else:
      return self

  def derivee(self,nomvar):
    if(self.nom == nomvar):
      return Nb(1)
    else:
      return Nb(0)


#x=Var("x")
#y=Var("y")
#z=Var("z")
#cercle = Plus(Plus(Mult(x,x),Mult(y,y)),Opp(Nb(-1)))
#print(cercle.eval( { 'x' : 1, 'y': -1}))