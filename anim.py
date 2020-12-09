# coding=utf-8
from rayon import *
from multiprocessing import Process
import math
import glob
import time
import os

pi = 4. * math.atan(1.)

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

def anim(cam, obj, nb, nom):
	folder_name = nom.split('/')[0] # on récupère le nom du dossier

	if not os.path.exists('./'+folder_name): # si le dossier n'existe pas on le crée
		os.makedirs(folder_name)

	t0= time.time()
	print("starting "+folder_name+" imgs generation")
	processes = []
	for i in range( 0, nb):
		theta= 2. * pi * float( i) / float( nb)
		o2 = rotaz( cam.o, theta)
		ox2 = rotaz( cam.ox, theta)		
		oy2 = rotaz( cam.oy, theta)		
		oz2 = rotaz( cam.oz, theta)		
		cam2 = Camera(o2, ox2, oy2, oz2, cam.hsizeworld, cam.hsizewin, cam.soleil)
		cam2.renderChessBoard = cam.renderChessBoard
		nom2 = nom + string_of_int( i, 10)
		cam2.nom = nom2
		processes.append(Process(target=raycasting,args=(cam2, obj),name="generate_"+folder_name+"0"))
	
	countStart = 0
	for p in processes: # on démarre le calcul de toutes les images
		p.start()
		print(folder_name+" start img"+str(countStart))
		countStart+=1

	countEnd = 0
	for p in processes: # attend que toutes les images soient généré
		p.join()
		print(folder_name+" end img"+str(countEnd))
		countEnd+=1

	t1 = time.time() - t0 # calcul le temps passer pour la génération des images
	print(folder_name+" imgs were generated in "+str(t1)+" s")

	frames = [] # on récupère toutes les images
	for f in glob.iglob('./'+folder_name+'/*.png'):
		frames.append(Image.open(f))

	first_image = frames[0]
	del frames[0] # on retire la première image car pillow va crée le gif à partir de la première image + toutes celles donner dans frames. On doit donc retirer la première
	gif=first_image.save('./'+folder_name+'/animation.gif', format='GIF', append_images=frames, save_all=True, duration=100, loop=0) # on crée le gif
	print("gif generated")

white_color = (255,255,255,255)

p_tore = Prim(tore(0.45, 1.), (0,0,255,200))
p_zitrus = Prim(zitrus(),white_color)
p_boule = Prim(boule((0., 2., -0.5), 1.), (255,0,0,150))
p_roman = Prim(roman(), white_color)
p_solitude = Prim(solitude(),white_color)
p_miau = Prim(miau(),white_color)
p_steiner2 = Prim(steiner2(),white_color)
p_steiner4 = Prim(steiner4(),white_color)
p_hyperboloide_2nappes = Prim(hyperboloide_2nappes(),white_color)
p_hyperboloide_1nappes = Prim(hyperboloide_1nappe(),white_color)
p_csg_op = Union((Intersection((p_tore,p_boule)),Difference((p_tore,p_boule)))) # heavy 
p_saturne = Prim(saturne(),white_color)
p_sextiqueDeBarth = Prim(sextiqueDeBarth(0.5),white_color)
p_weirdHeart = Prim(weirdHeart(),white_color)

def tore_anim():
	object_name = "tore"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	anim(camera, p_tore, 20, object_name+"/"+object_name)

def roman_anim():
	object_name = "roman"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	camera.renderChessBoard = True
	anim(camera, p_roman, 20, object_name+"/"+object_name)

def zitrus_anim():
	object_name = "zitrus"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 0.75, 100, normalize3((0., -1., 2.)))
	camera.renderChessBoard = True
	anim(camera, p_zitrus, 20, object_name+"/"+object_name)

def solitude_anim():
	object_name = "solitude"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 8, 100, normalize3((0., -1., 2.)))
	anim(camera, p_solitude, 20, object_name+"/"+object_name)

def miau_anim():
	object_name = "miau"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 8, 100, normalize3((0., -1., 2.)))
	anim(camera, p_miau, 20, object_name+"/"+object_name)

def steiner2_anim():
	object_name = "steiner2"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 10, 100, normalize3((0., -1., 2.)))
	anim(camera, p_steiner2, 20, object_name+"/"+object_name)

def steiner4_anim():
	object_name = "steiner4"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 5, 100, normalize3((0., -1., 2.)))
	anim(camera, p_steiner4, 20, object_name+"/"+object_name)

def hyperboloide_2nappes():
	object_name = "hyperboloide_2nappes"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 5, 100, normalize3((0., -1., 2.)))
	anim(camera, p_hyperboloide_2nappes, 20, object_name+"/"+object_name)

def hyperboloide_1nappes():
	object_name = "hyperboloide_1nappes"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 5, 100, normalize3((0., -1., 2.)))
	anim(camera, p_hyperboloide_1nappes, 20, object_name+"/"+object_name)

def csg_op_anim():
	object_name = "csg_op"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 1.5, 100, normalize3((0., -1., 2.)))
	anim(camera, p_csg_op, 20, object_name+"/"+object_name)

def saturne_anim():
	object_name = "saturne"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 1, 100, normalize3((0., -1., 2.)))
	anim(camera, p_saturne, 20, object_name+"/"+object_name)

def sextiqueDeBarth_anim():
	object_name = "sextiqueDeBarth"
	oeil=(-0,-4,0)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 8, 100, normalize3((0., -1., 2.)))
	anim(camera, p_sextiqueDeBarth, 20, object_name+"/"+object_name)

def weirdHeart_anim():
	object_name = "weirdHeart"
	oeil=(-0,-4,-2)
	droite=  (1.,0.,0.)
	regard=  (0.,1.,0.)
	vertical=(0.,0.,1.)
	camera=Camera(oeil, droite, regard, vertical, 16, 100, normalize3((0., -1., 2.)))
	anim(camera, p_weirdHeart, 20, object_name+"/"+object_name)


if __name__ == '__main__':
	'''
	tore_anim()
	roman_anim()
	zitrus_anim()
	solitude_anim()
	miau_anim()
	steiner2_anim()
	steiner4_anim()
	hyperboloide_2nappes()
	hyperboloide_1nappes()
	csg_op_anim()
	saturne_anim()
	sextiqueDeBarth_anim()
	weirdHeart_anim()
	'''
