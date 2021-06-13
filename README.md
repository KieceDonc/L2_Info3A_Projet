> Destiné à but pédagogique j'ai réalisé ces programmes à mes débuts en informatique à l'université. Il est donc loin de respecter toutes les règles de l'art en développement et en programmation. N'hésitez pas à corriger, compléter, modifier, ou d'ajouter vos remarques et bonnes pratiques soit par l'intermédiaire de Pull requests ou d'issues, c'est aussi pour ça que je le partage avec la communauté Github 💪 😀

# • Présentation

Ce répertoire contient le projet de fin d'année du module d'info3A ( Licence 2 ) dont voici la présentation :

* Structures de données : liste, pile, file, tas, arbre, graphe. Tris. Recherche arborescente (« backtrack ») : compte est bon, problème des reines. Plus court chemin. Algorithmes de programmation dynamique. Algorithmes récursifs (dessins de fractales). 

Responsable du module : Dominique Michelucci

# • Explications

## Intro

Vous réaliserez un programme de lancer de rayons. Le langage de programmation est Python ; éventuellement, un autre langage fonctionnel peut être accepté (Caml, Ocaml) : demandez à votre encadrant ; cependant vous aurez moins de soutien de la part des enseignants. 

Vous devrez ajouter quelque chose de spécifique à votre projet : visualiser des polyèdres, ou des fractales, ou des textures 3D, ou des procédures d'accélération, etc. Pour ces ajouts spécifiques, aucune correction ne sera fournie. 

Le principe du lancer de rayons est le suivant. Un objet solide est : 

