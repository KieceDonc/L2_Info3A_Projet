# coding=utf-8

from rayon import *
import math
pi = 4. * math.atan(1.)
#math.pi

def rotaz( pt, theta):
	c= math.cos( theta)
	s= math.sin( theta)
	(x, y, z) = pt
	x2= c*x - s*y
	y2= s*x + c*y
	z2= z
	return (x2,y2,z2)

def string_of_int( n, nbch):
	tabstr=[0]*nbch
	for i in range( nbch-1, -1, -1) :
		tabstr[i] = n % 10
		n = n // 10
	ch=""
	for i in range( 0, nbch):
		ch = ch + str( tabstr[i])  # ch += str( tabstr[i])
	return ch

def anim( cam, obj, nb, nom):
	for i in range( 0, nb):
		theta= 2. * pi * float( i) / float( nb)
		o2 = rotaz( cam.o, theta)
		ox2 = rotaz( cam.ox, theta)		
		oy2 = rotaz( cam.oy, theta)		
		oz2 = rotaz( cam.oz, theta)		
		cam2 = Camera( o2, ox2, oy2, oz2, cam.hsizeworld, cam.hsizewin, cam.soleil)
		nom2 = nom + string_of_int( i, 10)
		cam2.nom = nom2+'.png'
		raycasting( cam2, obj)

#https://imaginary.org/fr/node/2221

tore = Prim(tore(0.45, 1.), (0,0, 255),200)
boule = Prim(boule( (0., 2., -0.5), 1.), (255,0, 0), 150)
roman = Prim( roman(), (255,200, 255),255)
solitude = Prim(solitude(),(255,200,255),255)
miau = Prim(miau(),(255,200,255),255)
zitrus = Prim(zitrus(),(255,200,255),255)

def zitrus_anim():
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
	#ox, oy,oz orthogonaux et normés
	camera=Camera(oeil, droite, regard, vertical, 0.75, 100, normalize3((0., -1., 2.)))
	camera.nom="IMG/zitrus"
	anim( camera, zitrus, 20, "zitrus/zitrus")

def miau_anim():
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
	#ox, oy,oz orthogonaux et normés
	camera=Camera(oeil, droite, regard, vertical, 8, 100, normalize3((0., -1., 2.)))
	camera.nom="IMG/miau"
	anim( camera, miau, 20, "miau/miau")

miau_anim()