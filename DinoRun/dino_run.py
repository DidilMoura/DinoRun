""" ##### ---------- BIBLIOTHEQUES ---------- ##### """

import pygame # type: ignore
import random

""" ##### ---------- VARIABLES GLOBALES ---------- ##### """

pygame.init()
pygame.mixer.init()

# Fenêtre
LARGEUR, HAUTEUR = 800, 400
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Dino Run")

# Background
fond = pygame.image.load("Image/background.jpg")
fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))

# Audio
son_point = pygame.mixer.Sound("Audio/audio.mp3")
son_point.set_volume(0.01)
musique = pygame.mixer.Sound("Audio/musique.mp3")
musique.set_volume(0.04)
fin = pygame.mixer.Sound("Audio/fin.mp3")
fin.set_volume(0.04)
acceuil = pygame.mixer.Sound("Audio/acceuil.mp3")
acceuil.set_volume(0.04)

# Fonts
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
police = pygame.font.Font(None, 36)

""" ##### --------------- FONCTIONS --------------- ##### """

""" Fonction pour l'écran d'accueil """

def ecran_accueil():
    
    pseudo = ""
    en_attente = True

    while en_attente:
        fenetre.blit(fond, (0, 0))
        acceuil.play()

        # Acceuil
        texte_accueil = police.render("C Koi tOn psEuD0 ?", True, NOIR)
        fenetre.blit(texte_accueil, (LARGEUR // 2 - texte_accueil.get_width() // 2, 100))

        # Pseudo
        texte_pseudo = police.render(pseudo, True, NOIR)
        fenetre.blit(texte_pseudo, (LARGEUR // 2 - texte_pseudo.get_width() // 2, 150))

        # Bouton "Jouer"
        bouton_jouer_text = "Jouer au jeu"
        bouton_jouer = police.render(bouton_jouer_text, True, NOIR)
        bouton_largeur = bouton_jouer.get_width() + 20  # Ajouter une marge
        bouton_hauteur = bouton_jouer.get_height() + 15  # Ajouter une marge

        # Bouton
        pygame.draw.rect(fenetre, (200, 200, 200), (LARGEUR // 2 - bouton_largeur // 2, 200, bouton_largeur, bouton_hauteur))
        fenetre.blit(bouton_jouer, (LARGEUR // 2 - bouton_jouer.get_width() // 2, 210))

        # Écriture
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and pseudo: # Enter
                    acceuil.stop()  
                    en_attente = False
                elif event.key == pygame.K_BACKSPACE:  # Backspace
                    pseudo = pseudo[:-1]
                else:
                    pseudo += event.unicode

        pygame.display.flip()

    return pseudo

""" Fonction pour l'écran de fin de partie """

def ecran_fin_partie(pseudo, score):
    
    en_attente = True

    while en_attente:
        fenetre.blit(fond, (0, 0))
        fin.play()

        # Message fin de partie
        message = f"T'as perdu, gros nul !"
        texte_fin = police.render(message, True, NOIR)
        fenetre.blit(texte_fin, (LARGEUR // 2 - texte_fin.get_width() // 2, 100))

        # Pseudo & score
        texte_pseudo = police.render(f"Pseudo: {pseudo}", True, NOIR)
        fenetre.blit(texte_pseudo, (LARGEUR // 2 - texte_pseudo.get_width() // 2, 150))
        texte_score = police.render(f"Score final: {score}", True, NOIR)
        fenetre.blit(texte_score, (LARGEUR // 2 - texte_score.get_width() // 2, 200))

        # Bouton "Retour"
        bouton_retour = police.render("Retour", True, NOIR)
        pygame.draw.rect(fenetre, (200, 200, 200), (LARGEUR // 2 - 50, 250, 100, 40))
        fenetre.blit(bouton_retour, (LARGEUR // 2 - bouton_retour.get_width() // 2, 260))

        # Boucle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Retour à l'écran d'accueil
                    fin.stop()
                    en_attente = False

        pygame.display.flip()

""" Fonction pour la boucle de jeu """

def jeu():
    
    # Dinosaure
    dino = pygame.Rect(50, 300, 50, 50)
    GRAVITE = 0.5
    saut = -10
    vitesse_y = 0
    est_saut = False

    # Cactus
    cactus_largeur, cactus_hauteur = 20, 50
    cactus_vitesse = 5  # Vitesse
    cactus_liste = []
    #intervalle_spawn = 1500
    dernier_spawn = pygame.time.get_ticks()

    # Score et seuil d'augmentation de vitesse
    score = 0
    seuil_vitesse = 5  # Augmente la vitesse tous les 5 points

    # Boucle principale
    jeu_en_cours = True
    clock = pygame.time.Clock()
    musique.play()

    while jeu_en_cours:
        # Background
        fenetre.blit(fond, (0, 0))
        
        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_en_cours = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not est_saut:
                    est_saut = True
                    vitesse_y = saut

        # Saut du dinosaure
        if est_saut:
            vitesse_y += GRAVITE
            dino.y += vitesse_y
            if dino.y >= 300:
                dino.y = 300
                est_saut = False

        # Intervalle de spawn en fonction de la vitesse
        if cactus_vitesse >= 5:
            intervalle_spawn = random.randint(750, 3000) 
        elif cactus_vitesse >= 7:
            intervalle_spawn = random.randint(650, 1500) 
        elif cactus_vitesse >= 9:
            intervalle_spawn = random.randint(550, 900)  
        elif cactus_vitesse >= 10:
            intervalle_spawn = random.randint(350, 750)
        elif cactus_vitesse >= 12:
            intervalle_spawn = random.randint(1, 5)

        # Apparition et mouvement des cactus
        if pygame.time.get_ticks() - dernier_spawn > intervalle_spawn:
            cactus = pygame.Rect(LARGEUR, 300, cactus_largeur, cactus_hauteur)
            cactus_liste.append(cactus)
            dernier_spawn = pygame.time.get_ticks()

        # Déplacement des cactus et gestion des points
        for cactus in cactus_liste:
            cactus.x -= cactus_vitesse
            if cactus.right < 0:
                cactus_liste.remove(cactus)
                score += 1  # Incrémente le score pour chaque cactus évité
                son_point.play()  # Joue le son lorsque le score augmente
                
                # Augmente la vitesse des cactus tous les 5 points
                if score % seuil_vitesse == 0:
                    cactus_vitesse += 1 
            pygame.draw.rect(fenetre, NOIR, cactus)

        # Collision
        for cactus in cactus_liste:
            if dino.colliderect(cactus):
                jeu_en_cours = False
                musique.stop()

        # Affichage du dinosaure
        pygame.draw.rect(fenetre, NOIR, dino)

        # Affichage du score
        texte_score = police.render(f"Score: {score}", True, NOIR)
        fenetre.blit(texte_score, (10, 10))

        # Mise à jour de l'affichage et contrôle des fps
        pygame.display.flip()
        clock.tick(60)

    return score 

""" ##### --------------- MAIN --------------- ##### """

while True:
    pseudo = ecran_accueil()
    if pseudo is None:
        break  # Quitte si l'utilisateur ferme la fenêtre

    score_final = jeu()  # Joue le jeu et obtenir le score final
    ecran_fin_partie(pseudo, score_final)  # Affiche l'écran de fin de partie

pygame.quit()



