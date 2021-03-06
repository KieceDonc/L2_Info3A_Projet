from dag import * 

def boule(tup1, r):
    (cx,cy,cz) = tup1
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x-Nb(cx))*(x-Nb(cx)) + (y-Nb(cy))*(y-Nb(cy)) + (z-Nb(cz))*(z-Nb(cz)) - Nb(r*r)
    
def tore( r, R):
    x=Var("x")
    y=Var("y")
    z=Var("z")
    tmp=x*x+y*y+z*z+Nb(R*R-r*r)
    return tmp*tmp- Nb(4.*R*R)*(x*x+z*z)

def steiner2():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x * x * y * y - x * x * z * z + y * y * z * z - x * y * z)

def steiner4():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return y * y - Nb( 2.) * x * y * y - x * z * z + x * x * y * y + x * x * z * z - z * z * z * z

def hyperboloide_2nappes():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return Nb(0.) - (z * z - (x * x + y * y + Nb(0.1)))

def hyperboloide_1nappe():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return Nb(0.)-(z * z - (x * x + y * y - Nb(0.1)))

def roman():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return ( x * x * y * y + x * x * z * z + y * y * z * z - Nb(2.) * x * y * z)

# https://lejournal.cnrs.fr/sites/default/files/styles/diaporama/public/assets/images/hauser_2.jpg?itok=sbbtGztR
def solitude():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x*x*y*z+x*y*y+y*y*y+y*y*y*z-x*x*z*z)

# https://lejournal.cnrs.fr/sites/default/files/styles/diaporama/public/assets/images/hauser_3.jpg?itok=c7zwNoRW
def miau(): 
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x*x*y*z+x*x*z*z+Nb(2)*y*y*z+Nb(3)*y*y*y)

# https://imaginary.org/fr/gallery/herwig-hauser-classic
def zitrus():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x*x+z*z-y*y*y*(Nb(1)-y)*(Nb(1)-y)*(Nb(1)-y))

# https://imaginary.org/fr/node/2221
def saturne(): 
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return ((Nb(0.2)*x*x+Nb(0.4)*y*y+z*z+Nb(0.12))*(Nb(0.2)*x*x+Nb(0.4)*y*y+z*z+Nb(0.12))-Nb(0.5)*(Nb(0.2)*x*x+Nb(0.4)*y*y))*(Nb(0.4)*x*x+Nb(0.6)*y*y+Nb(0.6)*z*z-Nb(0.1))

# https://imaginary.org/fr/gallery/oliver-labs
def sextiqueDeBarth(r):
    x=Var("x")
    y=Var("y")
    z=Var("z")
    P6 = (Nb(r)*Nb(r)*x*x-y*y)*(Nb(r)*Nb(r)*y*y-z*z)*(Nb(r)*Nb(r)*z*z-x*x)
    alpha = (Nb(2)*Nb(r)+Nb(1))*(Nb(4e-1))
    K = x*x+y*y+z*z-Nb(1)
    return P6-alpha*K

# https://imaginary.org/fr/node/888
def weirdHeart():
    y=Var("y")
    z=Var("z")
    return y*y+z*z*z-Nb(1)