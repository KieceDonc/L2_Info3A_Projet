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

def solitude(): # https://lejournal.cnrs.fr/sites/default/files/styles/diaporama/public/assets/images/hauser_2.jpg?itok=sbbtGztR
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x*x*y*z+x*y*y+y*y*y+y*y*y*z-x*x*z*z)

def miau(): # https://lejournal.cnrs.fr/sites/default/files/styles/diaporama/public/assets/images/hauser_3.jpg?itok=c7zwNoRW
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x*x*y*z+x*x*z*z+Nb(2)*y*y*z+Nb(3)*y*y*y)

def zitrus():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x*x+z*z-y*y*y*(Nb(1)-y)*(Nb(1)-y)*(Nb(1)-y))

def saturne():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return ((Nb(0.2)*x*x+Nb(0.4)*y*y+z*z+Nb(0.12))*(Nb(0.2)*x*x+Nb(0.4)*y*y+z*z+Nb(0.12))-Nb(0.5)*(Nb(0.2)*x*x+Nb(0.4)*y*y))*(Nb(0.4)*x*x+Nb(0.6)*y*y+Nb(0.6)*z*z-Nb(0.1))