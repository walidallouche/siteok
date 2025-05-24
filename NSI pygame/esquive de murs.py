import pygame
import random

pygame.init()

# Taille de la fenêtre
fenetre = pygame.display.set_mode((900, 600))
pygame.display.set_caption("vaisseau flappeux")

# Variables pour le jeu
largeur_fenetre = 900
hauteur_fenetre = 600
couleur_fond = (0, 0, 0)
etoile = (random.randint(0,600), random.randint(0,400))
etoiles=[etoile]
propulsion=[]
score=0
bonus=1  #multiplicateur de points
police= pygame.font.Font(None, 36) 

for i in range(250):
    i=i+1
    if i!=250:
        etoiles.append((random.randint(0,900), random.randint(0,700))) #ajoute des étoiles pour faire un fond qui bouge afin de simuler le mouvement

# Chargement des images
imagepoint = pygame.image.load("laser.png")
imagepoint = pygame.transform.scale(imagepoint, (40, 150))
imagevaisseau= pygame.image.load("vaisseau.png")
imagevaisseau = pygame.transform.scale(imagevaisseau, (75, 75))  # Redimensionner le vaisseau

# Position initiale
positionvaisseau = [100, 250]

# Liste des barreaux
barreaux = []
points=[] #barreaux entre les deux visibles sur l'ecran pouvant attribuer un point si toucher (ces barreaux sont invisibles)
barreauxlargeur = 70
espacebarreaux = 150
vitessebarreaux = 18
tempjeu = -1

def dessiner():
    fenetre.fill(couleur_fond)  # Remplir la fenêtre avec le fond noir
    for i in range(len(etoiles)):
        pygame.draw.circle(fenetre, (220,220,255), etoiles[i], 1)
        i=i+1
    fenetre.blit(imagevaisseau, positionvaisseau)  # Afficher le vaisseau
    propulsion.append([positionvaisseau[0] - 8, positionvaisseau[1] + 38, 10])  # [x, y, taille]
    for barreau in barreaux:
        pygame.draw.rect(fenetre, (100, 100, 100), barreau[0])  # barreaux du haut
        pygame.draw.rect(fenetre, (100, 100, 100), barreau[1])  # barreaux du bas
        # Calcul de la position du "trou"
        x = barreau[0].x + barreauxlargeur // 2 - 20  # Centré horizontalement
        y = barreau[0].height + (espacebarreaux // 2) -75  # Centré verticalement dans l'espace entre les barres
        # Affiche l'image dans le "trou"
        fenetre.blit(imagepoint, (x, y))
        # Dessiner et faire évoluer la fumée
    for particule in propulsion:
        x, y, taille = particule
        pygame.draw.circle(fenetre, (31, 81, 255), (x, y), taille)
        particule[0] -= 5         # déplacement vers la gauche
        particule[2] -= 0.2       # rétrécissement
    # Supprimer les particules trop petites
    propulsion[:] = [p for p in propulsion if p[2] > 0]
    pygame.display.update()
    score_text = police.render(f"Score : {score}", True, (100, 100, 255))  #pour afficher le score
    bonus_text = police.render(f"Bonus : {bonus-1}", True, (100, 100, 255))
    fenetre.blit(score_text, (10, 10))
    fenetre.blit(bonus_text, (10, 40))
    pygame.display.flip()

# Fonction pour créer de nouveaux barreaux
def nouveauxbarreaux():
    hauteur_haut = random.randint(100, 400)
    hauteur_bas = hauteur_haut + espacebarreaux
    barreauxhaut = pygame.Rect(largeur_fenetre, 0, barreauxlargeur, hauteur_haut)
    barreauxbas = pygame.Rect(largeur_fenetre, hauteur_bas, barreauxlargeur, hauteur_fenetre - hauteur_bas)
    return barreauxhaut, barreauxbas

# Fonction pour déplacer les barreaux et éléments
def deplacerbarreaux():
    global barreaux, score , bonus 
    for i in range(len(barreaux)):
        barreauxhaut, barreauxbas = barreaux[i]
        barreauxhaut.x -= vitessebarreaux
        barreauxbas.x -= vitessebarreaux
        barreaux[i] = (barreauxhaut, barreauxbas)  # on met à jour le tuple
        #ajout des points
    for barreau in barreaux:
        if barreau[0].x + barreauxlargeur < positionvaisseau[0] and barreau not in points:
            points.append(barreau)
            score = score +  bonus #mulitplicateur de score si l'on augmente la vitesse du jeu 
    # Supprimer les barreaux sortis de l'écran
    if len(barreaux) > 0 and barreaux[0][0].x < -barreauxlargeur:
        barreaux.pop(0)
    for i in range(len(etoiles)): #pour faire réapparaitre aléatoirement les étoiles sorties de l'ecran à l'autre coté de la fenetre
        etoiles[i] = (etoiles[i][0]-10-bonus*1.25, etoiles[i][1])
        if etoiles[i][0]<0:
            etoiles[i] = (random.randint(0,1000), random.randint(0,600)) 

# Fonction pour vérifier les collisions
def collision():
    global positionvaisseau, barreaux
    # Si le vaisseau touche le haut ou le bas de l'écran
    if positionvaisseau[1] <= 0 or positionvaisseau[1] >= hauteur_fenetre - 50:
        return True
    # Créer le rectangle du vaisseau
    vaisseau_rect = pygame.Rect(positionvaisseau[0], positionvaisseau[1], 65, 50)
    # Vérifier les collisions avec tous les barreaux
    for barreauxhaut, barreauxbas in barreaux:
        if barreauxhaut.colliderect(vaisseau_rect) or barreauxbas.colliderect(vaisseau_rect):
            return True
    return False



def touches():
# entrées clavier
    global tempjeu, positionvaisseau, vitessebarreaux , bonus , étoiles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    touchesPressees = pygame.key.get_pressed()
    if touchesPressees[pygame.K_SPACE]==True:
        if vitessebarreaux<30:
            vitessebarreaux+=1
            bonus+=0.5 
    if touchesPressees[pygame.K_UP] == True:
        positionvaisseau =  ( positionvaisseau[0], positionvaisseau[1]-8)
    if touchesPressees[pygame.K_DOWN] == True:
        positionvaisseau = ( positionvaisseau[0], positionvaisseau[1]+8)
# Horloge
clock = pygame.time.Clock()

# Boucle principale
running = True
while running:
    clock.tick(50)  # Limiter à 50 images par seconde
    tempjeu += 1
    # Déplacer les tuyaux
    if tempjeu % 125 == 0:
        barreaux.append(nouveauxbarreaux())
    deplacerbarreaux()
    # Vérifier les collisions
    if collision():
        running= False
        fenetre.fill(couleur_fond)
        GG = police.render("Défaite!", True, (100, 250, 100))  #pour afficher la défaite
        fenetre.blit(GG, (10, 10))
        

    touches() 
    dessiner()

pygame.quit()
