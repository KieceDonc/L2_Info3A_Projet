import math
import random
import os
import sys
from bernstein import *
from primitives import * 

from PIL import Image, ImageDraw, ImageFont

class Rayon(object):
	def __init__(self, source, dir):
		self.source=source
		self.dir=dir

#Contact decrit un point d'intersection entre un rayon et un solide:
# il y a le t,  un pt: (x,y,z), un plan: (a,b,c,d), une couleur : int

class Contact(object):
	def __init__( self, t, pt, plan, color):
		self.t = t
		self.pt = pt
		self.plan = plan
		self.color = color

#trf est une Trfo, contact est un Contact
def transform_contact(trf, contact) :
	if is_num( contact):
		print('a nombre dans transform_contact=' + str( contact))
		return 1/0
	t_pt = vec2xyz(mat_vec(trf.direct, xyz2vec( contact.pt)))
	t_plan= vec2abcd(vec_mat(contact.plan, trf.inverse))
	return Contact(contact.t, t_pt, t_plan, contact.color)

class Camera(object):

	def __init__(self, o, ox, oy, oz, hsizeworld, hsizewin, soleil):
		self.o=o
		self.ox= ox #vers la droite du spectateur
		self.oy= oy #regard du spectateur
		self.oz= oz #vertical du spectateur
		self.hsizeworld=hsizeworld
		self.hsizewin=hsizewin
		self.soleil = normalize3( soleil)
		self.background=(100,100, 255,255)
		self.nom= "img"

	def generate_ray(self, x, z):
		(x0, y0, z0)= self.o
		kx = interpole(0., 0., self.hsizewin, self.hsizeworld, float(x))
		kz = interpole(0., 0., self.hsizewin, self.hsizeworld, float(z))
		return Rayon((x0 + kx*self.ox[0] + kz*self.oz[0], y0 + kx*self.ox[1] + kz*self.oz[1], z0 + kx*self.ox[2] + kz*self.oz[2]), self.oy)  
	
def transform_ray(trf, rayon) :
	src = rayon.source
	dir = rayon.dir
	t_src = vec2xyz(mat_vec(trf.direct, xyz2vec( rayon.source )))
	t_dir = vec2abc(mat_vec(trf.direct, abc2vec( rayon.dir )))
	return Rayon( t_src, t_dir)

def transform_cam(trf, cam):
	o2= vec2xyz(mat_vec(trf.direct, xyz2vec(cam.o)))
	ox2= vec2abc(mat_vec(trf.direct, abc2vec(cam.ox)))
	oy2= vec2abc(mat_vec(trf.direct, abc2vec(cam.oy)))
	oz2= vec2abc(mat_vec(trf.direct, abc2vec(cam.oz)))
	return Camera(o2, ox2, oy2, oz2, cam.hsizeworld, cam.hsizewin, cam.soleil)

class Obj(object):
	def __init__(self):
		" "

def transform_ray(trf, rayon) :
	src = rayon.source
	dir = rayon.dir
	t_src = vec2xyz(mat_vec(trf.direct, xyz2vec(rayon.source )))
	t_dir = vec2abc(mat_vec(trf.direct, abc2vec(rayon.dir )))
	return Rayon(t_src, t_dir)

def transform_cam(trf, cam):
	o2= vec2xyz(mat_vec(trf.direct, xyz2vec(cam.o)))
	ox2= vec2abc(mat_vec(trf.direct, abc2vec(cam.ox)))
	oy2= vec2abc(mat_vec(trf.direct, abc2vec(cam.oy)))
	oz2= vec2abc(mat_vec(trf.direct, abc2vec(cam.oz)))
	return Camera(o2, ox2, oy2, oz2, cam.hsizeworld, cam.hsizewin, cam.soleil)

def pt_sur_rayon(rayon, t) :
	(x, y, z)= rayon.source
	(a, b, c)= rayon.dir
	return (x + t*a, y + t*b, z + t*c)
	
class Prim(Obj):
	def __init__(self, fonc_xyz, color):
		self.fonc=fonc_xyz
		self.color=color

	def normale(self, xyz):
		(x,y,z) = xyz
		fx=self.fonc.derivee("x") 
		fy=self.fonc.derivee("y") 
		fz=self.fonc.derivee("z") 
		dico={"x":x, "y":y, "z":z}
		(a,b,c)= (fx.eval(dico), fy.eval(dico), fz.eval(dico))
		return normalize3((a, b, c))

	def creer_contact(self, rayon, t) :
		pt=pt_sur_rayon(rayon, t)
		abc=(a,b,c) = self.normale(pt)
		d= 0 - pscal3(pt, abc)
		plan= (a,b,c,d)
		return Contact(t, pt, plan, self.color)

	def two_contacts(self, rayon, t1t2):
			(t1, t2)= t1t2
			return (self.creer_contact(rayon, t1), self.creer_contact(rayon, t2))

	def intersection(self, rayon):
		dico = {"x": Nb(rayon.source[0]) + Nb(rayon.dir[0])*Var("t"), "y": Nb(rayon.source[1]) + Nb(rayon.dir[1])*Var("t"), "z": Nb(rayon.source[2]) + Nb(rayon.dir[2])*Var("t")}
		expression_en_t=self.fonc.evalsymb(dico)
		pol_t = topolent(expression_en_t) 
		#intervalles= ... remplace: roots = racines( pol_t)
		intervalles= inter_polca(1e-4, pol_t)
		intervals_contacts= mymap((lambda t1t2: self.two_contacts(rayon, t1t2)), intervalles)
		return intervals_contacts	

