import math
import random
import os
import sys
from bernstein import *
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

class Obj(object):
    def __init__(self):
        " "

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

class Prim(Obj):
    def __init__(self, fonc_xyz, color):
        self.fonc=fonc_xyz
        self.color=color

    def intersection(self, rayon):
        dico = { "x": Nb(rayon.source[0]) + Nb(rayon.dir[0])*Var("t"),
        "y": Nb(rayon.source[1]) + Nb(rayon.dir[1])*Var("t"),
        "z": Nb(rayon.source[2]) + Nb(rayon.dir[2])*Var("t")}
        expression_en_t=self.fonc.evalsymb(dico)
        pol_t = topolent(expression_en_t)
        return racines(1e-9,pol_t)

    def normale(self, tup):
        (x,y,z) = tup
        fx=self.fonc.derivee("x")
        fy=self.fonc.derivee("y")
        fz=self.fonc.derivee("z")
        dico={"x":x, "y":y, "z":z}
        (a,b,c)= (fx.eval(dico), fy.eval(dico), fz.eval(dico))
        return normalize3((a, b, c))

def pscal3(tup1, tup2):
    (x1,y1,z1) = tup1
    (x2,y2,z2) = tup2
    return x1*x2 + y1*y2 + z1*z2

def clamp(mi, ma, v):
    return min(ma, max( mi, v))

def raycasting(cam, objet):
    img=Image.new("RGB", (2*cam.hsizewin+1, 2*cam.hsizewin+1), (255,255,255))
    for xpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
        for zpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
            rayon= cam.generate_ray(xpix, zpix)
            roots=objet.intersection(rayon)
            if None==roots:
                (r,v,b)= cam.background
            else:
                t= hd(roots) # roots[0] #c'est le 1er element (un t) de la pire (tete, queue)
                pt=(xo,yo,zo)= (rayon.source[0]+ t*rayon.dir[0],
                rayon.source[1]+ t*rayon.dir[1],
                rayon.source[2]+ t*rayon.dir[2])
                (a,b,c)=normalize3(objet.normale(pt))
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
            (r,v,b))
    img.show()
    img.save( cam.nom)

oeil=(0.001,-4.,0.003)
droite= (1.,0.,0.)
regard= (0.,1.,0.)
vertical=(0.,0.,1.)
#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil

intersection = 'intersection'
union = 'union'
diff = 'difference'

def raycastingIntersection(cam,object0,object1):
    if(object0==None or object1==None):
        print("raycasting erreur : un paramètre est null")
    else:  
        img=Image.new("RGB", (2*cam.hsizewin+1, 2*cam.hsizewin+1), (255,255,255))
        for xpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
            for zpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
                rayon= cam.generate_ray( xpix, zpix)
                roots_obj0 = object0.intersection(rayon)
                if roots_obj0==None:
                    (r,v,b)= cam.background
                else:
                    roots_obj1 = object1.intersection(rayon)
                    if roots_obj1 == None:
                        (r,v,b)= cam.background
                    else:
                        t= hd(roots_obj0) # roots[0] #c'est le 1er element (un t) de la pire (tete, queue)
                        pt=(xo,yo,zo)= (rayon.source[0]+ t*rayon.dir[0],
                        rayon.source[1]+ t*rayon.dir[1],
                        rayon.source[2]+ t*rayon.dir[2])
                        (a,b,c)=normalize3(object0.normale(pt))
                        (rr0,vv0,bb0)=object0.color
                        (rr0,vv0,bb0)= (float(rr0), float(vv0), float(bb0))
                        (rr1,vv1,bb1)=object1.color
                        (rr1,vv1,bb1)= (float(rr1), float(vv1), float(bb1))
                        (rr,vv,bb)= ((rr0+rr1)/2, (vv0+vv1)/2, (bb0+bb1)/2)
                        ps=pscal3((a,b,c), cam.soleil)
                        if ps < -1. or 1 < ps:
                            print("PS="+str(ps))
                            ps = clamp( -1., 1., ps)
                        coef= interpole( -1., 0.5, 1., 1., ps)
                        r=coef*rr
                        v=coef*vv
                        b=coef*bb
                        (r,v,b) = (int(r), int(v), int(b))
                img.putpixel(
                (xpix+cam.hsizewin,
                2*cam.hsizewin-(zpix+cam.hsizewin)),
                (r,v,b))
        img.show()
        img.save( cam.nom)

