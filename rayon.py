import math
import random
import os
import sys
from bernstein import *
from primitives import * 

from PIL import Image, ImageDraw, ImageFont

def interpole( x1, y1, x2, y2, x) :
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

def topolent(e):
    return e.topolent()


class Rayon( object):
    def __init__(self, source, dir):
        self.source=source
        self.dir=dir

class Camera( object):
    def __init__(self, o, ox, oy, oz, hsizeworld, hsizewin, soleil):
        self.o=o
        self.ox= ox #vers la droite du spectateur
        self.oy= oy #regard du spectateur
        self.oz= oz #vertical du spectateur
        self.hsizeworld=hsizeworld
        self.hsizewin=hsizewin
        self.soleil = normalize3(soleil)
        self.background=(100,100, 255)
        self.nom= "img.png"

    def generate_ray(self, x, z):
        (x0, y0, z0)= self.o
        kx = interpole( 0., 0., self.hsizewin, self.hsizeworld, float(x))
        kz = interpole( 0., 0., self.hsizewin, self.hsizeworld, float(z))
        return Rayon( (x0 + kx*self.ox[0] + kz*self.oz[0],
        y0 + kx*self.ox[1] + kz*self.oz[1],
        z0 + kx*self.ox[2] + kz*self.oz[2]),
        self.oy)

    def topolent(self,e):
        return e.topolent()

racines_precision = 1e-9

class Obj(object):
    def __init__(self):
        " "

class Prim(Obj):
    def __init__(self, fonc_xyz, color, transparency):
        self.fonc=fonc_xyz
        self.color=color
        if transparency == None : 
            self.transparency = 255
        else : 
            self.transparency = int(transparency)

    def intersection(self, rayon):
        dico = { "x": Nb(rayon.source[0]) + Nb(rayon.dir[0])*Var("t"),
        "y": Nb(rayon.source[1]) + Nb(rayon.dir[1])*Var("t"),
        "z": Nb(rayon.source[2]) + Nb(rayon.dir[2])*Var("t")}
        expression_en_t=self.fonc.evalsymb(dico)
        pol_t = topolent(expression_en_t)
        return racines(racines_precision,pol_t)

    def normale(self, tup):
        (x,y,z) = tup
        fx=self.fonc.derivee("x")
        fy=self.fonc.derivee("y")
        fz=self.fonc.derivee("z")
        dico={"x":x, "y":y, "z":z}
        (a,b,c)= (fx.eval(dico), fy.eval(dico), fz.eval(dico))
        return normalize3((a, b, c))

class Union(Obj):
    def __init__(self,objectList):
        self.objectList = objectList
        self.objectNormale = 0
        self.color = 0
        self.transparency = 255

    def intersection(self,rayon):
        roots = None
        r=0
        g=0
        b=0
        accumulateTransparency = 0
        accumulateCount = 0 # contient après exécution le nombre de fois où des composantes ont été additionner

        for x in range(len(self.objectList)):
            currentObject = self.objectList[x]
            currentRoots = currentObject.intersection(rayon)
            if currentRoots != None:
                roots = currentRoots
                self.objectNormale = currentObject
                (cr,cg,cb)=currentObject.color 
                r+= cr
                g+= cg
                b+= cb
                accumulateTransparency+=currentObject.transparency
                accumulateCount+= 1

        if(accumulateCount>0):
            self.color = (r/accumulateCount,g/accumulateCount,b/accumulateCount)
            self.transparency = accumulateTransparency/accumulateCount

        return roots

    def normale(self,tup):
        return self.objectNormale.normale(tup)

class Intersection(Obj):
    def __init__(self,objectList):
        self.objectList = objectList
        self.objectNormale = 0
        self.color = 0
        self.transparency = 255

    def intersection(self,rayon):
        roots = None
        r=0
        g=0
        b=0
        accumulateTransparency = 0
        accumulateCount = 0 # contient après exécution le nombre de fois où des composantes ont été additionner

        for x in range(len(self.objectList)):
            currentObject = self.objectList[x]
            currentRoots = currentObject.intersection(rayon)
            if currentRoots != None:
                roots = currentRoots
                self.objectNormale = currentObject
                (cr,cg,cb)=currentObject.color 
                r+= cr
                g+= cg
                b+= cb
                accumulateTransparency+=currentObject.transparency
                accumulateCount+= 1
            else :
                return None

        if(accumulateCount>0):
            self.color = (r/accumulateCount,g/accumulateCount,b/accumulateCount)
            self.transparency = accumulateTransparency/accumulateCount

        return roots

    def normale(self,tup):
        return self.objectNormale.normale(tup)