def transform_interval(transfo, intervalle_contacts):
	(contact1, contact2) = intervalle_contacts
	return (transform_contact(transfo, contact1), \
		transform_contact(transfo, contact2))


class TransfObj(Obj):
	def __init__(self, transformation, obj):
		self.transfo=transformation
		self.obj=obj

	def intersection(self, rayon):
		rayon_aux = transform_ray(trf_inverse(self.transfo), rayon)
		# contacts_aux est une liste de paire de contacts:
		contacts_aux = self.obj.intersection(rayon_aux)
		contacts = mymap((lambda ival: \
		   transform_interval(self.transfo, ival)), contacts_aux)
		return contacts

class Union(Prim):
	def __init__(self,objectList):
		self.objectList = objectList

	def intersection(self,rayon):
		intervalles_contacts = None
		accumulateR=0
		accumulateG=0
		accumulateB=0
		accumulateT = 0
		accumulateCount = 0 # contient après exécution le nombre de fois où des composantes ont été additionner

		for x in range(len(self.objectList)):
			currentObject = self.objectList[x]
			currentIntervals_contacts = currentObject.intersection(rayon)
			if currentIntervals_contacts != None:
				intervalles_contacts = currentIntervals_contacts
				(cr,cg,cb,ct)= currentObject.color 
				accumulateB+= cr
				accumulateR+= cg
				accumulateG+= cb
				accumulateT+= ct
				accumulateCount+= 1

		if(accumulateCount>0):
			self.color = (accumulateB/accumulateCount,accumulateG/accumulateCount,accumulateB/accumulateCount,accumulateT/accumulateCount)

		return intervalles_contacts

class Intersection(Prim):
	def __init__(self,objectList):
		self.objectList = objectList
		self.fonc=objectList[0].fonc

	def intersection(self, rayon):
		intervalles_contacts = None
		accumulateR = 0
		accumulateG = 0
		accumulateB = 0
		accumulateT = 0
		accumulateCount = 0 # contient après exécution le nombre de fois où des composantes ont été additionner

		for x in range(len(self.objectList)):
			currentObject = self.objectList[x]
			currentIntervals_contacts = currentObject.intersection(rayon)
			if currentIntervals_contacts != None:
				intervalles_contacts = currentIntervals_contacts
				(cr,cg,cb,ct)=currentObject.color 
				accumulateR+= cr
				accumulateG+= cg
				accumulateB+= cb
				accumulateT+= ct
				accumulateCount+= 1
			else :
				return None

		if(accumulateCount>0):
			self.color = (accumulateR/accumulateCount,accumulateG/accumulateCount,accumulateB/accumulateCount,accumulateT/accumulateCount)

		return intervalles_contacts	

class Difference(Prim):
	def __init__(self,objectList):
		self.objectList = objectList
		self.fonc=objectList[0].fonc
		self.color=objectList[0].color

	def intersection(self,rayon):
		mainObject = self.objectList[0]
		intervalles_contacts = mainObject.intersection(rayon)

		if intervalles_contacts != None : 
			for x in range(len(self.objectList)):
				if(x>0): # a changer, trouver comment retirer le premier élément
					currentObject = self.objectList[x]
					currentIntervals_contacts = currentObject.intersection(rayon)
					if currentIntervals_contacts != None:
						return None

			return intervalles_contacts
		else:
			return None

# calcule la couleur du contact, en attenuant la color du contact en fonction
# de l'angle avec le soleil dans la camera cam
def rendering(cam, contact):
	if 1.0 == contact.t :
		#l'oeil est "dans la matiere", à l'intérieur d'une primitive
		(r,v,b,t)=contact.color
		return (r//2, v//2, b//2,t)
	(rr,vv,bb,tt)= contact.color
	(rr,vv,bb,tt)= (float(rr), float(vv), float(bb),float(tt))
	(a,b,c,d) = contact.plan
# avec les soustractions, il peut arriver que le plan soit mal orienté, ie la normale ne pointe pas vers l'extérieur de l'objet
# si le point du contact est vu, alors pscal3( sa normale, cam.oy)<= 0  
	if pscal3(cam.oy, (a,b,c)) > 0. :
		(a,b,c,d) = (-a, -b, -c, -d)
	ps= pscal3((a,b,c), cam.soleil)
	ps = clamp(-1., 1., ps)
	coef= interpole(-1., 0.5, 1., 1., ps)
	return (int(coef*rr), int(coef*vv), int(coef*bb),int(tt))

def raycasting( cam, objet):
	img=Image.new("RGBA", (2*cam.hsizewin+1, 2*cam.hsizewin+1), (255,255,255))
	for xpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
		for zpix in range(-cam.hsizewin, cam.hsizewin+1, 1):
			rayon= cam.generate_ray(xpix, zpix)
			contacts = objet.intersection(rayon)
			if None==contacts:
				(r,v,b,t)= cam.background
			else:
				(contact1, contact2)=  hd(contacts) 
				if is_num(contact1):
					print('contact1 = nb '+str(contact1))
				(r, v, b, t) = rendering(cam, contact1) 
			img.putpixel((xpix+cam.hsizewin, 2*cam.hsizewin-(zpix+cam.hsizewin)), (r,v,b,t))
	img.save(cam.nom + '.png')