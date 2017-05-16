# Gravithaum - Game Design

Gravithaum est un jeu de type réflexion dont le but est de créer des molécules à
partir d'atomes en faisant entrchoquer ces derniers à une vitesse suffisante
pour permettre leur liaison.

On contrôle la vitesse des atomes en influençant la gravité de l'environnement.

## Les éléments de jeu

L'*univers* est un plateau de taille illimitée sur lequel se déplace des atomes.

Un *atome* est l'élément de base du jeu. L'*atome* a une *position* dans
l'univers, une *vitesse* et un *poids*.
Un atome est représenté par un cercle de couleur et de diamètre variant en
fonction de son poids.

Une *molécule* est un ensemble d'atomes liés entre eux via des liaisons.
Les liaisons sont modélisés par des lignes. 

Un *puits de gravité* est un élément non physique qui exerce une force
d'attraction sur l'ensemble des éléments du jeu. Un puits de gravité a une
position et un poids.

## Mécanisme de jeu

Le joueur doit créer la *molécule cible* donnée en début de partie en contrôlant
des puits de gravité dans l'univers afin d'influencer la vitesse des atomes et
permettre leur assemblage en molécules.

Les atomes s'exercent une attraction mutuelle basée sur le principe de la
mécanique newtonienne.

### Les atomes et leurs liaisons

Plus un atome est lourd, plus il a un *stock de liaisons*. Toutes les
liaisons sont de la même longueur. L'angle entre deux liaisons d'un atome est
régulier et trouvé grâce à la formule:

		((nombre de liaisons - 1) * angle = 2 * pi).

Une liaison entre deux atome a un cout qui dépend du poids respectif des deux
atomes en liaison. Par exemple, un atome de poids 4 qui se lie à un atome de
poids 4 consommera 4 du stock de liaison (le plus gros atome en liaison étant
référent). Un atome de poids 4 pourra donc être connecté au maximum avec :
- 4 atomes de poids 1
- 2 atomes de poids 2
- 1 atome de poids 2 et deux atomes de poids 1
- 1 atome de poids 3 et un atome de poids 1
- 1 atome de poids 4

		Une règle simple pour savoir si deux atomes en collision peuvent
		créer une liaison est de vérifier que au moins l'un des deux
		a un stock de liaison positif.

### Création de liaison entre deux atomes

Pour créer une liaison entre deux atomes, il faut que le choque de deux atomes
ait une énergie suffisante et fixée que l'on appellera
*énergie minimale de liaison*. 

		Formule force de collision

Ainsi, plus un atome est léger plus il devra entrechoquer rapidement un autre
atome pour former une liaison.

### Les puits de gravité

Les puits de gravités sont le seul moyen donné au joueur pour influencer
l'environnement.
Le joueur peut placer autant de puits de gravité qu'il veut dans l'univers.
Le joueur peut spécifier l'attraction exercé par le puits de gravité.

(peut on déplacer et supprimer les puits de gravité ? A tester :p)


## Affichage et intercation avec le jeu