def raycastingDifference(cam,object0,object1):
    if(object0==None or object1==None):
        print("raycasting erreur : un paramètre est null")
    else:  
        img=Image.new("RGB", (2*cam.hsizewin+1, 2*cam.hsizewin+1), (255,255,255))
        for xpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
            for zpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
                rayon= cam.generate_ray( xpix, zpix)
                roots_obj0 = object0.intersection(rayon)
                if roots_obj0==None:
                    (r,v,b)= cam.background
                else:
                    roots_obj1 = object1.intersection(rayon)
                    if roots_obj1 != None:
                        (r,v,b)= cam.background
                    else:
                        t= hd(roots_obj0) # roots[0] #c'est le 1er element (un t) de la pire (tete, queue)
                        pt=(xo,yo,zo)= (rayon.source[0]+ t*rayon.dir[0],
                        rayon.source[1]+ t*rayon.dir[1],
                        rayon.source[2]+ t*rayon.dir[2])
                        (a,b,c)=normalize3(object0.normale(pt))
                        (rr,vv,bb)=object0.color
                        (rr,vv,bb)= (float(rr), float(vv), float(bb))
                        ps=pscal3((a,b,c), cam.soleil)
                        if ps < -1. or 1 < ps:
                            print("PS="+str(ps))
                            ps = clamp( -1., 1., ps)
                        coef= interpole( -1., 0.5, 1., 1., ps)
                        r=coef*rr
                        v=coef*vv
                        b=coef*bb
                        (r,v,b) = (int(r), int(v), int(b))
                img.putpixel(
                (xpix+cam.hsizewin,
                2*cam.hsizewin-(zpix+cam.hsizewin)),
                (r,v,b))
        img.show()
        img.save( cam.nom)

def raycastingUnion(cam,object0,object1):
    if(object0==None or object1==None):
        print("raycasting erreur : un paramètre est null")
    else:  
        img=Image.new("RGB", (2*cam.hsizewin+1, 2*cam.hsizewin+1), (255,255,255))
        for xpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
            for zpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
                rayon= cam.generate_ray( xpix, zpix)
                roots_obj0 = object0.intersection(rayon)
                roots_obj1 = object1.intersection(rayon)
                if roots_obj0==None and roots_obj1==None:
                    (r,v,b)= cam.background
                else:
                    objectToWorkWith = None
                    t = 0 
                    if roots_obj0!=None and roots_obj1 == None:
                        (rr,vv,bb)=object0.color
                        (rr,vv,bb)= (float(rr), float(vv), float(bb))
                        objectToWorkWith = object0
                        t = hd(roots_obj0)
                    elif roots_obj1!=None and roots_obj0 == None:
                        (rr,vv,bb)=object1.color
                        (rr,vv,bb)= (float(rr), float(vv), float(bb))      
                        objectToWorkWith = object1          
                        t = hd(roots_obj1)
                    else:
                        (rr0,vv0,bb0)=object0.color
                        (rr0,vv0,bb0)= (float(rr0), float(vv0), float(bb0))
                        (rr1,vv1,bb1)=object1.color
                        (rr1,vv1,bb1)= (float(rr1), float(vv1), float(bb1))
                        (rr,vv,bb)= ((rr0+rr1)/2, (vv0+vv1)/2, (bb0+bb1)/2)
                        objectToWorkWith = object0
                        t = hd(roots_obj0)
                    pt=(xo,yo,zo)= (rayon.source[0]+ t*rayon.dir[0],
                    rayon.source[1]+ t*rayon.dir[1],
                    rayon.source[2]+ t*rayon.dir[2])
                    (a,b,c)=normalize3(objectToWorkWith.normale(pt))
                    ps=pscal3((a,b,c), cam.soleil)
                    if ps < -1. or 1 < ps:
                        print("PS="+str(ps))
                        ps = clamp( -1., 1., ps)
                    coef= interpole( -1., 0.5, 1., 1., ps)
                    r=coef*rr
                    v=coef*vv
                    b=coef*bb
                    (r,v,b) = (int(r), int(v), int(b))
                img.putpixel(
                (xpix+cam.hsizewin,
                2*cam.hsizewin-(zpix+cam.hsizewin)),
                (r,v,b))
        img.show()
        img.save( cam.nom)
        
camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
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



tore = Prim(tore(0.45, 1.), ((0,0, 255)))
boule = Prim(boule( (0., 2., -0.5), 1.), (255,0, 0))

camera.nom="union.png"
raycastingUnion(camera,tore,boule)

'''
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