class Difference(Obj):
    def __init__(self,objectList):
        self.mainObject = objectList[0]
        self.objectList = objectList
        self.objectNormale = 0
        self.color = self.mainObject.color
        self.transparency = self.mainObject.transparency    

    def intersection(self,rayon):
        mainObjectRoots = self.mainObject.intersection(rayon)
        if mainObjectRoots != None : 
            for x in range(len(self.objectList)):
                if(x>0): # a changer, trouver comment retirer le premier élément
                    currentObject = self.objectList[x]
                    currentRoots = currentObject.intersection(rayon)
                    if currentRoots != None:
                        return None

            return mainObjectRoots
        else:
            return None

    def normale(self,tup):
        return self.mainObject.normale(tup)

def pscal3(tup1, tup2):
    (x1,y1,z1) = tup1
    (x2,y2,z2) = tup2
    return x1*x2 + y1*y2 + z1*z2

def clamp(mi, ma, v):
    return min(ma, max( mi, v))

def raycasting(cam, objet):
    img=Image.new("RGBA", (2*cam.hsizewin+1, 2*cam.hsizewin+1), (255,255,255,255))
    for xpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
        for zpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
            rayon= cam.generate_ray(xpix, zpix)
            roots=objet.intersection(rayon)
            transparency = 255
            if None==roots:
                (r,v,b)= cam.background
            else:
                t= hd(roots) # roots[0] #c'est le 1er element (un t) de la pire (tete, queue)
                pt=(xo,yo,zo)= (rayon.source[0]+ t*rayon.dir[0],
                rayon.source[1]+ t*rayon.dir[1],
                rayon.source[2]+ t*rayon.dir[2])
                (a,b,c)=normalize3(objet.normale(pt))
                transparency = int(objet.transparency)
                (rr,vv,bb)=objet.color
                (rr,vv,bb)= (float(rr), float(vv), float(bb))
                ps=pscal3((a,b,c), cam.soleil)
                if ps < -1. or 1 < ps:
                    print("PS="+str(ps))
                    ps = clamp(-1., 1., ps)
                coef= interpole(-1., 0.5, 1., 1., ps)
                r=coef*rr
                v=coef*vv
                b=coef*bb
                (r,v,b) = (int(r), int(v), int(b))
            img.putpixel(
            (xpix+cam.hsizewin,
            2*cam.hsizewin-(zpix+cam.hsizewin)),
            (r,v,b,transparency))
    img.show()
    img.save( cam.nom)


vec = 10
oeil=(1,-4,0)
droite= (1.,0.,0.)
regard= (0,1.,0.)
vertical=(0.,0.,1)
#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil

camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))

'''
def test_zitrus():
    oeil=(0,-2,0)
    camera=Camera( oeil, droite, regard, vertical, 0.5, 100, normalize3((0., -1., 2.)))
    camera.nom="zitrus.png"
    raycasting(camera,zitrus)

camera.nom="miau.png"
raycasting(camera,miau)

camera.nom="solitude.png"
raycasting(camera,solitude)

camera.nom="union-intersection-difference.png"
u = Union((Intersection((tore,boule)),Difference((tore,boule))))
raycasting(camera,u)


camera.nom="intersection.png"
raycastingIntersection(camera,tore,boule)

camera.nom="difference.png"
raycastingDifference(camera,tore,boule)


camera.nom="boule.png"
raycasting(camera,boule)

camera.nom="tore.png"
raycasting(camera,tore)

camera.nom="boule.png"
raycasting(camera, Prim( boule( (0., 2., -0.5), 1.), ((255,255,255))))

camera.nom="tore.png"
raycasting(camera, Prim( tore(0.45, 1.), (255,200, 255)))

camera.hsizeworld=10.
camera.nom="steiner2.png"
raycasting( camera, Prim( steiner2(), (255,200, 255)))

camera.hsizeworld=1.5
camera.nom="roman.png"
raycasting( camera, Prim( roman(), (255,200, 255)))

camera.nom="hyper1.png"
raycasting( camera, Prim( hyperboloide_1nappe(), (255,200, 255)))

camera.nom="hyper2.png"
raycasting( camera, Prim( hyperboloide_2nappes(), (255,200, 255)))

camera.nom="steiner4.png"
raycasting( camera, Prim( steiner4(), (255,200, 255)))
'''

'''

https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_de_Sturm
https://fr.wikipedia.org/wiki/Algorithme_de_recherche_d%27un_z%C3%A9ro_d%27une_fonction

'''