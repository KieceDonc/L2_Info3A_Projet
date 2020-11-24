import math
pi = 4. * math.atan( 1. )
from rayon import *

#camera.nom="steiner4.png"
#raycasting( camera, Prim( steiner4(), (255,200, 255)))

def rotaz(pt, theta):
	(x, y, z) = pt
	x2 = math.cos( theta)*x - math.sin( theta)*y 
	y2 = math.sin( theta)*x + math.cos( theta)*y 
	return (x2, y2, z)

def to_entier(n, nbchiffres):
	ch= [0]*nbchiffres
	for i in range(0, nbchiffres):
		ch[i]= (str( n % 10))[0]
		n = n // 10
	ch = [ ch[ nbchiffres - i - 1] for i in range(0, nbchiffres)]
	# ici ch est un tableau, pour le convertir en chaine:
	return "".join(ch)

def animation(cam, obj, n, nom):
	for i in range( 0, n) :
		theta = float( i)  * (2. * math.pi) / float(n) 
		r_o = rotaz(cam.o, theta)	
		r_ox = rotaz(cam.ox, theta)	
		r_oy = rotaz(cam.oy, theta)	
		r_oz = rotaz(cam.oz, theta)	
		cam_i = Camera(r_o, r_ox, r_oy, r_oz, cam.hsizeworld, cam.hsizewin, cam.soleil)
		cam_i.nom = nom + to_entier( i, 4)
		raycasting( cam_i, obj)

oeil=(0.001,-4.,0.003)
droite=  (1.,0.,0.)
regard=  (0.,1.,0.)
vertical=(0.,0.,1.)
#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
#ox, oy,oz orthogonaux et normés
camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))

animation( camera, Prim( tore(0.45, 1.), (255, 0, 0)), 20, "IMG/roue")