* Soit un objet simple, tel qu'une sphère, un ellipsoïde, un tore, un demi-plan, etc, représenté par une inéquation polynomiale P(x,y,z) <= 0 et une couleur. Par exemple, la sphère centrée à l'origine et de rayon 1 est décrite par : x^2 + 37^2 + zA2 — 1 <= O. La couleur est encodée par un entier c : b=(c % 256) est la composante bleue, v=((c // 256) % 256) est la composante verte, r=(c // 256 // 256) % 256 est la composante rouge. Donc c= 256*256*r + 256*v + b. 
* Soit la transformation (translation, homothétie ou affinité, rotation, symétrie, etc) d'un objet solide. Les transformations pourront être représentées par des matrices 4x4. 
* Soit la réunion, l'intersection ou la différence entre deux objets solides. Cette représentation arborescente est appelée CSG, Constructive Solid Geometry. 

Pour chaque classe d'objet, il faudra programmer une méthode (ou une fonction) récursive calculant l'intersection entre un rayon (une demi-droite, représenté par son point origine o et un vecteur d donnant la direction du rayon : p(t) = (x(t), y(t), z(t))= o + t d est l'équation des points du rayon) et un objet de cette classe. 
Il y a 5 phases dans le projet : 

Phase 1 : Programmer l'intersection entre un rayon et un objet simple ; l'équation polynomiale de l'objet simple est décrite par un DAG (« directed acyclic graph »), représenté par un arbre avec partage éventuel de noeuds ; les feuilles de cet arbre sont soit des nombres ; soit des variables parmi t, x, y, z ; soit la somme de deux DAGs ; soit le produit de deux DAGs ; soit l'opposé d'un DAG. Dans ce DAG, vous substituerez x, y, z par leurs expressions en fonction de t : p(t) = (x(t), y(t), z(t))= o + t d avec o=(xo, yo, zo) un point 3D (xo, yo, zo sont des nombres), et d=(xd, yd, zd) est un vecteur 3D : xd, yd, zd sont des nombres. Cette substitution donne un DAG avec des noeuds +, *, opposé, et des feuilles qui sont soit des nombres, soit la variable t. Il faut transformer cet arbre en un polynôme uni-varié en la variable t. Pour cela, il faut associer à chaque type ou classe de noeuds une méthode ou une fonction qui convertit le noeud en polynôme uni-varié en t. 

Phase 2 : Générer un rayon pour chaque pixel (point) de l'image à calculer. Générer des images d'objets simples. Des équations d'objets simples (quadriques, tores, etc) sont fournies. Vous pourrez créer des animations. 

Phase 3 : Programmer l'intersection entre un rayon et un objet de la classe transformation. 

Phase 4 : Programmer l'intersection entre un rayon et l'union, l'intersection, la différence entre 2 objets. 

Phase 5 : Programmer quelque chose de spécifique.

## Mon rendu

Plusieurs personnalisations ont été apportés au projet :
* Rendu en multiprocessing pour les animations ( exploite le processeur à 100 %  donc rendu plus rapide ) + indique le temps du rendu
* Possibilité de mettre une image de fond ( dans le dossier 'background', une seule image )
* Possibilité de crée des intersections / différences / union avec plusieurs objets. Exemple : Intersection((obj1,obj2,obj3....))
* Ajout d'un paramètre de transparence ( pas très incroyable ) 
* Création automatique du dossier pour un rendu

Quelques primitives ont été ajouté -> voir fichier primitives.py ( leur source est également donné )

Pour lancer un rendu veuillez vous rendre dans anim.py. Vous trouvez toutes les primitives + une fonction associée pour les animer
Exemple : p_tore pour la primitive du tore et tore_anim() pour lancer l'animation
Pour lancer un rendu avec la couleur d'un échiquier veuillez vous rendre dans la fonction associée et rajouter 'camera.renderChessBoard = True' comme dans zitrus ou roman

Attention, due au rendu en multiprocessing veuillez appeler les fonctions uniquement à la fin de anim.py

J'ai choisi de ne pas reprendre la méthode donner pour les opérations booléennes mais je pense que le code est beaucoup moins performant
La fonction Union() est notamment très lourde. 
De plus l'animation de plusieurs opérations booléennes ne correspond pas au résultat attendu ( voir csg_op )

La primitive ajouté la plus belle est saturne. 

Normalement aucune bibliothèque n'a été rajouté et donc le code peut tourner "nativement"

# • Compiler et exécuté

Partons d'un exemple :

<img src="https://www.imaginary.org/sites/default/files/styles/gallery-full/public/zitrus_rtp_0.jpg?itok=bB-yw3vT" width="300" height="300" />

On ajoute d'abord la primitive dans primitives.py

```python
def zitrus():
    x=Var("x")
    y=Var("y")
    z=Var("z")
    return (x*x+z*z-y*y*y*(Nb(1)-y)*(Nb(1)-y)*(Nb(1)-y))
```

On ajoute une nouvelle fonction dans anim.py

```python
def zitrus_anim():
	p_zitrus = Prim(zitrus(),(255,255,255,255)) # Prim pour construire l'objet à partir d'une primitive, zitrus() on appel la primitive, (255,255,255,255) = rouge vert bleu transparence
	object_name = "zitrus" # nom de la primitive
	oeil=(-0,-4,0) # position de la caméra par rapport à l'origine
	droite=  (1.,0.,0.) # vers la droite du spectateur
	regard=  (0.,1.,0.) # regard du spectateur
	vertical=(0.,0.,1.) # vertical du spectateur
	camera=Camera(oeil, droite, regard, vertical, 0.75, 100, normalize3((0., -1., 2.))) # 0.75 = taille du monde
	camera.renderChessBoard = True # nécessaire si on souhaite ajouter l'effet d'un échiquier
	anim(camera, p_zitrus, 20, object_name+"/"+object_name) # 20 = nombres d'images pour l'animation, "object_name+"/"+object_name" = nom des images
```

Enfin on appel notre fonction dans le main 

```python
if __name__ == '__main__':
	zitrus_anim()
```
# • Quelques exemples
<img src="https://raw.githubusercontent.com/KieceDonc/L2_Info3A_Projet/master/hyperboloide_1nappes/animation.gif" /> <img src="https://raw.githubusercontent.com/KieceDonc/L2_Info3A_Projet/master/saturne/animation.gif" /> <img src="https://raw.githubusercontent.com/KieceDonc/L2_Info3A_Projet/master/hyperboloide_2nappes/animation.gif" /> 

<img src="https://raw.githubusercontent.com/KieceDonc/L2_Info3A_Projet/master/zitrus/animation.gif" /> <img src="https://raw.githubusercontent.com/KieceDonc/L2_Info3A_Projet/master/tore/animation.gif" /> <img src="https://raw.githubusercontent.com/KieceDonc/L2_Info3A_Projet/master/roman/animation.gif" />

<img src="https://raw.githubusercontent.com/KieceDonc/L2_Info3A_Projet/master/sextiqueDeBarthsave_r0.5/animation.gif" /> <img src="https://github.com/KieceDonc/L2_Info3A_Projet/blob/master/steiner4/animation.gif" /> <img src="https://raw.githubusercontent.com/KieceDonc/L2_Info3A_Projet/master/sextiqueDeBarthsave_r1/animation.gif" />
