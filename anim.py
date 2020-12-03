import math
pi = 4. * math.atan( 1. )
from rayon import *

#camera.nom="steiner4.png"
#raycasting( camera, Prim( steiner4(), (255,200, 255)))

def rotaz( pt, theta):
	(x, y, z) = pt
	x2 = math.cos( theta)*x - math.sin( theta)*y 
	y2 = math.sin( theta)*x + math.cos( theta)*y 
	return (x2, y2, z)

#ca doit etre du O(n^2) mais n est petit
def concat_array_of_strings( tab) :
	ch=""
	for i in range( 0, len( tab)):
					ch= ch + tab[i]
	return ch

# convertit l'entier n en chaine de caracteres avec des 0 au debut 
# pour que sa longueur soit nbchiffres. 
# Ainsi l'ordre alphabetique et l'ordre des entier coincident
def string_of_int( n, nbchiffres):
	ch= [0]*nbchiffres
	for i in range(nbchiffres-1, -1, -1):
					ch[i]= str( n % 10)
					n = n // 10
	return concat_array_of_strings( ch)


#autre version de string_of_int, utilisant string.join( tab de caracteres)
def to_entier( n, nbchiffres):
	ch= [0]*nbchiffres
	for i in range(0, nbchiffres):
		ch[i]= (str( n % 10))[0]
		n = n // 10
	ch = [ ch[ nbchiffres - i - 1] for i in range(0, nbchiffres)]
	# ici ch est un tableau, pour le convertir en chaine:
	return "".join(ch)

def animation( cam, obj, n, nom):
	for i in range( 0, n) :
		theta = float( i)  * (2. * math.pi) / float( n) 
		r_o = rotaz( cam.o, theta)	 #tourner oeil o
		r_ox = rotaz( cam.ox, theta)	 #tourner axe ox (vers la droite)
		r_oy = rotaz( cam.oy, theta)	 #tourner axe oy (regard)
		r_oz = rotaz( cam.oz, theta)	 #tourner axeoz (vers le haut)
		cam_i = Camera( r_o, r_ox, r_oy, r_oz, cam.hsizeworld, cam.hsizewin, cam.soleil)
		cam_i.nom = nom + string_of_int( i, 5)
		raycasting( cam_i, obj)
'''
oeil=(0.001,-4.,0.003)
droite=  (1.,0.,0.)
regard=  (0.,1.,0.)
vertical=(0.,0.,1.)
#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
#ox, oy,oz orthogonaux et normés
camera=Camera( oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))

animation(camera, Prim(tore(0.45, 1.), (255, 0, 0)), 20, "IMG/roue")
'''
oeil=(0.001,-4.,0.003)
droite=  (1.,0.,0.)
regard=  (0.,1.,0.)
vertical=(0.,0.,1.)
#le repere local est tel que regard=oy, vertical=oz, droite=ox, o=oeil
#ox, oy,oz orthogonaux et normés
camera=Camera(oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))

